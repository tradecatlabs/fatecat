# Experiment Scripts

## Setup

```bash
cd experiments/prediction-validation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Scripts

| Script | Purpose |
|--------|---------|
| `polymarket_client.py` | API client for Polymarket (read-only, no auth needed) |
| `market_selector.py` | Randomly selects markets with stratified sampling |
| `experiment_logger.py` | Audit logging to JSON/CSV |
| `experiment_runner.py` | Orchestrates the experiment workflow |
| `stats_analyzer.py` | Statistical significance testing |

## Workflow

### 1. Select Markets
```bash
python experiment_runner.py select 10
```
- Fetches eligible markets from Polymarket
- Stratifies by category (politics, crypto, finance, etc.)
- Saves to `data/experiment_state.json`
- Generates prompts in `data/prompts/batch_XXX/`

### 2. Run Predictions in Claude Code

For each market, run two predictions:

**Control** (no Meihua):
```
[Read prompts/batch_XXX/NN_XXX_control.txt]
[Paste to Claude Code]
[Get prediction: YES/NO + confidence]
```

**Meihua** (with skill):
```
[Read prompts/batch_XXX/NN_XXX_meihua.txt]
[Paste to Claude Code with Meihua skill enabled]
[Get hexagram + prediction]
```

### 3. Record Predictions

```python
from experiment_runner import ExperimentRunner
runner = ExperimentRunner()

# Record control prediction
runner.record_control_prediction(
    market_id="abc123",
    prediction="YES",
    confidence=0.65,
    reasoning="Based on 60% probability..."
)

# Record meihua prediction
runner.record_meihua_prediction(
    market_id="abc123",
    prediction="NO",
    confidence=0.70,
    reasoning="雷水解 體生用...",
    hexagram_number=40,
    hexagram_name="雷水解",
    transformed_hexagram=16,
    casting_method="text_based",
    ti_yong_analysis="體生用 - favorable"
)
```

### 4. Check Resolutions
```bash
python experiment_runner.py check
```

### 5. Analyze Results
```bash
python stats_analyzer.py
```

## Data Files

| File | Format | Purpose |
|------|--------|---------|
| `data/experiment_state.json` | JSON | Current state (markets, predictions) |
| `data/experiment_log.jsonl` | JSONL | Append-only audit log |
| `data/results.csv` | CSV | Flat file for statistical analysis |
| `data/prompts/` | TXT | Saved prompts by batch |

## Sample Size Guide

Run `python stats_analyzer.py` to see:

```
To detect different effect sizes (80% power, α=0.05):

  5% accuracy difference:  ~800 markets
  10% accuracy difference: ~200 markets
  15% accuracy difference: ~90 markets
  20% accuracy difference: ~50 markets

Recommended:
  Minimum pilot:  50 markets
  Recommended:    100 markets
  Ideal:          200 markets
```
