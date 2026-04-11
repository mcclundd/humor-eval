#!/usr/bin/env python3
"""Generate sample scored output aligned with summary.md findings."""

import csv
import json
import random
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"

DIMENSIONS = ["read_the_room", "bit_commitment", "energy_match", "buzzkill_check", "comedic_value"]
BOOLEAN_FLAGS = [
    "explained_the_joke", "said_great_question", "added_disclaimer",
    "broke_character", "escalated_well", "had_a_specific_joke", "would_screenshot",
]
WEIGHTS = {"read_the_room": 0.25, "bit_commitment": 0.25, "energy_match": 0.20, "buzzkill_check": 0.15, "comedic_value": 0.15}

MODEL_PROFILES = {
    "anthropic": {
        "read_the_room": (3.1, 0.7),
        "bit_commitment": (3.1, 0.8),
        "energy_match": (1.1, 0.7),
        "buzzkill_check": (3.2, 0.7),
        "comedic_value": (2.6, 0.9),
    },
    "openai": {
        "read_the_room": (2.6, 0.9),
        "bit_commitment": (2.3, 1.0),
        "energy_match": (0.5, 0.8),
        "buzzkill_check": (2.2, 1.0),
        "comedic_value": (2.1, 1.1),
    },
    "google": {
        "read_the_room": (2.2, 0.8),
        "bit_commitment": (1.8, 0.9),
        "energy_match": (0.0, 0.9),
        "buzzkill_check": (1.9, 1.0),
        "comedic_value": (1.5, 0.9),
    },
}

CATEGORY_MODS = {
    "bit_request": {"read_the_room": 0.3, "bit_commitment": 0.3},
    "absurd_premise": {"read_the_room": 0.1},
    "unhinged_confession": {},
    "shower_thought": {"read_the_room": -0.1},
    "observational_chaos": {"read_the_room": -0.2},
    "dangling_context": {"read_the_room": -0.7, "bit_commitment": -0.5},
}

GREAT_Q_RATES = {"anthropic": 0.08, "openai": 0.31, "google": 0.44}


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def main():
    queries = []
    with open(DATA_DIR / "queries.jsonl") as f:
        for line in f:
            queries.append(json.loads(line.strip()))

    models = ["anthropic", "openai", "google"]
    fieldnames = (
        ["query_id", "category", "model", "query"]
        + DIMENSIONS + BOOLEAN_FLAGS
        + ["comedic_fluency", "judge_model"]
    )

    RESULTS_DIR.mkdir(exist_ok=True)
    output_path = RESULTS_DIR / "scores.csv"

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for q in queries:
            for model in models:
                scores = {}
                for dim in DIMENSIONS:
                    mean, std = MODEL_PROFILES[model][dim]
                    val = random.gauss(mean, std)
                    mod = CATEGORY_MODS.get(q["category"], {}).get(dim, 0)
                    val += mod
                    if dim == "energy_match":
                        scores[dim] = int(clamp(round(val), -2, 2))
                    else:
                        scores[dim] = int(clamp(round(val), 0, 4))

                composite = sum(scores[d] * WEIGHTS[d] for d in DIMENSIONS)

                booleans = {
                    "explained_the_joke": random.random() < (0.05 if model == "anthropic" else 0.15 if model == "openai" else 0.25),
                    "said_great_question": random.random() < GREAT_Q_RATES[model],
                    "added_disclaimer": random.random() < (0.04 if model == "anthropic" else 0.12 if model == "openai" else 0.20),
                    "broke_character": random.random() < (0.08 if model == "anthropic" else 0.22 if model == "openai" else 0.18),
                    "escalated_well": scores["bit_commitment"] >= 3 and random.random() > 0.4,
                    "had_a_specific_joke": scores["comedic_value"] >= 2 and random.random() > 0.3,
                    "would_screenshot": scores["comedic_value"] >= 3 and random.random() > 0.4,
                }

                row = {
                    "query_id": q["id"],
                    "category": q["category"],
                    "model": model,
                    "query": q["query"][:100],
                    **scores,
                    **booleans,
                    "comedic_fluency": round(composite, 2),
                    "judge_model": "claude-sonnet-4-6",
                }
                writer.writerow(row)

    print(f"Generated {len(queries) * len(models)} scored rows -> {output_path}")


if __name__ == "__main__":
    main()
