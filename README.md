# generate-docs

A Claude Code skill that automatically generates high-quality documentation from any codebase and publishes it to [ReadMe](https://readme.com).

Point it at a repo, pick a style (Stripe, ReadMe, or Mintlify), and get a full set of documentation guides, an `llms.txt` index, and an OpenAPI spec — planned, written, and uploaded without leaving your terminal.

## How it works

The pipeline has five phases, each backed by a standalone Python script:

```
Codebase ──> Fetch Examples ──> Plan Guides ──> Generate Guides ──> Upload
                 (Phase 1)       (Phase 2)        (Phase 3)       (Phase 4-5)
```

1. **Fetch examples** — Downloads real markdown docs from Stripe, ReadMe, or Mintlify (via their `llms.txt` `.md` URLs) to use as style references.
2. **Plan guides** — Scans every markdown file in your codebase and asks an LLM to propose a set of guides with slugs, titles, and descriptions.
3. **Generate guides** — For each planned guide, sends codebase context + style examples to an LLM and writes the output as markdown with YAML frontmatter. Also assembles an `llms.txt` index.
4. **Upload OpenAPI spec** — Optionally generates and uploads an OpenAPI 3.1 spec to ReadMe via the `rdme` CLI.
5. **Upload guides** — Pushes all generated guides to ReadMe via `rdme docs upload`.

## Quick start

### Prerequisites

- Python 3.10+
- Node.js (for the `rdme` CLI)
- An [OpenRouter](https://openrouter.ai) API key

### Setup

```bash
# Clone the repo
cd hackathon

# Create a .env file with your API key
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env

# Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install openai

# Install the ReadMe CLI (for uploading)
npm install -g rdme
rdme login
```

### Usage

There are two ways to run the pipeline:

#### Option A: Interactive CLI

```bash
python3 .claude/skills/generate-docs/scripts/run.py
```

This walks you through each step interactively — codebase path, style, project name, etc.

#### Option B: Claude Code skill

If you have [Claude Code](https://claude.ai/code) installed, just ask:

```
generate docs for /path/to/my/repo
```

Claude orchestrates the full pipeline, asks clarifying questions, shows you the plan for approval, and runs each phase.

#### Option C: Run scripts individually

```bash
cd .claude/skills/generate-docs

# 1. Fetch style examples (uses reference llms.txt files with .md URLs)
python3 scripts/fetch_examples.py references/reference_llms_txt -o fetched_examples

# 2. Plan guides
python3 scripts/plan_guides.py /path/to/codebase -o guide_plan.json -e fetched_examples

# 3. Generate guides
python3 scripts/generate_guides.py /path/to/codebase \
  -p guide_plan.json \
  -o output \
  -e fetched_examples \
  -n "My Project"

# 4. Upload OpenAPI spec (optional)
python3 scripts/upload_openapi.py output/openapi.yaml --branch stable

# 5. Upload guides to ReadMe
python3 scripts/upload_guides.py output/guides --branch stable
```

## Project structure

```
hackathon/
├── .env                          # OPENROUTER_API_KEY
├── README.md
└── .claude/skills/generate-docs/
    ├── SKILL.md                  # Claude Code skill definition
    ├── scripts/
    │   ├── run.py                # Interactive CLI (all-in-one)
    │   ├── fetch_examples.py     # Phase 1: fetch style reference docs
    │   ├── plan_guides.py        # Phase 2: LLM-powered guide planning
    │   ├── generate_guides.py    # Phase 3: LLM-powered guide generation
    │   ├── upload_openapi.py     # Phase 4: upload OpenAPI spec via rdme
    │   └── upload_guides.py      # Phase 5: upload guides via rdme
    └── references/
        ├── llms-txt-format.md    # llms.txt format specification
        └── reference_llms_txt/   # Real llms.txt files for style presets
            ├── stripe_llms.txt
            ├── readme_llms.txt
            └── mintlify_llms.txt
```

## Output

After a run, the `output/` directory contains:

```
output/
├── guides/
│   ├── overview.md               # Each guide has YAML frontmatter for ReadMe
│   ├── getting-started.md
│   ├── api-reference.md
│   └── ...
└── llms.txt                      # LLM-friendly index of all guides
```

Each guide includes YAML frontmatter compatible with ReadMe's `rdme docs upload`:

```yaml
---
title: Overview
slug: overview
category:
  uri: Documentation
content:
  excerpt: High-level introduction to the project...
---
```

## Configuration

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | Yes | API key for LLM calls (via [OpenRouter](https://openrouter.ai)) |
| `MODEL` | No | LLM model override (default: `anthropic/claude-sonnet-4-5`) |
| `BASE_URL` | No | API base URL override (default: `https://openrouter.ai/api/v1`) |
| `RDME_API_KEY` | No | ReadMe API key (alternative to `rdme login`) |

The scripts automatically load variables from the `.env` file in the project root.

## Style presets

The fetcher pulls real markdown from documentation sites to use as quality references:

| Preset | Source | What it fetches |
|---|---|---|
| **Stripe** | `docs.stripe.com` | Payment quickstarts, API auth docs |
| **ReadMe** | `docs.readme.com` | Getting started guides, API reference setup |
| **Mintlify** | `mintlify.com/docs` | Quickstart, API playground, navigation guides |

You can also pass `--url` to fetch from any documentation site that serves `.md` files, or point at the `references/reference_llms_txt/` directory to sample from hundreds of pages across all three providers.

## How the LLM calls work

- **Planning** (`plan_guides.py`): Sends all markdown files from the codebase (up to 120K chars) to the LLM and asks it to propose a table of contents. Returns a JSON array of `{slug, title, description}`.
- **Generation** (`generate_guides.py`): For each guide in the plan, sends the codebase context + fetched style examples + the specific guide spec. The LLM writes a complete markdown guide with frontmatter. Runs sequentially (one LLM call per guide).

Both scripts use [OpenRouter](https://openrouter.ai) as the default API gateway, which gives access to Claude, GPT-4, Gemini, and other models through a single API key.
