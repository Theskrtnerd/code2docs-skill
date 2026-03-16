#!/usr/bin/env python3
"""Fetch example .md guides from llms.txt files to use as quality references.

Parses llms.txt files, extracts URLs, fetches a sample of .md files,
and saves them locally as examples of top-tier documentation.
"""

import argparse
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

STYLE_PRESETS = {
    "stripe": [
        "https://docs.stripe.com/payments/quickstart.md",
        "https://docs.stripe.com/payments/accept-a-payment.md",
        "https://docs.stripe.com/api/authentication.md",
        "https://docs.stripe.com/testing.md",
    ],
    "readme": [
        "https://docs.readme.com/main/docs/quickstart.md",
        "https://docs.readme.com/main/docs/about-readme.md",
        "https://docs.readme.com/main/docs/rdme.md",
        "https://docs.readme.com/main/docs/api-reference.md",
    ],
    "mintlify": [
        "https://www.mintlify.com/docs/quickstart.md",
        "https://www.mintlify.com/docs/index.md",
        "https://www.mintlify.com/docs/api-playground/openapi-setup.md",
        "https://www.mintlify.com/docs/organize/navigation.md",
    ],
}


def parse_llms_txt(content: str) -> list[dict]:
    """Extract entries from llms.txt content.

    Returns list of {title, url, description}.
    """
    entries = []
    for line in content.splitlines():
        m = re.match(r"^-\s+\[(.+?)\]\((.+?)\)(?::\s*(.+))?$", line.strip())
        if m:
            entries.append({
                "title": m.group(1),
                "url": m.group(2),
                "description": m.group(3) or "",
            })
    return entries


def fetch_url(url: str, timeout: int = 15) -> str | None:
    """Fetch a URL and return its text content, or None on failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DocGenerator/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def fetch_from_urls(urls: list[str], output_dir: Path, label: str = "custom") -> int:
    """Fetch markdown content directly from a list of URLs.

    Returns the number of successfully fetched pages.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    fetched = 0

    for url in urls:
        print(f"  Fetching: {url}")
        content = fetch_url(url)
        if content and len(content) > 200:
            if len(content) > 15000:
                content = content[:15000] + "\n\n... (truncated for reference)"
            # Derive a filename from the URL path
            slug = re.sub(r"[^a-z0-9]+", "-", url.split("//", 1)[-1].lower()).strip("-")
            # Keep filename reasonable length
            if len(slug) > 80:
                slug = slug[:80].rstrip("-")
            out_file = output_dir / f"{label}--{slug}.md"
            out_file.write_text(content)
            fetched += 1
            print(f"    -> Saved ({len(content)} chars)")
            time.sleep(0.5)
        else:
            print(f"    -> Skipped (too short or failed)")

    return fetched


def main():
    parser = argparse.ArgumentParser(description="Fetch example docs from llms.txt files or style presets")
    parser.add_argument("llms_dir", nargs="?", default=None, help="Directory containing example llms.txt files (optional if --style or --url is used)")
    parser.add_argument("--output", "-o", default="fetched_examples", help="Output directory (default: fetched_examples)")
    parser.add_argument("--style", choices=list(STYLE_PRESETS.keys()), help="Use a style preset (stripe, readme, mintlify)")
    parser.add_argument("--url", action="append", default=[], help="Custom documentation URL to fetch (can be repeated)")
    parser.add_argument("--max-per-file", "-m", type=int, default=3, help="Max guides to fetch per llms.txt (default: 3)")
    parser.add_argument("--max-total", "-t", type=int, default=10, help="Max total guides to fetch (default: 10)")
    args = parser.parse_args()

    output_dir = Path(args.output)

    # Three-mode branching: preset -> custom URL -> original llms.txt behavior
    if args.style:
        # Mode 1: Style preset
        urls = STYLE_PRESETS[args.style]
        print(f"Using {args.style} style preset ({len(urls)} URLs)")
        total_fetched = fetch_from_urls(urls, output_dir, label=args.style)
        print(f"\nFetched {total_fetched} example guides to {output_dir}/")

    elif args.url:
        # Mode 2: Custom URLs
        print(f"Fetching from {len(args.url)} custom URLs")
        total_fetched = fetch_from_urls(args.url, output_dir, label="custom")
        print(f"\nFetched {total_fetched} example guides to {output_dir}/")

    else:
        # Mode 3: Original llms.txt behavior
        if not args.llms_dir:
            print("Error: Must provide llms_dir, --style, or --url", file=sys.stderr)
            sys.exit(1)

        llms_dir = Path(args.llms_dir)
        if not llms_dir.is_dir():
            print(f"Error: {llms_dir} is not a directory", file=sys.stderr)
            sys.exit(1)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Collect all llms.txt files
        llms_files = sorted(llms_dir.glob("*llms*.txt"))
        if not llms_files:
            print(f"Error: No llms.txt files found in {llms_dir}", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(llms_files)} llms.txt files")
        total_fetched = 0

        for llms_file in llms_files:
            if total_fetched >= args.max_total:
                break

            source_name = llms_file.stem.replace("_llms", "").replace("_", "-")
            content = llms_file.read_text(errors="replace")
            entries = parse_llms_txt(content)

            if not entries:
                continue

            print(f"\n{llms_file.name}: {len(entries)} entries")

            # Pick a diverse sample: prefer quickstart, overview, getting-started, auth
            priority_keywords = ["quickstart", "overview", "getting-started", "introduction", "authentication"]
            prioritized = []
            rest = []
            for e in entries:
                slug = e["url"].lower()
                if any(kw in slug for kw in priority_keywords):
                    prioritized.append(e)
                else:
                    rest.append(e)

            sample = (prioritized + rest)[: args.max_per_file]

            for entry in sample:
                if total_fetched >= args.max_total:
                    break

                url = entry["url"]
                title = entry["title"]
                print(f"  Fetching: {title} ({url})")

                md_content = fetch_url(url)
                if md_content and len(md_content) > 200:
                    # Truncate very long docs
                    if len(md_content) > 15000:
                        md_content = md_content[:15000] + "\n\n... (truncated for reference)"

                    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
                    out_file = output_dir / f"{source_name}--{slug}.md"
                    out_file.write_text(md_content)
                    total_fetched += 1
                    print(f"    -> Saved ({len(md_content)} chars)")
                    time.sleep(0.5)  # Be polite

        print(f"\nFetched {total_fetched} example guides to {output_dir}/")


if __name__ == "__main__":
    main()
