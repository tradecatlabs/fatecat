# Meihua Yishu Prediction Validation Experiment

## Experiment Overview

**Goal**: Empirically test whether 梅花易數 (Meihua Yishu) divination provides statistically significant predictive value compared to random chance.

**Platform**: Polymarket (prediction markets with clear binary outcomes)

**Approach**: Two Claude Code agents — one uses the Meihua skill, one does not — both predict the same markets.

---

## Experiment Design

### Two-Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MARKET SELECTOR                              │
│  (Automated: randomly selects eligible markets from Polymarket)  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│      AGENT A (Control)   │     │   AGENT B (Experiment)   │
│  - NO skill access       │     │   - HAS Meihua skill     │
│  - Same market info      │     │   - Same market info     │
│  - Makes prediction      │     │   - Casts hexagram       │
│    based on reasoning    │     │   - Makes prediction     │
└───────────┬─────────────┘     └───────────┬─────────────┘
            │                               │
            ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        RECORDER                                  │
│  - Logs both predictions with timestamps                         │
│  - Records hexagram details (experiment only)                    │
│  - Tracks market resolution                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Why Two Agents (Not Random Coin Flip)?

| Control Type | Problem |
|--------------|---------|
| Coin flip (50/50) | Too naive — doesn't account for market information |
| Market consensus | Just following the crowd — not a fair comparison |
| **LLM without skill** | Fair comparison — same intelligence, same info, different method |

The control agent can use reasoning, market data, news — everything EXCEPT the Meihua skill. This isolates the variable we're testing.

---

## Statistical Requirements

### Sample Size Calculation

Using power analysis for comparing two proportions:

| Effect Size | Required N (per group) | Total Markets | Detectable Difference |
|-------------|------------------------|---------------|----------------------|
| Small (h=0.2) | 393 | ~400 | 50% vs 55% |
| Medium (h=0.5) | 64 | ~65 | 50% vs 62% |
| Large (h=0.8) | 26 | ~30 | 50% vs 70% |

**Recommendation** (updated for publication-grade):
- **Pilot**: 30 markets (methodology validation)
- **Phase 1**: 100 markets (interim analysis)
- **Minimum for publication**: 200 markets (detect ~10% difference)
- **Ideal**: 300 markets (90% power)

### Statistical Tests

1. **Primary**: McNemar's test (paired comparison — same markets, different predictions)
2. **Secondary**: Chi-square test for independence
3. **Effect size**: Cohen's h
4. **Confidence interval**: 95% CI for accuracy difference

### Success Criteria

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| p-value | < 0.05 | Statistically significant |
| Effect size (h) | > 0.2 | Practically meaningful |
| Experiment accuracy | > Control + 5% | Minimum useful edge |

---

## Casting Methods to Test

**Important**: Do NOT use time-based casting (same time = same hexagram for all markets)

### Methods to Use

| Method | Description | Input Source |
|--------|-------------|--------------|
| **Number-based (數字起卦)** | Use market metrics | Volume digits, trader count, probability % |
| **Text-based (測字起卦)** | Use market title | Character/word count, stroke count |
| **Direction-based (方位起卦)** | Map category to direction | Category → 八卦方位 |
| **Color-based (顏色起卦)** | Derive from context | Market sentiment → color → element |
| **Measurement-based (尺寸起卦)** | Use market numbers | Days until resolution, price levels |

### Casting Input Derivation

For each market, derive casting inputs from market data:

```
Market: "Will Bitcoin reach $100k?"
│
├── Number-based:
│   ├── Upper: Volume last 2 digits (e.g., 125000 → 50 mod 8 = 2)
│   ├── Lower: Trader count (e.g., 340 mod 8 = 4)
│   └── Line: (Volume + Traders) mod 6
│
├── Text-based:
│   ├── Upper: Word count (7 words mod 8 = 7)
│   ├── Lower: Character count (25 chars mod 8 = 1)
│   └── Line: (7 + 25) mod 6 = 2
│
├── Direction-based:
│   └── Category "Crypto" → 西北 → 乾卦
│
└── Measurement-based:
    ├── Upper: Days until resolution (14 mod 8 = 6)
    └── Lower: Current probability % (45 mod 8 = 5)
```

### Multiple Methods Per Market

Each market gets predictions from ALL applicable methods:

```
Market X:
├── Number-based prediction: YES (用生體)
├── Text-based prediction: NO (用克體)
├── Direction-based prediction: YES (體克用)
├── Measurement-based prediction: YES (比和)
└── Ensemble: YES (3/4 majority)
```

This allows us to:
1. Compare which method performs best
2. Test if ensemble improves accuracy
3. Identify if certain methods suit certain categories

---

## Information to Provide

### To BOTH Agents (Same Core Input)

