#!/usr/bin/env python3
"""
Experiment Logger

Comprehensive audit logging for the Meihua prediction experiment.
Uses JSON for easy AI reading + CSV export for statistical analysis.

Data Schema designed for:
- Full audit trail (every action logged)
- Statistical significance testing
- Reproducibility
"""

import json
import csv
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
from enum import Enum


class PredictionType(str, Enum):
    CONTROL = "control"      # Pure probability-based
    MEIHUA = "meihua"        # Meihua Yishu enhanced


class OutcomeType(str, Enum):
    YES = "YES"
    NO = "NO"
    PENDING = "PENDING"
    INVALID = "INVALID"      # Market cancelled/voided


@dataclass
class Prediction:
    """A single prediction record."""
    prediction_id: str
    prediction_type: str           # "control" or "meihua"
    prediction: str                # "YES" or "NO"
    confidence: float              # 0.0 to 1.0
    reasoning: str                 # Full reasoning text
    timestamp: str

    # For Meihua predictions
    hexagram_number: Optional[int] = None
    hexagram_name: Optional[str] = None
    transformed_hexagram: Optional[int] = None
    casting_method: Optional[str] = None
    ti_yong_analysis: Optional[str] = None


@dataclass
class MarketRecord:
    """Complete record for a single market in the experiment."""
    # Identifiers
    record_id: str
    market_id: str
    condition_id: Optional[str]

    # Selection metadata
    selection_timestamp: str
    selection_batch: int           # Which batch this market was in

    # Market data at selection time (snapshot)
    title: str
    description: str
    url: str
    categories: List[str]
    initial_probability: float
    volume_usd: float
    liquidity_usd: float
    expected_resolution_date: str
    days_until_resolution: int

    # Meihua casting inputs (for reproducibility)
    meihua_inputs: Dict[str, Any]

    # Predictions
    control_prediction: Optional[Dict[str, Any]] = None
    meihua_prediction: Optional[Dict[str, Any]] = None

    # Outcome
    actual_outcome: str = "PENDING"  # YES, NO, PENDING, INVALID
    resolution_timestamp: Optional[str] = None
    final_probability: Optional[float] = None

    # Scoring
    control_correct: Optional[bool] = None
    meihua_correct: Optional[bool] = None

    # Audit
    last_updated: str = ""
    notes: List[str] = field(default_factory=list)


def generate_prediction_hash(
    market_id: str,
    prediction_type: str,
    prediction: str,
    confidence: float,
    timestamp: str
) -> str:
    """
    Generate SHA-256 hash of a prediction for verification.

    This hash can be published BEFORE market resolution to prove
    the prediction wasn't changed after seeing the outcome.
    """
    # Create deterministic string representation
    data = f"{market_id}|{prediction_type}|{prediction}|{confidence:.4f}|{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()


def verify_prediction_hash(
    market_id: str,
    prediction_type: str,
    prediction: str,
    confidence: float,
    timestamp: str,
    expected_hash: str
) -> bool:
    """Verify a prediction hash matches the data."""
    actual_hash = generate_prediction_hash(
        market_id, prediction_type, prediction, confidence, timestamp
    )
    return actual_hash == expected_hash


