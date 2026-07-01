# OSF Registration Fields - Copy & Paste

Go to: **https://osf.io/registries/osf/new**

Select template: **"OSF Standard Pre-Data Collection Registration"**

---

## 1. Title

```
Empirical Validation of Meihua Yishu (梅花易數) Divination Using Prediction Markets
```

---

## 2. Description

```
This study tests whether predictions made using the traditional Chinese divination method Meihua Yishu (Plum Blossom I Ching numerology) demonstrate statistically significant predictive accuracy when applied to binary prediction market outcomes.

We compare two prediction approaches on identical prediction markets:
- Control: AI-assisted prediction using market data and reasoning only
- Meihua: AI-assisted prediction enhanced with Meihua Yishu hexagram casting and interpretation
```

---

## 3. Hypotheses

```
Primary Hypothesis (H1):
Predictions made using Meihua Yishu divination will have higher accuracy than control predictions on the same binary prediction markets.

Null Hypothesis (H0):
There is no difference in accuracy between Meihua-enhanced predictions and control predictions.

Secondary Hypotheses:
- H2: Meihua predictions with favorable 體用關係 (ti-yong relationship: 用生體, 體克用, 比和) will have higher accuracy than those with unfavorable relationships (用克體, 體生用)
- H3: Prediction accuracy will not vary significantly across market categories (politics, crypto, tech, etc.)
```

---

## 4. Study Type

```
Observational study with paired comparisons
```

---

## 5. Blinding

```
- Predictions are recorded with SHA-256 hashes before market resolution
- Hash file can be published to prove predictions were not modified post-hoc
- Control and Meihua predictions are made independently for each market
```

---

## 6. Study Design

```
- Markets are randomly selected from Polymarket using stratified sampling across categories
- Both prediction methods receive identical market information
- Meihua method additionally receives structured casting inputs (numbers, text analysis, direction mapping)
- Predictions are locked before market resolution
```

---

## 7. Randomization

```
Markets are selected using stratified random sampling:
- Categories: politics, crypto, finance, tech, science, legal, entertainment, world, other
- Equal allocation across available categories
- Python random.sample() with recorded seed for reproducibility
```

---

## 8. Existing Data

```
No existing data. All data will be collected prospectively.
```

---

## 9. Data Collection Procedures

```
1. Fetch active binary markets from Polymarket API
2. Filter by eligibility criteria:
   - Volume > $1,000 USD
   - Current probability between 15% and 85%
   - Resolution date 3-60 days in future
   - Exclude: sports, celebrities, self-referential markets
3. Stratified random selection across categories
4. For each market, generate both predictions
5. Record predictions with timestamps and hashes
6. Wait for market resolution
7. Record outcomes and calculate accuracy
```

---

## 10. Sample Size

```
Target: 200 markets (minimum)

Justification:
- Using McNemar's test for paired binary outcomes
- Assuming 30% discordant pairs (predictions disagree)
- For 80% power to detect 10% accuracy difference: n ≈ 200
- For 90% power to detect 10% difference: n ≈ 300

Phases:
- Pilot: 30 markets (methodology validation)
- Phase 1: 100 markets (interim analysis)
- Phase 2: 200 markets (primary endpoint)
- Phase 3: 300+ markets (if continuing)
```

---

## 11. Sample Size Rationale

```
Based on power analysis for McNemar's test (Connor, 1987).

Sample size formula:
n = [(z_α/2 + z_β)² × p_d] / (p_12 - p_21)²

Where:
- z_α/2 = 1.96 (two-tailed α = 0.05)
- z_β = 0.84 (power = 0.80)
- p_d = proportion of discordant pairs (estimated 0.30)
- p_12 - p_21 = expected difference in discordant proportions
```

---

## 12. Stopping Rule

```
- Futility: Stop if p > 0.50 at n = 100 (interim analysis)
- Success: Continue to n = 200 regardless of interim results
- Extension: If 0.05 < p < 0.20 at n = 200, consider extending to n = 300
```

---

## 13. Manipulated Variables

```
None (observational study)
```

---

## 14. Measured Variables

```
Primary Outcome:
- Binary correctness for each prediction (correct/incorrect)

Prediction Data:
- Market ID and title
- Initial market probability (at prediction time)
- Prediction (YES/NO)
- Confidence (0.0-1.0)
- Timestamp
- SHA-256 hash

Meihua-Specific Data:
- Hexagram number and name (本卦)
- Transformed hexagram (變卦)
- Casting method used
- 體用 relationship category
- Interpretation reasoning

Market Data:
- Volume (USD)
- Category
- Resolution date
- Actual outcome (YES/NO/INVALID)
```

---

## 15. Indices

```
None
```

---

## 16. Statistical Models

```
Primary Analysis: McNemar's Exact Test
- Tests whether discordant pairs favor one method
- Uses exact binomial distribution for n < 25 discordant pairs
- Uses chi-square approximation for n ≥ 25

Secondary Analyses:
1. Binomial test: Each method vs. 50% chance
2. Binomial test: Each method vs. market probability baseline
3. Cohen's h effect size for the difference in proportions
4. Subgroup analysis by 體用 relationship category
5. Subgroup analysis by market category
```

---

## 17. Transformations

```
None
```

---

## 18. Inference Criteria

```
- Primary: Two-tailed α = 0.05
- Secondary analyses: Bonferroni-corrected α = 0.05/k (k = number of tests)
```

---

## 19. Data Exclusion

```
Exclude markets where:
- Market was voided/cancelled (INVALID outcome)
- Resolution was disputed or ambiguous
- Prediction was not recorded before resolution (hash verification failed)

Document all exclusions with reasons.
```

---

## 20. Missing Data

```
- If either prediction is missing for a market, exclude from paired analysis
- Report number of markets with complete vs. incomplete data
```

---

## 21. Exploratory Analyses

```
- Accuracy by casting method (number-based, text-based, direction-based, measurement-based)
- Correlation between confidence and accuracy
- Time-series analysis of cumulative accuracy
- Calibration analysis (Brier score)
```

---

## 22. Other

```
Hash Verification Protocol:
1. Each prediction generates SHA-256 hash at recording time
2. Hash = SHA256(market_id | prediction_type | prediction | confidence | timestamp)
3. Hashes stored in separate file that can be published before resolution
4. Any prediction with mismatched hash is excluded from analysis

Reproducibility:
- All code available in repository
- Random seeds recorded for market selection
- Full data logged in JSON and CSV formats

References:
- Connor, R.J. (1987). Sample size for testing differences in proportions for the paired-sample design. Biometrics, 43(1), 207-211.
- Shao, Y. (邵雍). Meihua Yishu (梅花易數). Song Dynasty.
```

---

## After Submitting

Update these in OSF-PREREGISTRATION.md:
- **Registration Date**: [fill in]
- **Registration DOI**: [fill in after registration]

Update README.md status:
- OSF Pre-registration: ✅ Complete