| Field | Description | Example |
|-------|-------------|---------|
| market_id | Polymarket market ID | "0x123..." |
| title | Market question | "Will X happen by Y date?" |
| description | Full market description | Detailed rules |
| current_prob | Current YES probability | 0.65 |
| volume | Total volume traded | $50,000 |
| trader_count | Number of traders | 340 |
| end_date | Resolution date | 2026-02-15 |
| category | Market category | "Politics", "Crypto", etc. |
| created_at | When market was created | 2026-01-01 |
| price_history | Recent price movement | [0.60, 0.62, 0.65] |
| related_markets | Similar active markets | [...] |

### Additional Context for BOTH Agents

| Field | Description | Use |
|-------|-------------|-----|
| days_until_resolution | Calculated from end_date | Timing analysis |
| market_sentiment | Rising/falling/stable | Trend direction |
| related_news | Recent headlines | Current events |
| market_liquidity | Depth of order book | Market quality |

### Additional for Experiment Agent (Meihua-Specific)

The experiment agent receives MAXIMUM context to leverage the skill fully:

#### Casting Inputs (Derived from Market Data)

| Input Type | Source | Calculation |
|------------|--------|-------------|
| 數字 (Numbers) | Volume, traders, probability | Last N digits |
| 文字 (Text) | Market title | Word/char count |
| 方位 (Direction) | Category mapping | Category → 八卦 |
| 尺寸 (Measurement) | Days, price levels | Direct numbers |
| 顏色 (Color) | Sentiment | Trend → color → element |

#### Interpretation Context (外應 / 十應)

| Context Type | Description | Skill Reference |
|--------------|-------------|-----------------|
| **天時** | Season, weather, time of day | shiying-guide.md |
| **地理** | Market origin/region | shiying-guide.md |
| **人事** | Key players, institutions | shiying-guide.md |
| **物象** | Related symbols/objects | wanwu-fu.md |
| **聲應** | Related sounds/announcements | shiying-guide.md |
| **色應** | Visual trends (green/red) | bagua-symbols.md |

#### Category-Specific Interpretation (十八類分占)

| Market Category | 分占類型 | Reference |
|-----------------|----------|-----------|
| Politics/Election | 求官 | 18-divinations.md |
| Finance/Crypto | 求財 | 18-divinations.md |
| Legal/Court | 訴訟 | 18-divinations.md |
| Health/Medical | 疾病 | 18-divinations.md |
| Travel/Transport | 出行 | 18-divinations.md |
| Weather | 天時 | 18-divinations.md |
| Business/Merger | 交易 | 18-divinations.md |

### Rich Context Example

```json
{
  "market_id": "0x123",
  "title": "Will SEC approve Bitcoin ETF by March 2026?",
  "description": "Resolves YES if SEC officially approves...",
  "category": "Crypto",

  "core_data": {
    "current_prob": 0.72,
    "volume": 2500000,
    "trader_count": 1850,
    "days_until_resolution": 45
  },

  "context": {
    "sentiment": "bullish",
    "trend": "rising",
    "recent_news": ["SEC chair comments positive...", "..."],
    "key_players": ["SEC", "BlackRock", "Grayscale"]
  },

  "meihua_inputs": {
    "casting_methods": {
      "number": {"upper": 250 % 8, "lower": 185 % 8},
      "text": {"upper": 9, "lower": 42 % 8},
      "direction": "西北 → 乾",
      "measurement": {"days": 45 % 8, "prob": 72 % 8}
    },
    "interpretation_context": {
      "category_type": "求財",
      "seasonal_element": "水 (冬)",
      "directional_element": "金 (西北)",
      "sentiment_color": "紅 (火)"
    }
  }
}
```

This rich context allows the Meihua skill to:
1. Cast hexagrams using multiple methods
2. Apply 外應 (environmental signs)
3. Use 十應 (ten responses) for nuanced interpretation
4. Apply category-specific 分占 rules

---

## Data to Record

### Per Prediction Record

```json
{
  "record_id": "uuid",
  "market_id": "polymarket_id",
  "market_title": "Will X happen?",
  "market_description": "Full description...",
  "market_end_date": "2026-02-15T00:00:00Z",
  "market_category": "Politics",
  "current_probability": 0.65,
  "volume_usd": 50000,

  "prediction_timestamp": "2026-01-18T06:00:00Z",

  "control_agent": {
    "prediction": "YES",
    "confidence": 0.7,
    "reasoning": "Based on polling data..."
  },

  "experiment_agent": {
    "prediction": "NO",
    "confidence": 0.8,
    "reasoning": "Hexagram indicates unfavorable...",
    "hexagram": {
      "casting_method": "time",
      "casting_timestamp": "2026-01-18T06:00:00Z",
      "lunar_date": "丙午年十二月十九日",
      "hour_branch": "卯時",
      "primary_hexagram": {
        "number": 20,
        "name": "風地觀",
        "upper": "巽",
        "lower": "坤",
        "changing_line": 2
      },
      "mutual_hexagram": {
        "number": 23,
        "name": "山地剝"
      },
      "transformed_hexagram": {
        "number": 59,
        "name": "風水渙"
      },
      "ti_trigram": "巽 (木)",
      "yong_trigram": "坤 (土)",
      "relationship": "體克用",
      "relationship_interpretation": "吉"
    }
  },

  "resolution": {
    "resolved_at": null,
    "outcome": null,
    "control_correct": null,
    "experiment_correct": null
  }
}
```

