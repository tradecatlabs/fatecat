# Meihua Yishu Qualitative Match Experiment

## Motivation

The Polymarket binary prediction experiment (N=100) yielded 51% accuracy -- indistinguishable from a coin flip. However, the experiment imposed a binary YES/NO frame onto a system designed to describe *situations qualitatively*. A hexagram for "Will Bitcoin hit $100k?" might say "obstacles ahead, hidden allies, eventual breakthrough after delay" -- and even if Bitcoin does not hit $100k, the *narrative* of obstacles, hidden allies, and delay might accurately describe what happened in the Bitcoin ecosystem during that period.

This follow-up experiment tests the hypothesis: **Meihua hexagram interpretations describe the qualitative character of unfolding situations with above-chance accuracy, independent of binary outcomes.**

---

## Experiment Design Overview

```
                    EVENT SELECTED
                         |
          +--------------+--------------+
          |                             |
    REAL HEXAGRAM                CONTROL HEXAGRAM
    (properly cast)              (randomly assigned)
          |                             |
    INTERPRETATION A             INTERPRETATION B
    (written BEFORE event)       (written BEFORE event)
          |                             |
          +---------> BLIND <----------+
                    EVALUATION
                   (AFTER event)
                         |
                   QUALITATIVE
                   MATCH SCORE
                    (0-5 scale)
```

**Core idea**: For each event, produce TWO interpretations -- one from a properly cast hexagram and one from a randomly assigned hexagram. After the event resolves, a blinded rater scores how well each interpretation matches what actually happened. If Meihua works qualitatively, the real hexagram's interpretation should score higher than the random control.

---

## Phase 1: Event Selection

### Selection Criteria

Events must satisfy ALL of the following:

| Criterion | Requirement | Rationale |
|-----------|-------------|-----------|
| **Upcoming** | Event has not yet occurred at time of casting | Prevents hindsight contamination |
| **Verifiable** | Outcome will be publicly documented in detail | Enables post-hoc factual narrative |
| **Narrative-rich** | Outcome involves process, dynamics, actors, not just a number | Hexagrams describe situations, not scalars |
| **Time-bounded** | Resolves within 3-21 days of casting | Practical turnaround; Meihua is best for near-term |
| **Describable** | Post-event, "what happened" can be written in 200-500 words | Enough detail for qualitative comparison |

### Recommended Event Types (12 events, mixed domains)

| # | Domain | Example Event Type |
|---|--------|--------------------|
| 1 | Politics / Diplomacy | Specific summit or negotiation round |
| 2 | Politics / Diplomacy | Legislative vote or policy announcement |
| 3 | Sports (narrative) | Championship game or playoff series |
| 4 | Sports (narrative) | Major tournament round |
| 5 | Business / Corporate | Earnings report + earnings call |
| 6 | Business / Corporate | Merger/acquisition milestone |
| 7 | Weather / Natural | Named storm or severe weather event |
| 8 | Technology | Major product launch or keynote |
| 9 | Legal / Regulatory | Court ruling or regulatory decision |
| 10 | Cultural / Entertainment | Awards ceremony or premiere |
| 11 | Science / Space | Rocket launch, mission milestone |
| 12 | International Crisis | Geopolitical situation with upcoming deadline |

### Event Selection Process

1. Identify 3-4 events per week in the coming 7-21 days that meet all criteria
2. Pre-register event before casting (record: name, resolution date, domain, description)
3. No cherry-picking: select events BEFORE knowing what hexagram they will produce
4. Target 12-15 events (allows for 1-2 dropouts)

---

## Phase 2: Hexagram Casting

### Real Hexagram (Treatment)

Cast ONE hexagram per event using text-based method (測字起卦):

1. Take event title (e.g., "US-China Trade Summit in Geneva")
2. Upper trigram = word count mod 8
3. Lower trigram = character count mod 8
4. Changing line = (word count + character count) mod 6
5. Use mapping: 1=乾, 2=兌, 3=離, 4=震, 5=巽, 6=坎, 7=艮, 0(8)=坤
6. Derive: primary hexagram, mutual hexagram (lines 2-3-4 / 3-4-5), changed hexagram
7. Record all calculations explicitly

### Control Hexagram (Random Assignment)

For each event, also assign a random hexagram:

1. Generate random integer 1-64
2. Generate random changing line 1-6
3. Derive mutual and changed hexagrams using standard rules
4. Generate ALL random hexagrams in a single batch BEFORE interpretation

---

## Phase 3: Pre-Event Interpretation

### Blinding Protocol

Present both hexagrams to the interpreter in randomized order, labeled only "Hexagram A" and "Hexagram B." The interpreter does NOT know which is real vs. control.

### Interpretation Template

For each hexagram, produce:

```
EVENT: [event title]
HEXAGRAM LABEL: [A or B]

1. SITUATION DESCRIPTION (2-3 sentences)
   What kind of situation does this hexagram describe?

2. KEY ACTORS / FORCES (2-3 bullet points)
   Who or what are the main forces at play?

3. PROCESS NARRATIVE (3-5 sentences)
   How will the situation unfold?

4. QUALITATIVE OUTCOME CHARACTER (2-3 sentences)
   Not YES/NO, but: What is the *flavor* of the outcome?

5. SPECIFIC IMAGERY / METAPHORS (2-3 bullet points)
   What concrete images does the hexagram suggest?

6. WARNINGS / SURPRISES (1-2 sentences)
   What unexpected element does the hexagram suggest?
```

