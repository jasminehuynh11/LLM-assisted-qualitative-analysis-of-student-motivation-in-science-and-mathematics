"""
Thematic coding: reads TestPerformance_Dataset.xlsx, calls an LLM, writes TestPerformance_Dataset_coded.xlsx.

Prompts live in ./prompts/ (edit codebook.md to refine definitions and few-shot examples).

Setup: pip install -r requirements.txt
       copy .env.example .env   # set OPENAI_API_KEY (default provider is OpenAI) — never commit .env

Examples:
  python code_responses.py --dry-run
  python code_responses.py --limit 5
  python code_responses.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

PROMPT_VERSION = "3.1.0"

_BASE = Path(__file__).resolve().parent
_PROMPTS = _BASE / "prompts"

# Load .env from this script's folder (utf-8-sig strips Windows BOM if present)
load_dotenv(_BASE / ".env", encoding="utf-8-sig")

ALLOWED_CODES: frozenset[str] = frozenset(
    {
        "valuing_positive",
        "valuing_negative",
        "social_agents_positive",
        "social_agents_negative",
        "mastery_positive",
        "mastery_negative",
        "self_beliefs_positive",
        "self_beliefs_negative",
        "uncertain_control_negative",
        "structural_positive",
        "structural_negative",
        "failure_avoidance_negative",
        "anxiety_negative",
    }
)


@lru_cache(maxsize=1)
def _question_type_context() -> dict[str, str]:
    path = _PROMPTS / "question_type_context.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {str(k): str(v) for k, v in data.items()}


@lru_cache(maxsize=1)
def _load_codebook() -> str:
    return (_PROMPTS / "codebook.md").read_text(encoding="utf-8").strip()


@lru_cache(maxsize=1)
def _load_user_template() -> str:
    return (_PROMPTS / "user_message_template.md").read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def _load_system_prompt() -> str:
    return (_PROMPTS / "system.txt").read_text(encoding="utf-8").strip()


def _question_context(question_type: str) -> str:
    return _question_type_context().get(
        question_type,
        f"Survey context: question_type is {question_type!r}.",
    )


def build_user_message(question_type: str, response_text: str) -> str:
    codebook = _load_codebook()
    qctx = _question_context(question_type)
    template = _load_user_template()
    return (
        template.replace("{codebook}", codebook)
        .replace("{question_context}", qctx)
        .replace("{response}", response_text)
    )


def strip_json_fence(text: str) -> str:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if m:
        return m.group(1).strip()
    return text


def parse_llm_json(text: str) -> dict[str, Any]:
    raw = strip_json_fence(text)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            return json.loads(m.group(0))
        raise


def _coerce_to_allowed_code(raw: str) -> str | None:
    """Map model output (e.g. 'valuing - positive') to canonical ALLOWED_CODES string."""
    t = raw.strip()
    if t in ALLOWED_CODES:
        return t
    s = t.lower()
    s = re.sub(r"\s*[-–—]\s*", "_", s)
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if s in ALLOWED_CODES:
        return s
    # Table-style typos / variants
    fixes = {
        "self_beliefs_beliefs_positive": "self_beliefs_positive",
        "failure_avoidance": "failure_avoidance_negative",
    }
    s2 = fixes.get(s, s)
    if s2 in ALLOWED_CODES:
        return s2
    return None


_NEGATIVE_QTYPES: frozenset[str] = frozenset(
    {"dislike_science", "dislike_math", "stopped_science", "stopped_math"}
)
_POSITIVE_QTYPES: frozenset[str] = frozenset(
    {"like_science", "like_math"}
)

# Bidirectional valence flip map.  Codes with no positive counterpart
# (failure_avoidance_negative, anxiety_negative, uncertain_control_negative)
# are intentionally absent — they are never flipped.
_VALENCE_FLIP: dict[str, str] = {
    "valuing_positive": "valuing_negative",
    "valuing_negative": "valuing_positive",
    "mastery_positive": "mastery_negative",
    "mastery_negative": "mastery_positive",
    "self_beliefs_positive": "self_beliefs_negative",
    "self_beliefs_negative": "self_beliefs_positive",
    "social_agents_positive": "social_agents_negative",
    "social_agents_negative": "social_agents_positive",
    "structural_positive": "structural_negative",
    "structural_negative": "structural_positive",
}


def enforce_valence(codes: list[str], question_type: str) -> tuple[list[str], bool]:
    """Flip any code whose valence contradicts the question type.

    Negative question types (dislike_*/stopped_*) must only produce negative
    codes.  Positive question types (like_*) must only produce positive codes.
    Codes with no positive counterpart (anxiety, failure_avoidance,
    uncertain_control) are never flipped — they cannot appear in positive
    contexts but the model is relied upon not to assign them there.

    Returns (corrected_codes, was_changed).
    """
    if question_type not in _NEGATIVE_QTYPES and question_type not in _POSITIVE_QTYPES:
        return codes, False

    corrected: list[str] = []
    changed = False
    for code in codes:
        if question_type in _NEGATIVE_QTYPES and code.endswith("_positive"):
            flipped = _VALENCE_FLIP.get(code, code)
            corrected.append(flipped)
            changed = True
        elif question_type in _POSITIVE_QTYPES and code.endswith("_negative"):
            flipped = _VALENCE_FLIP.get(code, code)
            # Only flip if a positive counterpart exists
            if flipped != code:
                corrected.append(flipped)
                changed = True
            else:
                corrected.append(code)
        else:
            corrected.append(code)
    return corrected, changed


def normalize_codes(data: dict[str, Any], question_type: str = "") -> tuple[list[str], list[int], int, str]:
    codes_raw = data.get("codes")
    if not isinstance(codes_raw, list):
        raise ValueError("codes must be a list")
    codes: list[str] = []
    for c in codes_raw[:3]:
        if not isinstance(c, str):
            continue
        canon = _coerce_to_allowed_code(c)
        if canon and canon not in codes:
            codes.append(canon)
    if not codes:
        fallback = "valuing_negative" if question_type in _NEGATIVE_QTYPES else "valuing_positive"
        conf_all_fb = 25
        rationale_fb = (
            "Fallback: model returned no valid codebook labels (response may be too brief). "
            "Review manually."
        )
        return [fallback], [conf_all_fb], conf_all_fb, rationale_fb

    conf_all = data.get("confidence_overall")
    if not isinstance(conf_all, int) or not (0 <= conf_all <= 100):
        if isinstance(conf_all, (int, float)) and 0 <= float(conf_all) <= 100:
            conf_all = int(round(float(conf_all)))
        else:
            conf_all = 50

    per = data.get("confidence_per_code")
    conf_per: list[int] = []
    if isinstance(per, list) and len(per) == len(codes):
        for x in per:
            if isinstance(x, (int, float)) and 0 <= float(x) <= 100:
                conf_per.append(int(round(float(x))))
            else:
                conf_per.append(conf_all)
    else:
        conf_per = [conf_all] * len(codes)

    rationale = data.get("rationale_short", "")
    if not isinstance(rationale, str):
        rationale = str(rationale)
    rationale = rationale.strip()[:2000]

    return codes, conf_per, conf_all, rationale


def call_openai(model: str, user_message: str, temperature: float) -> str:
    from openai import OpenAI

    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set (create a .env file in this folder)")
    client = OpenAI(api_key=api_key)
    system = _load_system_prompt()
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
    )
    choice = completion.choices[0].message.content
    if not choice:
        raise RuntimeError("Empty response from OpenAI")
    return choice


def call_gemini(model: str, user_message: str, temperature: float) -> str:
    import google.generativeai as genai

    api_key = (os.environ.get("GEMINI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set (create a .env file in this folder)")
    genai.configure(api_key=api_key)
    system = _load_system_prompt()
    gm = genai.GenerativeModel(model, system_instruction=system)
    response = gm.generate_content(
        user_message,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            response_mime_type="application/json",
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Empty response from Gemini")
    return text


def code_row(
    provider: str,
    model: str,
    question_type: str,
    response_text: str,
    temperature: float,
    retry: int = 1,
) -> tuple[dict[str, Any], str | None]:
    if not isinstance(response_text, str) or not response_text.strip():
        return (
            {
                "code_1": "",
                "code_2": "",
                "code_3": "",
                "confidence_overall": "",
                "confidence_code_1": "",
                "confidence_code_2": "",
                "confidence_code_3": "",
                "rationale_short": "",
                "coding_error": "empty_response",
                "llm_raw_json": "",
            },
            None,
        )

    user_message = build_user_message(question_type, response_text.strip())
    last_err: str | None = None
    raw_accum: str | None = None

    for attempt in range(retry + 1):
        try:
            if provider == "openai":
                raw = call_openai(model, user_message, temperature)
            else:
                raw = call_gemini(model, user_message, temperature)
            raw_accum = raw
            data = parse_llm_json(raw)
            codes, conf_per, conf_all, rationale = normalize_codes(data, question_type)
            codes, valence_changed = enforce_valence(codes, question_type)
            if valence_changed:
                rationale = f"[valence enforced for {question_type}] " + rationale
            row_out: dict[str, Any] = {
                "code_1": codes[0] if len(codes) > 0 else "",
                "code_2": codes[1] if len(codes) > 1 else "",
                "code_3": codes[2] if len(codes) > 2 else "",
                "confidence_overall": conf_all,
                "confidence_code_1": conf_per[0] if len(conf_per) > 0 else "",
                "confidence_code_2": conf_per[1] if len(conf_per) > 1 else "",
                "confidence_code_3": conf_per[2] if len(conf_per) > 2 else "",
                "rationale_short": rationale,
                "coding_error": "",
                "llm_raw_json": raw_accum or "",
            }
            return row_out, raw_accum
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt < retry:
                time.sleep(1.5 * (attempt + 1))
            continue

    return (
        {
            "code_1": "",
            "code_2": "",
            "code_3": "",
            "confidence_overall": "",
            "confidence_code_1": "",
            "confidence_code_2": "",
            "confidence_code_3": "",
            "rationale_short": "",
            "coding_error": last_err or "unknown_error",
            "llm_raw_json": raw_accum or "",
        },
        raw_accum,
    )


CORE_OUTPUT_COLS = [
    "code_1",
    "code_2",
    "code_3",
    "confidence_overall",
    "confidence_code_1",
    "confidence_code_2",
    "confidence_code_3",
    "rationale_short",
    "llm_model",
    "prompt_version",
    "coding_error",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Thematic coding via LLM → Excel columns.")
    parser.add_argument("--input", default="TestPerformance_Dataset.xlsx", help="Input xlsx path")
    parser.add_argument("--output", default="TestPerformance_Dataset_coded.xlsx", help="Output xlsx path")
    parser.add_argument("--provider", choices=("openai", "gemini"), default="openai", help="API provider")
    parser.add_argument(
        "--model",
        default="",
        help="Model id (default: gpt-4o-mini / gemini-1.5-flash)",
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--limit", type=int, default=0, help="Process at most N rows (0 = all)")
    parser.add_argument("--start", type=int, default=0, help="0-based row index to start")
    parser.add_argument("--overwrite", action="store_true", help="Recode rows that already have code_1")
    parser.add_argument("--checkpoint-every", type=int, default=25, help="Save workbook every N coded rows")
    parser.add_argument("--include-raw", action="store_true", help="Keep llm_raw_json column in output")
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.2,
        help="Seconds to wait between API calls (rate limits)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Load xlsx only, no API calls")
    parser.add_argument(
        "--force-unlock",
        action="store_true",
        help="Remove stale .code_responses.lock if a previous run crashed",
    )
    args = parser.parse_args()

    if args.provider == "openai" and not args.model:
        args.model = "gpt-4o-mini"
    if args.provider == "gemini" and not args.model:
        args.model = "gemini-1.5-flash"

    project_root = str(_BASE)
    input_path = args.input if os.path.isabs(args.input) else os.path.join(project_root, args.input)
    output_path = args.output if os.path.isabs(args.output) else os.path.join(project_root, args.output)

    if not (_PROMPTS / "codebook.md").is_file():
        print("Missing prompts/codebook.md next to this script.", file=sys.stderr, flush=True)
        sys.exit(1)

    lock_path = _BASE / ".code_responses.lock"
    if args.force_unlock and lock_path.exists():
        lock_path.unlink(missing_ok=True)
        print("Removed .code_responses.lock", file=sys.stderr, flush=True)

    df_input = pd.read_excel(input_path)
    if "code " in df_input.columns:
        df_input = df_input.rename(columns={"code ": "code_legacy"})

    # Always resume from existing output as the base so rows outside the
    # current --start/--limit range are never lost. --overwrite only controls
    # whether already-coded rows *within* the requested range get re-coded.
    if (
        os.path.isfile(output_path)
        and not args.dry_run
    ):
        try:
            df_prev = pd.read_excel(output_path)
            if len(df_prev) == len(df_input):
                df = df_prev
                print(
                    f"Resuming from existing output ({output_path})",
                    file=sys.stderr,
                    flush=True,
                )
            else:
                df = df_input.copy()
                print(
                    f"Warning: output row count ({len(df_prev)}) != input ({len(df_input)}); using input only",
                    file=sys.stderr,
                    flush=True,
                )
        except Exception as e:
            df = df_input.copy()
            print(f"Warning: could not read output ({e}); using input only", file=sys.stderr, flush=True)
    else:
        df = df_input.copy()

    for c in CORE_OUTPUT_COLS:
        if c not in df.columns:
            df[c] = pd.NA
    for c in CORE_OUTPUT_COLS:
        if c in df.columns:
            df[c] = df[c].astype(object)
    if args.include_raw and "llm_raw_json" not in df.columns:
        df["llm_raw_json"] = pd.NA
    elif not args.include_raw and "llm_raw_json" in df.columns:
        df = df.drop(columns=["llm_raw_json"])

    if args.dry_run:
        print(f"Loaded {input_path}: {len(df)} rows, columns={list(df.columns)}", file=sys.stderr, flush=True)
        return

    if lock_path.exists():
        print(
            "Another run may be active (.code_responses.lock exists). "
            "Wait for it to finish, or delete the lock with: python code_responses.py --force-unlock",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)
    try:
        lock_path.write_text(str(os.getpid()), encoding="utf-8")
    except OSError as e:
        print(f"Could not create lock file: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

    n = len(df)
    end = n if args.limit <= 0 else min(n, args.start + args.limit)
    processed = 0

    try:
        for i in range(args.start, end):
            row = df.iloc[i]
            if not args.overwrite:
                existing = row.get("code_1", pd.NA)
                if pd.notna(existing) and str(existing).strip() != "":
                    continue

            qtype = row.get("question_type", "")
            if pd.isna(qtype):
                qtype = ""
            qtype = str(qtype).strip()

            resp = row.get("response", "")
            if pd.isna(resp):
                resp = ""

            out, _raw = code_row(
                args.provider,
                args.model,
                qtype,
                str(resp),
                args.temperature,
                retry=2,
            )
            out["llm_model"] = f"{args.provider}:{args.model}"
            out["prompt_version"] = PROMPT_VERSION
            if not args.include_raw:
                out.pop("llm_raw_json", None)

            for k, v in out.items():
                if k in df.columns:
                    df.at[i, k] = v

            processed += 1
            if processed % args.checkpoint_every == 0:
                save_df = df.copy()
                if not args.include_raw and "llm_raw_json" in save_df.columns:
                    save_df = save_df.drop(columns=["llm_raw_json"])
                save_df.to_excel(output_path, index=False)
                print(f"Checkpoint: saved {output_path} ({processed} rows this run)", file=sys.stderr, flush=True)

            if args.sleep > 0 and i < end - 1:
                time.sleep(args.sleep)

        save_df = df.copy()
        if not args.include_raw and "llm_raw_json" in save_df.columns:
            save_df = save_df.drop(columns=["llm_raw_json"])
        save_df.to_excel(output_path, index=False)
        print(
            f"Done: wrote {output_path} (rows index {args.start}..{end - 1}, {processed} coded this run)",
            file=sys.stderr,
            flush=True,
        )
    finally:
        lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
