# generate-docs

A Claude Code skill that automatically generates high-quality documentation from any codebase and publishes it to [ReadMe](https://readme.com).

Point it at a repo, pick a style (Stripe, ReadMe, or Mintlify), and get a full set of documentation guides, an `llms.txt` index, and an OpenAPI spec — planned, written, and uploaded without leaving your terminal.

## How it works

The pipeline has five phases, orchestrated directly by Claude Code (no external AI APIs needed):

```
Codebase ──> Fetch Examples ──> Plan Guides ──> Generate Guides ──> Upload
                 (Phase 1)       (Phase 2)        (Phase 3)       (Phase 4-5)
```

1. **Fetch examples** — Downloads real markdown docs from Stripe, ReadMe, or Mintlify (via their `llms.txt` `.md` URLs) to use as style references.
2. **Plan guides** — Claude scans every markdown file in your codebase and proposes a set of guides with slugs, titles, and descriptions.
3. **Generate guides** — For each planned guide, Claude writes the output as markdown with YAML frontmatter and MDX components. Also assembles an `llms.txt` index.
4. **Generate OpenAPI spec** — Claude reads the codebase's route definitions, schemas, and types to produce an OpenAPI 3.1 spec.
5. **Upload** — Pushes guides and OpenAPI spec to ReadMe via `rdme` CLI.

## Quick start

### Prerequisites

- [Claude Code](https://claude.ai/code)
- Node.js (for the `rdme` CLI)
- Python 3.10+ (for the fetch/upload helper scripts)

### Setup

```bash
# Install the ReadMe CLI (for uploading)
npm install -g rdme

# Authenticate with ReadMe (production)
rdme login

# Or authenticate with a local ReadMe instance
RDME_LOCALHOST=1 rdme login
```

### Usage

With [Claude Code](https://claude.ai/code) installed, just ask:

```
generate docs for /path/to/my/repo
```

Claude orchestrates the full pipeline — asks clarifying questions (style, doc type, target environment), shows you the plan for approval, generates each guide, and uploads everything to ReadMe.

#### Local dev mode

If you're running a local ReadMe instance, Claude will ask whether to target production or local dev. When using local dev mode:

- Uploads go to `http://dash.readme.local:3000` instead of `dash.readme.com`
- Requires `readme.local` in your `/etc/hosts` (pointing to `127.0.0.1`)
- Requires a one-time login: `RDME_LOCALHOST=1 rdme login`

You can also use the upload scripts directly with the `--local` flag:

```bash
# Upload guides to local instance
python3 scripts/upload_guides.py output/guides --branch stable --local

# Upload OpenAPI spec to local instance
python3 scripts/upload_openapi.py output/openapi.yaml --branch stable --local
```

## Project structure

```
generate-docs/
├── SKILL.md                  # Claude Code skill definition
├── README.md
├── scripts/
│   ├── fetch_examples.py     # Phase 1: fetch style reference docs
│   ├── upload_openapi.py     # Upload OpenAPI spec via rdme
│   └── upload_guides.py      # Upload guides via rdme
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
├── openapi.yaml                  # OpenAPI 3.1 spec (if generated)
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
| `RDME_API_KEY` | No | ReadMe API key (alternative to `rdme login`) |

For local dev mode, the `RDME_LOCALHOST` env var is set automatically by the `--local` flag on upload scripts.

## Style presets

The fetcher pulls real markdown from documentation sites to use as quality references:

| Preset | Source | What it fetches |
|---|---|---|
| **Stripe** | `docs.stripe.com` | Payment quickstarts, API auth docs |
| **ReadMe** | `docs.readme.com` | Getting started guides, API reference setup |
| **Mintlify** | `mintlify.com/docs` | Quickstart, API playground, navigation guides |

You can also pass `--url` to `fetch_examples.py` to fetch from any documentation site that serves `.md` files, or point at the `references/reference_llms_txt/` directory to sample from hundreds of pages across all three providers.
