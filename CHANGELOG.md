# Prompt Changelog

## v3.2.0 — Post-meeting updates

### Code definitions
- Updated all 13 code definitions with exact boundary conditions from Section A
- Added "broadens my understanding" and "helps me understand things better" as 
  explicit mastery_positive signals (based on Martin 2007 mastery orientation literature)
- Clarified mastery_positive vs valuing_positive boundary for learning-goal language

### Edge case handling
- Updated edge case categories to formally align with Section B methodology:
  - Category 1: Insufficient Data (single/two word, no evaluative statement)
  - Category 2: Ambiguous (could fit multiple codes, weak evidence)
  - Category 3: Uncodeable (does not map to any construct)
- All three categories: confidence_overall = 25, flagged for human self-assignment
- Removed automatic multi-code assignment for ambiguous responses
- Human reviewer (Emma) will self-assign final codes for all confidence ≤ 25 rows

### Terminology
- Standardised all code names to use exact underscore format throughout
  (e.g. valuing_positive not "valuing - positive" or "valuing positive")

## v3.1.0 — mastery_positive disambiguation correction
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
