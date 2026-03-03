#!/usr/bin/env python3
"""Generate guide markdown files and assemble llms.txt from a plan JSON."""

import argparse
import json
import os
import re
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

CUSTOM_COMPONENTS_REFERENCE = """\
You have access to custom components to style the content. Use them to make guides
visually rich and scannable. Variables in curly braces are replaced with actual values.
For icon, use Font Awesome free icon names (e.g. "globe", "heart-pulse", "code").

### Accordion
Collapsible section for grouping related details:
```
<Accordion title="Section Title" icon="font_awesome_icon">
  Content here (supports markdown: lists, bold, code, etc.)
</Accordion>
```

### Cards
Grid of cards for highlighting key points, features, or links:
```
<Cards columns={2}>
  <Card title="Card Title" icon="font_awesome_icon">
    Brief description or content
  </Card>
  <Card title="Another Card" href="/link" icon="icon_name">
    More content
  </Card>
</Cards>
```
The `columns` prop is optional (default auto). `href` on Card is optional.

### Tabs
Tabbed content for organizing alternatives (e.g. languages, skill levels):
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

### Columns
Side-by-side layout:
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

### Usage Guidelines
- Use Cards to highlight 2-4+ key points, features, or navigation links in a grid
- Use Tabs to organize content by category, language, skill level, or platform
- Use Accordions inside Tabs or standalone to group detailed content that can be collapsed
- Use Columns for side-by-side comparisons
- Components can be nested (e.g. Accordions inside Tabs)
- Mix custom components with standard markdown (headers, lists, code blocks, tables)
- Do NOT overuse components — use them where they genuinely improve scannability

### CRITICAL MDX RULES — You MUST follow these to avoid parse errors
- ALWAYS leave a blank line after an opening tag (<Tab>, <Accordion>, <Column>, <Card>) before any markdown content
- ALWAYS leave a blank line before a closing tag (</Tab>, </Accordion>, </Column>, </Card>) after any markdown content
- This is ESPECIALLY important when using markdown lists (*, -, 1.) inside components
- NEVER put a list item immediately after an opening tag or immediately before a closing tag without a blank line

CORRECT example:
```
<Accordion title="Example" icon="list">

- Item one
- Item two
- Item three

</Accordion>
```

WRONG example (will cause MDX parse error):
```
<Accordion title="Example" icon="list">
- Item one
- Item two
- Item three
</Accordion>
```

CORRECT example with Tab:
```
<Tab title="First">

Some text here.

- List item one
- List item two

More text here.

</Tab>
```

WRONG example (will cause MDX parse error):
```
<Tab title="First">
Some text here.
- List item one
- List item two
</Tab>
```
"""

IDEAL_STRUCTURE_EXAMPLE = """\
Here is an example of ideal guide structure using custom components.
NOTE: Blank lines after opening tags and before closing tags are MANDATORY for valid MDX.

```markdown
# Guide Title

Brief intro paragraph explaining what this guide covers.

## Key Concepts

<Cards columns={2}>
  <Card title="Concept A" icon="lightbulb">
    Short explanation of concept A.
  </Card>
  <Card title="Concept B" icon="gear">
    Short explanation of concept B.
  </Card>
</Cards>

## Detailed Sections

<Tabs>
  <Tab title="Getting Started">

    <Accordion title="Prerequisites" icon="list-check">

      - Item one
      - Item two

    </Accordion>

    <Accordion title="Installation" icon="download">

      Step-by-step instructions here with code blocks.

    </Accordion>

  </Tab>

  <Tab title="Advanced">

    <Accordion title="Configuration" icon="sliders">

      Detailed configuration options.

      - Option A: description
      - Option B: description

    </Accordion>

  </Tab>
</Tabs>

## Summary

<Cards columns={3}>
  <Card title="Next Step 1" icon="arrow-right">
    What to do next
  </Card>
  <Card title="Next Step 2" icon="book">
    Further reading
  </Card>
  <Card title="Next Step 3" icon="code">
    Try it yourself
  </Card>
</Cards>
```
"""


def fix_mdx_component_spacing(content: str) -> str:
    """Post-process generated markdown to fix MDX component spacing issues.

    Ensures blank lines exist between JSX component tags and markdown content,
    which is required by the MDX parser to avoid listItem nesting errors.
    """
    component_tags = r"(?:Tab|Accordion|Column|Card|Cards|Tabs|Columns)"

    # Ensure blank line after opening tags when followed by content
    # Match: <Tag ...>\n(non-blank content) -> <Tag ...>\n\n(content)
    content = re.sub(
        rf"(<{component_tags}(?:\s[^>]*)?>)\n(?!\n)(\S)",
        r"\1\n\n\2",
        content,
    )

    # Ensure blank line before closing tags when preceded by content
    # Match: (non-blank content)\n</Tag> -> (content)\n\n</Tag>
    content = re.sub(
        rf"(\S)\n(\s*</{component_tags}>)",
        r"\1\n\n\2",
        content,
    )

    return content


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


