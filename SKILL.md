---
name: generate-docs
description: >
  Generate documentation guides, llms.txt, and OpenAPI specs for any codebase. Use when the user asks to
  "generate docs", "create documentation", "generate guides", "make llms.txt", "create llms.txt",
  "generate openapi spec", or wants to produce documentation files from a codebase. Handles the full
  pipeline - fetching example docs for quality reference, planning which guides to create, generating
  guide markdown files, assembling an llms.txt index, generating OpenAPI 3.1 specs from code, and
  uploading to ReadMe via rdme CLI. Supports both production and local dev ReadMe instances.
---

# Generate Docs

Generate high-quality documentation guides and an llms.txt index for any codebase by studying top-tier examples and writing guides directly.

## How to Orchestrate (Claude Code instructions)

When this skill is invoked, YOU (Claude) are the orchestrator. You handle planning and guide generation directly — no external AI APIs or LLM scripts are involved. You read the codebase, decide what guides to write, and write them yourself.

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
7. **Target environment** — "Production" (default, uploads to `dash.readme.com`) or "Local dev" (uploads to a local ReadMe instance at `readme.local:3000`). If the user mentions "local", "localhost", "local dev", or "local ReadMe", use local dev mode.

### Step 2: Check Prerequisites

Before running the pipeline, verify the `rdme` CLI is installed and the user is authenticated:

```bash
which rdme && rdme whoami
```

- If `rdme` is not installed: tell the user to run `npm install -g rdme`
- If not authenticated: the user must run `rdme login` (interactive — they must run this themselves in their terminal). For local dev mode, they must run `RDME_LOCALHOST=1 rdme login` instead.
- Do NOT proceed with upload phases until auth is confirmed. Guide generation can proceed without auth.

### Step 3: Run the Pipeline

The skill directory is the directory containing this SKILL.md. Use `python3` for script invocations.

#### Phase 1: Fetch Example Docs (soft failure OK)

Based on the user's style choice, run the fetch script:

**Style preset (Stripe/ReadMe/Mintlify):**
```bash
python3 scripts/fetch_examples.py --style <stripe|readme|mintlify> -o fetched_examples
```

**Custom URL:**
```bash
python3 scripts/fetch_examples.py --url "<user-provided-url>" -o fetched_examples
```

If this step fails, warn the user and continue — examples are optional.

#### Phase 2: Plan Guides (you do this directly)

1. **Scan the codebase** for markdown files (`.md`). Skip directories like `.git`, `node_modules`, `.venv`, `__pycache__`, `dist`, `build`, `.next`. Use Glob and Read tools.
2. **Read fetched examples** from the `fetched_examples/` directory (if available) to understand the target quality and style.
3. **Propose a set of documentation guides** based on the codebase content. Follow common documentation patterns:
   - Overview / Introduction
   - Getting Started / Quickstart
   - Authentication / Authorization
   - Core Concepts
   - API Reference summaries
   - Configuration
   - Deployment
   - Troubleshooting / FAQ
4. Only propose guides that are well-supported by the existing documentation content. Each guide should be distinct and cover a coherent topic.
5. **Write the plan** to `guide_plan.json` in the skill directory as a JSON array:
   ```json
   [
     {"slug": "overview", "title": "Overview", "description": "High-level introduction to the project."},
     {"slug": "getting-started", "title": "Getting Started", "description": "Step-by-step setup guide."}
   ]
   ```
6. **Show the user** the proposed guides and ask if they want to adjust before proceeding.

#### Phase 3: Generate Guides (you do this directly — with progress tracking)

For each guide in the plan:

1. Create a task for each guide using `TaskCreate` with:
   - `subject`: `"Generate guide: <title>"`
   - `activeForm`: `"Generating <title>"`
2. For each guide:
   a. Update its task to `in_progress` via `TaskUpdate`.
   b. **Write the guide markdown file** to `output/guides/<slug>.md`. Use the codebase content and fetched examples as reference. Follow the formatting rules below.
   c. Update its task to `completed` via `TaskUpdate`.
3. After all guides are generated, assemble `output/llms.txt` (see llms.txt format below).

##### Guide Formatting Rules

Each guide file must have YAML frontmatter for ReadMe CLI compatibility:

```markdown
---
title: Guide Title
slug: guide-slug
category:
  uri: Documentation
content:
  excerpt: Brief description of the guide
---

# Guide Title

Guide content here...
```

