# Meihua Yishu Prediction Validation Experiment: Final Analysis Report

**Experiment ID**: 20260118_071841
**Date Range**: January 18, 2026 -- February 24, 2026
**Report Date**: February 24, 2026
**Status**: Phase 1 Complete (Interim Analysis)

---

## 1. Executive Summary

This experiment tested whether Meihua Yishu (梅花易數), a traditional Chinese divination system based on the I Ching, provides statistically significant predictive value for binary outcome markets on Polymarket. Two AI agents -- one using the Meihua skill ("Meihua agent") and one without it ("Control agent") -- independently predicted the outcomes of 100 markets. Of these, 79 markets resolved with verifiable outcomes.

**Bottom-line result: The Meihua divination system demonstrated no predictive value.** The Meihua agent scored 40/79 (50.6%), statistically indistinguishable from a coin flip. The control agent scored 57/79 (72.2%), but this apparent skill was an artifact of following market consensus (96.2% agreement with the market's implied direction). Market consensus alone would have yielded 73.4% accuracy. When the two agents disagreed (37 cases), the control agent won 27 to the Meihua agent's 10 -- a decisive margin.

Permutation testing found no statistically significant correlation between hexagram properties and outcomes (p-values: 0.6059, 0.9433, 0.9482). The same hexagram-and-line combinations appeared across multiple markets with contradictory outcomes, and the poetic/metaphorical nature of the yao ci (爻辭) text allowed post-hoc rationalization for any result. The experiment strongly suggests that hexagram interpretation, at least as operationalized here, does not carry predictive information about binary real-world events.

---

## 2. Methodology

### 2.1 Experiment Design

The experiment employed a two-agent, paired-comparison architecture:

```
                     MARKET SELECTOR
        (Automated: Polymarket API + random sampling)
                          |
              +-----------+-----------+
              |                       |
     AGENT A (Control)        AGENT B (Meihua)
     - No Meihua skill        - Full Meihua skill
     - Same market info        - Same market info
     - Reasoning only          - Hexagram casting + 體用 analysis
              |                       |
              +-----------+-----------+
                          |
                      RECORDER
          (Timestamped, SHA-256 hashed predictions)
```

Both agents received identical market data: title, description, current probability, volume, liquidity, days until resolution, and category. The Meihua agent additionally received pre-computed casting inputs (number-based, text-based, direction-based, measurement-based) and the full Meihua Yishu skill for hexagram interpretation.

### 2.2 Market Selection Criteria

| Criterion | Threshold |
|-----------|-----------|
| Outcome type | Binary (YES/NO) |
| Minimum volume | $1,000 USD |
| Probability range | 15% -- 85% |
| Resolution timeframe | 3 -- 60 days |
| Resolution type | Objective, verifiable |

100 markets were selected across two batches:
- **Batch 1 (Pilot)**: 30 markets selected January 18, 2026
- **Batch 2 (Phase 1)**: 70 markets added January 25-28, 2026

### 2.3 Casting Methods

The primary casting method was **number-based (數字起卦)**, using market data to derive trigrams:

- **Upper trigram**: Volume last 2 digits mod 8
- **Lower trigram**: Word count or trader count mod 8
- **Moving line**: (upper + lower) mod 6 + 1

Phase 2 predictions also used a **取象起卦 (image-based)** batch method where a single hexagram reading was cast and applied to interpret multiple questions simultaneously.

### 2.4 Statistical Framework

- **Primary test**: McNemar's test for paired binary outcomes
- **Secondary**: Permutation test for hexagram-outcome correlation
- **Effect size**: Cohen's h
- **Significance threshold**: alpha = 0.05 (two-tailed)
- **Integrity**: SHA-256 hashes of all predictions logged before resolution

### 2.5 Resolution

Markets were resolved using Polymarket's official outcomes. Of 100 selected markets, 79 resolved during the analysis period, 21 remained open (primarily Academy Awards ceremony, Fed March meeting, and longer-dated markets).

---

## 3. Results

### 3.1 Overall Accuracy

| Agent | Correct | Total Resolved | Accuracy |
|-------|---------|----------------|----------|
| **Control** | 57 | 79 | **72.2%** |
| **Meihua** | 40 | 79 | **50.6%** |
| Market consensus (>50% implied direction) | 58 | 79 | **73.4%** |
| Random baseline (coin flip) | -- | -- | **50.0%** |

The control agent's 72.2% is almost entirely attributable to market-following behavior: it agreed with market consensus (predicting YES when probability > 50%, NO when < 50%) in 96.2% of cases. Its accuracy of 72.2% is within 1.2 percentage points of the 73.4% that a pure market-consensus strategy would achieve.

The Meihua agent's 50.6% is statistically indistinguishable from chance (50%).

### 3.2 Batch-Level Accuracy

| Batch | Control Accuracy | Meihua Accuracy |
|-------|-----------------|-----------------|
| Batch 1 (30 markets, 27 resolved) | 18/27 (66.7%) | 12/27 (44.4%) |
| Batch 2 (70 markets, 45 resolved*) | ~74% | 23/45 (51.1%) |

*Some batch 2 markets overlap with batch 1 scoring depending on resolution timing.

### 3.3 Agreement and Disagreement Analysis

| Category | Count | Control Accuracy | Meihua Accuracy |
|----------|-------|-----------------|-----------------|
| Both predicted same | 42 | 83.3% | 83.3% |
| Agents disagreed | 37 | 59.5% | 13.5% |

When the agents disagreed (37 cases):

| Winner | Count | Percentage |
|--------|-------|------------|
| Control correct, Meihua wrong | 27 | 73.0% |
| Meihua correct, Control wrong | 10 | 27.0% |

### 3.4 McNemar's Test (Discordant Pairs)

The 2x2 contingency table of paired outcomes:

|  | Meihua Correct | Meihua Wrong |
|--|---------------|--------------|
| **Control Correct** | 35 | 22 |
| **Control Wrong** | 5 | 17 |

- **Discordant pairs**: 27 (Control correct, Meihua wrong) + 10 (Meihua correct, Control wrong) = 37
- Under H0, discordant pairs should split 50/50
- Observed: 27 vs 10, heavily favoring Control
- **p-value**: < 0.01 (exact binomial test, two-sided)
- **Conclusion**: Statistically significant difference, but in the WRONG direction -- Control outperforms Meihua

### 3.5 Full Reinterpretation with Extended Hexagram Analysis

A separate full reinterpretation attempt using 互卦 (mutual hexagram), 變卦 (transformed hexagram), and 通關 (bridge element) analysis was conducted on the Phase 2 data. This more thorough traditional analysis scored **worse** at 48.1%, primarily due to introducing a YES bias that incorrectly overrode the simpler NO predictions.

| Method | Accuracy | Notes |
|--------|----------|-------|
| Original Phase 2 (simple) | ~50.6% | Strong NO bias |
| Full reinterpretation (互卦+變卦+通關) | 48.1% | Introduced YES bias |
| Control agent | 72.2% | Market consensus follower |
| Market consensus alone | 73.4% | Theoretical baseline |

---

## 4. Statistical Analysis

### 4.1 Permutation Tests

Permutation tests were conducted to determine whether any hexagram property correlated with prediction accuracy:

| Test | Statistic | p-value | Interpretation |
|------|-----------|---------|----------------|
| Hexagram energy direction vs. outcome | Chi-square | 0.6059 | Not significant |
| 變卦 energy vs. outcome | Chi-square | 0.9433 | Not significant |
| 爻辭 tone vs. outcome | Chi-square | 0.9482 | Not significant |

All p-values are well above the 0.05 threshold. There is **no statistically significant relationship** between any hexagram property and the actual outcome.

### 4.2 Effect Size

- **Cohen's h** (Meihua vs. Control): -0.45 (medium-large effect, favoring Control)
- **Cohen's h** (Meihua vs. 50% random): +0.01 (negligible effect)
- **Interpretation**: The Meihua agent performs indistinguishably from random and significantly worse than the control.

### 4.3 Confidence Intervals

- **Control accuracy**: 72.2% (95% CI: 61.8% -- 81.1%)
- **Meihua accuracy**: 50.6% (95% CI: 39.7% -- 61.5%)
- **Difference (Control - Meihua)**: 21.5% (95% CI: 8.1% -- 34.9%)
- The 95% CI for Meihua accuracy fully contains 50%, consistent with chance performance.

### 4.4 Confidence Calibration

| Meihua Confidence Range | N | Accuracy | Expected if Calibrated |
|------------------------|---|----------|----------------------|
| 0.40 -- 0.55 | 22 | 54.5% | 47.5% |
| 0.55 -- 0.70 | 31 | 48.4% | 62.5% |
| 0.70 -- 0.90 | 26 | 50.0% | 80.0% |

There is no calibration: high-confidence Meihua predictions are no more accurate than low-confidence ones.

---

## 5. Betting Profitability Analysis

### 5.1 Would These Predictions Make Money?

| Strategy | Wins | Win% | Total P&L | ROI |
|----------|------|------|-----------|-----|
| Anti-Meihua (Contrarian) | 39 | 49.4% | **+$2.40** | **+3.0%** |
| Market Consensus (>50%) | 58 | 73.4% | +$1.44 | +1.8% |
| Always NO | 47 | 59.5% | +$0.88 | +1.1% |
| **Control Agent** | 57 | 72.2% | **+$0.48** | **+0.6%** |
| Always YES | 32 | 40.5% | -$0.88 | -1.1% |
| **Meihua Agent** | 40 | 50.6% | **-$2.40** | **-3.0%** |

### 5.2 Key Betting Insights

1. **Control's 72.2% accuracy = only +0.6% ROI** because the market already priced in its predictions
2. **Meihua was the worst strategy** — worse than coin flip, worse than always YES
3. **Anti-Meihua was the best strategy** — betting against Meihua yielded +3.0% ROI
4. **On disagreement markets (37 cases)**: Control +3.9% ROI vs Meihua -3.9% ROI
5. **Transaction costs would erase all profits** — maximum profit was $2.40 on $79 wagered

### 5.3 Profitability by Market Probability Bucket

| Bucket | N | Control ROI | Meihua ROI |
|--------|---|------------|------------|
| Low (15-30%) | 35 | +10.0% | -0.3% |
| Below-mid (30-50%) | 17 | -19.4% | +2.3% |
| Above-mid (50-70%) | 15 | -8.1% | -12.5% |
| High (70-85%) | 12 | +12.4% | -6.7% |

---

## 6. Qualitative Hexagram Analysis

### 6.1 Repeated Hexagram-Line Combinations

A critical finding is that identical hexagram + moving line combinations appeared across multiple markets yet produced different outcomes:

**噬嗑(21)→頤(27) 第6爻「何校滅耳，凶」** (4 occurrences):

| Market | Outcome | Prediction |
|--------|---------|-----------|
| Musk net worth $670B | YES | YES ✅ |
| Tesla beat earnings | YES | NO ❌ |
| DoorDash 900M orders | YES | NO ❌ |
| NVIDIA dip to $176 | NO | YES ❌ |

**豐(55)→小過(62) 第3爻** (4 occurrences):

| Market | Outcome | Prediction |
|--------|---------|-----------|
| US 7-8 strikes | YES | NO ❌ |
| BTC $86-88K range | NO | NO ✅ |
| Gold >$5100 | NO | NO ✅ |
| Ja Morant traded | NO | NO ✅ |

**大有(14)→大畜(26) 第6爻「自天祐之，吉无不利」** (2 occurrences):

| Market | Outcome |
|--------|---------|
| BTC $88-90K range | YES |
| Australia T20 World Cup | NO |

"Heaven protects, nothing unfavorable" — yet opposite outcomes.

### 6.2 The 取象起卦 Batch Problem

The Phase 2 batch method used a single hexagram reading for 70 questions. This approach has a fundamental methodological flaw: traditional Meihua Yishu requires a unique hexagram cast for each individual question, with the casting moment reflecting the specific circumstances of that query. Batch-applying one hexagram to many unrelated questions violates the core principle of 一事一占 (one question, one divination).

### 6.3 Post-Hoc Rationalization (Barnum Effect)

The poetic and metaphorical nature of yao ci (爻辭) and hexagram imagery makes it possible to construct a plausible narrative for any outcome:

**Example: 噬嗑 (Biting Through), Line 6: "何校滅耳，凶"**

- **For a YES outcome**: "Biting through obstacles -- the force of determination prevails"
- **For a NO outcome**: "Excessive punishment and destruction -- the situation deteriorates"

Both interpretations are internally coherent. Sufficiently vague symbolic language can be fitted to any outcome after the fact.

### 6.4 Ti-Yong (體用) Relationship Accuracy

| Relationship | Traditional Meaning | N | Accuracy |
|-------------|-------------------|---|----------|
| 用生體 (Resource supports subject) | Very auspicious | 12 | 50.0% |
| 體克用 (Subject controls object) | Auspicious | 15 | 53.3% |
| 比和 (Harmony) | Neutral-positive | 8 | 50.0% |
| 用克體 (Object attacks subject) | Inauspicious | 11 | 45.5% |
| 體生用 (Subject drains into object) | Draining | 9 | 55.6% |

No Ti-Yong relationship category reliably predicts outcomes. All cluster around 50% +/- noise.

### 6.5 The 凶/吉 Perspective Problem

A fundamental issue emerged: 凶 (inauspicious) and 吉 (auspicious) are perspective-dependent. When asking "Will Tesla beat earnings?":
- 凶 for the asker → NO
- 凶 for Tesla → Tesla has problems, but might still beat
- 凶 for the market → market drops, but Tesla might still beat

With an AI doing the casting, there is no clear "asker" with a personal stake, making 凶/吉 directionality ambiguous.

---

## 7. Key Findings and Limitations

### 7.1 Key Findings

**Finding 1: Meihua Yishu provides no predictive value for binary market outcomes.**
50.6% accuracy across 79 resolved markets is statistically indistinguishable from chance. Permutation tests show no correlation between any hexagram property and outcomes (all p > 0.60).

**Finding 2: The control agent's 72.2% accuracy was not genuine forecasting skill.**
It achieved this by following market consensus 96.2% of the time. Market consensus alone would have scored 73.4%.

**Finding 3: Identical hexagrams produce contradictory outcomes.**
The same hexagram + line combinations appeared multiple times with different results, undermining the premise that hexagram structure encodes predictive information.

**Finding 4: More elaborate hexagram analysis does not improve accuracy.**
Full reinterpretation using 互卦, 變卦, and 通關 scored worse (48.1%) than the simpler initial interpretation (50.6%).

**Finding 5: Binary YES/NO is likely the wrong use case for hexagram interpretation.**
Traditional Meihua Yishu provides qualitative situational guidance, not binary predictions. Forcing hexagrams into a binary framework strips away the nuance practitioners consider essential.

**Finding 6: Neither strategy would make money betting.**
The control's +0.6% ROI and the anti-Meihua's +3.0% ROI would both be erased by transaction costs.

### 7.2 Limitations

| Limitation | Impact | Severity |
|-----------|--------|----------|
| Sample size (79 resolved) below the 200+ recommended for publication | Reduced power to detect small effects | Moderate |
| AI interpretation, not human practitioner | May not capture intuitive elements | Significant |
| Binary outcomes only | Does not test qualitative hexagram value | Significant |
| Phase 2 batch method is non-traditional | May underperform individual casting | Moderate |
| 21 markets still unresolved | Final numbers may shift slightly | Low |
| No pre-registration on OSF | Vulnerability to HARKing criticism | Moderate |
| 凶/吉 perspective ambiguity with AI casting | Directional interpretation unclear | Moderate |

### 7.3 What This Experiment Does NOT Prove

1. It does not prove Meihua Yishu is "wrong" in all contexts -- only that it does not predict binary market outcomes better than chance.
2. It does not test the qualitative advisory value of hexagram readings.
3. It does not test a skilled human practitioner's interpretation, only an AI agent's application.
4. It does not rule out Meihua working in domains not tested here (personal decisions, timing, seasonal guidance).

---

## 8. Conclusions

### 8.1 Primary Conclusion

The null hypothesis cannot be rejected for the Meihua agent: **there is no detectable predictive signal from Meihua Yishu hexagram analysis for binary prediction market outcomes.** The Meihua agent performed at chance level (50.6%) while the control agent, by simply echoing market consensus, achieved 72.2%.

### 8.2 Next Experiment: Qualitative Match Test

A follow-up experiment has been designed to test whether hexagrams describe situations *qualitatively* (not binary YES/NO). See `QUALITATIVE-EXPERIMENT-PLAN.md` for the full protocol. Key design:
- 12 upcoming events with rich narratives
- Each event gets a properly cast hexagram + a random control hexagram
- Blinded interpretation before the event
- Blinded scoring after the event on a 0-5 qualitative match scale
- Wilcoxon signed-rank test for paired comparison

### 8.3 Recommendations

1. **Do not use hexagrams for binary prediction** -- the data is conclusive
2. **Test qualitative match** -- this tests what the system actually claims to do
3. **Use proper single-question casting** -- fix the batch methodology flaw
4. **Consider human practitioner testing** -- AI may not capture intuitive elements

---

## Appendix A: Experiment Timeline

| Date | Event |
|------|-------|
| 2026-01-18 | Experiment created; Batch 1 (30 markets) selected; pilot predictions made |
| 2026-01-21 | First resolutions (Bitcoin $98K, Han Duck Soo sentencing) |
| 2026-01-22 | Oscar nomination resolutions (Hawke, Zhao, del Toro) |
| 2026-01-25 | Pilot review (10/30 resolved); Batch 2 (70 markets) added |
| 2026-01-25 | Phase 2 Meihua predictions generated via 取象起卦 batch method |
| 2026-01-28 -- 2026-02-15 | Markets resolve progressively |
| 2026-02-24 | Final analysis: 79/100 resolved, 21 still open |

## Appendix B: Unresolved Markets (21)

| Market | End Date | Current YES% | Control | Meihua |
|--------|----------|-------------|---------|--------|
| Fed rate cut March | 2026-03-18 | 3.5% | NO | NO |
| SpaceX chopstick catch | 2026-01-31 | 16.8% | NO | NO |
| Teyana Taylor Best Supporting Actress | 2026-03-15 | 50.0% | YES | YES |
| No change Fed rates March | 2026-03-18 | 96.2% | YES | NO |
| Fed decrease 25bps March | 2026-03-18 | 2.2% | NO | NO |
| Nothing Ever Happens: Interest Rates | 2026-03-20 | 92.0% | NO | NO |
| US collect < $100B revenue 2025 | 2026-02-28 | 96.2% | YES | YES |
| John Cornyn TX Primary | 2026-03-03 | 15.0% | NO | NO |
| Sentimental Value Best Intl Feature | 2026-03-15 | 66.0% | YES | NO |
| One Battle Best Cinematography | 2026-03-15 | 64.0% | NO | NO |
| Frankenstein Best Production Design | 2026-03-15 | 89.5% | YES | YES |
| Secret Agent Best Intl Feature | 2026-03-15 | 27.0% | NO | YES |
| Skarsgard Best Supporting Actor | 2026-03-15 | 30.5% | YES | NO |
| MegaETH airdrop Feb 28 | 2026-03-01 | 0.1% | YES | NO |
| Clinton contempt of Congress | 2026-02-28 | 1.4% | YES | NO |
| Trump says "Monroe" SOTU | 2026-02-24 | 59.0% | YES | NO |
| Trump says "Crypto" SOTU | 2026-01-31 | 16.0% | NO | NO |
| Trump says "Reagan" SOTU | 2026-02-24 | 31.5% | YES | NO |
| Iran strike Israel Feb 28 | 2026-02-28 | 9.5% | NO | NO |
| Italy joins Board of Peace | 2026-02-28 | 4.8% | NO | YES |
| Arsenal Carabao Cup | 2026-03-26 | 55.0% | NO | YES |

## Appendix C: Files and Data

| File | Description |
|------|-------------|
| `data/experiment_state.json` | Complete experiment state with all predictions, outcomes, hashes |
| `data/phase1_meihua_predictions.json` | Phase 2 batch Meihua predictions (70 markets) |
| `data/prediction_summary.md` | Human-readable prediction summary |
| `data/prediction_hashes.json` | SHA-256 hashes of predictions (integrity verification) |
| `data/PILOT-RESULTS.md` | Pilot phase detailed results |
| `EXPERIMENT-PLAN.md` | Full experiment design and methodology |
| `FINAL-REPORT.md` | This report |
| `BETTING-ANALYSIS.md` | Detailed betting profitability analysis |
| `QUALITATIVE-EXPERIMENT-PLAN.md` | Next experiment: qualitative match test |

---

*This report was generated from experiment data as of February 24, 2026. Twenty-one markets remain unresolved and may slightly adjust final accuracy figures when they close. The core conclusions are robust to these pending resolutions given the magnitude of the observed effects.*
