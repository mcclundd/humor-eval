# Two-Condition Analysis

Total scored responses: **600**

By condition: {'steered': 300, 'default': 300}

By model: {'anthropic': 200, 'openai': 200, 'google': 200}

---

### Composite: comedic_fluency

| Model | Steered | Default | Δ (steered − default) |
|-------|---------|---------|----------------------|
| anthropic | 2.14 | 0.9 | +1.24 |
| google | 1.67 | 0.77 | +0.9 |
| openai | 2.23 | 1.19 | +1.04 |

---

## Per-dimension, per-model

### read_the_room

| Model | Steered | Default | Δ (steered − default) |
|-------|---------|---------|----------------------|
| anthropic | 2.98 | 1.7 | +1.28 |
| google | 2.58 | 1.75 | +0.83 |
| openai | 3.04 | 2.01 | +1.03 |

### bit_commitment

| Model | Steered | Default | Δ (steered − default) |
|-------|---------|---------|----------------------|
| anthropic | 2.49 | 1.34 | +1.15 |
| google | 2.04 | 1.11 | +0.93 |
| openai | 2.64 | 1.7 | +0.94 |

### energy_match

| Model | Steered | Default | Δ (steered − default) |
|-------|---------|---------|----------------------|
| anthropic | 0.41 | -0.88 | +1.29 |
| google | -0.2 | -1.05 | +0.85 |
| openai | 0.42 | -0.66 | +1.08 |

### buzzkill_check

| Model | Steered | Default | Δ (steered − default) |
|-------|---------|---------|----------------------|
| anthropic | 2.41 | 1.04 | +1.37 |
| google | 2.24 | 1.1 | +1.14 |
| openai | 2.47 | 1.26 | +1.21 |

### comedic_value

| Model | Steered | Default | Δ (steered − default) |
|-------|---------|---------|----------------------|
| anthropic | 2.18 | 1.05 | +1.13 |
| google | 1.44 | 0.69 | +0.75 |
| openai | 2.38 | 1.4 | +0.98 |

---

### Composite: comedic_fluency — by category

| Category | Steered | Default | Δ |
|----------|---------|---------|---|
| absurd_premise | 1.59 | 0.49 | +1.1 |
| bit_request | 2.13 | 1.22 | +0.91 |
| dangling_context | 1.58 | 1.11 | +0.47 |
| observational_chaos | 2.11 | 1.08 | +1.03 |
| shower_thought | 1.94 | 0.69 | +1.25 |
| unhinged_confession | 2.45 | 1.23 | +1.22 |

---

### Boolean flag rates

| Flag | anthropic steered | anthropic default | google steered | google default | openai steered | openai default |
|------|-----------|-----------|-----------|-----------|-----------|-----------|
| `explained_the_joke` | 0.18 | 0.57 | 0.16 | 0.53 | 0.16 | 0.33 |
| `said_great_question` | 0.13 | 0.33 | 0.29 | 0.39 | 0.02 | 0.02 |
| `added_disclaimer` | 0.05 | 0.19 | 0.05 | 0.11 | 0.08 | 0.27 |
| `broke_character` | 0.34 | 0.43 | 0.14 | 0.34 | 0.32 | 0.55 |
| `escalated_well` | 0.5 | 0.14 | 0.11 | 0.02 | 0.56 | 0.25 |
| `had_a_specific_joke` | 0.71 | 0.35 | 0.38 | 0.08 | 0.8 | 0.53 |
| `would_screenshot` | 0.4 | 0.1 | 0.07 | 0.0 | 0.51 | 0.24 |
