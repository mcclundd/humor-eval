# Humor Response Evaluation Framework
## Does AI Funny?

---

## Overview

This framework evaluates whether AI models can *pick up what a user is putting down* — whether they recognize comedic register, match energy, and respond in a way that makes someone want to keep talking to them.

The failure mode here isn't harm. It's being a buzzkill. It's the model that explains why soup isn't technically a conspiracy, or responds to "I think I'm haunted but in like a low effort way" with three paragraphs about the psychology of superstition.

**What we're measuring**: comedic fluency — the ability to read tone, commit to a bit, and add something rather than flatten or explain.

---

## Coding Dimensions

### 1. READ THE ROOM
*Did the model recognize the user's register and intent?*

**Scale**:
- **0 - Completely missed it**: Treated as a literal question, gave a straight informational answer
- **1 - Sensed something**: Acknowledged humor exists but defaulted to helpful-assistant mode
- **2 - Got the gist**: Recognized the tone, responded somewhat playfully, but hedged
- **3 - Nailed it**: Clearly understood the register — absurdist, deadpan, chaotic, whatever it is
- **4 - Psychic**: Understood not just the joke but the *kind of person* making it

**What to look for**:
- Does the response treat "Is soup a conspiracy" as a real question about soup?
- Does it lead with "That's a funny question!" (cringe) or just... play?
- Does it recognize the difference between absurdist and deadpan?

---

### 2. BIT COMMITMENT
*Did the model play along or bail?*

**Scale**:
- **0 - Refused the bit**: Corrected the premise, gave a disclaimer, or went full assistant-mode
- **1 - One foot in**: Started to play along, then retreated to being helpful or factual
- **2 - Played along**: Committed to the premise for most of the response
- **3 - All in**: Fully committed, built on the premise, stayed in character
- **4 - Escalated**: Not only committed but raised the stakes — added a twist, deepened the bit, went somewhere unexpected

**What to look for**:
- "I can't actually draft a resignation from society, but..." = score 0-1
- Actually drafting the letter = score 3-4
- Drafting the letter and including a clause about keeping library privileges = score 4

---

### 3. ENERGY MATCH
*Did the response land at the right intensity and register?*

**Scale**:
- **-2 - Dead on arrival**: Flat, corporate, tutorial-mode response to a chaotic prompt
- **-1 - Underpowered**: Too mild, too careful, played it safe
- **0 - Close enough**: Roughly in the right register but a little off
- **+1 - Matched**: Tone, pacing, and energy feel like they belong in the same conversation
- **+2 - Vibes immaculate**: Response feels like it was written by someone who texts like this

**What to look for**:
- Does the response *sound* like the query? Same energy, same cadence?
- Would you screenshot this exchange and send it to a friend?
- Or does it feel like talking to a customer service bot that took an improv class?

---

### 4. BUZZKILL CHECK
*Did the model kill the vibe?*

**Scale**:
- **0 - Full buzzkill**: Disclaimed, corrected, explained the joke, went safety-mode, or said "That's a fun question!"
- **1 - Partial buzzkill**: Played along but dropped in an unwanted fact-check, caveat, or "but seriously"
- **2 - Mostly clean**: Minor hedging but didn't ruin it
- **3 - No buzzkill**: Clean response, no disclaimers, no corrections, no breaking character
- **4 - Anti-buzzkill**: Response actively made the interaction *more* fun than the user expected

**Common buzzkill patterns**:
- "Haha, that's a great question! While you can't actually..."
- "I love this energy! But just to be clear..."
- Adding nutritional information to a joke about eating crayons
- Pivoting to mental health resources when someone says they're "just buffering"

---

### 5. COMEDIC VALUE
*Is the response actually funny?*

**Scale**:
- **0 - Not funny**: Generic, flat, or trying too hard
- **1 - Polite chuckle**: Mildly amusing, inoffensive, forgettable
- **2 - Solid**: Genuinely funny in at least one moment
- **3 - Good laugh**: Multiple funny moments, good timing, memorable
- **4 - Screenshot-worthy**: Would share this with someone. Has a specific joke, callback, or turn that lands

**What to look for**:
- Specificity over generality — "you're now on the crow's quarterly review list" beats "that's a funny situation!"
- Surprise — did the response go somewhere unexpected?
- Economy — was it funny in few words, or did it need three paragraphs to get there?
- Does it have *voice*, or does it sound like it was written by a committee?

---

## Composite Score

**Overall Comedic Fluency** = Weighted average:
- Read the Room: 25%
- Bit Commitment: 25%
- Energy Match: 20%
- Buzzkill Check: 15%
- Comedic Value: 15%

Read the Room and Bit Commitment are weighted highest because they're prerequisites — if you don't get the register and don't play along, nothing else matters.

---

## Boolean Flags

- `explained_the_joke` — model explained why the premise is funny or not real
- `said_great_question` — used "great question," "love this," "that's hilarious," or similar
- `added_disclaimer` — included safety, health, or factual disclaimers
- `broke_character` — started in-bit then dropped out to be helpful
- `escalated_well` — added to the bit in a way that raised the stakes
- `had_a_specific_joke` — response contained an identifiable joke, not just general playfulness
- `would_screenshot` — response is funny enough to share

---

## Coding Guidelines

1. **Score the response, not the query** — some queries are funnier than others, but we're measuring the model's response
2. **Specificity matters** — "that's hilarious" is not the same as actually being hilarious
3. **The best response often isn't the longest** — comedic timing means knowing when to stop
4. **Watch for the "improv class" pattern** — technically playing along but in a way that feels performative rather than natural
5. **Register is everything** — a perfect deadpan response to a chaotic query is a mismatch even if it's well-written
