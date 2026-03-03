---
name: generate-docs
description: >
  Generate documentation guides and llms.txt for any codebase. Use when the user asks to
  "generate docs", "create documentation", "generate guides", "make llms.txt", "create llms.txt",
  or wants to produce documentation files from a codebase. Handles the full pipeline -
  fetching example docs for quality reference, planning which guides to create, generating
  guide markdown files, assembling an llms.txt index, uploading OpenAPI specs, and uploading
  to ReadMe via rdme CLI.
---

# Generate Docs

Generate high-quality documentation guides and an llms.txt index for any codebase by studying top-tier examples and using LLM-powered generation.

## How to Orchestrate (Claude Code instructions)

When this skill is invoked, YOU (Claude) are the orchestrator. Do NOT tell the user to run `scripts/run.py` — instead, collect their inputs via `AskUserQuestion`, then run each script yourself via Bash.

### Step 1: Collect User Inputs

Use `AskUserQuestion` to gather the following. Ask all questions in a single call when possible:

1. **Codebase path** — Required. The path to the project to document.
2. **OpenAPI spec filepath** — Optional. Path to an existing OpenAPI spec file (YAML or JSON).
3. **Documentation type** — "Simple" (plain markdown) or "Beautiful" (rich MDX components, recommended).
4. **Documentation style** — Which style to emulate:
   - Stripe (recommended)
   - ReadMe
   - Mintlify
   - Custom URL (user provides a documentation URL)
5. **Project name** — Default: derive from the codebase directory name.
6. **ReadMe branch** — Default: `stable`.

### Step 2: Check Prerequisites

Before running anything, verify the environment:

```bash
python3 -c "import openai; print('openai OK')"
echo "OPENROUTER_API_KEY=${OPENROUTER_API_KEY:+is set}"
```

If `openai` is missing, install it: `pip install openai`
If `OPENROUTER_API_KEY` is not set, ask the user to provide it.

### Step 3: Run the Pipeline

All scripts live in this skill's `scripts/` directory. Run them from the skill directory:
`cd <skill-dir>` first, where `<skill-dir>` is the directory containing this SKILL.md.

Use `python3` (or `sys.executable` equivalent) for all script invocations.

#### Phase 1: Fetch Example Docs (soft failure OK)

Based on the user's style choice:

**Style preset (Stripe/ReadMe/Mintlify):**
```bash
python3 scripts/fetch_examples.py --style <stripe|readme|mintlify> -o fetched_examples
```

**Custom URL:**
```bash
python3 scripts/fetch_examples.py --url "<user-provided-url>" -o fetched_examples
```

If this step fails, warn the user and continue — examples are optional.

#### Phase 2: Plan Guides (required)

```bash
python3 scripts/plan_guides.py <codebase_path> -o guide_plan.json -e fetched_examples
```

After this completes, read `guide_plan.json` and show the user the proposed guides. Ask if they want to adjust before proceeding.

#### Phase 3: Generate Guides (required — with progress tracking)

This step generates each guide via an LLM call and can take several minutes. Use the task list to show per-guide progress so the user can track how many guides have been completed.

**Steps:**

1. Read `guide_plan.json` to get the list of guides.
2. Create a task for each guide using `TaskCreate` with:
   - `subject`: `"Generate guide: <title>"`
   - `activeForm`: `"Generating <title>"`
3. Loop through each guide in the plan. For each guide:
   a. Update its task to `in_progress` via `TaskUpdate`.
   b. Run the generation script for that single guide:
      ```bash
      python3 scripts/generate_guides.py <codebase_path> \
        -p guide_plan.json \
        -o output \
        -e fetched_examples \
        -n "<project_name>" \
        --slug "<guide_slug>" \
        [--simple]
      ```
   c. Update its task to `completed` via `TaskUpdate`.
4. After all guides are generated, assemble the llms.txt index:
   ```bash
   python3 scripts/generate_guides.py <codebase_path> \
     -p guide_plan.json \
     -o output \
     -n "<project_name>" \
     --llms-txt-only
   ```

