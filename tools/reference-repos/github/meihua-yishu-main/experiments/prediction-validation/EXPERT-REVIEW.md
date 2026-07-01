# Expert Review: Meihua Yishu Prediction Validation Experiment

**Review Date**: 2026-01-18
**Document Version**: 1.0
**Status**: Initial Review

---

## Executive Summary

This document provides expert review of the experiment design from four perspectives:
1. Statistician
2. I Ching Scholar (易學專家)
3. Prediction Market Expert
4. Experimental Psychologist

**Overall Assessment**: The experiment design is **sound but requires improvements** before execution.

---

## 1. Statistician Review

### 1.1 Sample Size Analysis

**Finding**: The current sample size calculations are **simplified approximations**.

The code uses a basic formula:
```python
n = ((z_alpha + z_beta) * se / effect) ** 2
```

**Issue**: For [McNemar's test](https://pubmed.ncbi.nlm.nih.gov/1509223/), sample size depends critically on the **proportion of discordant pairs** (cases where control and meihua disagree). The current formula assumes 50% discordant pairs.

**Recommendation**: Use the proper McNemar sample size formula:
```
n = (z_α/2 + z_β)² × (p_d) / (p_12 - p_21)²

where:
  p_d = proportion of discordant pairs
  p_12 = P(control correct, meihua wrong)
  p_21 = P(control wrong, meihua correct)
```

**Updated Sample Size Estimates** (assuming 30% discordant pairs):

| Effect Size | Current Estimate | Corrected Estimate |
|-------------|------------------|-------------------|
| 5% difference | 785 | ~1,200 |
| 10% difference | 196 | ~300 |
| 15% difference | 87 | ~140 |

### 1.2 Statistical Test Selection

**Finding**: McNemar's test is **appropriate** for this design.

✅ **Correct**:
- Paired binary outcomes (same markets, different methods)
- Tests if disagreements favor one method
- Accounts for correlation between predictions

**Issue**: The chi-square approximation in the code may be inaccurate for small samples.

**Recommendation**:
- For n < 25 discordant pairs, use **exact McNemar test** (binomial)
- Add confidence intervals for the difference in proportions

### 1.3 Multiple Comparisons Problem

**Finding**: The plan tests multiple casting methods but doesn't address multiple comparisons.

**Issue**: Testing 4 casting methods × multiple categories = inflated Type I error.

**Recommendation**:
1. Pre-specify ONE primary hypothesis (e.g., "Any Meihua method vs Control")
2. Apply [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction) for secondary analyses
3. Or use a hierarchical testing procedure

### 1.4 Power Analysis Concerns

**Finding**: 80% power may be insufficient for a novel claim.

**Recommendation**: Consider 90% power for extraordinary claims:
- 80% power → 20% chance of Type II error
- 90% power → 10% chance of Type II error

For 90% power with 10% effect size: **~350 markets needed**

### 1.5 Statistician Verdict

| Aspect | Rating | Notes |
|--------|--------|-------|
| Test selection | ✅ Good | McNemar appropriate |
| Sample size | ⚠️ Needs work | Underestimated |
| Multiple comparisons | ❌ Missing | Must address |
| Effect size | ✅ Good | Cohen's h appropriate |
| Confidence intervals | ⚠️ Missing | Should add |

---

## 2. I Ching Scholar (易學專家) Review

### 2.1 Casting Method Validity

**Finding**: The casting methods are **partially correct** but have issues.

#### Number-Based (數字起卦)
✅ **Correct**: Using volume digits and counts for upper/lower trigrams
⚠️ **Issue**: Moving line calculation should be `(upper + lower) % 6`, giving lines 1-6, not 0-5

**Fix needed in code**:
```python
# Current (may give 0):
"moving_line": ((volume_last_2 + word_count) % 6) or 6

# Should be:
"moving_line": ((volume_last_2 + word_count) % 6) + 1
```

Wait, the current code uses `or 6` which handles the 0 case. This is acceptable but non-traditional. Traditional method: `% 6` gives 0-5, then add 1 to get 1-6.

#### Text-Based (測字起卦)
✅ **Correct**: Word/character count method is valid
⚠️ **Issue**: For English text, character count is less meaningful than for Chinese characters. Consider using:
- Word count (上卦)
- Letter count (下卦)
- Or stroke-equivalent approximations

#### Direction-Based (方位起卦)
✅ **Correct**: Category → direction → trigram mapping uses 後天八卦
⚠️ **Issue**: The mapping is subjective. Document the rationale:

| Category | Direction | Reasoning |
|----------|-----------|-----------|
| Crypto/Finance | 西北 乾 | Wealth, metal, authority |
| Politics | 南 離 | Visibility, governance, fire |
| Tech | 東 震 | Innovation, movement, wood |

### 2.2 體用 (Ti-Yong) Analysis

**Finding**: The experiment correctly emphasizes 體用關係.

✅ **Correct elements**:
- Identifying 體卦 (stationary) and 用卦 (moving)
- Five relationships: 用生體, 體克用, 比和, 用克體, 體生用

⚠️ **Missing**: The experiment should track:
1. **互卦** (Mutual hexagram) - provides additional context
2. **卦氣** (Hexagram energy) - seasonal appropriateness
3. **外應** (External signs) - environmental factors at casting time

### 2.3 Interpretation Concerns

**Finding**: Binary YES/NO predictions oversimplify Meihua.

**Issue**: Traditional Meihua provides nuanced interpretations:
- Timing (何時應驗)
- Degree (程度大小)
- Conditions (條件變化)

**Recommendation**:
1. Allow "UNCERTAIN" as a third category (when 體用 is unclear)
2. Record confidence based on 體用 strength:
   - 用生體: High confidence YES
   - 用克體: High confidence NO
   - 比和: Medium confidence (depends on context)

### 2.4 I Ching Scholar Verdict

| Aspect | Rating | Notes |
|--------|--------|-------|
| Casting methods | ⚠️ Adequate | Minor fixes needed |
| 體用 analysis | ✅ Good | Core concept correct |
| 互卦 inclusion | ❌ Missing | Should add |
| Nuanced predictions | ⚠️ Limited | Consider 3-way classification |
| 外應 documentation | ⚠️ Partial | Need more context |

---

## 3. Prediction Market Expert Review

### 3.1 Market Selection Criteria

**Finding**: Current criteria are **reasonable but could be improved**.

✅ **Good**:
- Volume minimum ($1,000) filters out illiquid markets
- Probability range (15-85%) avoids obvious outcomes
- Resolution timeframe (3-60 days) is reasonable

⚠️ **Issues**:

| Criterion | Current | Recommendation |
|-----------|---------|----------------|
| Volume | >$1,000 | Consider >$10,000 for better liquidity |
| Probability | 15-85% | 20-80% is more standard |
| Liquidity | Not checked | Add liquidity depth check |

### 3.2 Resolution Mechanics

**Finding**: Need to handle edge cases.

**Issues identified**:
1. **Early resolution**: Some markets resolve before end date
2. **Extended resolution**: Markets may extend past end date
3. **Invalid outcomes**: Markets can be voided/cancelled
4. **Ambiguous resolution**: Some outcomes are disputed

**Recommendation**: Add resolution status categories:
- `RESOLVED_YES`
- `RESOLVED_NO`
- `VOIDED` (exclude from analysis)
- `DISPUTED` (flag for review)
- `EXTENDED` (update tracking)

### 3.3 Favorite-Longshot Bias

**Finding**: The experiment doesn't account for [favorite-longshot bias](https://www.pnas.org/doi/10.1073/pnas.1516179112).

**Issue**: Prediction markets systematically overestimate unlikely outcomes. A naive 50% baseline is incorrect.

**Recommendation**:
1. Use **market probability as baseline**, not 50%
2. Compare: Does Meihua outperform the market consensus?
3. Alternative metric: [Brier Score](https://en.wikipedia.org/wiki/Brier_score) for calibration

### 3.4 Market Categories

**Finding**: Category stratification is good but incomplete.

Current categories: politics, crypto, finance, tech, science, legal, entertainment, world

**Missing**:
- Weather/Climate (distinct prediction dynamics)
- Mergers/Acquisitions (corporate events)
- Geopolitical (distinct from politics)

### 3.5 Prediction Market Expert Verdict

| Aspect | Rating | Notes |
|--------|--------|-------|
| Market selection | ⚠️ Good | Increase volume threshold |
| Resolution handling | ⚠️ Needs work | Add edge case handling |
| Baseline comparison | ❌ Wrong | Don't use 50%, use market prob |
| Category coverage | ✅ Good | Consider adding 2-3 more |
| Liquidity check | ❌ Missing | Add order book depth |

---

## 4. Experimental Psychologist Review

### 4.1 Blinding Procedures

**Finding**: Current blinding is **adequate but could be stronger**.

✅ **Good**:
- Predictions logged before resolution
- Control agent doesn't see Meihua prediction

⚠️ **Issues**:
1. Same person (you) runs both agents → potential [experimenter bias](https://libguides.uark.edu/bias/research)
2. No independent verification of predictions

**Recommendations**:
1. **Hash predictions** before resolution (SHA-256 → publish hash)
2. **Independent witness**: Have someone else verify logging
3. **Automated recording**: Remove human from recording loop

### 4.2 Pre-Registration

**Finding**: The experiment is **not pre-registered**.

This is a significant weakness per [current best practices](https://www.psychologicalscience.org/observer/preregistration-replication-and-nonexperimental-studies).

**Issue**: Without pre-registration, results are vulnerable to:
- [HARKing](https://www.clrn.org/what-is-harking-in-psychology/) (Hypothesizing After Results Known)
- Selective reporting
- p-hacking

**Strong Recommendation**:
1. Pre-register on [OSF](https://osf.io/) before collecting data
2. Include:
   - Primary hypothesis
   - Sample size justification
   - Analysis plan
   - Stopping rules

### 4.3 Confirmation Bias

**Finding**: Design has some confirmation bias risks.

**Risks**:
1. Subjective interpretation of hexagrams
2. Researcher wants Meihua to work
3. No adversarial review

**Mitigations to add**:
1. **Devil's advocate**: Have skeptic review interpretations
2. **Blind analysis**: Analyze without knowing which method is which
3. **Adversarial collaboration**: Involve a skeptic in design

### 4.4 Replication Considerations

**Finding**: Replication needs are not addressed.

Per the [replication crisis](https://en.wikipedia.org/wiki/Replication_crisis), even significant findings often fail to replicate.

**Recommendations**:
1. **Document everything**: Full methodology, code, data
2. **Split sample**: Use half for discovery, half for confirmation
3. **External replication**: Plan for independent replication

### 4.5 Experimental Psychologist Verdict

| Aspect | Rating | Notes |
|--------|--------|-------|
| Blinding | ⚠️ Adequate | Add hash verification |
| Pre-registration | ❌ Missing | Critical - must add |
| Confirmation bias | ⚠️ Present | Add devil's advocate |
| Replication plan | ❌ Missing | Add split-sample design |
| Documentation | ✅ Good | Comprehensive logging |

---

## 5. Summary of Required Changes

### Critical (Must Fix Before Starting)

| Issue | Expert | Fix |
|-------|--------|-----|
| Pre-registration | Psychologist | Register on OSF |
| Sample size underestimated | Statistician | Increase to 150+ for pilot |
| Wrong baseline (50%) | Market Expert | Use market probability |
| Multiple comparisons | Statistician | Pre-specify primary hypothesis |

### Important (Should Fix)

| Issue | Expert | Fix |
|-------|--------|-----|
| Missing 互卦 | I Ching Scholar | Add to analysis |
| No hash verification | Psychologist | Add SHA-256 hashing |
| Exact McNemar for small n | Statistician | Add exact test |
| Liquidity check | Market Expert | Add order book depth |

### Nice to Have

| Issue | Expert | Fix |
|-------|--------|-----|
| 3-way predictions | I Ching Scholar | Add UNCERTAIN option |
| Brier score | Market Expert | Add calibration metric |
| Split-sample | Psychologist | Reserve 30% for confirmation |

---

## 6. Revised Sample Size Recommendation

Based on expert review:

| Phase | Original | Revised | Rationale |
|-------|----------|---------|-----------|
| Pilot | 20 | 30 | Better estimate of discordant pairs |
| Phase 1 | 50 | 100 | Minimum for McNemar power |
| Phase 2 | 100 | 200 | Detect 10% effect |
| Phase 3 | 200 | 350 | 90% power, publishable |

**Total recommended: 350 markets** for publishable results.

---

## 7. Pre-Registration Template

Before starting, register the following on [OSF Registries](https://osf.io/registries):

```markdown
# Meihua Yishu Prediction Validation Study

## Hypothesis
H1: Predictions made using Meihua Yishu divination will have
    higher accuracy than control predictions on the same markets.

H0: There is no difference in accuracy between Meihua and control.

## Primary Outcome
McNemar's test comparing paired predictions on resolved markets.

## Sample Size
N = 200 markets (minimum)
Justification: 80% power to detect 10% accuracy difference,
assuming 30% discordant pairs.

## Analysis Plan
1. Primary: McNemar's exact test (two-tailed, α = 0.05)
2. Effect size: Cohen's h
3. Secondary: Accuracy by casting method (Bonferroni-corrected)

## Stopping Rules
- Stop for futility if p > 0.50 at N = 100
- Continue if 0.05 < p < 0.50

## Exclusion Criteria
- Markets voided/cancelled
- Markets with ambiguous resolution
```

---

## 8. Next Steps

1. [ ] **Fix code issues** identified in this review
2. [ ] **Pre-register** on OSF before any data collection
3. [ ] **Increase sample size** targets per recommendations
4. [ ] **Add hash verification** for predictions
5. [ ] **Update baseline** to market probability, not 50%
6. [ ] **Add exact McNemar** test for small samples
7. [ ] **Document casting rationale** for each method
8. [ ] **Run updated pilot** with 30 markets

---

## Sources

- [McNemar Test Power Analysis](https://pubmed.ncbi.nlm.nih.gov/1509223/)
- [Pre-registration in Psychology](https://www.psychologicalscience.org/observer/preregistration-replication-and-nonexperimental-studies)
- [Prediction Markets for Scientific Research](https://www.pnas.org/doi/10.1073/pnas.1516179112)
- [Open Science Framework](https://osf.io/)
- [Replication Crisis](https://en.wikipedia.org/wiki/Replication_crisis)
- [Research Bias Control](https://libguides.uark.edu/bias/research)
- [HARKing in Psychology](https://www.clrn.org/what-is-harking-in-psychology/)

---

*Review completed: 2026-01-18*
