#!/usr/bin/env python3
"""Upload an OpenAPI spec to a ReadMe project using the rdme CLI.

Requires:
  - rdme CLI installed: npm install -g rdme
  - Authenticated: rdme login (or RDME_API_KEY env var)

For local dev: use --local flag to target a local ReadMe instance (readme.local:3000).
Requires: RDME_LOCALHOST=1 rdme login (run once to authenticate with your local instance).
"""

import argparse
import os
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


def validate_spec(spec_path: Path) -> bool:
    """Basic validation that the file looks like an OpenAPI spec."""
    content = spec_path.read_text(errors="replace")
    if "openapi:" in content or '"openapi"' in content:
        return True
    print(f"Warning: {spec_path.name} does not appear to contain an OpenAPI spec.", file=sys.stderr)
    print("Expected to find 'openapi:' keyword in the file.", file=sys.stderr)
    return False


def upload_openapi(spec_path: Path, branch: str, local: bool = False) -> bool:
    """Upload an OpenAPI spec to ReadMe via rdme CLI."""
    target = "local ReadMe instance" if local else "ReadMe"
    print(f"Uploading {spec_path.name} to {target} (branch '{branch}')...")

    env = os.environ.copy()
    if local:
        env["RDME_LOCALHOST"] = "1"

    cmd = ["rdme", "openapi", "upload", str(spec_path), "--branch", branch]
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, timeout=120, env=env)

    if result.returncode == 0:
        print("\nOpenAPI spec uploaded successfully!")
        return True
    else:
        print(f"\nrdme exited with code {result.returncode}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload an OpenAPI spec to ReadMe")
    parser.add_argument("spec", help="Path to the OpenAPI spec file (YAML or JSON)")
    parser.add_argument("--branch", "-b", default="stable", help="ReadMe branch/version (default: stable)")
    parser.add_argument("--local", "-l", action="store_true", help="Upload to local ReadMe instance (readme.local:3000)")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        print(f"Error: {spec_path} is not a file", file=sys.stderr)
        sys.exit(1)

    if not validate_spec(spec_path):
        sys.exit(1)

    if not check_rdme():
        sys.exit(1)

    success = upload_openapi(spec_path, args.branch, local=args.local)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
