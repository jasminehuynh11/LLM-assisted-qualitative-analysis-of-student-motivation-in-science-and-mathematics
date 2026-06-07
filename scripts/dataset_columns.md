# Raw Dataset Column Reference

Per-question-type Excel files in `data/raw/` use question-specific column names (case-sensitive).
Use these **exact** `--response-col` values with `scripts/prep_dataset.py`.

| Raw file | Rows | `--question-type` | `--response-col` (exact) |
|---|---:|---|---|
| `like_science.xlsx` | 998 | `like_science` | `Why do you like SCIENCE?` |
| `like_math.xlsx` | 895 | `like_math` | `Why do you like MATHS?` |
| `not_like_science.xlsx` | 264 | `dislike_science` | `Why do you not like SCIENCE?` |
| `not_like_math.xlsx` | 353 | `dislike_math` | `Why do you not like MATHS?` |
| `stop_liking_science.xlsx` | 262 | `stopped_science` | `Why did you stop liking SCIENCE? (e.g., subject content, classroom experiences)` |
| `stop_liking_math.xlsx` | 353 | `stopped_math` | `Why did you stop liking MATHS? (e.g., subject content, classroom experiences)` |

All six files use `PID` as the participant ID column (default `--pid-col`).

## Example commands

### like_science (dry-run)
```bash
python scripts/prep_dataset.py \
  --input data/raw/like_science.xlsx \
  --question-type like_science \
  --response-col "Why do you like SCIENCE?" \
  --dry-run
```

### like_science (prepare + code)
```bash
python scripts/prep_dataset.py \
  --input data/raw/like_science.xlsx \
  --output data/prepared/like_science_prepared.xlsx \
  --question-type like_science \
  --response-col "Why do you like SCIENCE?"

python code_responses.py \
  --input data/prepared/like_science_prepared.xlsx \
  --output data/coded/like_science_coded.xlsx \
  --provider openai \
  --model gpt-4o \
  --temperature 0.2 \
  --checkpoint-every 25 \
  --sleep 0.3
```

Prepared files go in `data/prepared/` to keep `data/raw/` for originals only.
