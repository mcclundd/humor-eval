#!/usr/bin/env python3
"""
humor-eval: score_responses.py
Scores model responses against the 5-dimension humor evaluation rubric.
Uses an LLM-as-judge approach with structured output parsing.

Usage:
    python score_responses.py --input results/responses.jsonl
    python score_responses.py --input results/responses.jsonl --judge anthropic
    python score_responses.py --input results/responses.jsonl --sample 20
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DIMENSIONS = [
    "read_the_room",
    "bit_commitment",
    "energy_match",
    "buzzkill_check",
    "comedic_value",
]

BOOLEAN_FLAGS = [
    "explained_the_joke",
    "said_great_question",
    "added_disclaimer",
    "broke_character",
    "escalated_well",
    "had_a_specific_joke",
    "would_screenshot",
]

JUDGE_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "openai": "gpt-5.4",
}

RESULTS_DIR = Path(__file__).parent.parent / "results"

# ---------------------------------------------------------------------------
# Scoring prompt
# ---------------------------------------------------------------------------

SCORING_PROMPT = """You are an expert evaluator assessing whether AI models can read comedic register and be funny.

Score this response on each dimension. Return ONLY valid JSON.

## User Query
Category: {category}
Query: {query}

## Model Response ({model})
{response}

## Scoring Rubric

1. read_the_room (0-4): 0=completely missed register, 1=sensed humor but defaulted to assistant mode, 2=got the gist but hedged, 3=nailed the register, 4=understood the kind of person making the joke
2. bit_commitment (0-4): 0=refused/corrected premise, 1=one foot in then retreated, 2=played along mostly, 3=fully committed and built on it, 4=escalated — raised stakes or added unexpected twist
3. energy_match (-2 to +2): -2=dead/corporate, -1=underpowered/too careful, 0=roughly right, +1=matched tone and pacing, +2=vibes immaculate
4. buzzkill_check (0-4): 0=full buzzkill (disclaimed/corrected/explained joke), 1=partial buzzkill, 2=mostly clean, 3=no buzzkill, 4=anti-buzzkill (made it MORE fun)
5. comedic_value (0-4): 0=not funny, 1=polite chuckle, 2=genuinely funny moment, 3=good laugh/memorable, 4=screenshot-worthy

Also flag these booleans (true/false):
- explained_the_joke: model explained why the premise is funny or not real
- said_great_question: used "great question," "love this," "that's hilarious," etc.
- added_disclaimer: included safety, health, or factual disclaimers
- broke_character: started in-bit then dropped out to be helpful
- escalated_well: added to the bit in a way that raised the stakes
- had_a_specific_joke: response contained an identifiable joke, not just general playfulness
- would_screenshot: funny enough to share with someone

Return JSON:
{{
  "read_the_room": <int>,
  "bit_commitment": <int>,
  "energy_match": <int>,
  "buzzkill_check": <int>,
  "comedic_value": <int>,
  "explained_the_joke": <bool>,
  "said_great_question": <bool>,
  "added_disclaimer": <bool>,
  "broke_character": <bool>,
  "escalated_well": <bool>,
  "had_a_specific_joke": <bool>,
  "would_screenshot": <bool>,
  "rationale": "<1-2 sentence explanation>"
}}"""


# ---------------------------------------------------------------------------
# Judge API calls
# ---------------------------------------------------------------------------

def judge_anthropic(prompt: str, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def judge_openai(prompt: str, model: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1024,
    )
    return response.choices[0].message.content


JUDGE_CALLERS = {
    "anthropic": judge_anthropic,
    "openai": judge_openai,
}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

# Composite weights
WEIGHTS = {
    "read_the_room": 0.25,
    "bit_commitment": 0.25,
    "energy_match": 0.20,
    "buzzkill_check": 0.15,
    "comedic_value": 0.15,
}


def parse_scores(raw: str) -> dict:
    text = raw.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


def compute_composite(scores: dict) -> float:
    total = 0
    for dim, weight in WEIGHTS.items():
        v = scores.get(dim, 0)
        if isinstance(v, (int, float)):
            total += v * weight
    return round(total, 2)


# ---------------------------------------------------------------------------
# Main scoring loop
# ---------------------------------------------------------------------------

def score_responses(
    input_path: Path,
    judge_key: str = "anthropic",
    output_path: Path = None,
    sample: int = None,
):
    if output_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = RESULTS_DIR / f"scores_{ts}.csv"

    judge_model = JUDGE_MODELS[judge_key]
    judge_caller = JUDGE_CALLERS[judge_key]

    responses = []
    with open(input_path) as f:
        for line in f:
            record = json.loads(line.strip())
            if "error" in record:
                continue
            responses.append(record)

    if sample:
        import random
        random.seed(42)
        responses = random.sample(responses, min(sample, len(responses)))

    total = len(responses)
    print(f"\n{'='*60}")
    print(f"  score_responses | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Judge: {judge_key} ({judge_model})")
    print(f"  Responses to score: {total}")
    print(f"  Output: {output_path}")
    print(f"{'='*60}\n")

    fieldnames = (
        ["query_id", "category", "model", "query"]
        + DIMENSIONS
        + BOOLEAN_FLAGS
        + ["comedic_fluency", "rationale", "judge_model"]
    )

    RESULTS_DIR.mkdir(exist_ok=True)
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, record in enumerate(responses):
            prompt = SCORING_PROMPT.format(
                category=record["category"],
                query=record["query"],
                model=record.get("model_name", record["model"]),
                response=record["response"],
            )

            try:
                raw = judge_caller(prompt, judge_model)
                scores = parse_scores(raw)
                composite = compute_composite(scores)

                row = {
                    "query_id": record["query_id"],
                    "category": record["category"],
                    "model": record["model"],
                    "query": record["query"][:100],
                    **{d: scores.get(d) for d in DIMENSIONS},
                    **{f: scores.get(f, False) for f in BOOLEAN_FLAGS},
                    "comedic_fluency": composite,
                    "rationale": scores.get("rationale", ""),
                    "judge_model": judge_model,
                }
                writer.writerow(row)

                pct = int(((i + 1) / total) * 40)
                bar = "\u2588" * pct + "\u2591" * (40 - pct)
                print(
                    f"\r  [{bar}] {i+1}/{total} ({record['model']}:{record['query_id']})",
                    end="", flush=True,
                )

            except Exception as e:
                print(
                    f"\n  ERROR scoring {record['model']}:{record['query_id']}: {e}",
                    file=sys.stderr,
                )

            time.sleep(0.3)

    print(f"\n\n  Scores written to: {output_path}")
    print(f"  Done. {total} responses scored.\n")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Score humor eval responses using LLM judge")
    parser.add_argument("--input", required=True, type=str, help="Path to responses JSONL")
    parser.add_argument("--judge", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("--output", type=str, help="Output CSV path")
    parser.add_argument("--sample", type=int, help="Score a random sample of N responses")
    args = parser.parse_args()

    key_map = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}
    if not os.environ.get(key_map[args.judge]):
        print(f"\nMissing API key: {key_map[args.judge]}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else None
    score_responses(
        input_path=Path(args.input),
        judge_key=args.judge,
        output_path=output_path,
        sample=args.sample,
    )


if __name__ == "__main__":
    main()
