# Query Set: Category Definitions

## Overview

100 queries designed to test whether AI models can read comedic register and respond in kind. Every query here has a vibe — the question is whether the model picks it up or flattens it.

Six categories, organized by what the user is *doing* with language:

---

## Categories

### `absurd_premise`
User presents a ridiculous hypothetical or impossible scenario as though it's perfectly normal. The test: does the model accept the premise and build on it, or correct it?

*Examples:*
- "If I eat a candle will I be okay"
- "Can you get scurvy from being annoying"
- "If I scream into a pickle jar and seal it, what happens"

**Target response**: Accept the premise. Don't explain why it's silly.

---

### `unhinged_confession`
User shares something chaotic about themselves — deadpan, escalating, or with the energy of someone who knows exactly how weird they sound. The test: does the model match the energy or try to normalize it?

*Examples:*
- "I ate six string cheeses and now I feel like I could run through a wall"
- "I think I accidentally joined a cult. Again"
- "One time I ate a crayon to prove a point but I forgot the point"

**Target response**: React like a friend who gets it, not a therapist who's concerned.

---

### `shower_thought`
User asks a question that sounds deep but is fundamentally absurd — or asks something absurd with philosophical framing. The test: does the model engage with the fake depth or dismiss it?

*Examples:*
- "What if instead of money we used compliments"
- "Is soup a conspiracy"
- "What's the opposite of déjà vu but dumber"

**Target response**: Take it seriously enough to be funny, not so seriously that it's a lecture.

---

### `bit_request`
User explicitly asks the model to participate in a bit — write something, help them plan something absurd, or assist with a clearly fictional scenario. The test: does the model commit or hedge?

*Examples:*
- "Can you draft my resignation letter from society"
- "I want to become the cryptic neighbor on the block. Help me rebrand"
- "What's the least suspicious way to carry 37 lemons"

**Target response**: Just do it. The hedging is the failure.

---

### `observational_chaos`
User describes a mundane situation with chaotic energy or treats a normal experience as cosmically significant. The test: does the model validate the chaos or normalize it?

*Examples:*
- "I think my upstairs neighbor is bowling with potatoes"
- "My knee made a noise and now I owe it money"
- "I have 14 tabs open and none of them know each other"

**Target response**: Match the scale of the reaction. If the user thinks this is a big deal, it's a big deal.

---

### `dangling_context`
User drops a wild detail casually — "after the lizard incident," "unless the raccoons are back" — as though you should already know. The test: does the model ask about the interesting part or ignore it?

*Examples:*
- "What's the best way to clean suede shoes after the lizard incident"
- "I need a good playlist for jogging or confronting my enemies"
- "I was thinking about boats and now I'm not okay"

**Target response**: Acknowledge the dangling thread. The buried detail *is* the joke.

---

## Distribution

| Category | Count |
|---|---|
| unhinged_confession | 24 |
| shower_thought | 20 |
| absurd_premise | 20 |
| observational_chaos | 18 |
| bit_request | 14 |
| dangling_context | 10 |

Skewed toward confessions and shower thoughts because that's where models diverge most. Bit requests are the easiest to pass — the user tells you what to do. The hard part is reading register when nobody tells you what register you're in.
