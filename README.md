# LLM-assisted qualitative coding (science & mathematics motivation)

Python pipeline that reads survey responses from Excel, calls OpenAI (JSON output), and writes thematic codes plus confidence scores to a new workbook.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set OPENAI_API_KEY (never commit .env)
```

## Run

```bash
python code_responses.py --dry-run
python code_responses.py
```

Options: `--limit N`, `--overwrite`, `--force-unlock`, `--provider gemini`, `--model ...`

## Project layout

- `code_responses.py` — CLI and pipeline  
- `prompts/` — `codebook.md`, `user_message_template.md`, `system.txt`, `question_type_context.json`  

## Data

`TestPerformance_Dataset*.xlsx` files are gitignored by default (student responses). Place your input file next to the script or pass `--input` / `--output`.

## License

Use and adapt for your research; ensure ethics approval and data handling match your institution’s rules.