class ExperimentLogger:
    """
    Manages experiment data with full audit trail.

    Data files:
    - experiment_state.json: Current state of all markets
    - experiment_log.jsonl: Append-only event log
    - results.csv: Flat file for statistical analysis
    - prediction_hashes.json: SHA-256 hashes for verification
    """

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, "..", "data")

        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

        self.state_file = os.path.join(data_dir, "experiment_state.json")
        self.log_file = os.path.join(data_dir, "experiment_log.jsonl")
        self.csv_file = os.path.join(data_dir, "results.csv")
        self.hash_file = os.path.join(data_dir, "prediction_hashes.json")

        # Load or initialize state
        self.state = self._load_state()
        self.hashes = self._load_hashes()

    def _load_hashes(self) -> Dict[str, Any]:
        """Load prediction hashes from file."""
        if os.path.exists(self.hash_file):
            with open(self.hash_file, "r") as f:
                return json.load(f)
        return {"hashes": [], "created": datetime.now().isoformat()}

    def _save_hashes(self):
        """Save prediction hashes to file."""
        with open(self.hash_file, "w") as f:
            json.dump(self.hashes, f, indent=2)

    def _load_state(self) -> Dict[str, Any]:
        """Load experiment state from file."""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)

        return {
            "experiment_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "created": datetime.now().isoformat(),
            "config": {
                "min_volume": 1000,
                "min_probability": 0.15,
                "max_probability": 0.85,
                "min_days": 3,
                "max_days": 60,
            },
            "statistics": {
                "total_markets": 0,
                "pending": 0,
                "resolved": 0,
                "control_correct": 0,
                "meihua_correct": 0,
                "batches": 0,
            },
            "markets": {},  # market_id -> MarketRecord
        }

    def _save_state(self):
        """Save experiment state to file."""
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def _append_log(self, event: Dict[str, Any]):
        """Append event to audit log (JSONL format)."""
        event["timestamp"] = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def add_market(self, market_data: Dict[str, Any], batch: int) -> str:
        """
        Add a new market to the experiment.

        Args:
            market_data: Formatted market data from polymarket_client
            batch: Batch number for this selection

        Returns:
            record_id
        """
        now = datetime.now().isoformat()
        record_id = f"{batch:03d}_{market_data['market_id'][:8]}"

        record = {
            "record_id": record_id,
            "market_id": market_data["market_id"],
            "condition_id": market_data.get("condition_id"),
            "selection_timestamp": now,
            "selection_batch": batch,
            "title": market_data["title"],
            "description": market_data.get("description", ""),
            "url": market_data.get("url", ""),
            "categories": market_data["context"]["categories"],
            "initial_probability": market_data["core_data"]["current_prob"],
            "volume_usd": market_data["core_data"]["volume_usd"],
            "liquidity_usd": market_data["core_data"]["liquidity"],
            "expected_resolution_date": market_data["core_data"]["end_date"],
            "days_until_resolution": market_data["core_data"]["days_until_resolution"],
            "meihua_inputs": market_data["meihua_inputs"],
            "control_prediction": None,
            "meihua_prediction": None,
            "actual_outcome": "PENDING",
            "resolution_timestamp": None,
            "final_probability": None,
            "control_correct": None,
            "meihua_correct": None,
            "last_updated": now,
            "notes": [],
        }

        self.state["markets"][market_data["market_id"]] = record
        self.state["statistics"]["total_markets"] += 1
        self.state["statistics"]["pending"] += 1
        self.state["statistics"]["batches"] = max(self.state["statistics"]["batches"], batch)

        self._append_log({
            "event": "market_added",
            "record_id": record_id,
            "market_id": market_data["market_id"],
            "title": market_data["title"],
            "batch": batch,
        })

        self._save_state()
        return record_id

    def record_prediction(
        self,
        market_id: str,
        prediction_type: str,  # "control" or "meihua"
        prediction: str,       # "YES" or "NO"
        confidence: float,
        reasoning: str,
        hexagram_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record a prediction for a market.

        Args:
            market_id: The market ID
            prediction_type: "control" or "meihua"
            prediction: "YES" or "NO"
            confidence: 0.0 to 1.0
            reasoning: Full reasoning text
            hexagram_info: For meihua predictions, hexagram details

        Returns:
            SHA-256 hash of the prediction (for verification)
        """
        if market_id not in self.state["markets"]:
            raise ValueError(f"Market {market_id} not found in experiment")

        now = datetime.now().isoformat()

        # Generate verification hash
        pred_hash = generate_prediction_hash(
            market_id, prediction_type, prediction, confidence, now
        )

        pred_record = {
            "prediction": prediction,
            "confidence": confidence,
            "reasoning": reasoning,
            "timestamp": now,
            "hash": pred_hash,  # Store hash with prediction
        }

        if hexagram_info:
            pred_record.update({
                "hexagram_number": hexagram_info.get("hexagram_number"),
                "hexagram_name": hexagram_info.get("hexagram_name"),
                "transformed_hexagram": hexagram_info.get("transformed_hexagram"),
                "casting_method": hexagram_info.get("casting_method"),
                "ti_yong_analysis": hexagram_info.get("ti_yong_analysis"),
            })

        field_name = f"{prediction_type}_prediction"
        self.state["markets"][market_id][field_name] = pred_record
        self.state["markets"][market_id]["last_updated"] = now

        # Save hash to separate file (can be published for verification)
        self.hashes["hashes"].append({
            "market_id": market_id,
            "prediction_type": prediction_type,
            "hash": pred_hash,
            "timestamp": now,
        })
        self._save_hashes()

        self._append_log({
            "event": "prediction_recorded",
            "market_id": market_id,
            "prediction_type": prediction_type,
            "prediction": prediction,
            "confidence": confidence,
            "hash": pred_hash,
        })

        self._save_state()

        print(f"📋 Prediction hash: {pred_hash[:16]}...")
        return pred_hash

    def record_outcome(
        self,
        market_id: str,
        outcome: str,  # "YES", "NO", or "INVALID"
        final_probability: Optional[float] = None
    ):
        """
        Record the actual outcome when a market resolves.
        """
        if market_id not in self.state["markets"]:
            raise ValueError(f"Market {market_id} not found in experiment")

        now = datetime.now().isoformat()
        market = self.state["markets"][market_id]

        market["actual_outcome"] = outcome
        market["resolution_timestamp"] = now
        market["final_probability"] = final_probability
        market["last_updated"] = now

        # Score predictions
        if outcome in ["YES", "NO"]:
            if market["control_prediction"]:
                market["control_correct"] = (
                    market["control_prediction"]["prediction"] == outcome
                )
                if market["control_correct"]:
                    self.state["statistics"]["control_correct"] += 1

            if market["meihua_prediction"]:
                market["meihua_correct"] = (
                    market["meihua_prediction"]["prediction"] == outcome
                )
                if market["meihua_correct"]:
                    self.state["statistics"]["meihua_correct"] += 1

        # Update statistics
        self.state["statistics"]["pending"] -= 1
        self.state["statistics"]["resolved"] += 1

        self._append_log({
            "event": "outcome_recorded",
            "market_id": market_id,
            "outcome": outcome,
            "control_correct": market["control_correct"],
            "meihua_correct": market["meihua_correct"],
        })

        self._save_state()
        self._export_csv()

    def add_note(self, market_id: str, note: str):
        """Add a note to a market record."""
        if market_id not in self.state["markets"]:
            raise ValueError(f"Market {market_id} not found")

        timestamped_note = f"[{datetime.now().isoformat()}] {note}"
        self.state["markets"][market_id]["notes"].append(timestamped_note)
        self.state["markets"][market_id]["last_updated"] = datetime.now().isoformat()
        self._save_state()

    def get_pending_markets(self) -> List[Dict[str, Any]]:
        """Get all markets awaiting resolution."""
        return [
            m for m in self.state["markets"].values()
            if m["actual_outcome"] == "PENDING"
        ]

    def get_markets_needing_predictions(self, prediction_type: str) -> List[Dict[str, Any]]:
        """Get markets that don't have a prediction of the given type."""
        field = f"{prediction_type}_prediction"
        return [
            m for m in self.state["markets"].values()
            if m["actual_outcome"] == "PENDING" and m[field] is None
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get current experiment statistics."""
        stats = self.state["statistics"].copy()

        # Calculate accuracy if we have resolved markets
        if stats["resolved"] > 0:
            # Count markets where we have both predictions
            resolved = [
                m for m in self.state["markets"].values()
                if m["actual_outcome"] in ["YES", "NO"]
            ]

            control_predictions = [m for m in resolved if m["control_prediction"]]
            meihua_predictions = [m for m in resolved if m["meihua_prediction"]]

            if control_predictions:
                stats["control_accuracy"] = (
                    sum(1 for m in control_predictions if m["control_correct"])
                    / len(control_predictions)
                )

            if meihua_predictions:
                stats["meihua_accuracy"] = (
                    sum(1 for m in meihua_predictions if m["meihua_correct"])
                    / len(meihua_predictions)
                )

        return stats

    def _export_csv(self):
        """Export results to CSV for statistical analysis."""
        if not self.state["markets"]:
            return

        # Flatten data for CSV
        rows = []
        for market_id, m in self.state["markets"].items():
            row = {
                "record_id": m["record_id"],
                "market_id": market_id,
                "batch": m["selection_batch"],
                "title": m["title"][:100],  # Truncate for readability
                "categories": "|".join(m["categories"]),
                "initial_prob": m["initial_probability"],
                "volume_usd": m["volume_usd"],
                "days_until": m["days_until_resolution"],
                "selection_date": m["selection_timestamp"][:10],
                "expected_resolution": m["expected_resolution_date"][:10] if m["expected_resolution_date"] else "",

                # Control prediction
                "control_pred": m["control_prediction"]["prediction"] if m["control_prediction"] else "",
                "control_conf": m["control_prediction"]["confidence"] if m["control_prediction"] else "",

                # Meihua prediction
                "meihua_pred": m["meihua_prediction"]["prediction"] if m["meihua_prediction"] else "",
                "meihua_conf": m["meihua_prediction"]["confidence"] if m["meihua_prediction"] else "",
                "hexagram": m["meihua_prediction"].get("hexagram_name", "") if m["meihua_prediction"] else "",

                # Outcome
                "outcome": m["actual_outcome"],
                "resolution_date": m["resolution_timestamp"][:10] if m["resolution_timestamp"] else "",
                "control_correct": 1 if m["control_correct"] else (0 if m["control_correct"] is False else ""),
                "meihua_correct": 1 if m["meihua_correct"] else (0 if m["meihua_correct"] is False else ""),
            }
            rows.append(row)

        # Write CSV
        if rows:
            fieldnames = list(rows[0].keys())
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def get_existing_market_ids(self) -> List[str]:
        """Get list of all market IDs already in the experiment."""
        return list(self.state["markets"].keys())

    def print_summary(self):
        """Print a summary of the experiment state."""
        stats = self.get_statistics()

        print("\n" + "="*60)
        print("EXPERIMENT SUMMARY")
        print("="*60)
        print(f"Experiment ID: {self.state['experiment_id']}")
        print(f"Created: {self.state['created']}")
        print(f"\nMarkets:")
        print(f"  Total: {stats['total_markets']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Resolved: {stats['resolved']}")

        if stats['resolved'] > 0:
            print(f"\nAccuracy (resolved markets):")
            if 'control_accuracy' in stats:
                print(f"  Control: {stats['control_accuracy']:.1%}")
            if 'meihua_accuracy' in stats:
                print(f"  Meihua:  {stats['meihua_accuracy']:.1%}")

        print("="*60 + "\n")


# CLI
if __name__ == "__main__":
    logger = ExperimentLogger()
    logger.print_summary()

    print("Pending markets:")
    for m in logger.get_pending_markets()[:5]:
        print(f"  - {m['title'][:60]}...")
