# Prompt Changelog

## v3.1.0 — [Current] mastery_positive disambiguation correction
- **Codebook Rule 1 updated** (`mastery_positive` vs `valuing_positive`):
  - "interesting / fun / cool" alone → `valuing_positive` ONLY (unchanged)
  - Added: "I like learning how things work / want to understand things" → `mastery_positive` (learning goal = mastery orientation)
  - Added: "broadens my understanding / helps me understand the world" → `mastery_positive`
  - Replaced blanket ❌ rule with a more precise boundary: DO NOT apply `mastery_positive` for pure enjoyment/interest with **no** learning or understanding component
- **Quick Reference table extended** with two new mastery_positive rows to match Rule 1
- Theoretical basis: distinguishes intrinsic enjoyment (valuing) from mastery-goal orientation (active desire to understand/learn), consistent with expectancy-value and achievement goal theory

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
