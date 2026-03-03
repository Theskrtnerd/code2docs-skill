#!/usr/bin/env python3
"""Collect codebase docs and ask an LLM to plan which guides to create."""

import argparse
import json
import os
import sys
from pathlib import Path

from openai import OpenAI


def load_dotenv():
    """Load .env file by walking up from the script directory."""
    d = Path(__file__).resolve().parent
    for _ in range(10):
        env_file = d / ".env"
        if env_file.is_file():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
            return
        d = d.parent


load_dotenv()

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "dist", "build", ".next"}
MAX_FILE_CHARS = 8000
MAX_TOTAL_CHARS = 120000


def collect_markdown_files(codebase: Path) -> list[dict]:
    """Glob for *.md files, skipping ignored directories."""
    files = []
    for md in sorted(codebase.rglob("*.md")):
        if any(part in SKIP_DIRS for part in md.parts):
            continue
        rel = md.relative_to(codebase)
        try:
            content = md.read_text(errors="replace")
        except Exception:
            continue
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS] + "\n\n... (truncated)"
        files.append({"path": str(rel), "content": content})
    return files


def build_prompt(files: list[dict], example_context: str = "") -> str:
    """Build the prompt that asks the LLM to propose guides."""
    doc_sections = []
    total = 0
    for f in files:
        if total + len(f["content"]) > MAX_TOTAL_CHARS:
            break
        doc_sections.append(f"### {f['path']}\n\n{f['content']}")
        total += len(f["content"])

    docs_block = "\n\n---\n\n".join(doc_sections)

    example_section = ""
    if example_context:
        example_section = f"""

Here are examples of high-quality documentation guides from top companies for reference
on the kind of content and structure to aim for:

{example_context}

---

"""

    return f"""\
You are a technical documentation expert. Below are the existing documentation files
from a software project. Based on these docs, propose a set of documentation guides
that should be generated for this project.
{example_section}
Follow common documentation patterns such as:
- Overview / Introduction
- Getting Started / Quickstart
- Authentication / Authorization
- Core Concepts
- API Reference summaries
- Configuration
- Deployment
- Troubleshooting / FAQ

Only propose guides that are well-supported by the existing documentation content.
Each guide should be distinct and cover a coherent topic.

Respond with ONLY a JSON array. Each element must have:
- "slug": a URL-friendly identifier (e.g. "getting-started")
- "title": a human-readable title (e.g. "Getting Started")
- "description": 1-2 sentences describing what the guide should cover

Example response format:
[
  {{"slug": "overview", "title": "Overview", "description": "High-level introduction to the project, its purpose, and key features."}},
  {{"slug": "getting-started", "title": "Getting Started", "description": "Step-by-step guide to setting up and running the project for the first time."}}
]

---

EXISTING DOCUMENTATION:

{docs_block}

---

Respond with ONLY the JSON array, no markdown fences or extra text."""


def main():
    parser = argparse.ArgumentParser(description="Plan documentation guides for a codebase")
    parser.add_argument("codebase", help="Path to the codebase root")
    parser.add_argument("--output", "-o", default="guide_plan.json", help="Output plan file (default: guide_plan.json)")
    parser.add_argument("--examples-dir", "-e", default=None, help="Directory containing fetched example guides for quality reference")
    parser.add_argument("--model", default=os.getenv("MODEL", "anthropic/claude-sonnet-4-5"), help="LLM model to use")
    parser.add_argument("--base-url", default=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"), help="LLM API base URL")
    args = parser.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    codebase = Path(args.codebase).resolve()
    if not codebase.is_dir():
        print(f"Error: {codebase} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {codebase} for markdown files...")
    files = collect_markdown_files(codebase)
    if not files:
        print("Error: No markdown files found", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(files)} markdown files")

    # Load example guides as quality reference if provided
    example_context = ""
    if args.examples_dir:
        examples_path = Path(args.examples_dir)
        if examples_path.is_dir():
            example_files = sorted(examples_path.glob("*.md"))[:5]
            if example_files:
                snippets = []
                for ef in example_files:
                    content = ef.read_text(errors="replace")[:3000]
                    snippets.append(f"#### Example: {ef.stem}\n\n{content}")
                example_context = "\n\n---\n\n".join(snippets)
                print(f"Loaded {len(example_files)} example guides as quality reference")

    prompt = build_prompt(files, example_context)
    print(f"Sending {len(prompt)} chars to {args.model}...")

    client = OpenAI(base_url=args.base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if the model wraps the response
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")]
        raw = raw.strip()

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse LLM response as JSON: {e}", file=sys.stderr)
        print(f"Raw response:\n{raw}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(plan, list) or not all(
        isinstance(g, dict) and "slug" in g and "title" in g and "description" in g for g in plan
    ):
        print("Error: LLM response is not in the expected format", file=sys.stderr)
        print(f"Parsed:\n{json.dumps(plan, indent=2)}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Wrote {len(plan)} guides to {output_path}")
    for g in plan:
        print(f"  - {g['slug']}: {g['title']}")


if __name__ == "__main__":
    main()
