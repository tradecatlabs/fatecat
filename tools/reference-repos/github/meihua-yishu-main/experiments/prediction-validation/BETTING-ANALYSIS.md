# Betting Profitability Analysis

**Date**: February 24, 2026
**Question**: Would following the control or Meihua predictions have been profitable on Polymarket?

---

## Key Insight: Accuracy ≠ Profitability

Prediction markets price in consensus. Being "right" doesn't mean you make money. If the market says 80% YES and you bet YES and win, you only gain $0.20 per $1 risked. But if you're wrong, you lose $0.80. You need >80% accuracy just to break even on that bet.

---

## Strategy Comparison (betting $1 per market, 79 resolved)

| Strategy | Wins | Win% | Total P&L | ROI | Sharpe |
|----------|------|------|-----------|-----|--------|
| Anti-Meihua (Contrarian) | 39 | 49.4% | **+$2.40** | **+3.0%** | +0.074 |
| Market Consensus (>50%) | 58 | 73.4% | +$1.44 | +1.8% | +0.045 |
| Always NO | 47 | 59.5% | +$0.88 | +1.1% | +0.027 |
| **Control Agent** | 57 | 72.2% | **+$0.48** | **+0.6%** | +0.015 |
| Always YES | 32 | 40.5% | -$0.88 | -1.1% | -0.027 |
| **Meihua Agent** | 40 | 50.6% | **-$2.40** | **-3.0%** | -0.074 |

---

## Disagreement Markets (37 cases where Control and Meihua diverged)

| Strategy | Wins | Win% | P&L | ROI |
|----------|------|------|-----|-----|
| Bet with Control | 27 | 73.0% | +$1.44 | +3.9% |
| Bet with Meihua | 10 | 27.0% | -$1.44 | -3.9% |

---

## Profitability by Market Probability Bucket

| Bucket | N | Control ROI | Meihua ROI |
|--------|---|------------|------------|
| Low (15-30%) | 35 | +10.0% | -0.3% |
| Below-mid (30-50%) | 17 | -19.4% | +2.3% |
| Above-mid (50-70%) | 15 | -8.1% | -12.5% |
| High (70-85%) | 12 | +12.4% | -6.7% |

---

## Edge Analysis

| Agent | Bet Type | Avg Market Prob | Actual Win Rate | Edge |
|-------|----------|----------------|-----------------|------|
| Control | YES bets | 0.686 | 0.679 | -0.7% |
| Control | NO bets | 0.732 | 0.745 | +1.3% |
| Meihua | YES bets | 0.440 | 0.387 | -5.3% |
| Meihua | NO bets | 0.599 | 0.583 | -1.6% |

Control had near-zero edge. Meihua had negative edge on both sides.

---

## Conclusions

1. **Control barely profitable (+$0.48)** — because it just followed market consensus with no real edge
2. **Meihua was the worst strategy (-$2.40)** — worse than always YES, worse than coin flip
3. **Anti-Meihua was the best strategy (+$2.40)** — but only +3.0% ROI, which transaction fees would erase
4. **No strategy generates meaningful alpha** — the market is well-calibrated
5. **Meihua's contrarian bets (against market) won only 23.5% of the time** — systematically wrong when disagreeing with consensus

**Bottom line**: Neither prediction system would make you money. The market is efficient enough that following consensus barely breaks even, and Meihua's contrarian tendencies are consistently money-losing.
