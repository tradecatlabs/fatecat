#!/usr/bin/env python3
"""
Experiment Runner

Orchestrates the prediction experiment workflow.
Designed for manual execution with Claude Code (no API integration).

Workflow:
1. Select markets randomly
2. Generate prompts for each market
3. You manually run prompts in Claude Code
4. Record predictions and hexagram results
5. Check for resolved markets and record outcomes
6. Run statistical analysis

Key Data Captured:
- SKILL INPUT: Full text sent to Meihua skill
- HEXAGRAM OUTPUT: Hexagram number, name, transformed hexagram
- BETTING DECISION: YES/NO + confidence level
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from polymarket_client import PolymarketClient, format_market_for_experiment
from market_selector import MarketSelector
from experiment_logger import ExperimentLogger


class ExperimentRunner:
    """Runs the Meihua prediction experiment."""

    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(script_dir, "..", "data")
        os.makedirs(self.data_dir, exist_ok=True)

        self.selector = MarketSelector()
        self.logger = ExperimentLogger(self.data_dir)
        self.client = PolymarketClient()

        # Prompt templates
        self.prompts_dir = os.path.join(self.data_dir, "prompts")
        os.makedirs(self.prompts_dir, exist_ok=True)

    def select_new_markets(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Select N new markets for the experiment.
        Excludes markets already in the experiment.
        """
        existing_ids = self.logger.get_existing_market_ids()
        markets = self.selector.select_random(n=n, exclude_ids=existing_ids)

        # Get next batch number
        batch = self.logger.state["statistics"]["batches"] + 1

        # Add to experiment
        for m in markets:
            self.logger.add_market(m, batch)
            print(f"Added: {m['title'][:60]}...")

        print(f"\n✅ Added {len(markets)} markets to experiment (Batch #{batch})")
        return markets

    def generate_control_prompt(self, market: Dict[str, Any]) -> str:
        """
        Generate prompt for control prediction (no Meihua).
        Pure probability-based analysis.
        """
        return f"""You are analyzing a prediction market. Based ONLY on the market data and your general knowledge, predict the outcome.

MARKET INFORMATION:
==================
Title: {market['title']}

Description: {market.get('description', 'N/A')[:500]}

Current Market Data:
- Current Probability: {market['core_data']['current_prob']:.1%}
- Trading Volume: ${market['core_data']['volume_usd']:,.0f}
- Liquidity: ${market['core_data']['liquidity']:.0f}
- Days Until Resolution: {market['core_data']['days_until_resolution']}
- Expected Resolution: {market['core_data']['end_date']}

Categories: {', '.join(market['context']['categories']) or 'None'}

INSTRUCTIONS:
=============
1. Analyze the question and market data
2. Consider current probability and market sentiment
3. Make a prediction

YOUR PREDICTION (required format):
==================================
PREDICTION: [YES or NO]
CONFIDENCE: [0.0 to 1.0]
REASONING: [2-3 sentences explaining your prediction]
"""

    def generate_meihua_prompt(self, market: Dict[str, Any]) -> str:
        """
        Generate prompt for Meihua prediction.
        Includes all casting inputs for the skill.
        """
        mi = market['meihua_inputs']

        return f"""Use the Meihua Yishu (梅花易數) skill to divine this prediction market question.

QUESTION TO DIVINE:
==================
{market['title']}

CONTEXT:
========
Description: {market.get('description', 'N/A')[:500]}

Current Market Data:
- Current Probability: {market['core_data']['current_prob']:.1%}
- Trading Volume: ${market['core_data']['volume_usd']:,.0f}
- Days Until Resolution: {market['core_data']['days_until_resolution']}
- Expected Resolution: {market['core_data']['end_date']}

Categories: {', '.join(market['context']['categories']) or 'General'}

CASTING INPUTS (use any method):
================================

1. NUMBER-BASED (數字起卦):
   - Upper trigram input: {mi['number_based']['upper_input']} → Trigram #{mi['number_based']['upper_trigram']}
   - Lower trigram input: {mi['number_based']['lower_input']} → Trigram #{mi['number_based']['lower_trigram']}
   - Moving line: {mi['number_based']['moving_line']}

2. TEXT-BASED (測字起卦):
   - Word count: {mi['text_based']['word_count']} → Upper trigram #{mi['text_based']['upper_trigram']}
   - Character count: {mi['text_based']['char_count']} → Lower trigram #{mi['text_based']['lower_trigram']}
   - Moving line: {mi['text_based']['moving_line']}

3. DIRECTION-BASED (方位起卦):
   - Category: {mi['direction_based']['category']}
   - Direction: {mi['direction_based']['direction']}
   - Trigram: {mi['direction_based']['trigram_name']} (#{mi['direction_based']['trigram_number']})

4. MEASUREMENT-BASED (尺寸起卦):
   - Days until resolution: {mi['measurement_based']['days']} → Upper #{mi['measurement_based']['upper_trigram']}
   - Probability %: {mi['measurement_based']['prob_percent']} → Lower #{mi['measurement_based']['lower_trigram']}
   - Moving line: {mi['measurement_based']['moving_line']}

INSTRUCTIONS:
=============
1. Cast the hexagram using one or more methods above
2. Identify: 本卦 (original), 變卦 (transformed), 互卦 (mutual)
3. Determine 體卦 and 用卦
4. Analyze 體用關係 (生, 剋, 比和)
5. Consider 外應 if any context clues
6. Provide final prediction

YOUR PREDICTION (required format):
==================================
HEXAGRAM: [Hexagram number and Chinese name, e.g., "40 雷水解"]
TRANSFORMED: [Transformed hexagram if applicable]
CASTING_METHOD: [Which method(s) used]
TI_YONG: [Brief 體用 analysis]
PREDICTION: [YES or NO]
CONFIDENCE: [0.0 to 1.0]
REASONING: [2-3 sentences with Meihua interpretation]
"""

    def save_prompts_for_batch(self, markets: List[Dict[str, Any]], batch: int):
        """Save all prompts for a batch to files for easy copying."""
        batch_dir = os.path.join(self.prompts_dir, f"batch_{batch:03d}")
        os.makedirs(batch_dir, exist_ok=True)

        for i, m in enumerate(markets, 1):
            market_id = m['market_id']

            # Control prompt
            ctrl_prompt = self.generate_control_prompt(m)
            ctrl_file = os.path.join(batch_dir, f"{i:02d}_{market_id[:8]}_control.txt")
            with open(ctrl_file, 'w') as f:
                f.write(ctrl_prompt)

            # Meihua prompt
            mh_prompt = self.generate_meihua_prompt(m)
            mh_file = os.path.join(batch_dir, f"{i:02d}_{market_id[:8]}_meihua.txt")
            with open(mh_file, 'w') as f:
                f.write(mh_prompt)

            # Also save to logger for audit
            self.logger.add_note(market_id, f"Prompts saved to {batch_dir}")

        print(f"\n📁 Prompts saved to: {batch_dir}")
        print(f"   {len(markets)} control prompts")
        print(f"   {len(markets)} meihua prompts")

    def record_control_prediction(
        self,
        market_id: str,
        prediction: str,
        confidence: float,
        reasoning: str
    ):
        """Record a control (non-Meihua) prediction."""
        self.logger.record_prediction(
            market_id=market_id,
            prediction_type="control",
            prediction=prediction.upper(),
            confidence=confidence,
            reasoning=reasoning
        )
        print(f"✅ Recorded control prediction: {prediction} ({confidence:.0%})")

    def record_meihua_prediction(
        self,
        market_id: str,
        prediction: str,
        confidence: float,
        reasoning: str,
        hexagram_number: int,
        hexagram_name: str,
        transformed_hexagram: Optional[int] = None,
        casting_method: str = "",
        ti_yong_analysis: str = ""
    ):
        """Record a Meihua prediction with hexagram details."""
        self.logger.record_prediction(
            market_id=market_id,
            prediction_type="meihua",
            prediction=prediction.upper(),
            confidence=confidence,
            reasoning=reasoning,
            hexagram_info={
                "hexagram_number": hexagram_number,
                "hexagram_name": hexagram_name,
                "transformed_hexagram": transformed_hexagram,
                "casting_method": casting_method,
                "ti_yong_analysis": ti_yong_analysis,
            }
        )
        print(f"✅ Recorded Meihua prediction: {hexagram_name} → {prediction} ({confidence:.0%})")

    def check_resolutions(self) -> List[Dict[str, Any]]:
        """
        Check pending markets for resolutions.
        Returns list of newly resolved markets.
        """
        pending = self.logger.get_pending_markets()
        resolved = []

        print(f"\nChecking {len(pending)} pending markets for resolutions...")

        for m in pending:
            try:
                result = self.client.check_resolution(m['market_id'])
                if result['resolved'] and result['outcome']:
                    self.logger.record_outcome(
                        market_id=m['market_id'],
                        outcome=result['outcome'],
                        final_probability=result.get('final_price')
                    )
                    resolved.append({
                        **m,
                        "outcome": result['outcome']
                    })
                    print(f"  ✅ Resolved: {m['title'][:50]}... → {result['outcome']}")
            except Exception as e:
                print(f"  ⚠️ Error checking {m['market_id']}: {e}")

        print(f"\nNewly resolved: {len(resolved)} markets")
        return resolved

    def get_next_market_for_prediction(self, prediction_type: str) -> Optional[Dict[str, Any]]:
        """Get the next market needing a prediction of the given type."""
        markets = self.logger.get_markets_needing_predictions(prediction_type)
        if markets:
            return markets[0]
        return None

    def print_status(self):
        """Print current experiment status."""
        self.logger.print_summary()

        # Show next actions
        ctrl_needed = self.logger.get_markets_needing_predictions("control")
        mh_needed = self.logger.get_markets_needing_predictions("meihua")

        print("Next Actions:")
        print(f"  Control predictions needed: {len(ctrl_needed)}")
        print(f"  Meihua predictions needed:  {len(mh_needed)}")

        if ctrl_needed:
            print(f"\n  Next control: {ctrl_needed[0]['title'][:50]}...")
        if mh_needed:
            print(f"  Next meihua:  {mh_needed[0]['title'][:50]}...")

    def export_prediction_summary(self) -> str:
        """Export a summary of all predictions for review."""
        state = self.logger.state
        lines = ["# Prediction Summary\n"]

        for market_id, m in state["markets"].items():
            lines.append(f"## {m['title'][:70]}")
            lines.append(f"- URL: {m.get('url', 'N/A')}")
            lines.append(f"- Initial Prob: {m['initial_probability']:.1%}")
            lines.append(f"- Status: {m['actual_outcome']}")

            if m['control_prediction']:
                cp = m['control_prediction']
                lines.append(f"- Control: {cp['prediction']} ({cp['confidence']:.0%})")

            if m['meihua_prediction']:
                mp = m['meihua_prediction']
                hex_info = f"{mp.get('hexagram_name', '?')}"
                lines.append(f"- Meihua: {mp['prediction']} ({mp['confidence']:.0%}) - {hex_info}")

            if m['actual_outcome'] != "PENDING":
                ctrl_icon = "✅" if m['control_correct'] else "❌"
                mh_icon = "✅" if m['meihua_correct'] else "❌"
                lines.append(f"- Results: Control {ctrl_icon}, Meihua {mh_icon}")

            lines.append("")

        summary = "\n".join(lines)

        # Save to file
        summary_file = os.path.join(self.data_dir, "prediction_summary.md")
        with open(summary_file, 'w') as f:
            f.write(summary)

        print(f"Summary saved to: {summary_file}")
        return summary


