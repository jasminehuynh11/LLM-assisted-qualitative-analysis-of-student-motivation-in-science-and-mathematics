# Logs

This folder tracks every coding run and human review session for reproducibility 
and research transparency. Every time you run the model or complete a human review, 
add an entry to the relevant log file.

## Why this matters
- Provides an audit trail for the paper's methods section
- Tracks which prompt version and model produced which output
- Records human review decisions and inter-rater notes
- Allows the team to reproduce any result from any point in time

## Files
- `coding_runs.md` — log of every LLM coding run (date, model, prompt version, dataset, results)
- `human_reviews.md` — log of every human review session (date, reviewer, dataset, accuracy metrics)
