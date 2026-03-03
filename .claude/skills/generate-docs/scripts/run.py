#!/usr/bin/env python3
"""Unified interactive CLI for the ReadMe Documentation Generator.

Guides users through the full pipeline:
  1. Fetch example docs (style preset, custom URL, or llms.txt)
  2. Plan documentation guides
  3. Generate guides (simple or beautiful mode)
  4. Upload OpenAPI spec to ReadMe (optional)
  5. Upload guides to ReadMe

Each step calls the individual scripts via subprocess so they remain
independently usable.
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
TIMEOUT = 300  # seconds per subprocess (LLM calls can be slow)

STYLE_PRESETS = {
    "1": ("stripe", "Stripe"),
    "2": ("readme", "ReadMe"),
    "3": ("mintlify", "Mintlify"),
}


def run_script(args: list[str], label: str, required: bool = True) -> bool:
    """Run a script as a subprocess.

    Args:
        args: Command-line arguments (first element is the script path).
        label: Human-readable label for this phase.
        required: If True, exit on failure. If False, warn and continue.

    Returns:
        True if the script succeeded, False otherwise.
    """
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}\n")

    try:
        result = subprocess.run(
            [sys.executable] + args,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        msg = f"Timed out after {TIMEOUT}s"
        if required:
            print(f"\nError: {label} — {msg}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"\nWarning: {label} — {msg}. Skipping.", file=sys.stderr)
            return False

    if result.returncode != 0:
        if required:
            print(f"\nError: {label} failed (exit code {result.returncode})", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"\nWarning: {label} failed (exit code {result.returncode}). Skipping.", file=sys.stderr)
            return False

    return True


def prompt_input(message: str, default: str = "") -> str:
    """Prompt the user for input with an optional default."""
    if default:
        raw = input(f"{message} (default: {default}): ").strip()
        return raw if raw else default
    return input(f"{message}: ").strip()


def prompt_choice(message: str, options: dict[str, str], allow_empty: bool = False) -> str:
    """Prompt the user to choose from numbered options."""
    print(message)
    for key, label in options.items():
        print(f"  [{key}] {label}")
    while True:
        choice = input("Enter choice: ").strip()
        if choice in options:
            return choice
        if allow_empty and choice == "":
            return ""
        print(f"  Invalid choice. Please enter one of: {', '.join(options.keys())}")


def main():
    print()
    print("ReadMe Documentation Generator")
    print("=" * 40)
    print()

    # --- Collect inputs ---
    codebase_path = prompt_input("Enter your codebase's path")
    if not codebase_path or not Path(codebase_path).is_dir():
        print(f"Error: '{codebase_path}' is not a valid directory", file=sys.stderr)
        sys.exit(1)

    openapi_spec = input("Enter your OpenAPI spec filepath (optional, press Enter to skip): ").strip()
    if openapi_spec and not Path(openapi_spec).is_file():
        print(f"Error: '{openapi_spec}' is not a valid file", file=sys.stderr)
        sys.exit(1)

    doc_type = prompt_choice(
        "\nDocumentation type:",
        {"1": "Simple (plain markdown)", "2": "Beautiful (rich MDX components)"},
    )
    simple_mode = doc_type == "1"

    # Style selection
    print("\nDocumentation style:")
    style_options = {
        "1": "Stripe",
        "2": "ReadMe",
        "3": "Mintlify",
        "4": "Paste your own documentation URL",
    }
    style_choice = prompt_choice("", style_options)

    custom_url = ""
    if style_choice == "4":
        custom_url = prompt_input("Enter documentation URL")
        if not custom_url:
            print("Error: URL is required for custom style", file=sys.stderr)
            sys.exit(1)

    project_name = prompt_input("Project name", default="My Project")
    branch = prompt_input("ReadMe branch", default="stable")

    # --- Derived paths ---
    examples_dir = "fetched_examples"
    plan_file = "guide_plan.json"
    output_dir = "output"

    print(f"\n{'=' * 40}")
    print("Starting documentation generation pipeline...")
    print(f"{'=' * 40}")

    # --- Phase 1: Fetch examples ---
    fetch_script = str(SCRIPTS_DIR / "fetch_examples.py")
    fetch_args = [fetch_script, "-o", examples_dir]

    if style_choice in ("1", "2", "3"):
        style_name = STYLE_PRESETS[style_choice][0]
        fetch_args += ["--style", style_name]
        label = f"Phase 1: Fetching {STYLE_PRESETS[style_choice][1]}-style example docs..."
    elif style_choice == "4":
        fetch_args += ["--url", custom_url]
        label = "Phase 1: Fetching example docs from custom URL..."
    else:
        label = "Phase 1: Fetching example docs..."

    run_script(fetch_args, label, required=False)

    # --- Phase 2: Plan guides ---
    plan_script = str(SCRIPTS_DIR / "plan_guides.py")
    plan_args = [plan_script, codebase_path, "-o", plan_file, "-e", examples_dir]
    run_script(plan_args, "Phase 2: Planning documentation guides...", required=True)

    # --- Phase 3: Generate guides ---
    gen_script = str(SCRIPTS_DIR / "generate_guides.py")
    gen_args = [
        gen_script, codebase_path,
        "-p", plan_file,
        "-o", output_dir,
        "-e", examples_dir,
        "-n", project_name,
    ]
    if simple_mode:
        gen_args.append("--simple")

    mode_label = "Simple" if simple_mode else "Beautiful"
    run_script(gen_args, f"Phase 3: Generating guides ({mode_label} mode)...", required=True)

    # --- Phase 4: Upload OpenAPI spec ---
    if openapi_spec:
        upload_api_script = str(SCRIPTS_DIR / "upload_openapi.py")
        upload_api_args = [upload_api_script, openapi_spec, "--branch", branch]
        run_script(upload_api_args, "Phase 4: Uploading OpenAPI spec to ReadMe...", required=False)
    else:
        print(f"\n{'=' * 60}")
        print("  Phase 4: OpenAPI spec upload — SKIPPED (no spec provided)")
        print(f"{'=' * 60}")
        print()
        print("NOTE: No OpenAPI spec was provided. To add API reference docs,")
        print("use the 'openapi-spec-generation' skill to generate a spec from")
        print("your codebase, then upload it with:")
        print(f"  python {SCRIPTS_DIR / 'upload_openapi.py'} output/openapi.yaml --branch {branch}")

        # Save config for downstream tooling
        config = {
            "openapi_spec_needed": True,
            "codebase_path": codebase_path,
            "branch": branch,
        }
        config_path = Path(output_dir) / "config.json"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(config, indent=2) + "\n")

    # --- Phase 5: Upload guides ---
    guides_dir = str(Path(output_dir) / "guides")
    upload_script = str(SCRIPTS_DIR / "upload_guides.py")
    upload_args = [upload_script, guides_dir, "--branch", branch]
    run_script(upload_args, "Phase 5: Uploading guides to ReadMe...", required=False)

    print(f"\n{'=' * 40}")
    print("Done! Your documentation is live.")
    print(f"{'=' * 40}")
    print(f"\nOutput directory: {output_dir}/")
    print(f"  - Guides: {output_dir}/guides/")
    print(f"  - llms.txt: {output_dir}/llms.txt")
    if not openapi_spec:
        print(f"  - config.json: {output_dir}/config.json (OpenAPI spec generation needed)")


if __name__ == "__main__":
    main()