### Interpretation Rules

- **No binary prediction**: Must NOT say "this will succeed/fail"
- **No hedging everything**: Each element must be specific enough to be falsifiable
- **No external knowledge**: Derive meaning ONLY from hexagram, not news/domain expertise
- **Timestamp**: All interpretations locked before event occurs

---

## Phase 4: Post-Event Narrative

After each event resolves, a SEPARATE agent (with no access to hexagrams) writes a factual 300-500 word narrative covering:
- What happened, chronologically
- Key actors and their actions
- Dynamics (cooperative, adversarial, chaotic, orderly)
- What was surprising or unexpected
- Character of the outcome (dramatic, anticlimactic, partial)
- Sources (2-3 independent news sources)

---

## Phase 5: Blind Evaluation

### Scoring Rubric (0-5 Scale)

| Score | Label | Definition |
|-------|-------|------------|
| **0** | No match | Interpretation is contradicted by reality |
| **1** | Trivial match | Only the most generic elements match |
| **2** | Partial match | 1-2 specific elements loosely connect, overall wrong |
| **3** | Moderate match | Overall character roughly right, 2-3 specifics connect |
| **4** | Strong match | Narrative arc matches well, most specifics connect |
| **5** | Remarkable match | Reads as if written by someone who knew the outcome |

### Anti-Rationalization Safeguards

| Threat | Mitigation |
|--------|------------|
| Post-hoc rationalization | Score each element INDEPENDENTLY, then aggregate |
| Confirmation bias | Score A fully before reading B |
| Vagueness exploitation | Rate each element as SPECIFIC or VAGUE; only SPECIFIC matches count for 3+ |
| Asymmetric effort | Use identical template for real and control |

### Multiple Raters

- Minimum: 1 AI rater (blinded)
- Recommended: 3 raters (2 AI + 1 human if available)
- Calculate inter-rater reliability (Krippendorff's alpha)

---

## Phase 6: Statistical Analysis

### Primary Test: Wilcoxon Signed-Rank Test

Appropriate for paired ordinal data with small N.

```python
from scipy.stats import wilcoxon
stat, p_value = wilcoxon(real_scores, control_scores, alternative='greater')
```

**Significance threshold**: p < 0.05 (one-tailed)

### Power Analysis (N=12)

| Effect Size (r) | Power | Detectable? |
|------------------|-------|-------------|
| 0.3 (small) | ~0.15 | No |
| 0.5 (medium) | ~0.45 | Marginal |
| 0.7 (large) | ~0.80 | Yes |

This is a pilot. Can only detect large effects.

### Decision Matrix

| Result | Interpretation | Next Step |
|--------|----------------|-----------|
| p < 0.05, r > 0.5 | Strong signal | N=40 confirmatory study |
| p < 0.10, r > 0.3 | Suggestive | N=40, refine methodology |
| p > 0.10, r < 0.3 | No signal | Hypothesis unsupported |
| Control > real | Reversed | Close this line of inquiry |

---

## Agent Execution Protocol

### Agent 1: Event Selector + Caster
- Selects events, casts real hexagrams, generates random controls
- Does NOT interpret

### Agent 2: Interpreter (Blinded)
- Receives hexagram pairs (A/B, randomized) + event titles
- Does NOT know which is real vs. control
- Has full Meihua skill loaded

### Agent 3: Narrator (Blinded)
- Writes factual narrative after event resolution
- Has NO access to hexagrams

### Agent 4: Evaluator (Blinded)
- Receives narrative + interpretation A + interpretation B
- Does NOT know which is real
- Scores using rubric

### Agent 5: Statistician
- Receives all scores + unblinding key
- Runs analysis, writes report

---

## Data Storage

```
experiments/qualitative-match/
  ├── protocol.md              (this document)
  ├── events/
  │   ├── event_registry.json
  │   └── E01_narrative.md ...
  ├── hexagrams/
  │   ├── casting_records.json
  │   └── random_seed.txt
  ├── interpretations/
  │   ├── E01_A.md ...
  │   └── blinding_key.json
  ├── evaluations/
  │   ├── E01_eval_r1.json ...
  │   └── inter_rater.json
  └── analysis/
      ├── results.json
      ├── statistics.py
      └── report.md
```

---

## Success Criteria

| Outcome | Criteria | Meaning |
|---------|----------|---------|
| Positive | p < 0.05, r > 0.5, mean diff > 1.0 | Meihua describes situations better than random |
| Suggestive | p < 0.10, r > 0.3, mean diff > 0.5 | Interesting but inconclusive |
| Null | p > 0.10, r < 0.3 | No qualitative match signal |
| Reversed | Control scores higher | Meihua casting is counterproductive |

---

*Version: 1.0 | Created: 2026-02-24 | Status: Ready for execution*
*Predecessor: prediction-validation (binary, N=100, 51% result)*
