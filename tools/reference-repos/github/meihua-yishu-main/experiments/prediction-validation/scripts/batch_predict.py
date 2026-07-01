#!/usr/bin/env python3
"""
Batch Prediction Generator for Phase 1

Generates predictions for all pending markets:
- Control: Based on market probability and reasoning
- Meihua: Using TEXT-BASED casting method (question-derived hexagrams)

Uses the hexagram strategy data from the skill for consistent predictions.
"""

import sys
import os
import json
from typing import Dict, Any, Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experiment_logger import ExperimentLogger

# Hexagram names mapping (number -> Chinese name)
HEXAGRAM_NAMES = {
    1: "乾為天", 2: "坤為地", 3: "水雷屯", 4: "山水蒙", 5: "水天需",
    6: "天水訟", 7: "地水師", 8: "水地比", 9: "風天小畜", 10: "天澤履",
    11: "地天泰", 12: "天地否", 13: "天火同人", 14: "火天大有", 15: "地山謙",
    16: "雷地豫", 17: "澤雷隨", 18: "山風蠱", 19: "地澤臨", 20: "風地觀",
    21: "火雷噬嗑", 22: "山火賁", 23: "山地剝", 24: "地雷復", 25: "天雷無妄",
    26: "山天大畜", 27: "山雷頤", 28: "澤風大過", 29: "坎為水", 30: "離為火",
    31: "澤山咸", 32: "雷風恆", 33: "天山遯", 34: "雷天大壯", 35: "火地晉",
    36: "地火明夷", 37: "風火家人", 38: "火澤睽", 39: "水山蹇", 40: "雷水解",
    41: "山澤損", 42: "風雷益", 43: "澤天夬", 44: "天風姤", 45: "澤地萃",
    46: "地風升", 47: "澤水困", 48: "水風井", 49: "澤火革", 50: "火風鼎",
    51: "震為雷", 52: "艮為山", 53: "風山漸", 54: "雷澤歸妹", 55: "雷火豐",
    56: "火山旅", 57: "巽為風", 58: "兌為澤", 59: "風水渙", 60: "水澤節",
    61: "風澤中孚", 62: "雷山小過", 63: "水火既濟", 64: "火水未濟"
}

# Hexagram strategy data (吉率 and strategy from hexagram-strategy.md)
# Format: hexagram_number: (吉率%, strategy, type)
HEXAGRAM_STRATEGY = {
    1: (50, "觀", "一般"), 2: (50, "觀", "一般"), 3: (33, "觀", "一般"),
    4: (50, "觀", "一般"), 5: (50, "觀", "一般"), 6: (33, "慎", "陷阱"),
    7: (17, "變", "困境"), 8: (67, "留", "吸引子"), 9: (33, "觀", "一般"),
    10: (33, "觀", "一般"), 11: (83, "守", "福地"), 12: (33, "走", "排斥子"),
    13: (50, "觀", "一般"), 14: (67, "留", "吸引子"), 15: (83, "守", "福地"),
    16: (17, "變", "困境"), 17: (50, "觀", "一般"), 18: (50, "觀", "一般"),
    19: (83, "守", "福地"), 20: (33, "觀", "一般"), 21: (50, "觀", "一般"),
    22: (33, "觀", "一般"), 23: (17, "變", "困境"), 24: (50, "觀", "一般"),
    25: (50, "觀", "一般"), 26: (50, "守", "福地"), 27: (50, "觀", "一般"),
    28: (33, "走", "排斥子"), 29: (33, "慎", "陷阱"), 30: (33, "觀", "一般"),
    31: (50, "觀", "一般"), 32: (0, "變", "困境"), 33: (50, "觀", "一般"),
    34: (50, "觀", "一般"), 35: (67, "留", "吸引子"), 36: (17, "變", "困境"),
    37: (67, "留", "吸引子"), 38: (17, "變", "困境"), 39: (33, "慎", "陷阱"),
    40: (50, "觀", "一般"), 41: (33, "觀", "一般"), 42: (67, "留", "吸引子"),
    43: (33, "走", "排斥子"), 44: (17, "變", "困境"), 45: (50, "觀", "一般"),
    46: (50, "觀", "一般"), 47: (17, "變", "困境"), 48: (50, "觀", "一般"),
    49: (50, "觀", "一般"), 50: (67, "守", "福地"), 51: (33, "觀", "一般"),
    52: (50, "觀", "一般"), 53: (50, "觀", "一般"), 54: (17, "變", "困境"),
    55: (33, "觀", "一般"), 56: (33, "觀", "一般"), 57: (50, "觀", "一般"),
    58: (50, "觀", "一般"), 59: (50, "觀", "一般"), 60: (50, "觀", "一般"),
    61: (67, "留", "吸引子"), 62: (33, "觀", "一般"), 63: (50, "觀", "一般"),
    64: (33, "觀", "一般")
}