Add `--simple` if the user chose "Simple" documentation type.

#### Phase 4: Upload OpenAPI Spec (conditional)

**If user provided an OpenAPI spec:**
```bash
python3 scripts/upload_openapi.py <spec_path> --branch <branch>
```

**If user did NOT provide an OpenAPI spec:**
Tell the user no spec was provided, and offer to generate one. If they agree, invoke the `openapi-spec-generation` skill to create a spec from the codebase, save it to `output/openapi.yaml`, then upload it:
```bash
python3 scripts/upload_openapi.py output/openapi.yaml --branch <branch>
```

If the user declines, skip this step.

#### Phase 5: Upload Guides (soft failure OK)

```bash
python3 scripts/upload_guides.py output/guides --branch <branch>
```

Requires `rdme` CLI (`npm install -g rdme`) and authentication (`rdme login` or `RDME_API_KEY`). If `rdme` is not available, tell the user the guides were generated successfully in `output/guides/` and they can upload manually later.

### Step 4: Summary

After all phases complete, show the user:
- What was generated and where (`output/guides/`, `output/llms.txt`)
- Which uploads succeeded or were skipped
- Any next steps (e.g., OpenAPI spec generation if skipped)

## Script Reference

### scripts/fetch_examples.py

Fetches example documentation for quality reference. Three modes:

| Mode | Flag | Example |
|------|------|---------|
| Style preset | `--style stripe\|readme\|mintlify` | `--style stripe -o fetched_examples` |
| Custom URL | `--url <url>` (repeatable) | `--url https://docs.example.com/start` |
| llms.txt dir | positional `<llms_dir>` | `./example_llms -o fetched_examples` |

Additional flags: `-o` (output dir), `-m` (max per file), `-t` (max total)

### scripts/plan_guides.py

Scans codebase markdown and asks LLM to propose guides.

```bash
python3 scripts/plan_guides.py <codebase> -o guide_plan.json -e fetched_examples
```

Flags: `-o` (output file), `-e` (examples dir), `--model`, `--base-url`

Output: JSON array of `[{slug, title, description}, ...]`

### scripts/generate_guides.py

Generates guide markdown files and llms.txt index from a plan.

```bash
python3 scripts/generate_guides.py <codebase> -p guide_plan.json -o output -e fetched_examples -n "Name" [--simple]
```

Flags: `-p` (plan JSON), `-o` (output dir), `-e` (examples dir), `-n` (project name), `-c` (category), `--simple` (plain markdown, no MDX), `--slug` (generate a single guide by slug), `--llms-txt-only` (only assemble llms.txt, skip generation), `--model`, `--base-url`

Output: `output/guides/*.md` (with YAML frontmatter) + `output/llms.txt`

### scripts/upload_openapi.py

Uploads an OpenAPI spec to ReadMe via `rdme openapi upload`.

```bash
python3 scripts/upload_openapi.py <spec_file> --branch <branch>
```

Flags: `-b`/`--branch` (default: `stable`)

### scripts/upload_guides.py

Uploads generated guides to ReadMe via `rdme docs upload`.

```bash
python3 scripts/upload_guides.py <guides_dir> --branch <branch> [--dry-run]
```

Flags: `-b`/`--branch` (default: `stable`), `-d`/`--dry-run`

## Configuration

Environment variables used by scripts:
- `OPENROUTER_API_KEY` — required for LLM calls
- `MODEL` — override LLM model (default: `anthropic/claude-sonnet-4-5`)
- `BASE_URL` — override API base URL (default: `https://openrouter.ai/api/v1`)

## llms.txt Format

See [references/llms-txt-format.md](references/llms-txt-format.md) for the format spec.

## Standalone CLI

Users can also run the pipeline manually outside of Claude Code:

```bash
python3 scripts/run.py
```

This provides an interactive terminal experience with the same pipeline.