# CLI
if __name__ == "__main__":
    import sys

    runner = ExperimentRunner()

    if len(sys.argv) < 2:
        print("""
Experiment Runner Commands:
===========================
  python experiment_runner.py status           - Show experiment status
  python experiment_runner.py select [N]       - Select N new markets (default: 10)
  python experiment_runner.py prompts          - Show next prompts to run
  python experiment_runner.py check            - Check for resolved markets
  python experiment_runner.py summary          - Export prediction summary
""")
        runner.print_status()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "status":
        runner.print_status()

    elif cmd == "select":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        markets = runner.select_new_markets(n)
        batch = runner.logger.state["statistics"]["batches"]
        runner.save_prompts_for_batch(markets, batch)

    elif cmd == "prompts":
        # Show next prompts
        ctrl = runner.get_next_market_for_prediction("control")
        if ctrl:
            print("\n" + "="*60)
            print("NEXT CONTROL PROMPT")
            print("="*60)
            print(f"Market ID: {ctrl['market_id']}")
            print(runner.generate_control_prompt(ctrl))

        mh = runner.get_next_market_for_prediction("meihua")
        if mh:
            print("\n" + "="*60)
            print("NEXT MEIHUA PROMPT")
            print("="*60)
            print(f"Market ID: {mh['market_id']}")
            print(runner.generate_meihua_prompt(mh))

    elif cmd == "check":
        runner.check_resolutions()
        runner.print_status()

    elif cmd == "summary":
        runner.export_prediction_summary()

    else:
        print(f"Unknown command: {cmd}")
