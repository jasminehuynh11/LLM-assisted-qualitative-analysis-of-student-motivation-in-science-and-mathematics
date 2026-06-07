#!/usr/bin/env python3
"""
verify_setup.py — run this from project root to confirm all v3.2.0 changes are correct.
Usage: python verify_setup.py
"""
import os
import re
import sys
from pathlib import Path

# Windows consoles often use cp1252; reconfigure so status symbols print cleanly.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "
results = []

def check(label, condition, fix=""):
    status = PASS if condition else FAIL
    results.append((status, label, fix))
    print(f"{status} {label}" + (f"\n   Fix: {fix}" if not condition and fix else ""))

def warn(label, condition, note=""):
    status = PASS if condition else WARN
    results.append((status, label, note))
    print(f"{status} {label}" + (f"\n   Note: {note}" if not condition and note else ""))

print("=" * 60)
print("VERIFY SETUP — v3.2.0")
print("=" * 60)

# ── 1. FILE EXISTENCE ─────────────────────────────────────────
print("\n--- File Existence ---")
required_files = [
    "prompts/codebook.md",
    "prompts/system.txt",
    "prompts/question_type_context.json",
    "prompts/user_message_template.md",
    "logs/README.md",
    "logs/coding_runs.md",
    "logs/human_reviews.md",
    "CHANGELOG.md",
    "README.md",
    "code_responses.py",
    "evaluation/evaluate.py",
    "data/raw",
    "data/coded",
    "data/human_review",
]
for f in required_files:
    check(f"Exists: {f}", Path(f).exists(), f"Create missing: {f}")

# ── 2. CODEBOOK — DEFINITIONS TABLE ───────────────────────────
print("\n--- Codebook: Code Definitions ---")
cb = Path("prompts/codebook.md").read_text(encoding="utf-8")

required_codes = [
    "valuing_positive", "valuing_negative",
    "social_agents_positive", "social_agents_negative",
    "mastery_positive", "mastery_negative",
    "self_beliefs_positive", "self_beliefs_negative",
    "uncertain_control_negative",
    "structural_positive", "structural_negative",
    "failure_avoidance_negative", "anxiety_negative",
]
for code in required_codes:
    check(f"Code defined: {code}", f"`{code}`" in cb,
          f"Add `{code}` to codebook.md definitions table")

# ── 3. CODEBOOK — KEY SECTIONS ────────────────────────────────
print("\n--- Codebook: Required Sections ---")
required_sections = [
    ("Code Definitions", "## Code Definitions"),
    ("Critical Disambiguation Rules", "## Critical Disambiguation Rules"),
    ("Quick Reference table", "## Quick Reference"),
    ("Question Type Valence Rule", "## Question Type Valence Rule"),
    ("Few-shot examples", "## Few-shot examples"),
    ("Confidence Score Rules", "## Confidence Score Rules"),
    ("Edge Case Handling", "## Edge Case Handling"),
    ("Three edge case categories", "Insufficient Data"),
    ("Ambiguous category", "Ambiguous"),
    ("Uncodeable category", "Uncodeable"),
    ("Human reviewer note in edge cases", "human"),
]
for label, marker in required_sections:
    check(f"Section present: {label}", marker in cb,
          f"Add section containing '{marker}' to codebook.md")

# ── 4. CODEBOOK — BOUNDARY CONDITIONS ─────────────────────────
print("\n--- Codebook: Boundary Conditions ---")
boundary_checks = [
    ("Apply when column present", "Apply when"),
    ("Do NOT apply column present", "Do NOT apply"),
    ("mastery vs valuing boundary", "valuing_positive" in cb and "mastery_positive" in cb),
    ("uncertain_control helplessness signal", "helpless"),
    ("failure_avoidance vs anxiety distinction", "shame"),
    ("structural vs valuing distinction", "real life"),
    ("broadens understanding as mastery signal", "broadens"),
]
for label, check_val in boundary_checks:
    if isinstance(check_val, bool):
        check(f"Boundary: {label}", check_val)
    else:
        check(f"Boundary: {label}", check_val in cb,
              f"Add '{check_val}' signal to codebook.md")

# ── 5. TERMINOLOGY — NO WRONG FORMATS ─────────────────────────
print("\n--- Terminology: Underscore Format ---")
wrong_patterns = [
    r"valuing - positive", r"valuing - negative",
    r"mastery - positive", r"mastery - negative",
    r"social agents", r"self beliefs",
    r"uncertain control", r"failure avoidance",
]
for prompt_file in Path("prompts").glob("*.md"):
    content = prompt_file.read_text(encoding="utf-8")
    for pat in wrong_patterns:
        found = re.search(pat, content, re.IGNORECASE)
        check(f"No wrong format '{pat}' in {prompt_file.name}",
              not found,
              f"Replace '{pat}' with underscore format in {prompt_file.name}")

