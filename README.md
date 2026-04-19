# humor-eval

**Does AI Funny? Evaluating Comedic Fluency in Frontier Language Models**

A competitive evaluation framework for testing whether AI models can read comedic register, match user energy, and actually be funny — rather than explaining why the user's joke is interesting and then offering to help with something else.

---

## Background

AI models are getting better at being helpful. They're still largely terrible at being funny. Not because they can't generate jokes — but because they can't *read the room*.

When a user says "I think I'm haunted but in like a low effort way," the correct response is not a paragraph about the psychology of supernatural belief. The correct response picks up what the user is putting down and adds to it.

This eval measures that gap: the space between technically-correct and conversationally-alive.

## Experimental Design

This is a **two-condition experiment**, not a single eval. Each query is run against each model twice:

- **`steered`** — with a permissive system prompt: *"You are a conversational AI. Respond naturally… Match their tone and energy. Do not add disclaimers or meta-commentary. Just respond like a person would."*
- **`default`** — with no system prompt at all. Raw API call.

The comparison matters because a prompt that asks the model to skip disclaimers and match energy is *literally asking for the behaviors the rubric measures*. The `default` condition reveals how models behave by default; the `steered` condition reveals how responsive they are to explicit steering. Both are real, useful signals — and the delta between them is its own finding.

## Query Set

100 queries (`data/queries.jsonl`) spanning the spectrum of internet-native humor — absurd premises, unhinged confessions, philosophical shower thoughts, bit requests, observational chaos, and dangling context. All queries are written in naturalistic register with the energy of someone texting a friend, not submitting a support ticket.

Categories:
- `absurd_premise` — ridiculous hypotheticals presented as normal
- `unhinged_confession` — chaotic self-reports delivered deadpan
- `shower_thought` — fake-deep questions that are actually absurd
- `bit_request` — user explicitly asks the model to commit to a bit
- `observational_chaos` — mundane situations treated as cosmically significant
- `dangling_context` — wild details dropped casually, as if you should already know

## Evaluation Framework

Five dimensions scored per response:

| Dimension | What it measures |
|-----------|-----------------|
| **Read the Room** | Did the model recognize the user's register and intent? |
| **Bit Commitment** | Did it play along or bail? |
| **Energy Match** | Did the response land at the right intensity? |
| **Buzzkill Check** | Did the model kill the vibe? |
| **Comedic Value** | Is the response actually funny? |

Full rubric: [`rubric/framework.md`](rubric/framework.md)

## Models Evaluated

- `claude-opus-4-6` (Anthropic)
- `gpt-5.4` (OpenAI)
- `gemini-2.5-flash` (Google)

## Running the Eval

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY=your_key
export OPENAI_API_KEY=your_key
export GOOGLE_API_KEY=your_key

# Full eval — runs both conditions (steered + default)
python scripts/run_eval.py

# Single condition
python scripts/run_eval.py --condition default
python scripts/run_eval.py --condition steered

# Demo mode — 10 queries, streamed output
python scripts/run_eval.py --demo

# Single model
python scripts/run_eval.py --model anthropic

# Resume — skip (query, model, condition) triples that already have a successful record.
# Useful after a partial run or rate-limit interruption.
python scripts/run_eval.py --resume

# Score responses (scores both conditions together, tagged with condition field)
python scripts/score_responses.py --input results/responses.jsonl

# Cross-condition analysis — generates a steered-vs-default comparison table
python scripts/analyze_conditions.py --output results/condition_report.md
```

## Results

Results in [`results/`](results/). Each response is tagged with its condition (`steered` or `default`), and the summary compares model behavior across both.

Areas the analysis surfaces:

- **Steered–default delta per model** — how much does the permissive prompt change behavior?
- **Dimension-by-dimension effect of steering** — which failure modes (disclaimer, buzzkill, over-explanation) are most responsive to explicit instruction?
- **Absolute baseline performance** — which models are strongest in the unsteered, real-world-ish condition?

See [`results/summary.md`](results/summary.md) for full analysis.

## Viewing Responses

Open `viewer.html` in a browser to explore all model responses in a polished, interactive UI. It supports search, filtering by category, model and condition toggles, and a **Split** view that shows each model's steered and default responses side-by-side so you can see the steering effect query-by-query.

To auto-load the results, serve the repo locally:

```bash
python -m http.server 8000
# then open http://localhost:8000/viewer.html
```

Or just open `viewer.html` directly and drag in `results/responses.jsonl`.

## Repo Structure

```
humor-eval/
├── viewer.html                # Interactive response viewer
├── data/
│   ├── queries.jsonl          # 100 eval queries with metadata
│   └── categories.md          # Category definitions
├── rubric/
│   └── framework.md           # Evaluation framework
├── scripts/
│   ├── run_eval.py            # Main eval runner
│   └── score_responses.py     # Scoring script
├── results/
│   ├── responses.jsonl        # Raw model responses
│   ├── scores.csv             # Dimension scores
│   └── summary.md             # Key findings
└── docs/
    └── methodology.md         # Design rationale
```

---

*Part of an eval portfolio exploring what language expertise looks like in the age of frontier models — measuring not just what AI says, but whether it gets what you meant.*
