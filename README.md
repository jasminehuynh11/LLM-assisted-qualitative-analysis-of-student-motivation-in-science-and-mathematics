# LLM-assisted qualitative coding (science & mathematics motivation)

Python pipeline that reads survey responses from Excel, calls OpenAI (JSON output), and writes thematic codes plus confidence scores to a new workbook.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

## Run

```bash
python code_responses.py --dry-run
python code_responses.py
```

Options: `--limit N`, `--overwrite`, `--force-unlock`, `--provider gemini`, `--model ...`

## Running a New Batch

### First time setup
```bash
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

### Code a new dataset
```bash
python code_responses.py \
  --input data/raw/YourNewDataset.xlsx \
  --output data/coded/YourNewDataset_coded.xlsx \
  --provider openai \
  --model gpt-4o-mini \
  --temperature 0.2
```

### Evaluate against human review
```bash
python evaluation/evaluate.py \
  --coded data/coded/YourNewDataset_coded.xlsx \
  --human data/human_review/YourNewDataset_HumanReview.xlsx \
  --output evaluation/evaluation_report.md
```

### Prompt versioning
- All prompt changes are tracked in CHANGELOG.md
- Current prompt version: v3.0.0
- The script stamps each coded row with `prompt_version` so you always know which prompt produced which output

## Project Layout

```
prompts/
  codebook.md                     ← code definitions, disambiguation rules, few-shot examples
  question_type_context.json      ← per-question-type context strings
  system.txt                      ← system prompt
  user_message_template.md        ← user message template

data/
  raw/                            ← original uncoded input files (never modify)
  coded/                          ← LLM output files
  human_review/                   ← human review files with correct? column

evaluation/
  evaluate.py                     ← compares LLM vs human codes
  evaluation_report.md            ← output summary of accuracy metrics

code_responses.py                 ← main coding script
CHANGELOG.md                      ← tracks prompt versions and what changed
```

## Data Folder Conventions
- `data/raw/` — original uncoded input files, never modify
- `data/coded/` — LLM output files
- `data/human_review/` — human review files with `correct?` column
  - Allowed values: `correct`, `partial`, `incorrect`, `unsure`

## License

Use and adapt for your research; ensure ethics approval and data handling match your institution's rules.