def build_context_block(files: list[dict]) -> str:
    """Build a context string from collected docs."""
    sections = []
    total = 0
    for f in files:
        if total + len(f["content"]) > MAX_TOTAL_CHARS:
            break
        sections.append(f"### {f['path']}\n\n{f['content']}")
        total += len(f["content"])
    return "\n\n---\n\n".join(sections)


def load_example_guides(examples_dir: Path, max_examples: int = 3) -> str:
    """Load fetched example guides as quality references."""
    if not examples_dir or not examples_dir.is_dir():
        return ""
    example_files = sorted(examples_dir.glob("*.md"))[:max_examples]
    if not example_files:
        return ""
    snippets = []
    for ef in example_files:
        content = ef.read_text(errors="replace")[:5000]
        snippets.append(f"#### Example: {ef.stem}\n\n{content}")
    return "\n\n---\n\n".join(snippets)


def build_sibling_guides_reference(all_guides: list[dict], current_slug: str, category: str) -> str:
    """Build a reference block listing all other guides for cross-linking."""
    siblings = [g for g in all_guides if g["slug"] != current_slug]
    if not siblings:
        return ""
    lines = ["## Cross-Referencing Other Guides", ""]
    lines.append("When linking to other guides in this documentation set, use ReadMe embed links:")
    lines.append(f'- Same category ("{category}"): `[Link Text](/<slug>)` — e.g. `[AI Agent](/ai-agent)`')
    lines.append("- Different category: `[Link Text](/<category>/<slug>)` — e.g. `[API Reference](/api/api-reference)`")
    lines.append("- Do NOT use relative file paths like `./slug.md` or `../slug.md`")
    lines.append("")
    lines.append(f'Available guides you can link to (all in the "{category}" category):')
    for g in siblings:
        lines.append(f"- `/{g['slug']}` — {g['title']}")
    lines.append("")
    return "\n".join(lines)