# Trigram names and five elements
TRIGRAM_INFO = {
    1: ("乾", "金"), 2: ("兌", "金"), 3: ("離", "火"), 4: ("震", "木"),
    5: ("巽", "木"), 6: ("坎", "水"), 7: ("艮", "土"), 8: ("坤", "土")
}

# Five element relationships
def get_element_relation(ti_element: str, yong_element: str) -> str:
    """Determine the Ti-Yong relationship based on five elements."""
    generate = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    conquer = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

    if ti_element == yong_element:
        return "比和"
    elif generate.get(yong_element) == ti_element:
        return "用生體"
    elif generate.get(ti_element) == yong_element:
        return "體生用"
    elif conquer.get(yong_element) == ti_element:
        return "用克體"
    elif conquer.get(ti_element) == yong_element:
        return "體克用"
    return "unknown"


def cast_hexagram_text_based(word_count: int, char_count: int, total: int) -> Tuple[int, int, int]:
    """
    Cast hexagram using TEXT-BASED method (測字起卦).

    Args:
        word_count: Number of words in question
        char_count: Number of characters in question
        total: word_count + char_count for moving line

    Returns:
        (upper_trigram, lower_trigram, moving_line)
    """
    upper = word_count % 8
    if upper == 0:
        upper = 8

    lower = char_count % 8
    if lower == 0:
        lower = 8

    moving = total % 6
    if moving == 0:
        moving = 6

    return upper, lower, moving


def get_hexagram_number(upper: int, lower: int) -> int:
    """Get hexagram number from upper and lower trigrams (先天八卦)."""
    # King Wen sequence mapping from trigram pairs
    hexagram_map = {
        (1, 1): 1, (1, 2): 10, (1, 3): 13, (1, 4): 25, (1, 5): 44, (1, 6): 6, (1, 7): 33, (1, 8): 12,
        (2, 1): 43, (2, 2): 58, (2, 3): 49, (2, 4): 17, (2, 5): 28, (2, 6): 47, (2, 7): 31, (2, 8): 45,
        (3, 1): 14, (3, 2): 38, (3, 3): 30, (3, 4): 21, (3, 5): 50, (3, 6): 64, (3, 7): 56, (3, 8): 35,
        (4, 1): 34, (4, 2): 54, (4, 3): 55, (4, 4): 51, (4, 5): 32, (4, 6): 40, (4, 7): 62, (4, 8): 16,
        (5, 1): 9, (5, 2): 61, (5, 3): 37, (5, 4): 42, (5, 5): 57, (5, 6): 59, (5, 7): 53, (5, 8): 20,
        (6, 1): 5, (6, 2): 60, (6, 3): 63, (6, 4): 3, (6, 5): 48, (6, 6): 29, (6, 7): 39, (6, 8): 8,
        (7, 1): 26, (7, 2): 41, (7, 3): 22, (7, 4): 27, (7, 5): 18, (7, 6): 4, (7, 7): 52, (7, 8): 23,
        (8, 1): 11, (8, 2): 19, (8, 3): 36, (8, 4): 24, (8, 5): 46, (8, 6): 7, (8, 7): 15, (8, 8): 2,
    }
    return hexagram_map.get((upper, lower), 1)


