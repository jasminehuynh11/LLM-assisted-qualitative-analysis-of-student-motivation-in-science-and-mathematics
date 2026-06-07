<!--
TEMPLATE — copy and paste this for each new review, add at the TOP of the file:

## Review 00X — [Dataset Name]
- **Date:** [DD Month YYYY]
- **Reviewer:** [Name]
- **Dataset reviewed:** data/coded/[filename]_coded.xlsx ([N] responses)
- **Type:** [Full manual / Spot-check / Automated analysis]
- **Results:**
  - [N] fully correct ([X]%)
  - [N] partially correct ([X]%)
  - [N] unsure / low confidence ([X]%)
  - [N] incorrect ([X]%)
- **Decisions made:**
  - [any coding decisions or rule changes agreed]
- **Pending:**
  - [anything that needs follow-up]
-->

# Human Review Log

Each entry records one human review session. Update this file every time 
a human reviewer codes or spot-checks a dataset.

---

## Review 002 — Refinement Dataset Spot Review
- **Date:** April 2025
- **Reviewer:** Jasmine
- **Dataset reviewed:** data/coded/refinement_dataset_coded.xlsx (390 responses)
- **Type:** Full automated analysis + manual spot-check of flagged rows
- **Results:**
  - 375 fully correct (~96.2%)
  - 14 flagged as too brief / low confidence (≤ 40) — pending Emma self-assignment
  - 1 remaining edge case (PID 1261: "Teachers, content" → valuing_negative conf 25)
  - 389/390 correct overall
  - 0 valence mismatches
- **Decisions made:**
  - All confidence ≤ 40 rows to be self-assigned by Emma (human reviewer)
  - Edge case handling formally documented in Section B methodology
- **Issues resolved since Review 001:**
  - Zero uncertain_control_negative over-application
  - Zero valence mismatches
  - Fallback code direction fixed for negative question types
  - Short response confidence correctly ≤ 40
- **Pending:**
  - Emma to self-assign final codes for 14 low-confidence rows
  - Emma and Mark to review Section A code definitions
  - Emma and Mark to confirm edge case handling approach (Section B)

---

## Review 001 — Training Set Human Review
- **Date:** April 2025
- **Reviewer:** Jasmine
- **Dataset reviewed:** data/coded/TrainingSet_Dataset_coded.xlsx (390 responses)
- **Type:** Full manual human review of all 390 rows
- **Results:**
  - 270 fully correct (69.2%)
  - 110 partially correct (28.2%)
  - 9 unsure (2.3%) — responses too brief to code confidently
  - 1 incorrect (0.3%) — "because I'm Asian" miscoded
  - 97.4% correct or partially correct overall
- **Four systematic errors identified:**
  1. mastery_positive over-applied — triggered by "learning" or "understanding" 
     (~84 partial errors)
  2. structural over-applied — triggered by real-world relevance instead of 
     class format/activities/pace
  3. uncertain_control_negative over-applied — triggered by difficulty alone 
     instead of persistent helplessness
  4. self_beliefs vs mastery confused — e.g. "I understand it" coded as 
     self_beliefs_positive
- **Actions taken:**
  - Rewrote all 13 code definitions (prompt v3.0.0)
  - Added disambiguation rules and quick reference table
  - Added question type valence rule
  - Added confidence score rules for short responses
  - Upgraded model from gpt-4o-mini to gpt-4o
  - Fixed fallback code direction for negative question types
- **Shared with:** Emma Burns, Mark Dras
