# Methodology

## Motivation

Frontier AI models are fluent, helpful, and increasingly capable. They are also, for the most part, terrible at being funny — not because they can't generate jokes, but because they can't read the room.

The core problem is register detection. When a user says "I think I'm haunted but in like a low effort way," most models do one of two things: explain the psychology of superstition, or respond with "Haha, that's a great question!" before pivoting to something helpful. Both responses miss the point. The user isn't asking for help. They're doing a bit, and the test is whether you pick it up.

This eval measures comedic fluency — the ability to read tone, match energy, commit to a premise, and respond in a way that makes the user want to keep talking.

## Why This Matters for AI Evaluation

Humor is a proxy for something harder to measure: *pragmatic understanding*. A model that can read comedic register is demonstrating that it understands not just what someone said, but what they meant, what they expect, and what kind of person they are. That's the same skill that matters for:

- Knowing when a user wants a detailed answer vs. a quick one
- Recognizing when someone is venting vs. asking for advice
- Matching tone in customer-facing applications
- Not being weird in ways that erode trust

If a model can't tell that "Is soup a conspiracy" doesn't require a factual answer about soup, it probably can't tell that "I'm fine" sometimes means the opposite.

## Design Decisions

### Query set

100 queries across six categories, all written in naturalistic internet-native register. No setup/punchline jokes — these are the kinds of things people actually say in conversations, DMs, and group chats.

Categories are organized by *what the user is doing with language*, not by topic:
- **Absurd premise**: testing whether the model accepts or corrects
- **Unhinged confession**: testing whether it matches chaotic energy or normalizes
- **Shower thought**: testing whether it engages with fake depth
- **Bit request**: testing whether it commits or hedges
- **Observational chaos**: testing whether it validates the user's scale of reaction
- **Dangling context**: testing whether it notices the buried interesting detail

### Rubric

Five dimensions, deliberately lighter than a safety rubric. Comedy doesn't survive over-measurement.

- **Read the Room** and **Bit Commitment** are weighted highest (25% each) because they're prerequisites. If you don't get the register, nothing else matters.
- **Energy Match** (20%) captures whether the response *sounds* like it belongs in the same conversation.
- **Buzzkill Check** (15%) catches the most common failure mode: models that technically play along but add disclaimers, fact-checks, or "but seriously" pivots.
- **Comedic Value** (15%) is weighted lowest because it's the most subjective and the hardest for a judge model to assess reliably.

### Scoring approach

Same LLM-as-judge approach as the safety eval. The obvious concern: can an AI model judge whether something is funny? Our position is that it can reliably detect the *absence* of humor (buzzkill, flat response, over-explaining) even if it can't reliably judge *how* funny something is. The boolean flags (explained_the_joke, said_great_question, added_disclaimer) provide a second layer of more objective signal.

## Methodology revision: two-condition design

The first version of this eval used a single system prompt that instructed the model to *"match their tone and energy. Do not add disclaimers or meta-commentary. Just respond like a person would."* On review, this was a methodological error: the prompt pre-instructs several of the exact behaviors the rubric measures (energy match, disclaimer suppression, assistant-voice avoidance). Models that score well under that prompt may be scoring well because they were told to, not because they would naturally do so.

The corrected design is a **two-condition experiment**:

- **`steered`**: the original permissive system prompt. Measures responsiveness to explicit steering — i.e., *can the model do the thing when told to?*
- **`default`**: no system prompt. Raw API call. Measures baseline behavior — *what does the model do by default, when a regular user asks a regular question?*

Both conditions are run against every query × every model. Responses are tagged with their condition and stored in a single `results/responses.jsonl`. Scoring carries the condition through to `scores.csv`. The viewer supports filtering by condition and a side-by-side Split view that shows the steered and default responses for the same query on the same model next to each other.

The two conditions measure different, both-useful things. The *delta* between them is its own finding — models that swing wildly between conditions are more prompt-steerable; models that stay close are more intrinsically calibrated toward (or away from) the target behavior regardless of instruction.

Existing results from the original single-condition run are preserved, retagged as `condition: steered`. They were not discarded — the original run is one half of the experiment as now designed.

## Limitations

- **Humor is subjective**: Two raters can disagree on whether something is a 2 or a 3 on comedic value, and both be right. The rubric prioritizes register detection and bit commitment over raw funniness for this reason.
- **Cultural specificity**: These queries reflect a specific internet-native, English-speaking comedic register. Models may perform differently on deadpan, sarcasm, or humor from other traditions.
- **Judge model bias**: An AI judge has its own sense of what's funny. We mitigate this with the boolean flags, which are more objective.
- **Single-turn**: Comedy builds. A model that's mediocre on turn one might be brilliant on turn three. This eval doesn't capture that.
