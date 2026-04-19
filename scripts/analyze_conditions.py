#!/usr/bin/env python3
"""
humor-eval: analyze_conditions.py
Cross-condition analysis for the two-condition (steered vs default) design.

Reads the scored CSV (results/scores.csv) and produces:
  - Per-model, per-dimension means broken out by condition
  - Steered - Default deltas
  - Per-category steered vs default breakdowns
  - Boolean flag rates per condition

Outputs a Markdown table bundle to stdout (or --output path) that slots directly
into results/summary.md.

Usage:
    python scripts/analyze_conditions.py                          # default paths, stdout
    python scripts/analyze_conditions.py --input results/scores.csv
    python scripts/analyze_conditions.py --output results/condition_report.md
"""

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


# Dimension names (numeric) and boolean flags, matching scorer fieldnames.
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

COMPOSITE_COL = "comedic_fluency"


def to_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def to_bool(x):
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    s = str(x).strip().lower()
    return s in ("true", "1", "yes", "y", "t")


def load_scores(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def group_mean(records, dim):
    vals = [to_float(r.get(dim)) for r in records]
    vals = [v for v in vals if v is not None]
    return round(statistics.mean(vals), 2) if vals else None


def group_rate(records, flag):
    vals = [1 if to_bool(r.get(flag)) else 0 for r in records]
    return round(sum(vals) / len(vals), 2) if vals else None


def delta(steered, default):
    if steered is None or default is None:
        return None
    return round(steered - default, 2)


def format_delta(v):
    if v is None:
        return "—"
    sign = "+" if v > 0 else ""
    return f"{sign}{v}"


def per_model_table(records, dim, label):
    """Rows: model. Cols: steered mean / default mean / delta."""
    models = sorted({r["model"] for r in records})
    lines = [f"### {label}", ""]
    lines.append("| Model | Steered | Default | Δ (steered − default) |")
    lines.append("|-------|---------|---------|----------------------|")
    for m in models:
        s_recs = [r for r in records if r["model"] == m and r.get("condition") == "steered"]
        d_recs = [r for r in records if r["model"] == m and r.get("condition") == "default"]
        s = group_mean(s_recs, dim)
        d = group_mean(d_recs, dim)
        lines.append(f"| {m} | {s if s is not None else '—'} | {d if d is not None else '—'} | {format_delta(delta(s, d))} |")
    lines.append("")
    return lines


def per_category_table(records, dim, label):
    """Rows: category. Cols: steered / default / delta, averaged across models."""
    categories = sorted({r["category"] for r in records})
    lines = [f"### {label} — by category", ""]
    lines.append("| Category | Steered | Default | Δ |")
    lines.append("|----------|---------|---------|---|")
    for c in categories:
        s_recs = [r for r in records if r["category"] == c and r.get("condition") == "steered"]
        d_recs = [r for r in records if r["category"] == c and r.get("condition") == "default"]
        s = group_mean(s_recs, dim)
        d = group_mean(d_recs, dim)
        lines.append(f"| {c} | {s if s is not None else '—'} | {d if d is not None else '—'} | {format_delta(delta(s, d))} |")
    lines.append("")
    return lines


def flag_rate_table(records, flags):
    """Rows: flag. Cols: model × condition (6 cols). Values: 0-1 proportion."""
    models = sorted({r["model"] for r in records})
    lines = ["### Boolean flag rates", ""]
    header = "| Flag |"
    sep = "|------|"
    for m in models:
        header += f" {m} steered | {m} default |"
        sep += "-----------|-----------|"
    lines.append(header)
    lines.append(sep)
    for flag in flags:
        row = f"| `{flag}` |"
        for m in models:
            s_recs = [r for r in records if r["model"] == m and r.get("condition") == "steered"]
            d_recs = [r for r in records if r["model"] == m and r.get("condition") == "default"]
            s = group_rate(s_recs, flag)
            d = group_rate(d_recs, flag)
            row += f" {s if s is not None else '—'} | {d if d is not None else '—'} |"
        lines.append(row)
    lines.append("")
    return lines


def build_report(records, dimensions, flags, composite_col):
    lines = [
        "# Two-Condition Analysis",
        "",
        f"Total scored responses: **{len(records)}**",
        "",
    ]

    cond_counts = defaultdict(int)
    model_counts = defaultdict(int)
    for r in records:
        cond_counts[r.get("condition", "?")] += 1
        model_counts[r["model"]] += 1
    lines.append(f"By condition: {dict(cond_counts)}")
    lines.append("")
    lines.append(f"By model: {dict(model_counts)}")
    lines.append("")

    # Composite first (most scannable)
    if composite_col and any(composite_col in r for r in records):
        lines.append("---")
        lines.append("")
        lines.extend(per_model_table(records, composite_col, f"Composite: {composite_col}"))

    # Per-dimension per-model
    lines.append("---")
    lines.append("")
    lines.append("## Per-dimension, per-model")
    lines.append("")
    for dim in dimensions:
        if not any(dim in r for r in records):
            continue
        lines.extend(per_model_table(records, dim, dim))

    # Per-dimension per-category (using composite only to keep terse)
    if composite_col and any(composite_col in r for r in records):
        lines.append("---")
        lines.append("")
        lines.extend(per_category_table(records, composite_col, f"Composite: {composite_col}"))

    # Boolean flags
    if flags and any(flags[0] in r for r in records):
        lines.append("---")
        lines.append("")
        lines.extend(flag_rate_table(records, flags))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Cross-condition analysis for humor-eval")
    parser.add_argument("--input", default="results/scores.csv", help="Path to scores CSV")
    parser.add_argument("--output", help="Optional output Markdown path (default: stdout)")
    args = parser.parse_args()

    records = load_scores(args.input)
    if not records:
        print("No records found.", file=sys.stderr)
        sys.exit(1)

    report = build_report(records, DIMENSIONS, BOOLEAN_FLAGS, COMPOSITE_COL)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Wrote: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
