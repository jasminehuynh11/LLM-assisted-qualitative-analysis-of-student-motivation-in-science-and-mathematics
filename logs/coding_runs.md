<!-- 
TEMPLATE — copy and paste this for each new run, add at the TOP of the file:

## Run 00X — [Dataset Name]
- **Date:** [DD Month YYYY]
- **Dataset:** data/raw/[filename].xlsx ([N] responses)
- **Output:** data/coded/[filename]_coded.xlsx
- **Model:** openai:[model-name]
- **Prompt version:** v[X.X.X]
- **Temperature:** 0.2
- **Command run:**
python code_responses.py 
--input data/raw/[filename].xlsx 
--output data/coded/[filename]_coded.xlsx 
--provider openai 
--model [model] 
--temperature 0.2 
--checkpoint-every 25
- **Notes:**
  - [anything notable about this run]
-->

# Coding Run Log

Each entry records one LLM coding run. Update this file every time 
code_responses.py is run on a new or existing dataset.

---

## Run 003 — like_science (per-type dataset)
- **Date:** June 2026
- **Dataset:** data/raw/like_science.xlsx → data/prepared/like_science_prepared.xlsx (998 responses)
- **Output:** data/coded/like_science_coded.xlsx
- **Model:** openai:gpt-4o
- **Prompt version:** v3.2.0
- **Temperature:** 0.2
- **Command run:**
python scripts/prep_dataset.py 
--input data/raw/like_science.xlsx 
--output data/prepared/like_science_prepared.xlsx 
--question-type like_science 
--response-col "Why do you like SCIENCE?"

python code_responses.py 
--input data/prepared/like_science_prepared.xlsx 
--output data/coded/like_science_coded.xlsx 
--provider openai 
--model gpt-4o 
--temperature 0.2 
--checkpoint-every 25 
--sleep 0.3
- **Notes:**
  - First run of per-type dataset format; preprocessed via prep_dataset.py
  - 998/998 rows coded successfully, 0 coding errors
  - code_1 distribution: valuing_positive 648, mastery_positive 259, structural_positive 46, social_agents_positive 38, self_beliefs_positive 7
  - 35 rows flagged confidence ≤ 25 for human review (Emma self-assignment)
  - 279 rows (28.0%) have code_2; 16 rows (1.6%) have code_3
  - Spot-test noted under-coding on dual-signal responses (mastery + valuing); full run multi-code rate ~28% on code_2
  - Column reference: scripts/dataset_columns.md

---

## Run 002 — Refinement Dataset
- **Date:** April 2025
- **Dataset:** data/raw/refinement_dataset.xlsx (390 responses)
- **Output:** data/coded/refinement_dataset_coded.xlsx
- **Model:** openai:gpt-4o
- **Prompt version:** v3.1.0 → v3.2.0 (updated mid-review)
- **Temperature:** 0.2
- **Command run:**
python code_responses.py 
--input data/raw/refinement_dataset.xlsx 
--output data/coded/refinement_dataset_coded.xlsx 
--provider openai 
--model gpt-4o 
--temperature 0.2 
--checkpoint-every 25
- **Notes:**
  - Upgraded from gpt-4o-mini to gpt-4o
  - Fixed fallback code direction for negative question types
  - Fixed valence rule enforcement via question_type_context.json
  - Added confidence ≤ 40 rule for short/vague responses
  - Zero valence mismatches across full dataset
  - 14 rows correctly flagged with confidence ≤ 40 for human review

---

## Run 001 — Training Set
- **Date:** April 2025
- **Dataset:** data/raw/TrainingSet_Dataset.xlsx (390 responses)
- **Output:** data/coded/TrainingSet_Dataset_coded.xlsx
- **Model:** openai:gpt-4o-mini
- **Prompt version:** v2.0.0
- **Temperature:** 0.2
- **Command run:**
python code_responses.py 
--input data/raw/TrainingSet_Dataset.xlsx 
--output data/coded/TrainingSet_Dataset_coded.xlsx 
--provider openai 
--model gpt-4o-mini 
--temperature 0.2 
--checkpoint-every 25
- **Notes:**
  - First full run on training set
  - Four systematic errors identified post-run (see human_reviews.md — Review 001)
  - mastery_positive over-applied (~84 partial errors)
  - structural over-applied
  - uncertain_control_negative over-applied
  - self_beliefs vs mastery confused
