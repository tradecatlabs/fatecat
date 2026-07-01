# Meihua Yishu Prediction Validation Experiment

**Goal**: Test if 梅花易數 provides statistically significant predictive value using Polymarket prediction markets.

## Quick Links

- [Full Experiment Plan](./EXPERIMENT-PLAN.md) — Detailed methodology
- [OSF Pre-Registration](./OSF-PREREGISTRATION.md) — Template for OSF registration
- [Expert Review](./EXPERT-REVIEW.md) — Statistician, I Ching scholar, and psychology review
- [Divination Records](./DIVINATION.md) — Meta-divinations about this experiment
- [Scripts README](./scripts/README.md) — How to run the experiment
- [Results](./data/) — Prediction logs and outcomes (TBD)

## Approach

Two prediction methods on the same markets:
- **Control**: Pure probability-based prediction (no Meihua)
- **Meihua**: Prediction enhanced with Meihua Yishu hexagram casting

Both see identical market information. The only variable is the divination skill.

## Bias Mitigation

| Potential Bias | Mitigation |
|----------------|------------|
| **Selection bias** (trending markets) | Stratified random sampling across categories |
| **Category imbalance** | Equal selection from: politics, crypto, finance, tech, science, legal, entertainment, world |
| **Time bias** (same-time casting) | NOT using time-based casting; using text/number/measurement methods |
| **Confirmation bias** | Predictions locked before resolution; blind to outcome |
| **Cherry-picking** | All markets logged, no exclusions after selection |

## Sample Size Requirements

For statistical significance (80% power, α=0.05):

| Effect Size | Markets Needed |
|-------------|----------------|
| 5% accuracy difference | ~800 |
| 10% accuracy difference | ~200 |
| 15% accuracy difference | ~90 |
| 20% accuracy difference | ~50 |

**Publication-grade targets**:
- Pilot: 30 markets
- Phase 1: 100 markets (interim analysis)
- Phase 2: 200 markets (primary endpoint, publishable)
- Phase 3: 300 markets (90% power)

## Statistical Tests

1. **McNemar's Test**: Paired comparison (when predictions disagree, who's right?)
2. **Binomial Test**: Is accuracy better than 50% chance?
3. **Cohen's h**: Effect size for practical significance

## Expert Review Needed

Before publishing results, the experiment plan should be reviewed by:

| Expert | Review Focus |
|--------|--------------|
| **Statistician** | Sample size calculation, test selection, power analysis, bias identification |
| **I Ching Scholar / 易學專家** | Meihua methodology correctness, casting method validity |
| **Prediction Market Expert** | Market selection criteria, resolution mechanics, liquidity considerations |
| **Experimental Psychologist** | Blinding procedures, confirmation bias prevention |

### Key Questions for Review

1. Is McNemar's test appropriate for paired binary outcomes?
2. Is stratified sampling sufficient to address selection bias?
3. Are the Meihua casting methods being applied correctly?
4. Should we pre-register the hypothesis (e.g., on OSF)?
5. What null hypothesis is most appropriate?
6. How to handle markets that resolve as INVALID?

## Status

| Phase | Status | Markets |
|-------|--------|---------|
| Planning | ✅ Complete | — |
| Expert Review | ✅ Complete | — |
| OSF Pre-registration | ✅ [Complete](https://osf.io/uvntf) | — |
| Pilot | ✅ Complete | 30/30 |
| Pilot Resolution | 🔶 In progress | 10/30 resolved |
| Phase 1 | ✅ Predictions made | 70/70 |
| Phase 1 Resolution | ⏳ Awaiting outcomes | 0/70 resolved |
| Phase 2 | ⏳ Not started | 0/100 |

### Pilot Phase Interim Results (2026-01-25)

| Method | Correct | Total | Accuracy |
|--------|---------|-------|----------|
| Control | 8 | 10 | **80.0%** |
| Meihua | 4 | 10 | **40.0%** |

- **p-value:** 0.2188 (NOT significant yet)
- **Effect size (Cohen's h):** -0.845 (large, favoring Control)
- **Details:** See [Pilot Results](./data/PILOT-RESULTS.md)

### Phase 1 Summary (2026-01-25)

| Metric | Value |
|--------|-------|
| Markets | 70 |
| Casting Method | 取象起卦 (semantic-based) |
| Concordant pairs | 39 (56%) |
| Discordant pairs | 31 (44%) |

**Methodological difference:**
- **Pilot (Batch 1):** Time-based casting (舊方法 / 時間起卦)
- **Phase 1 (Batch 2):** Semantic-based casting (新方法 / 取象起卦)

The 取象起卦 method analyzes the full question context and maps concepts to trigrams based on the 八卦萬物類象 correspondences, rather than using arbitrary time-derived numbers.

### Timeline

| Date | Action |
|------|--------|
| Jan 18 | ✅ Pilot predictions made (30 markets, time-based) |
| Jan 25 | ✅ Interim review (10/30 resolved) |
| Jan 25 | ✅ Phase 1 predictions made (70 markets, 取象起卦) |
| Jan 31 | Final pilot resolutions (~25/30) |
| Feb 15+ | Phase 1 resolutions (~50/70) |
| Feb 28+ | Full analysis (100+ resolved markets) |

## Publication-Grade Features

- ✅ **SHA-256 hash verification** - Predictions hashed before resolution
- ✅ **Exact McNemar test** - For small sample sizes (n < 25 discordant)
- ✅ **Market baseline comparison** - Fairer than 50% chance
- ✅ **Stratified sampling** - Balance across categories
- ✅ **OSF pre-registration template** - Ready to submit
- ✅ **Comprehensive logging** - JSON + CSV + JSONL audit trail

## Meta-Divination Summary

Before starting, we consulted the Meihua skill:

| Question | Hexagram | Answer |
|----------|----------|--------|
| Should we run this experiment? | 觀 → 渙 | Yes, observe and share |
| Private or public first? | 乾 → 小畜 | Private first, accumulate, then share |

---

*Created: 2026-01-18*