def generate_guide(client: OpenAI, model: str, guide: dict, context: str, examples: str,
                   simple: bool = False, all_guides: list[dict] | None = None, category: str = "Documentation") -> str:
    """Call the LLM to generate a single guide."""
    example_section = ""
    if examples:
        example_section = f"""

Here are examples of high-quality documentation from top companies. Match this level
of quality, clarity, and structure:

{examples}

---
"""

    # Build cross-reference section if sibling guides are available
    sibling_section = ""
    if all_guides:
        sibling_section = build_sibling_guides_reference(all_guides, guide["slug"], category)

    if simple:
        components_section = """
## Formatting Rules
- Use plain markdown only (headers, lists, code blocks, tables, bold/italic)
- Do NOT use any custom JSX/MDX components
- Do NOT use HTML tags
"""
        requirements = """\
## Requirements
- Use clear, professional technical writing
- Use plain markdown only — no custom components, no HTML, no JSX
- Include practical examples and code snippets where relevant
- Structure with headers (##, ###), lists, and code blocks
- Start with a brief introduction, then cover the topic thoroughly
- Start with a top-level # heading matching the guide title
- Write substantive content (at least several paragraphs)"""
    else:
        components_section = f"""
## Custom Components Available

{CUSTOM_COMPONENTS_REFERENCE}

{IDEAL_STRUCTURE_EXAMPLE}
"""
        requirements = """\
## Requirements
- Use clear, professional technical writing
- Use the custom components (Cards, Tabs, Accordion, Columns) to make the guide visually
  rich, scannable, and well-organized
- Include practical examples and code snippets where relevant
- Structure with headers (##, ###), and use components within sections
- Start with a brief introduction, then cover the topic thoroughly
- Start with a top-level # heading matching the guide title
- Write substantive content (at least several paragraphs)"""

    prompt = f"""\
You are a technical documentation writer. Write a complete, well-structured documentation
guide in Markdown format.

Guide to write:
- Title: {guide['title']}
- Description: {guide['description']}
{example_section}
{components_section}

{sibling_section}

{requirements}

Use the following project documentation as your reference material:

{context}

Write the guide now. Output ONLY the markdown content, no extra commentary."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()


def assemble_llms_txt(plan: list[dict], project_name: str) -> str:
    """Build llms.txt index following the standard format."""
    lines = [f"# {project_name} Documentation", "", "## Docs", ""]
    for guide in plan:
        slug = guide["slug"]
        title = guide["title"]
        desc = guide.get("description", "")
        entry = f"- [{title}](guides/{slug}.md)"
        if desc:
            entry += f": {desc}"
        lines.append(entry)
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate guide markdown files from a plan")
    parser.add_argument("codebase", help="Path to the codebase root")
    parser.add_argument("--plan", "-p", default="guide_plan.json", help="Path to guide plan JSON (default: guide_plan.json)")
    parser.add_argument("--output-dir", "-o", default="output", help="Output directory (default: output)")
    parser.add_argument("--project-name", "-n", default=None, help="Project name for llms.txt header (default: derived from codebase dir)")
    parser.add_argument("--category", "-c", default="Documentation", help="ReadMe category name for frontmatter (default: Documentation)")
    parser.add_argument("--examples-dir", "-e", default=None, help="Directory containing fetched example guides for quality reference")
    parser.add_argument("--simple", action="store_true", help="Generate plain markdown without custom MDX components")
    parser.add_argument("--slug", default=None, help="Generate only a single guide by slug (skips llms.txt assembly)")
    parser.add_argument("--llms-txt-only", action="store_true", help="Only assemble llms.txt from existing guides (skip generation)")
    parser.add_argument("--model", default=os.getenv("MODEL", "anthropic/claude-sonnet-4-5"), help="LLM model to use")
    parser.add_argument("--base-url", default=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"), help="LLM API base URL")
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.is_file():
        print(f"Error: Plan file not found: {plan_path}", file=sys.stderr)
        sys.exit(1)

    plan = json.loads(plan_path.read_text())

    codebase = Path(args.codebase).resolve()
    if not codebase.is_dir():
        print(f"Error: {codebase} is not a directory", file=sys.stderr)
        sys.exit(1)

    project_name = args.project_name or codebase.name.replace("-", " ").replace("_", " ").title()

    # Set up output dirs
    output_dir = Path(args.output_dir)
    guides_dir = output_dir / "guides"
    guides_dir.mkdir(parents=True, exist_ok=True)

    # --llms-txt-only: just assemble the index from existing guides and exit
    if args.llms_txt_only:
        llms_txt = assemble_llms_txt(plan, project_name)
        (output_dir / "llms.txt").write_text(llms_txt)
        print(f"Wrote llms.txt to {output_dir / 'llms.txt'}")
        sys.exit(0)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    # Keep the full plan for cross-references, filter iteration list if --slug
    full_plan = plan
    if args.slug:
        matching = [g for g in plan if g["slug"] == args.slug]
        if not matching:
            print(f"Error: No guide with slug '{args.slug}' found in plan", file=sys.stderr)
            sys.exit(1)
        plan = matching

    # Collect codebase docs as context
    print(f"Scanning {codebase} for markdown files...")
    files = collect_markdown_files(codebase)
    print(f"Found {len(files)} markdown files for context")
    context = build_context_block(files)

    # Load example guides for quality reference
    examples = ""
    if args.examples_dir:
        examples = load_example_guides(Path(args.examples_dir))
        if examples:
            print(f"Loaded example guides from {args.examples_dir}")

    client = OpenAI(base_url=args.base_url, api_key=api_key)

    # Generate each guide
    category = args.category
    for i, guide in enumerate(plan, 1):
        slug = guide["slug"]
        title = guide["title"]
        description = guide.get("description", "")
        print(f"[{i}/{len(plan)}] Generating: {title} ({slug}.md)...")

        content = generate_guide(client, args.model, guide, context, examples,
                                simple=args.simple, all_guides=full_plan, category=category)

        # Post-process to fix MDX component spacing issues (skip in simple mode)
        if not args.simple:
            content = fix_mdx_component_spacing(content)

        # Build YAML frontmatter for rdme CLI compatibility
        frontmatter = f"""---
title: {title}
slug: {slug}
category:
  uri: {category}
content:
  excerpt: {description}
---

"""
        md = f"{frontmatter}{content}\n"
        (guides_dir / f"{slug}.md").write_text(md)
        print(f"  -> Wrote {len(md)} chars to {guides_dir / f'{slug}.md'}")

    # Assemble llms.txt (only when generating all guides, not single)
    if not args.slug:
        llms_txt = assemble_llms_txt(plan, project_name)
        (output_dir / "llms.txt").write_text(llms_txt)
        print(f"\nWrote llms.txt to {output_dir / 'llms.txt'}")

    print("Done!")


if __name__ == "__main__":
    main()
