#!/usr/bin/env python3
"""
Prepare a per-question-type raw Excel file for code_responses.py.

Reads a file with a question-specific response column, renames it to `response`,
adds `question_type`, and writes a prepared workbook with columns:
PID, response, question_type.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ALLOWED_QUESTION_TYPES = frozenset({
    "like_science",
    "like_math",
    "dislike_science",
    "dislike_math",
    "stopped_science",
    "stopped_math",
})


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_prepared{input_path.suffix}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare a raw per-question-type Excel file for code_responses.py "
            "(adds response + question_type columns)."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the raw Excel file (e.g. data/raw/like_science.xlsx)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Path for the prepared file. Default: same directory as input, "
            "with _prepared before .xlsx (e.g. like_science_prepared.xlsx)"
        ),
    )
    parser.add_argument(
        "--question-type",
        required=True,
        choices=sorted(ALLOWED_QUESTION_TYPES),
        help="Question type to assign to every row",
    )
    parser.add_argument(
        "--response-col",
        required=True,
        help='Exact column name containing student responses (e.g. "Why do you like science?")',
    )
    parser.add_argument(
        "--pid-col",
        default="PID",
        help="Column name for participant ID (default: PID)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary only; do not write the output file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path: Path = args.input
    output_path: Path = args.output or default_output_path(input_path)

    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    if input_path.suffix.lower() not in {".xlsx", ".xls"}:
        print(f"Error: input must be an Excel file (.xlsx): {input_path}", file=sys.stderr)
        return 1

    df = pd.read_excel(input_path)

    if args.response_col not in df.columns:
        print(f"Error: response column not found: {args.response_col!r}", file=sys.stderr)
        print("Available columns:", file=sys.stderr)
        for col in df.columns:
            print(f"  - {col!r}", file=sys.stderr)
        return 1

    if args.pid_col not in df.columns:
        print(
            f"Warning: PID column not found: {args.pid_col!r} — continuing without PID values.",
            file=sys.stderr,
        )
        pid_series = pd.Series([None] * len(df), name="PID")
    else:
        pid_series = df[args.pid_col].rename("PID")

    prepared = pd.DataFrame({
        "PID": pid_series,
        "response": df[args.response_col],
        "question_type": args.question_type,
    })

    empty_responses = (
        prepared["response"].isna()
        | prepared["response"].astype(str).str.strip().eq("")
    ).sum()

    print("=== prep_dataset.py summary ===")
    print(f"Input:        {input_path}")
    print(f"Output:       {output_path}")
    print(f"Rows:         {len(prepared)}")
    print(f"Empty/NaN responses: {empty_responses}")
    print(f"Question type: {args.question_type}")
    print(f"Columns:      {list(prepared.columns)}")

    if args.dry_run:
        print("Dry run — file not saved.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prepared.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Saved: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
