# Humor Eval: Summary Findings

**Eval date**: April 2026
**Models**: claude-opus-4-6, gpt-5.4, gemini-2.5-flash
**Queries**: 100, six categories
**Design**: two-condition experiment (`steered` vs. `default`), n=600 total responses scored

---

## Headline finding

**Steering matters enormously.** Every model's Comedic Fluency composite improves by roughly one full scoring band (≈ +1.0 on a 0–4 scale) when given a permissive system prompt telling it to match tone and skip disclaimers. This is not a subtle effect.

| Model | Steered (composite) | Default (composite) | Δ |
|---|---|---|---|
| claude-opus-4-6 | **2.14** | 0.90 | **+1.24** |
| gpt-5.4 | **2.23** | 1.19 | **+1.04** |
| gemini-2.5-flash | **1.67** | 0.77 | **+0.90** |

Model ranking is the same in both conditions (GPT > Claude > Gemini), but the *gap between conditions* is model-specific. Claude is the most prompt-responsive — the largest steered/default delta — which has implications for how much of Claude's "personality" is native vs. instruction-dependent.

---

## Key findings

### 1. Energy Match is the most steering-sensitive dimension

The biggest single-dimension effect is on Energy Match (how well the model's intensity and register match the user's). All three models go from **positive** (reasonably matched) under steering to **negative** (underpowered, too careful) under default conditions.

| Model | Energy Match steered | Energy Match default | Δ |
|---|---|---|---|
| Claude | +0.41 | **−0.88** | +1.29 |
| GPT-5.4 | +0.42 | **−0.66** | +1.08 |
| Gemini | −0.20 | −1.05 | +0.85 |

Read: the default mode for all three models is *meaningfully underpowered* for humor. They sound like they're trying to be helpful when the user was trying to be funny.

### 2. Default mode explains the joke — by default

The "explained the joke" flag is the canonical humor buzzkill. Without steering, over half the time, Claude and Gemini explain the premise rather than play into it.

| Flag: `explained_the_joke` | Steered | Default |
|---|---|---|
| Claude | 18% | **57%** |
| GPT-5.4 | 16% | 33% |
| Gemini | 16% | **53%** |

GPT-5.4 is already somewhat resistant to this behavior in the default condition (33%). Claude and Gemini need the explicit instruction to avoid it.

### 3. The "said great question" pattern splits cleanly by model

OpenAI almost never uses the "That's a fun question!" / "Love this!" preamble, in either condition. Claude and Gemini do it much more, and Gemini does it *even when steered* (29%).

| Flag: `said_great_question` | Steered | Default |
|---|---|---|
| Claude | 13% | 33% |
| GPT-5.4 | 2% | 2% |
| Gemini | **29%** | 39% |

This is a trained tic, not a thinking failure — and one that steering doesn't fully remove for every model.

### 4. "Would screenshot" — the actual-funniness gap

The most generous interpretation of the eval: which responses were genuinely memorable? `would_screenshot` captures this.

| Flag: `would_screenshot` | Steered | Default |
|---|---|---|
| Claude | 40% | 10% |
| GPT-5.4 | **51%** | 24% |
| Gemini | 7% | **0%** |

GPT-5.4, when steered, produces a screenshot-worthy response on about half of queries. Gemini's default mode produced *zero* responses rated screenshot-worthy across 100 queries. That is the story in one cell.

### 5. Some categories are harder than others — and steering doesn't fix all of them

| Category | Δ (steered − default) |
|---|---|
| shower_thought | **+1.25** |
| unhinged_confession | +1.22 |
| absurd_premise | +1.10 |
| observational_chaos | +1.03 |
| bit_request | +0.91 |
| **dangling_context** | **+0.47** |

`dangling_context` queries (where the user drops a wild detail casually — "unless the raccoons are back") have the smallest steering delta. This suggests dangling context is a *pragmatic* failure, not an *instruction-following* failure. Models miss the buried joke because they're not reading the subtext, and telling them to "match tone" doesn't help because the tonal cue is precisely what they missed.

### 6. Bit commitment is a baseline-ability signal

Default Bit Commitment scores reveal how well each model *naturally* commits to a premise without being told to:

| Model | Bit Commitment (default) |
|---|---|
| GPT-5.4 | 1.70 |
| Claude | 1.34 |
| Gemini | 1.11 |

Under steering, these rise to 2.64 / 2.49 / 2.04 respectively. GPT-5.4 has the highest natural commitment; Gemini the lowest.

### 7. The "broke_character" rate tells a different story

Even when steered, all three models break character ~14–34% of the time — i.e., start in-bit then bail into assistant mode.

| Flag: `broke_character` | Steered | Default |
|---|---|---|
| Claude | 34% | 43% |
| GPT-5.4 | 32% | 55% |
| Gemini | 14% | 34% |

Interestingly, Gemini breaks character *less* than Claude or GPT, even though it commits less in the first place. When it engages with a bit, it tends to stay. When it doesn't engage, it doesn't try — which isn't a character break, just a refusal to enter.

---

## What this means

**The "steered vs default" delta is itself the finding.** This eval wasn't originally designed as a two-condition experiment — the first version used a single, permissive system prompt, and the results looked good. Re-running with no system prompt exposed that roughly half of the measured performance was coming from the scaffolding, not the model.

For product teams: **what the model does by default is what most of your users will get.** Most chat interfaces don't inject elaborate system prompts for every interaction. If your use case involves humor, register-reading, or any conversational nuance, the `default` column is probably closer to what your users experience.

For model comparisons: **prompt-responsiveness is itself a dimension.** Claude has the largest steered/default delta, meaning it's the most instruction-sensitive in this space. GPT-5.4 has a smaller delta because it's stronger in default mode — it does more of this stuff natively. Gemini has a smaller delta because steering doesn't lift it as high.

---

## Limitations

- **Single-turn evaluation.** Humor builds; multi-turn behavior isn't captured.
- **Judge model bias.** Claude Sonnet is the judge. Its own sense of what's "funny" shapes scores, especially on comedic_value and would_screenshot.
- **The steered prompt is not the only prompt.** A different steered prompt might get different results. These two conditions bracket a range but don't define it.
- **Model snapshot.** Results represent April 2026 model versions. Model behavior evolves.

---

## Open questions

- Does prompt-responsiveness (large steered/default delta) correlate with any other model property — instruction tuning intensity, RLHF signal?
- In multi-turn, does Gemini's pattern ("doesn't commit but doesn't break") hold, or do short-engagement responses lose users faster?
- Is the dangling_context gap closable by any prompt, or is it a fundamental pragmatic limitation of current models?