def get_transformed_hexagram(hex_num: int, moving_line: int) -> int:
    """Get the transformed hexagram after the moving line changes."""
    # This is a simplified calculation - in practice would need full line data
    # For now, use a reasonable approximation based on the moving line
    return ((hex_num + moving_line * 7) % 64) + 1


def make_control_prediction(market: Dict[str, Any]) -> Dict[str, Any]:
    """Make a control prediction based on market probability."""
    prob = market.get("initial_probability", 0.5)

    # Simple rule: follow market consensus with slight adjustment
    if prob >= 0.5:
        prediction = "YES"
        confidence = min(0.9, prob + 0.05)
    else:
        prediction = "NO"
        confidence = min(0.9, (1 - prob) + 0.05)

    # Round confidence
    confidence = round(confidence, 2)

    # Generate reasoning
    if prediction == "YES":
        reasoning = f"Market probability of {prob:.0%} indicates consensus for YES. Following market sentiment with {confidence:.0%} confidence."
    else:
        reasoning = f"Market probability of {prob:.0%} suggests unlikely outcome. Predicting NO with {confidence:.0%} confidence."

    return {
        "prediction": prediction,
        "confidence": confidence,
        "reasoning": reasoning
    }


def analyze_question_for_trigrams(title: str, description: str, categories: list) -> Tuple[int, int, int]:
    """
    取象起卦 - Analyze question semantics to derive trigrams.

    Maps question content to trigram correspondences based on:
    - Subject matter (what is being asked about)
    - Key concepts and imagery
    - Domain-specific mappings

    Returns (upper_trigram, lower_trigram, moving_line)
    """
    title_lower = title.lower()
    desc_lower = description.lower() if description else ""
    full_text = title_lower + " " + desc_lower

    # Default trigrams
    upper = 1  # 乾
    lower = 8  # 坤

    # === UPPER TRIGRAM: The subject/questioner side ===

    # Crypto/Finance/Value → 乾/兌 (Metal)
    if any(w in full_text for w in ['bitcoin', 'btc', 'crypto', 'ethereum', 'xrp', 'gold', 'silver', 'price']):
        upper = 1  # 乾 - valuable, leadership in market

    # Government/Leadership/Politics → 乾
    elif any(w in full_text for w in ['trump', 'president', 'putin', 'government', 'fed', 'congress', 'senate', 'supreme court']):
        upper = 1  # 乾 - ruler, authority

    # Military/Strike/War → 震/離
    elif any(w in full_text for w in ['strike', 'military', 'war', 'attack', 'russia', 'israel', 'ukraine']):
        upper = 4  # 震 - movement, action, military

    # Sports/Competition → 震 (movement)
    elif any(w in full_text for w in ['win', 'match', 'game', 'ufc', 'tennis', 'football', 'basketball', 'super bowl']):
        upper = 4  # 震 - competition, movement

    # Entertainment/Awards → 離 (brightness, fame)
    elif any(w in full_text for w in ['oscar', 'grammy', 'award', 'nomination', 'actor', 'actress', 'director', 'perform']):
        upper = 3  # 離 - visibility, fame, culture

    # Technology/AI → 乾/巽
    elif any(w in full_text for w in ['ai', 'nvidia', 'tech', 'spacex', 'tesla', 'apple', 'meta', 'google']):
        upper = 5  # 巽 - wind, communication, spread

    # Weather/Natural events → 坎/震
    elif any(w in full_text for w in ['earthquake', 'weather', 'rain', 'storm']):
        upper = 6  # 坎 - water, natural forces

    # === LOWER TRIGRAM: The environment/situation ===

    # Time pressure (short deadline) → 震 (urgency)
    if any(w in full_text for w in ['january', 'this week', 'tomorrow', 'today']):
        lower = 4  # 震 - quick, urgent

    # Uncertainty/Risk → 坎
    elif any(w in full_text for w in ['risk', 'danger', 'uncertain', 'volatile']):
        lower = 6  # 坎 - danger, hidden

    # Stability/Foundation → 坤/艮
    elif any(w in full_text for w in ['stable', 'foundation', 'base', 'ground']):
        lower = 8  # 坤 - earth, stability

    # Competition/Opposition → 兌
    elif any(w in full_text for w in ['vs', 'versus', 'against', 'face']):
        lower = 2  # 兌 - exchange, opposition

    # Announcement/Speech → 巽
    elif any(w in full_text for w in ['say', 'announce', 'speech', 'call', 'talk']):
        lower = 5  # 巽 - communication

    # Achievement/Success → 離
    elif any(w in full_text for w in ['win', 'beat', 'achieve', 'reach', 'above']):
        lower = 3  # 離 - success, brightness

    # Geographic/Location → 艮
    elif any(w in full_text for w in ['city', 'country', 'region', 'area', 'territory']):
        lower = 7  # 艮 - mountain, location

    # Default based on probability sentiment
    else:
        lower = 8  # 坤 - general situation

    # === MOVING LINE: Based on timing and specificity ===
    word_count = len(title.split())
    moving = (word_count % 6) + 1
    if moving > 6:
        moving = 6

    return upper, lower, moving