### Aggregated Metrics to Track

| Metric | Description |
|--------|-------------|
| total_predictions | Total markets predicted |
| resolved_predictions | Markets with known outcomes |
| control_accuracy | Control correct / resolved |
| experiment_accuracy | Experiment correct / resolved |
| agreement_rate | How often both agents agree |
| accuracy_when_agree | Accuracy when both predict same |
| accuracy_when_disagree | Accuracy when predictions differ |

### By Casting Method

| Method | N | Accuracy | vs Control |
|--------|---|----------|------------|
| Number-based | ? | ? | ? |
| Text-based | ? | ? | ? |
| Direction-based | ? | ? | ? |
| Measurement-based | ? | ? | ? |

*Note: NOT using time-based casting (same time = same hexagram for all markets)*

### By Relationship Type

| 體用關係 | N | Accuracy | Expected |
|----------|---|----------|----------|
| 用生體 (大吉) | 30 | ? | Highest |
| 體克用 (吉) | 25 | ? | High |
| 比和 (吉) | 20 | ? | High |
| 用克體 (凶) | 15 | ? | Low |
| 體生用 (洩) | 10 | ? | Low |

---

## Market Selection Criteria

### Inclusion Criteria

| Criterion | Requirement |
|-----------|-------------|
| Outcome type | Binary (YES/NO) |
| Resolution | Objective, verifiable |
| Timeframe | 3-30 days until resolution |
| Liquidity | > $1,000 volume |
| Probability | 20% < prob < 80% (not too obvious) |

### Exclusion Criteria

| Criterion | Reason |
|-----------|--------|
| Sports betting | Too many variables, user preference |
| Celebrity gossip | Subjective resolution |
| Self-referential | "Will this market reach X?" |
| Very low volume | Manipulation risk |
| Already resolved | Obvious |

### Selection Process

```python
1. Fetch all active markets from Polymarket API
2. Filter by inclusion criteria
3. Exclude by exclusion criteria
4. Randomly sample N markets (no human selection!)
5. Verify each market is truly binary
```

---

## Timeline Strategy

### Resolution Timeframe Trade-offs

| Timeframe | Pros | Cons |
|-----------|------|------|
| 1-7 days | Fast results, more iterations | Less significant events |
| 7-30 days | Balanced | Medium wait |
| 30+ days | Major events | Too slow for iteration |

**Strategy**: Mixed portfolio
- 50% short-term (7 days)
- 40% medium-term (7-30 days)
- 10% long-term (30+ days)

### Experiment Phases

| Phase | Duration | Goal |
|-------|----------|------|
| **Pilot** | 1-2 weeks | Test methodology, 30 markets |
| **Phase 1** | 4 weeks | 100 markets, interim analysis |
| **Phase 2** | 8 weeks | 200 markets, primary endpoint (publishable) |
| **Phase 3** | 12 weeks | 300 markets, 90% power (optional extension) |

---

## Polymarket API Integration

### API Capabilities Needed

| Capability | Endpoint | Notes |
|------------|----------|-------|
| List markets | GET /markets | Filter by active, binary |
| Market details | GET /markets/{id} | Full description |
| Current prices | GET /prices | Real-time probability |
| Historical data | GET /markets/{id}/history | Price movement |
| Place bet (optional) | POST /orders | Requires wallet |

### API Documentation
- Polymarket API: https://docs.polymarket.com/
- CLOB API: https://docs.polymarket.com/#clob-api

### Authentication
- API key required for trading
- Read-only access for market data (no key needed)

---

## Betting Strategy (If Actually Betting)

### Paper Trading vs Real Money

| Approach | Pros | Cons |
|----------|------|------|
| Paper trading | No financial risk | Less "real" |
| Real money | Skin in the game | Financial risk |

**Recommendation**: Start with paper trading, then small real bets for validation.

### Bet Sizing (If Real)

| Rule | Amount |
|------|--------|
| Per bet | Fixed $10 |
| Daily limit | $50 |
| Total bankroll | $500 |
| Stop loss | Stop if down 50% |

### Kelly Criterion (Optional)

