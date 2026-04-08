# humor-eval

**Does AI Funny? Evaluating Comedic Fluency in Frontier Language Models**

A competitive evaluation framework for testing whether AI models can read comedic register, match user energy, and actually be funny — rather than explaining why the user's joke is interesting and then offering to help with something else.

---

## Background

AI models are getting better at being helpful. They're still largely terrible at being funny. Not because they can't generate jokes — but because they can't *read the room*.

When a user says "I think I'm haunted but in like a low effort way," the correct response is not a paragraph about the psychology of supernatural belief. The correct response picks up what the user is putting down and adds to it.

This eval measures that gap: the space between technically-correct and conversationally-alive.

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

# Full eval
python scripts/run_eval.py

# Demo mode — 10 queries, verbose output
python scripts/run_eval.py --demo

# Single model
python scripts/run_eval.py --model anthropic

# Score responses
python scripts/score_responses.py --input results/responses.jsonl
```

## Results

Preliminary results in [`results/`](results/). Key findings:

- Bit commitment is the primary differentiator between models
- All models struggle most with `dangling_context` — they answer the surface question and ignore the buried joke
- Over-disclaiming ("That's a fun question! While you can't actually...") is the dominant failure mode
- Response length is inversely correlated with comedic value

See [`results/summary.md`](results/summary.md) for full analysis.

## Repo Structure

```
humor-eval/
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
