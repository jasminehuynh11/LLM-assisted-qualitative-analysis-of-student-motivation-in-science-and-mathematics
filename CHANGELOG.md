# Prompt Changelog

## v3.1.0 — [Current] Valence enforcement + confidence rules
- Updated question_type_context.json with explicit valence enforcement per question type
  (positive codes for like_*, negative codes for dislike_*/stopped_*)
- Added Confidence Score Rules table to codebook.md
- Added short-response rule to system.txt (≤ 3 words → confidence ≤ 35)

## v3.0.0 — Post human-review improvements
- Rewrote all 13 code definitions with explicit boundary conditions
- Added Critical Disambiguation Rules section targeting 4 systematic errors:
  - mastery_positive over-applied
  - structural over-applied
  - uncertain_control_negative over-applied
  - self_beliefs vs mastery confusion
- Added Quick Reference disambiguation table
- Added Question Type Valence Rule
- Added edge case handling instructions

## v2.0.0 — Original training set run
- Basic definitions + 13 few-shot examples
- Identified issues: mastery_positive over-applied, structural over-applied,
  uncertain_control_negative over-applied, self_beliefs/mastery confusion
- Training set accuracy: 69.2% strict, 97.4% lenient (390 responses)

## v1.0.0 — Initial prototype
- First prompt structure, basic codebook only