# Also check system.txt
sys_content = Path("prompts/system.txt").read_text(encoding="utf-8")
for pat in wrong_patterns:
    found = re.search(pat, sys_content, re.IGNORECASE)
    check(f"No wrong format '{pat}' in system.txt",
          not found,
          f"Replace '{pat}' with underscore format in system.txt")

# ── 6. SYSTEM.TXT — KEY CONTENT ───────────────────────────────
print("\n--- system.txt: Required Content ---")
sys_checks = [
    ("Martin framework reference", "Martin"),
    ("Valence context rule", "question_type"),
    ("Max 3 codes rule", "1 to 3"),
    ("Confidence 25 for uncodeable", "confidence_overall = 25"),
    ("Human reviewer note", "human"),
]
for label, marker in sys_checks:
    check(f"system.txt has: {label}", marker in sys_content,
          f"Add '{marker}' to system.txt")

# ── 7. CONFIDENCE CONSISTENCY ─────────────────────────────────
print("\n--- Confidence Score Consistency ---")
warn("Confidence threshold consistent (should all be 25 for uncodeable)",
     "25" in cb and "35" not in cb,
     "system.txt may still have ≤35 from older version — align to 25 for v3.2.0")

warn("No conflicting ≤40 and ≤25 thresholds for same case",
     not ("≤ 35" in sys_content and "= 25" in sys_content),
     "system.txt has both ≤35 and =25 — remove the ≤35 rule, standardise to 25")

# ── 8. QUESTION TYPE CONTEXT ──────────────────────────────────
print("\n--- question_type_context.json ---")
import json
try:
    qtc = json.loads(Path("prompts/question_type_context.json").read_text(encoding="utf-8"))
    expected_keys = ["like_science","like_math","dislike_science","dislike_math",
                     "stopped_science","stopped_math"]
    for k in expected_keys:
        check(f"question_type_context has key: {k}", k in qtc,
              f"Add '{k}' to question_type_context.json")
    for k in expected_keys:
        if k in qtc:
            is_positive = k.startswith("like_")
            valence_word = "positive" if is_positive else "negative"
            check(f"Valence instruction in context for {k}",
                  valence_word in qtc[k].lower(),
                  f"Add explicit valence instruction to '{k}' context")
except Exception as e:
    check("question_type_context.json readable", False, str(e))

# ── 9. LOGS ───────────────────────────────────────────────────
print("\n--- Logs ---")
for log_file in ["logs/coding_runs.md", "logs/human_reviews.md"]:
    content = Path(log_file).read_text(encoding="utf-8") if Path(log_file).exists() else ""
    check(f"{log_file} has template comment", "TEMPLATE" in content,
          "Add template comment block at top of file")
    check(f"{log_file} has Run/Review 001 (training set)", "001" in content,
          "Add Run/Review 001 entry for training set")
    check(f"{log_file} has Run/Review 002 (refinement)", "002" in content,
          "Add Run/Review 002 entry for refinement dataset")

# ── 10. CHANGELOG ─────────────────────────────────────────────
print("\n--- CHANGELOG.md ---")
cl = Path("CHANGELOG.md").read_text(encoding="utf-8") if Path("CHANGELOG.md").exists() else ""
for version in ["v3.2.0", "v3.1.0", "v3.0.0", "v2.0.0"]:
    check(f"CHANGELOG has {version}", version in cl,
          f"Add {version} entry to CHANGELOG.md")
check("v3.2.0 is at top of CHANGELOG",
      cl.index("v3.2.0") < cl.index("v3.1.0") if "v3.2.0" in cl and "v3.1.0" in cl else False,
      "Move v3.2.0 to top of CHANGELOG.md")
check("No [Current] tag remaining (should be removed)", "[Current]" not in cl,
      "Remove [Current] tag from CHANGELOG.md")

# ── SUMMARY ───────────────────────────────────────────────────
print("\n" + "=" * 60)
passed = sum(1 for s, _, _ in results if s == PASS)
failed = sum(1 for s, _, _ in results if s == FAIL)
warned = sum(1 for s, _, _ in results if s == WARN)
total = len(results)
print(f"SUMMARY: {passed}/{total} passed | {failed} failed | {warned} warnings")
if failed == 0 and warned == 0:
    print("🎉 All checks passed — ready to run next batch!")
elif failed == 0:
    print("✅ No failures — warnings are minor alignment issues only")
else:
    print(f"❌ {failed} issues need fixing before next run")
print("=" * 60)