def make_meihua_prediction(market: Dict[str, Any]) -> Dict[str, Any]:
    """Make a Meihua prediction using 取象起卦 (semantic-based casting)."""
    title = market.get("title", "")
    description = market.get("description", "")
    categories = market.get("categories", [])

    # Use 取象起卦 - semantic analysis of question
    upper_trigram, lower_trigram, moving_line = analyze_question_for_trigrams(
        title, description, categories
    )

    # Calculate hexagram
    hex_num = get_hexagram_number(upper_trigram, lower_trigram)
    hex_name = HEXAGRAM_NAMES.get(hex_num, f"卦{hex_num}")

    # Calculate transformed hexagram
    trans_hex = get_transformed_hexagram(hex_num, moving_line)

    # Get Ti-Yong relationship
    # Ti is the trigram without the moving line, Yong has the moving line
    if moving_line <= 3:
        ti_trigram = upper_trigram
        yong_trigram = lower_trigram
    else:
        ti_trigram = lower_trigram
        yong_trigram = upper_trigram

    ti_name, ti_element = TRIGRAM_INFO.get(ti_trigram, ("", ""))
    yong_name, yong_element = TRIGRAM_INFO.get(yong_trigram, ("", ""))
    ti_yong_relation = get_element_relation(ti_element, yong_element)

    # Get hexagram strategy
    ji_rate, strategy, hex_type = HEXAGRAM_STRATEGY.get(hex_num, (50, "觀", "一般"))

    # Make prediction based on Ti-Yong relationship and strategy
    # Enhanced logic: combine Ti-Yong with strategy type
    favorable_relations = ["用生體", "體克用", "比和"]
    unfavorable_relations = ["用克體", "體生用"]

    favorable_types = ["吸引子", "福地"]
    unfavorable_types = ["排斥子", "困境", "陷阱"]

    # Score calculation
    score = 0.5  # Start neutral

    # Ti-Yong contribution
    if ti_yong_relation in favorable_relations:
        score += 0.15
    elif ti_yong_relation in unfavorable_relations:
        score -= 0.15

    # Hexagram type contribution
    if hex_type in favorable_types:
        score += 0.1
    elif hex_type in unfavorable_types:
        score -= 0.1

    # 吉率 contribution (normalize to -0.1 to +0.1)
    ji_contribution = (ji_rate - 50) / 500
    score += ji_contribution

    # Make prediction
    if score >= 0.5:
        prediction = "YES"
        confidence = min(0.75, 0.5 + (score - 0.5))
    else:
        prediction = "NO"
        confidence = min(0.75, 0.5 + (0.5 - score))

    confidence = round(confidence, 2)

    # Generate reasoning
    ti_yong_analysis = f"{ti_yong_relation} - {yong_name}({yong_element}) {'生' if '生' in ti_yong_relation else '克' if '克' in ti_yong_relation else '和'} {ti_name}({ti_element})"

    if prediction == "YES":
        reasoning = f"{hex_name}卦，{ti_yong_relation}。{hex_type}類型，吉率{ji_rate}%，策略「{strategy}」。卦象整體有利，預測為YES。"
    else:
        reasoning = f"{hex_name}卦，{ti_yong_relation}。{hex_type}類型，吉率{ji_rate}%，策略「{strategy}」。卦象整體不利，預測為NO。"

    return {
        "prediction": prediction,
        "confidence": confidence,
        "reasoning": reasoning,
        "hexagram_number": hex_num,
        "hexagram_name": hex_name,
        "transformed_hexagram": trans_hex,
        "casting_method": "取象起卦",
        "ti_yong_analysis": ti_yong_analysis
    }


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")

    logger = ExperimentLogger(data_dir)

    # Get markets needing predictions
    markets = logger.state["markets"]

    control_needed = []
    meihua_needed = []

    for market_id, market in markets.items():
        if market["control_prediction"] is None:
            control_needed.append((market_id, market))
        if market["meihua_prediction"] is None:
            meihua_needed.append((market_id, market))

    print(f"Markets needing control predictions: {len(control_needed)}")
    print(f"Markets needing Meihua predictions: {len(meihua_needed)}")

    if not control_needed and not meihua_needed:
        print("\nAll predictions already recorded!")
        return

    # Process control predictions
    print(f"\n{'='*60}")
    print("CONTROL PREDICTIONS")
    print('='*60)

    for market_id, market in control_needed:
        pred = make_control_prediction(market)

        logger.record_prediction(
            market_id=market_id,
            prediction_type="control",
            prediction=pred["prediction"],
            confidence=pred["confidence"],
            reasoning=pred["reasoning"]
        )

        print(f"  {market['title'][:50]}...")
        print(f"    → {pred['prediction']} ({pred['confidence']:.0%})")

    # Process Meihua predictions
    print(f"\n{'='*60}")
    print("MEIHUA PREDICTIONS (取象起卦 / Semantic-based)")
    print('='*60)

    for market_id, market in meihua_needed:
        pred = make_meihua_prediction(market)

        logger.record_prediction(
            market_id=market_id,
            prediction_type="meihua",
            prediction=pred["prediction"],
            confidence=pred["confidence"],
            reasoning=pred["reasoning"],
            hexagram_info={
                "hexagram_number": pred["hexagram_number"],
                "hexagram_name": pred["hexagram_name"],
                "transformed_hexagram": pred["transformed_hexagram"],
                "casting_method": pred["casting_method"],
                "ti_yong_analysis": pred["ti_yong_analysis"],
            }
        )

        print(f"  {market['title'][:50]}...")
        print(f"    卦: {pred['hexagram_name']} | {pred['ti_yong_analysis']}")
        print(f"    → {pred['prediction']} ({pred['confidence']:.0%})")

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Control predictions recorded: {len(control_needed)}")
    print(f"Meihua predictions recorded: {len(meihua_needed)}")

    # Count agreements/disagreements in new predictions
    agreements = 0
    disagreements = 0

    for market_id, market in meihua_needed:
        ctrl = logger.state["markets"][market_id].get("control_prediction", {})
        mh = logger.state["markets"][market_id].get("meihua_prediction", {})

        if ctrl and mh:
            if ctrl.get("prediction") == mh.get("prediction"):
                agreements += 1
            else:
                disagreements += 1

    if agreements + disagreements > 0:
        print(f"\nNew predictions analysis:")
        print(f"  Concordant (agree): {agreements}")
        print(f"  Discordant (disagree): {disagreements}")
        print(f"  Discordance rate: {disagreements/(agreements+disagreements):.1%}")


if __name__ == "__main__":
    main()
