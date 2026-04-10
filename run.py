"""
run.py — friendly entry point for coding any registered dataset.

Usage:
  python run.py --list                        # show all registered datasets
  python run.py --dataset Refinement_Dataset  # run full dataset
  python run.py --dataset Refinement_Dataset --limit 5          # first 5 rows
  python run.py --dataset Refinement_Dataset --start 50 --limit 25
  python run.py --dataset Refinement_Dataset --overwrite        # recode all rows
  python run.py --dataset Refinement_Dataset --dry-run          # inspect without API calls

Adding a new dataset:
  1. Drop the .xlsx file into  data/raw/
  2. Add an entry to          config/datasets.json
  3. Run:  python run.py --dataset <name>

All other flags (--model, --provider, --temperature, --sleep, --checkpoint-every,
--include-raw, --force-unlock) are forwarded directly to code_responses.py.
Defaults come from config/datasets.json → "defaults".
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_BASE = Path(__file__).resolve().parent
_CONFIG = _BASE / "config" / "datasets.json"


def load_config() -> dict:
    with open(_CONFIG, encoding="utf-8") as f:
        return json.load(f)


def list_datasets(config: dict) -> None:
    datasets = config.get("datasets", [])
    if not datasets:
        print("No datasets registered in config/datasets.json.")
        return
    print(f"{'Name':<35} {'Phase':<12} {'Prompt':<10} Description")
    print("-" * 90)
    for d in datasets:
        name = d.get("name", "")
        phase = d.get("phase", "")
        version = d.get("prompt_version", "")
        desc = d.get("description", "")
        input_path = _BASE / d.get("input", "")
        output_path = _BASE / d.get("output", "")
        status = ""
        if not input_path.exists():
            status = " [! input missing]"
        elif output_path.exists():
            status = " [coded]"
        else:
            status = " [not yet coded]"
        print(f"{name:<35} {phase:<12} {version:<10} {desc}{status}")


def find_dataset(config: dict, name: str) -> dict:
    for d in config.get("datasets", []):
        if d.get("name", "").lower() == name.lower():
            return d
    print(f"Error: dataset '{name}' not found in config/datasets.json.")
    print("Run  python run.py --list  to see available datasets.")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run thematic coding on a registered dataset.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--list", action="store_true", help="List all registered datasets and exit")
    parser.add_argument("--dataset", help="Dataset name (as registered in config/datasets.json)")

    # Pass-through args for code_responses.py
    parser.add_argument("--provider", choices=("openai", "gemini"), help="API provider (overrides config default)")
    parser.add_argument("--model", help="Model id (overrides config default)")
    parser.add_argument("--temperature", type=float, help="Sampling temperature")
    parser.add_argument("--limit", type=int, default=0, help="Process at most N rows (0 = all)")
    parser.add_argument("--start", type=int, default=0, help="0-based row index to start from")
    parser.add_argument("--overwrite", action="store_true", help="Recode rows that already have code_1")
    parser.add_argument("--checkpoint-every", type=int, help="Save every N coded rows")
    parser.add_argument("--sleep", type=float, help="Seconds between API calls")
    parser.add_argument("--include-raw", action="store_true", help="Keep llm_raw_json column in output")
    parser.add_argument("--dry-run", action="store_true", help="Load xlsx only, no API calls")
    parser.add_argument("--force-unlock", action="store_true", help="Remove stale lock file")

    args = parser.parse_args()

    config = load_config()
    defaults = config.get("defaults", {})

    if args.list:
        list_datasets(config)
        return

    if not args.dataset:
        parser.print_help()
        print("\nTip: use --list to see available datasets, or --dataset <name> to run one.")
        sys.exit(0)

    ds = find_dataset(config, args.dataset)

    input_path = str(_BASE / ds["input"])
    output_path = str(_BASE / ds["output"])

    if not Path(input_path).exists():
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    # Build forwarded argument list
    provider = args.provider or defaults.get("provider", "openai")
    model = args.model or defaults.get("model", "")
    temperature = args.temperature if args.temperature is not None else defaults.get("temperature", 0.2)
    checkpoint_every = args.checkpoint_every if args.checkpoint_every is not None else defaults.get("checkpoint_every", 25)
    sleep = args.sleep if args.sleep is not None else defaults.get("sleep", 0.2)

    cmd = [
        sys.executable, str(_BASE / "code_responses.py"),
        "--input", input_path,
        "--output", output_path,
        "--provider", provider,
        "--temperature", str(temperature),
        "--checkpoint-every", str(checkpoint_every),
        "--sleep", str(sleep),
    ]
    if model:
        cmd += ["--model", model]
    if args.limit:
        cmd += ["--limit", str(args.limit)]
    if args.start:
        cmd += ["--start", str(args.start)]
    if args.overwrite:
        cmd.append("--overwrite")
    if args.include_raw:
        cmd.append("--include-raw")
    if args.dry_run:
        cmd.append("--dry-run")
    if args.force_unlock:
        cmd.append("--force-unlock")

    print(f"Dataset  : {ds['name']}")
    print(f"Phase    : {ds.get('phase', '-')}")
    print(f"Input    : {input_path}")
    print(f"Output   : {output_path}")
    print(f"Provider : {provider}  |  Model: {model or '(default)'}  |  Temp: {temperature}")
    print("-" * 60)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
