#!/usr/bin/env python3
"""
Update Phase 1 Meihua predictions with authentic 取象起卦 predictions.
Replaces the script-generated predictions with ones from Sonnet agents.
"""

import json
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")

# Load authentic predictions
with open(os.path.join(data_dir, "phase1_meihua_predictions.json")) as f:
    authentic = json.load(f)

# Load experiment state
state_file = os.path.join(data_dir, "experiment_state.json")
with open(state_file) as f:
    state = json.load(f)

# Get batch 2 market IDs (Phase 1)
batch2_markets = [
    mid for mid, m in state["markets"].items()
    if m.get("selection_batch") == 2
]

print(f"Found {len(batch2_markets)} Phase 1 markets to update")
print(f"Have {len(authentic['predictions'])} authentic predictions")

# Map predictions by index (they should align)
if len(batch2_markets) != len(authentic["predictions"]):
    print(f"WARNING: Market count mismatch!")

# Sort batch2 markets by record_id to ensure correct order
batch2_sorted = sorted(batch2_markets, key=lambda mid: state["markets"][mid]["record_id"])

# Update each prediction
updated = 0
for i, market_id in enumerate(batch2_sorted):
    if i >= len(authentic["predictions"]):
        break

    pred = authentic["predictions"][i]
    market = state["markets"][market_id]

    # Update Meihua prediction
    old_pred = market.get("meihua_prediction", {})

    # Parse hexagram info
    hex_parts = pred["hexagram"].split()
    hex_num = int(hex_parts[0]) if hex_parts else 0
    hex_name = hex_parts[1] if len(hex_parts) > 1 else ""

    trans_parts = pred["transformed"].split()
    trans_num = int(trans_parts[0]) if trans_parts else 0

    # Create new prediction with hash
    import hashlib
    now = datetime.now().isoformat()
    pred_data = f"{pred['prediction']}|{pred['confidence']}|{pred.get('hexagram', '')}|{now}"
    pred_hash = hashlib.sha256(pred_data.encode()).hexdigest()

    new_meihua = {
        "prediction": pred["prediction"],
        "confidence": pred["confidence"],
        "reasoning": f"{pred['hexagram']}卦，變{pred['transformed']}。取象起卦分析。",
        "timestamp": now,
        "hash": pred_hash,
        "hexagram_number": hex_num,
        "hexagram_name": hex_name,
        "transformed_hexagram": trans_num,
        "casting_method": "取象起卦",
        "ti_yong_analysis": "Semantic-based casting using full skill analysis"
    }

    market["meihua_prediction"] = new_meihua
    market["last_updated"] = now

    print(f"  {i+1}. {pred['title'][:40]}... → {pred['prediction']} ({pred['confidence']:.0%})")
    updated += 1

# Save updated state
with open(state_file, 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"\n✅ Updated {updated} Meihua predictions with authentic 取象起卦 results")
print(f"State saved to: {state_file}")

# Count prediction distribution
yes_count = sum(1 for p in authentic["predictions"] if p["prediction"] == "YES")
no_count = sum(1 for p in authentic["predictions"] if p["prediction"] == "NO")
print(f"\nPrediction distribution: YES={yes_count}, NO={no_count}")
