# Pilot Phase Results

**Date:** 2026-01-18
**Markets Selected:** 30
**Batch:** 001

---

## Actual Outcomes (Updated 2026-01-25)

**Resolution Status:** 10/30 markets resolved

### Summary Results

| Method | Correct | Total | Accuracy |
|--------|---------|-------|----------|
| **Control** | 8 | 10 | **80.0%** |
| **Meihua** | 4 | 10 | **40.0%** |

**Gap:** 40 percentage points in favor of Control

### McNemar's Test (Discordant Pairs Analysis)

| Both Correct | Only Control Correct | Only Meihua Correct | Both Wrong |
|--------------|---------------------|---------------------|------------|
| 3 | 5 | 1 | 1 |

- **χ² statistic:** 0.0000
- **p-value:** 0.2188 (NOT significant at α=0.05)
- **Effect size (Cohen's h):** -0.845 (large, favoring Control)

### Full Results Table

| Market | Actual | Control | Meihua | C ✓ | M ✓ | Discordant? |
|--------|--------|---------|--------|-----|-----|-------------|
| Bitcoin > $98K Jan 21 | **NO** | NO | YES | ✅ | ❌ | Yes |
| Ethan Hawke Best Actor | **YES** | YES | NO | ✅ | ❌ | Yes |
| Han Duck Soo 5-10 years | **NO** | NO | YES | ✅ | ❌ | Yes |
| Trump-Putin talk Jan | **YES** | YES | NO | ✅ | ❌ | Yes |
| Israel strike 2 countries | **YES** | NO | YES | ❌ | ✅ | Yes |
| Cerundolo tennis | **NO** | NO | YES | ✅ | ❌ | Yes |
| Atmane tennis | **NO** | YES | YES | ❌ | ❌ | No |
| Chloé Zhao Best Director | **YES** | YES | YES | ✅ | ✅ | No |
| del Toro Best Director | **NO** | NO | NO | ✅ | ✅ | No |
| UFC Yadong vs O'Malley | **NO** | NO | NO | ✅ | ✅ | No |

### Discordant Pairs Breakdown

**Control won 5/6 discordant pairs (83%)**

| Market | Actual | Winner |
|--------|--------|--------|
| Bitcoin > $98K | NO | Control |
| Ethan Hawke | YES | Control |
| Han Duck Soo | NO | Control |
| Trump-Putin | YES | Control |
| Cerundolo tennis | NO | Control |
| Israel 2 countries | YES | **Meihua** |

### Critical Methodology Note

**The pilot used TIME-BASED casting (舊方法 - old method)**
- Hexagrams derived from timestamp, not question content
- This is the traditional 時間起卦 method

**The enhanced skill uses QUESTION-BASED casting (新方法 - new method)**
- Hexagrams derived from question text, word count, context
- Full question details provided to skill
- This is 測字起卦 + contextual analysis

**These are fundamentally different methods.** The pilot results (40% Meihua accuracy) may not represent the enhanced skill's capabilities.

---

## Prediction Agreement Analysis

| Metric | Count | Percentage |
|--------|-------|------------|
| Concordant pairs (same prediction) | 16 | 53% |
| Discordant pairs (different prediction) | 14 | 47% |

**Note:** Pre-registration assumed 30% discordant rate. Actual rate is 47%, which provides more statistical power for McNemar's test.

## Observation

Many predictions align because both methods often follow market consensus:
- When market probability is high (>70%), both tend to predict YES
- When market probability is low (<30%), both tend to predict NO
- Discordance occurs more often in mid-range probabilities (30-70%)

This is expected behavior - the Meihua method is not designed to always contradict market consensus. The test is whether, among discordant pairs, one method is more often correct.

## Discordant Pairs Detail

### Meihua predicts YES, Control predicts NO (11 markets)

| Market | Initial Prob | Hexagram | 體用 |
|--------|-------------|----------|------|
| Bitcoin > $98K | 17% | 風火家人 | 用生體 |
| Israel strike 2 countries | 26% | 火地晉 | 用生體 |
| Han Duck Soo 5-10 years | 29% | 山火賁 | 體生用 |
| USD/Rial 1.5M | 39% | 風天小畜 | 體克用 |
| US GDP > 2.5% | 17% | 火澤睽 | 體克用 |
| Powell "Stock Market" | 26% | 澤天夬 | 比和 |
| Portugal Seguro | 42% | 雷澤歸妹 | 體克用 |
| Greenland tariffs | 19% | 山雷頤 | 體克用 |
| Bank of Russia rate | 31% | 火風鼎 | 用生體 |
| Silver > $90 | 49% | 山水蒙 | 體克用 |
| Cerundolo tennis | 33% | 山天大畜 | 用生體 |

### Control predicts YES, Meihua predicts NO (3 markets)

| Market | Initial Prob | Hexagram | 體用 |
|--------|-------------|----------|------|
| Ethan Hawke nomination | 76% | 天風姤 | 用克體 |
| GE Vernova "Administration" | 67% | 山地剝 | 比和 |
| Trump-Putin talk | 48% | 雷地豫 | 用克體 |

## Pattern Observation

Meihua tends to predict YES (against market consensus) when:
- 體用 relationship is favorable (用生體, 體克用, 比和)
- Even when market probability is low

Meihua tends to predict NO (against market consensus) when:
- 體用 relationship is unfavorable (用克體, 體生用)
- Even when market probability is high

This suggests the hexagram interpretation is functioning as designed - using 體用 relationships rather than simply following market probability.

## Sports Markets Note

5 markets are sports-related (should potentially be excluded per protocol):
- Australian Open Men's: Atmane vs Maestrelli
- UFC 324: Yadong vs O'Malley
- Manchester United win
- Australian Open Women's: Jovic vs Volynets
- Australian Open Men's: Cerundolo vs Thompson

## Rigorous Timeline

Following conservative methodology validation approach:

| Date | Action | Milestone |
|------|--------|-----------|
| Jan 18 | ✅ Pilot predictions made | 30/30 predictions with hashes |
| Jan 21 | Check resolutions | Bitcoin, Han Duck Soo sentencing |
| Jan 22 | Check resolutions | Oscar nominations (Hawke, Zhao, del Toro) |
| Jan 25 | **Methodology review** | ~10 markets resolved |
| Jan 28+ | If validated → Start Phase 1 | Add 70 markets |

### Methodology Review Checklist (Jan 25)

Before proceeding to Phase 1, verify:

- [ ] SHA-256 hashes verify correctly for resolved markets
- [ ] Resolution tracking captures outcomes accurately
- [ ] Discordance rate is reasonable (expect 30-50%)
- [ ] No systematic issues with hexagram casting
- [ ] Data logging (JSONL, CSV) working correctly

### Commands to Run

```bash
# Check for resolved markets (run daily starting Jan 21)
cd experiments/prediction-validation
source venv/bin/activate
python scripts/experiment_runner.py check

# View current status
python scripts/experiment_runner.py status

# After methodology review passes (Jan 28+)
python scripts/experiment_runner.py select 70  # Phase 1
```

## Files Generated

- `data/experiment_state.json` - Full experiment state
- `data/experiment_log.jsonl` - Append-only audit log with hashes
- `data/prompts/batch_001/` - All 60 prompts (30 control, 30 meihua)
- `data/prediction_summary.md` - Human-readable summary
