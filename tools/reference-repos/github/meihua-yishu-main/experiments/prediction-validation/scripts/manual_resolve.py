#!/usr/bin/env python3
"""
Manually record outcomes for resolved markets.
Based on web search verification of actual results.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiment_logger import ExperimentLogger

# Outcomes verified via web search on 2026-01-25
RESOLVED_OUTCOMES = {
    # Market ID: (outcome, final_probability, verification_note)
    "618531": ("YES", None, "Ethan Hawke nominated for Best Actor - Oscar noms Jan 22"),
    "1183931": ("NO", None, "Bitcoin ~$93K on Jan 21, below $98K threshold"),
    "1090519": ("YES", None, "Israel struck Yemen and Syria in January 2026"),
    "903574": ("NO", None, "Han Duck Soo sentenced to 23 years, NOT 5-10 years"),
    "1191043": ("NO", None, "Atmane lost - Maestrelli won the match"),
    "1114754": ("NO", None, "Yadong lost - O'Malley won UFC 324"),
    "614713": ("NO", None, "del Toro not nominated for Best Director"),
    "614702": ("YES", None, "Chloe Zhao nominated for Best Director"),
    "1190999": ("NO", None, "Cerundolo lost - Thompson won the match"),
    "920389": ("YES", None, "Trump-Putin phone call confirmed in January 2026"),
}


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")

    logger = ExperimentLogger(data_dir)

    print("Recording manual outcomes for 10 resolved markets...\n")

    for market_id, (outcome, final_prob, note) in RESOLVED_OUTCOMES.items():
        if market_id not in logger.state["markets"]:
            print(f"  WARNING: Market {market_id} not found in experiment")
            continue

        market = logger.state["markets"][market_id]

        # Skip if already resolved
        if market["actual_outcome"] != "PENDING":
            print(f"  SKIP: {market['title'][:50]}... (already resolved)")
            continue

        # Record outcome
        logger.record_outcome(market_id, outcome, final_prob)

        # Add verification note
        logger.add_note(market_id, f"Manual resolution: {note}")

        # Show result
        control = market["control_prediction"]["prediction"]
        meihua = market["meihua_prediction"]["prediction"]
        c_correct = "✓" if control == outcome else "✗"
        m_correct = "✓" if meihua == outcome else "✗"

        print(f"  {market['title'][:50]}...")
        print(f"    Outcome: {outcome} | Control: {control} {c_correct} | Meihua: {meihua} {m_correct}")
        print()

    # Print summary
    stats = logger.state["statistics"]
    print("\n" + "="*60)
    print("UPDATED STATISTICS")
    print("="*60)
    print(f"Total markets: {stats['total_markets']}")
    print(f"Resolved: {stats['resolved']}")
    print(f"Pending: {stats['pending']}")
    print(f"Control correct: {stats['control_correct']}")
    print(f"Meihua correct: {stats['meihua_correct']}")

    if stats['resolved'] > 0:
        print(f"\nControl accuracy: {stats['control_correct']}/{stats['resolved']} ({100*stats['control_correct']/stats['resolved']:.1f}%)")
        print(f"Meihua accuracy: {stats['meihua_correct']}/{stats['resolved']} ({100*stats['meihua_correct']/stats['resolved']:.1f}%)")


if __name__ == "__main__":
    main()
