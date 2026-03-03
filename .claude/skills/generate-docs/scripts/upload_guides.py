#!/usr/bin/env python3
"""Upload generated guides to a ReadMe project using the rdme CLI.

Requires:
  - rdme CLI installed: npm install -g rdme
  - Authenticated: rdme login (or RDME_API_KEY env var)
"""

import argparse
import subprocess
import sys
from pathlib import Path


def check_rdme():
    """Verify rdme CLI is installed."""
    try:
        result = subprocess.run(
            ["rdme", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"Found rdme {version}")
            return True
    except FileNotFoundError:
        pass
    print("Error: rdme CLI not found. Install with: npm install -g rdme", file=sys.stderr)
    print("Then authenticate with: rdme login", file=sys.stderr)
    return False


def upload_guides(guides_dir: Path, branch: str, dry_run: bool = False):
    """Upload guides directory to ReadMe via rdme CLI."""
    md_files = sorted(guides_dir.glob("*.md"))
    if not md_files:
        print(f"Error: No .md files found in {guides_dir}", file=sys.stderr)
        return False

    print(f"Uploading {len(md_files)} guides to branch '{branch}'...")
    for f in md_files:
        print(f"  - {f.name}")

    cmd = ["rdme", "docs", "upload", str(guides_dir), "--branch", branch]
    if dry_run:
        cmd.append("--dry-run")
        print("\n[DRY RUN] Validating frontmatter and previewing changes...\n")
    else:
        print("\n[UPLOADING] Creating/updating guides on ReadMe...\n")

    result = subprocess.run(cmd, timeout=120)

    if result.returncode == 0:
        if dry_run:
            print("\nDry run passed! Run without --dry-run to upload for real.")
        else:
            print("\nUpload complete!")
        return True
    else:
        print(f"\nrdme exited with code {result.returncode}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload generated guides to ReadMe")
    parser.add_argument("guides_dir", help="Directory containing guide .md files with frontmatter")
    parser.add_argument("--branch", "-b", default="stable", help="ReadMe branch/version (default: stable)")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Validate without uploading")
    args = parser.parse_args()

    guides_dir = Path(args.guides_dir)
    if not guides_dir.is_dir():
        print(f"Error: {guides_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Check at least one file has frontmatter
    sample = next(guides_dir.glob("*.md"), None)
    if sample:
        content = sample.read_text(errors="replace")
        if not content.startswith("---"):
            print(f"Warning: {sample.name} is missing YAML frontmatter.", file=sys.stderr)
            print("Guides need frontmatter for rdme. Re-run generate_guides.py to add it.", file=sys.stderr)
            sys.exit(1)

    if not check_rdme():
        sys.exit(1)

    success = upload_guides(guides_dir, args.branch, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
