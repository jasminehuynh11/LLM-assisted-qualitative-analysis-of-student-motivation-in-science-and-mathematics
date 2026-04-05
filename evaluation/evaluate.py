"""
evaluate.py — compares LLM-coded output against human review labels.

Usage:
  python evaluation/evaluate.py \
    --coded data/coded/TrainingSet_Dataset_coded.xlsx \
    --human data/human_review/TrainingSet_HumanReview.xlsx \
    --output evaluation/evaluation_report.md
"""
import argparse
import pandas as pd
from pathlib import Path


def load(path: str) -> pd.DataFrame:
    return pd.read_excel(path)


def evaluate(coded: pd.DataFrame, human: pd.DataFrame) -> dict:
    """
    Expects human review file to have a 'correct?' column with values:
      'correct', 'partial', 'incorrect', 'unsure'
    """
    merged = coded.copy()
    merged["human_label"] = human["correct?"].values

    total = len(merged)
    correct = (merged["human_label"] == "correct").sum()
    partial = (merged["human_label"] == "partial").sum()
    incorrect = (merged["human_label"] == "incorrect").sum()
    unsure = (merged["human_label"] == "unsure").sum()

    return {
        "total": total,
        "correct": int(correct),
        "partial": int(partial),
        "incorrect": int(incorrect),
        "unsure": int(unsure),
        "accuracy_strict": round(correct / total * 100, 2),
        "accuracy_lenient": round((correct + partial) / total * 100, 2),
        "error_rate": round(incorrect / total * 100, 2),
    }


def report(metrics: dict, output_path: str) -> None:
    lines = [
        "# Evaluation Report\n",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total reviewed | {metrics['total']} |",
        f"| Correct | {metrics['correct']} ({metrics['accuracy_strict']}%) |",
        f"| Partially correct | {metrics['partial']} |",
        f"| Incorrect | {metrics['incorrect']} ({metrics['error_rate']}%) |",
        f"| Unsure | {metrics['unsure']} |",
        f"| **Strict accuracy** | **{metrics['accuracy_strict']}%** |",
        f"| **Lenient accuracy (correct + partial)** | **{metrics['accuracy_lenient']}%** |",
    ]
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {output_path}")
    for k, v in metrics.items():
        print(f"  {k}: {v}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--coded", required=True)
    parser.add_argument("--human", required=True)
    parser.add_argument("--output", default="evaluation/evaluation_report.md")
    args = parser.parse_args()

    coded = load(args.coded)
    human = load(args.human)
    metrics = evaluate(coded, human)
    report(metrics, args.output)


if __name__ == "__main__":
    main()