**Writing quality guidelines:**
- Use clear, professional technical writing
- Include practical examples and code snippets where relevant
- Structure with headers (##, ###)
- Start with a brief introduction, then cover the topic thoroughly
- Start with a top-level # heading matching the guide title
- Write substantive content (at least several paragraphs)

**If "Simple" mode:** Use plain markdown only (headers, lists, code blocks, tables, bold/italic). No custom JSX/MDX components or HTML tags.

**If "Beautiful" mode:** Use custom MDX components to make guides visually rich and scannable. Available components:

<details>
<summary>Custom Components Reference</summary>

**Accordion** — Collapsible section:
```
<Accordion title="Section Title" icon="font_awesome_icon">

  Content here (supports markdown)

</Accordion>
```

**Cards** — Grid of cards:
```
<Cards columns={2}>
  <Card title="Card Title" icon="font_awesome_icon">
    Brief description
  </Card>
  <Card title="Another Card" href="/link" icon="icon_name">
    More content
  </Card>
</Cards>
```

**Tabs** — Tabbed content:
```
<Tabs>
  <Tab title="Tab One">

    Content for first tab

  </Tab>
  <Tab title="Tab Two">

    Content for second tab

  </Tab>
</Tabs>
```

**Columns** — Side-by-side layout:
```
<Columns layout="auto">
  <Column>

    Left content

  </Column>
  <Column>

    Right content

  </Column>
</Columns>
```

**Usage guidelines:**
- Use Cards to highlight 2-4+ key points, features, or navigation links in a grid
- Use Tabs to organize content by category, language, skill level, or platform
- Use Accordions inside Tabs or standalone to group detailed content
- Use Columns for side-by-side comparisons
- Components can be nested (e.g. Accordions inside Tabs)
- Mix custom components with standard markdown
- Do NOT overuse components — use them where they genuinely improve scannability

**CRITICAL MDX RULES — follow these to avoid parse errors:**
- ALWAYS leave a blank line after an opening tag before any markdown content
- ALWAYS leave a blank line before a closing tag after any markdown content
- This is ESPECIALLY important when using markdown lists inside components
- Use Font Awesome free icon names for the `icon` prop (e.g. "globe", "code", "list-check")

</details>

##### Cross-Linking Between Guides

When linking to other guides in the documentation set, use ReadMe embed links:
- Same category: `[Link Text](/<slug>)` — e.g. `[AI Agent](/ai-agent)`
- Different category: `[Link Text](/<category>/<slug>)`
- Do NOT use relative file paths like `./slug.md`

##### llms.txt Format

After all guides are generated, assemble `output/llms.txt`:

```
# {Project Name} Documentation

## Docs

- [{Guide Title}](guides/{slug}.md): {Brief description}
- [{Guide Title}](guides/{slug}.md): {Brief description}
```

See [references/llms-txt-format.md](references/llms-txt-format.md) for the full format spec.

#### Phase 4: Generate OpenAPI Spec (you do this directly — conditional)

**If user provided an existing OpenAPI spec**, skip generation and use their file directly.

**If user did NOT provide an OpenAPI spec**, offer to generate one. If they agree:

1. **Scan the codebase** for route definitions, API endpoints, request/response schemas (Zod schemas, TypeScript types, Pydantic models, Express/Fastify routes, etc.). Use Glob, Read, and Agent tools as needed.
2. **Write a complete OpenAPI 3.1 spec** to `output/openapi.yaml` following these guidelines:

**OpenAPI 3.1 best practices:**
- Use `openapi: 3.1.0`
- Include `info` with title, description, and version (derive from package.json or equivalent)
- Define `servers` (production, staging, local dev if applicable)
- Use `tags` to group endpoints logically
- For each endpoint: `operationId`, `summary`, `description`, request/response schemas, auth requirements
- Use `$ref` to reuse schemas, parameters, and responses in `components`
- Include `securitySchemes` (bearer, apiKey, OAuth, etc.)
- Add realistic `examples` where helpful
- Document all error responses (400, 401, 404, 500, etc.)
- Use proper types: `format: email`, `format: uri`, `format: date-time`, `format: uuid`
- Mark fields as `required` where appropriate
- Use `enum` for fixed value sets
- For streaming endpoints, document the content type (`text/event-stream`)

If the user declines, skip this step.

#### Phase 5: Upload to ReadMe

**If the user chose "Local dev" mode**, add `--local` to all upload script commands. The scripts set `RDME_LOCALHOST=1` internally to target the local ReadMe instance at `readme.local:3000`. If the user hasn't logged into their local instance yet, have them run `RDME_LOCALHOST=1 rdme login` first (this is interactive and must be run by the user directly).

**Upload OpenAPI spec** (if generated or provided):
```bash
python3 scripts/upload_openapi.py <spec_path> --branch <branch> [--local]
```

**Upload guides:**
```bash
python3 scripts/upload_guides.py output/guides --branch <branch> [--local]
```

Requires `rdme` CLI (`npm install -g rdme`) and authentication (`rdme login` or `RDME_API_KEY`). For local dev mode, use `RDME_LOCALHOST=1 rdme login`. If `rdme` is not available, tell the user the guides were generated successfully in `output/guides/` and they can upload manually later.

### Step 4: Summary

After all phases complete, show the user:
- What was generated and where (`output/guides/`, `output/llms.txt`, `output/openapi.yaml`)
- Which uploads succeeded or were skipped
- The target environment (production or local dev)

## Script Reference

### scripts/fetch_examples.py

Fetches example documentation for quality reference. Three modes:

| Mode | Flag | Example |
|------|------|---------|
| Style preset | `--style stripe\|readme\|mintlify` | `--style stripe -o fetched_examples` |
| Custom URL | `--url <url>` (repeatable) | `--url https://docs.example.com/start` |
| llms.txt dir | positional `<llms_dir>` | `./example_llms -o fetched_examples` |

Additional flags: `-o` (output dir), `-m` (max per file), `-t` (max total)

### scripts/upload_openapi.py

Uploads an OpenAPI spec to ReadMe via `rdme openapi upload`.

```bash
python3 scripts/upload_openapi.py <spec_file> --branch <branch> [--local]
```

Flags: `-b`/`--branch` (default: `stable`), `-l`/`--local` (target local ReadMe instance)

### scripts/upload_guides.py

Uploads generated guides to ReadMe via `rdme docs upload`.

```bash
python3 scripts/upload_guides.py <guides_dir> --branch <branch> [--dry-run] [--local]
```

Flags: `-b`/`--branch` (default: `stable`), `-d`/`--dry-run`, `-l`/`--local` (target local ReadMe instance)

## llms.txt Format

See [references/llms-txt-format.md](references/llms-txt-format.md) for the format spec.
