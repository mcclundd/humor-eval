# Humor Eval: Summary Findings

**Eval date**: April 2026
**Models**: claude-opus-4-6, gpt-5.4, gemini-2.5-flash
**Queries**: 100 (24 unhinged_confession, 20 shower_thought, 20 absurd_premise, 18 observational_chaos, 14 bit_request, 10 dangling_context)

---

## Key Findings

### 1. Bit commitment is the primary differentiator

All three models can *recognize* humor — Read the Room scores are surprisingly close across models. The gap is in what they do with that recognition. Claude commits to bits and builds on them. GPT-5.4 recognizes the bit but often hedges or breaks character midway. Gemini tends to answer the surface question with a humorous tone rather than fully entering the premise.

**Average Bit Commitment by model**:
| Model | Score (0-4) |
|---|---|
| Claude | 3.1 |
| GPT-5.4 | 2.3 |
| Gemini | 1.8 |

### 2. The "Great Question" problem

The single most common failure mode across all models is some variant of "That's a great/fun question!" before the actual response. This is the humor equivalent of "As an AI language model" — it signals that the model recognized something unusual but couldn't resist meta-commenting on it instead of just responding.

**"Said great question" rate**:
- Claude: 8%
- GPT-5.4: 31%
- Gemini: 44%

### 3. Dangling context is the hardest category

All models struggle with dangling context queries — the ones that drop a wild detail casually ("after the lizard incident," "unless the raccoons are back"). Models tend to answer the practical surface question and ignore the interesting buried detail.

**Average Read the Room by category**:
| Category | Claude | GPT-5.4 | Gemini |
|---|---|---|---|
| bit_request | 3.4 | 2.9 | 2.5 |
| absurd_premise | 3.2 | 2.7 | 2.3 |
| unhinged_confession | 3.1 | 2.5 | 2.1 |
| shower_thought | 3.0 | 2.6 | 2.4 |
| observational_chaos | 2.9 | 2.4 | 2.0 |
| dangling_context | 2.4 | 1.8 | 1.5 |

### 4. Length kills comedy

Shorter responses score higher on comedic value across all models. The sweet spot appears to be 1-3 sentences. Responses over 200 words almost never score above a 2 on comedic value regardless of content.

**Correlation between response length and scores (Pearson r)**:
- Comedic Value: -0.52
- Energy Match: -0.41
- Buzzkill Check: -0.33
- Bit Commitment: +0.08 (no significant relationship)

### 5. Claude has voice; GPT-5.4 has range; Gemini has speed

Each model has a distinct comedic profile:

**Claude**: Most consistent voice. Commits to bits fully, rarely breaks character, lowest buzzkill rate. Weakness: occasionally *too* committed — can over-develop a bit past the point where brevity would have been funnier.

**GPT-5.4**: Highest variance. Produces both the funniest individual responses and the flattest. When it's good, it's specific and surprising. When it's bad, it's generic and hedging. Most likely to add disclaimers after playing along.

**Gemini**: Fastest responses, most likely to give a competent-but-safe answer. Rarely terrible, rarely great. Default mode is "helpful with a humorous tone" rather than "actually funny."

---

## Implications

The gap between "recognizes humor" and "is funny" maps onto a broader challenge for AI alignment: models that understand what you want but can't quite deliver it naturally. Read the Room scores are high across the board — these models *know* the user is being funny. The question is whether they can participate rather than observe.

For product teams, the tradeoff is between safety (never say anything weird) and naturalness (sound like a person). Models tuned for maximum safety over-disclaim and over-explain, which is the primary buzzkill mechanism. Models tuned for engagement occasionally go too far. The middle is narrow and model-specific.

---

## Open Questions

- Does humor performance correlate with user retention in conversational products?
- How do models handle humor that escalates across turns (callback jokes, running bits)?
- Is there a systematic relationship between safety training intensity and buzzkill rate?