If hexagram provides edge, optimal bet size:
```
f* = (bp - q) / b
where:
  b = odds received (decimal - 1)
  p = probability of winning
  q = probability of losing (1 - p)
```

---

## Potential Confounds to Control

### Bias Sources

| Bias | Mitigation |
|------|------------|
| **Selection bias** | Random market selection |
| **Timing bias** | Fixed casting time per market |
| **Interpretation bias** | Deterministic rules, no human judgment |
| **Reporting bias** | Log ALL predictions, even losses |
| **Survivorship bias** | Track voided/cancelled markets too |
| **Hindsight bias** | Predictions logged BEFORE resolution |

### Additional Controls

1. **Blinding**: Control agent doesn't know experiment agent's prediction
2. **Pre-registration**: Publish methodology before seeing results
3. **Third-party verification**: Hash predictions to blockchain (optional)

---

## Edge Cases

### Market Issues

| Issue | Handling |
|-------|----------|
| Market voided | Exclude from analysis |
| Resolution delayed | Wait, include when resolved |
| Ambiguous resolution | Exclude, document reason |
| Market manipulation | Flag for review |

### Hexagram Edge Cases

| Issue | Handling |
|-------|----------|
| Multiple changing lines | Use traditional priority rules |
| 乾/坤 special mutual | Apply special rules |
| Tie in methods | Use text-based as primary, number-based as tiebreaker |

---

## Deliverables

### During Experiment

| Item | Frequency |
|------|-----------|
| Prediction log | Real-time |
| Progress dashboard | Weekly |
| Interim analysis | At 100, 200 markets |

### Final Report

1. **Methodology** — Full documentation
2. **Results** — Raw data, statistics
3. **Analysis** — What worked, what didn't
4. **Conclusions** — Does Meihua have predictive value?
5. **Recommendations** — Future experiments

---

## Open Questions (Resolved)

### Decisions Made

1. **Casting frequency**: ✅ Cast once per market using text-based as primary
2. **Ensemble method**: ✅ Single method per prediction (not ensemble)
3. **Confidence weighting**: ✅ Track but don't weight in primary analysis
4. **Time of casting**: ✅ NOT using time-based (would give same hexagram for all)
5. **Lunar calendar**: ✅ N/A - not using time-based casting

### Research Questions

1. Does any casting method outperform others?
2. Do certain 體用關係 predict accuracy better?
3. Does accuracy vary by market category?
4. Is there a "confidence calibration" — high confidence = higher accuracy?

---

## Next Steps

1. [ ] Set up Polymarket API access
2. [ ] Create market selector script
3. [ ] Create control agent prompt
4. [ ] Create experiment agent prompt (with skill)
5. [ ] Create recorder/logger
6. [ ] Run pilot (20 markets)
7. [ ] Analyze pilot, adjust methodology
8. [ ] Run full experiment

---

## Meta Divination Reference

Before starting, we consulted the Meihua skill itself about this experiment:

**Hexagram**: 乾為天 → 風天小畜
**Interpretation**: Proceed independently first, accumulate small results, then share publicly.

See [DIVINATION.md](./DIVINATION.md) for full details.

---

---

## Results (Added 2026-02-24)

### Phase 1 Complete: 79/100 Markets Resolved

| Metric | Control | Meihua | Market Consensus |
|--------|---------|--------|-----------------|
| Accuracy | 57/79 (72.2%) | 40/79 (50.6%) | 58/79 (73.4%) |
| ROI (betting $1/market) | +0.6% | -3.0% | +1.8% |
| Agreement with market | 96.2% | 57.0% | 100% |

### Key Findings

1. **Meihua = coin flip**: 50.6% accuracy, all permutation tests p > 0.60
2. **Control = market follower**: 96.2% agreement with consensus, no real skill
3. **Same hexagram → different outcomes**: Identical hexagram+line combos produced opposite results
4. **More analysis = worse**: Full 互卦+變卦+通關 reinterpretation scored 48.1% (worse)
5. **Neither strategy is profitable**: Transaction costs would erase any gains
6. **Anti-Meihua was best strategy**: Betting against Meihua yielded +3.0% ROI

### Detailed Reports

- `FINAL-REPORT.md` — Full statistical analysis and qualitative hexagram assessment
- `BETTING-ANALYSIS.md` — Profitability analysis of all strategies
- `QUALITATIVE-EXPERIMENT-PLAN.md` — Next experiment design (qualitative match test)

### Status: Moving to Qualitative Experiment

Binary prediction is the wrong use case for hexagrams. The next experiment tests qualitative situational description (what the system was actually designed for) using a blinded paired comparison with random control hexagrams.

---

*Document Version: 1.1*
*Created: 2026-01-18*
*Updated: 2026-02-24*
*Status: Phase 1 Complete, Phase 2 (Qualitative) Planned*
