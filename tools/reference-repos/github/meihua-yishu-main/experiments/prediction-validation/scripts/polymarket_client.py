#!/usr/bin/env python3
"""
Polymarket API Client

Fetches market data from Polymarket's Gamma API.
No authentication required for read-only access.

API Docs: https://docs.polymarket.com/
"""

import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class PolymarketClient:
    """Client for Polymarket Gamma API (read-only market data)."""

    BASE_URL = "https://gamma-api.polymarket.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "MeihuaExperiment/1.0"
        })

    def get_markets(
        self,
        limit: int = 100,
        offset: int = 0,
        closed: bool = False,
        volume_min: Optional[float] = None,
        liquidity_min: Optional[float] = None,
        end_date_min: Optional[datetime] = None,
        end_date_max: Optional[datetime] = None,
        order: str = "volume",
        ascending: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Fetch markets from Polymarket.

        Args:
            limit: Maximum number of markets to return
            offset: Pagination offset
            closed: If True, include closed markets
            volume_min: Minimum volume in USD
            liquidity_min: Minimum liquidity
            end_date_min: Minimum end date
            end_date_max: Maximum end date
            order: Field to sort by (volume, liquidity, etc.)
            ascending: Sort direction

        Returns:
            List of market dictionaries
        """
        params = {
            "limit": limit,
            "offset": offset,
            "closed": str(closed).lower(),
            "order": order,
            "ascending": str(ascending).lower(),
        }

        if volume_min is not None:
            params["volume_num_min"] = volume_min
        if liquidity_min is not None:
            params["liquidity_num_min"] = liquidity_min
        if end_date_min is not None:
            params["end_date_min"] = end_date_min.strftime("%Y-%m-%d")
        if end_date_max is not None:
            params["end_date_max"] = end_date_max.strftime("%Y-%m-%d")

        response = self.session.get(f"{self.BASE_URL}/markets", params=params)
        response.raise_for_status()
        return response.json()

    def get_market(self, market_id: str) -> Dict[str, Any]:
        """Fetch a single market by ID."""
        response = self.session.get(f"{self.BASE_URL}/markets/{market_id}")
        response.raise_for_status()
        return response.json()

    def get_market_by_condition_id(self, condition_id: str) -> Optional[Dict[str, Any]]:
        """Fetch market by condition ID."""
        response = self.session.get(
            f"{self.BASE_URL}/markets",
            params={"condition_id": condition_id}
        )
        response.raise_for_status()
        markets = response.json()
        return markets[0] if markets else None

    def check_resolution(self, market_id: str) -> Dict[str, Any]:
        """
        Check if a market has resolved and get the outcome.

        Returns:
            Dict with keys: resolved (bool), outcome (str|None), resolution_time (str|None)
        """
        market = self.get_market(market_id)

        resolved = market.get("closed", False)
        outcome = None
        resolution_time = None

        if resolved:
            # Outcome is typically in outcomePrices or resolved field
            outcome_prices = market.get("outcomePrices", "")
            if outcome_prices:
                # Parse outcome - "1,0" means YES won, "0,1" means NO won
                try:
                    prices = [float(p) for p in outcome_prices.split(",")]
                    if len(prices) >= 2:
                        outcome = "YES" if prices[0] > prices[1] else "NO"
                except:
                    pass

            resolution_time = market.get("endDate")

        return {
            "resolved": resolved,
            "outcome": outcome,
            "resolution_time": resolution_time,
            "final_price": market.get("lastTradePrice"),
            "raw": market
        }


def format_market_for_experiment(market: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format raw Polymarket data for the experiment.
    Returns a clean structure with all info needed for analysis.
    """
    # Parse dates
    end_date = None
    if market.get("endDate"):
        try:
            end_date = datetime.fromisoformat(market["endDate"].replace("Z", "+00:00"))
        except:
            pass

    # Calculate days until resolution
    days_until = None
    if end_date:
        days_until = (end_date - datetime.now(end_date.tzinfo)).days

    # Extract current probability
    current_prob = None
    if market.get("lastTradePrice"):
        current_prob = float(market["lastTradePrice"])
    elif market.get("bestAsk"):
        current_prob = float(market["bestAsk"])

    # Get volume
    volume = float(market.get("volumeNum", 0) or 0)

    # Extract categories
    categories = []
    if market.get("tags"):
        categories = [tag.get("label", tag.get("slug", "")) for tag in market["tags"]]

    return {
        "market_id": market.get("id") or market.get("conditionId"),
        "condition_id": market.get("conditionId"),
        "title": market.get("question", ""),
        "description": market.get("description", ""),
        "slug": market.get("slug", ""),
        "url": f"https://polymarket.com/event/{market.get('slug', '')}",

        "core_data": {
            "current_prob": current_prob,
            "volume_usd": volume,
            "liquidity": float(market.get("liquidityNum", 0) or 0),
            "end_date": end_date.isoformat() if end_date else None,
            "days_until_resolution": days_until,
        },

        "context": {
            "categories": categories,
            "active": market.get("active", True),
            "closed": market.get("closed", False),
        },

        "meihua_inputs": calculate_meihua_inputs(market, days_until, current_prob, categories),
    }


def calculate_meihua_inputs(
    market: Dict[str, Any],
    days_until: Optional[int],
    current_prob: Optional[float],
    categories: List[str]
) -> Dict[str, Any]:
    """
    Pre-calculate all Meihua casting inputs from market data.
    These provide multiple methods for hexagram casting.
    """
    title = market.get("question", "")
    volume = float(market.get("volumeNum", 0) or 0)

    # Word and character counts
    words = title.split()
    word_count = len(words)
    char_count = len(title.replace(" ", ""))

    # Volume digits
    volume_last_2 = int(volume) % 100

    # Category to direction mapping (後天八卦)
    category_direction_map = {
        "politics": ("南", "離", 3),
        "crypto": ("西北", "乾", 1),
        "finance": ("西北", "乾", 1),
        "tech": ("東", "震", 4),
        "technology": ("東", "震", 4),
        "health": ("西南", "坤", 8),
        "medical": ("西南", "坤", 8),
        "legal": ("西", "兌", 2),
        "science": ("北", "坎", 6),
        "entertainment": ("東南", "巽", 5),
    }

    direction_info = ("東北", "艮", 7)  # Default
    for cat in categories:
        cat_lower = cat.lower()
        for key, val in category_direction_map.items():
            if key in cat_lower:
                direction_info = val
                break

    # Probability as integer
    prob_int = int((current_prob or 0.5) * 100)

    return {
        "number_based": {
            "upper_input": volume_last_2,
            "upper_trigram": (volume_last_2 % 8) or 8,
            "lower_input": word_count,
            "lower_trigram": (word_count % 8) or 8,
            "moving_line": ((volume_last_2 + word_count) % 6) or 6,
        },
        "text_based": {
            "word_count": word_count,
            "char_count": char_count,
            "upper_trigram": (word_count % 8) or 8,
            "lower_trigram": (char_count % 8) or 8,
            "moving_line": ((word_count + char_count) % 6) or 6,
        },
        "direction_based": {
            "category": categories[0] if categories else "other",
            "direction": direction_info[0],
            "trigram_name": direction_info[1],
            "trigram_number": direction_info[2],
        },
        "measurement_based": {
            "days": days_until or 0,
            "prob_percent": prob_int,
            "upper_trigram": ((days_until or 0) % 8) or 8,
            "lower_trigram": (prob_int % 8) or 8,
            "moving_line": (((days_until or 0) + prob_int) % 6) or 6,
        },
    }


# CLI for testing
if __name__ == "__main__":
    client = PolymarketClient()

    print("Fetching active markets...")
    markets = client.get_markets(
        limit=5,
        closed=False,
        volume_min=1000,
        end_date_min=datetime.now(),
        end_date_max=datetime.now() + timedelta(days=30),
    )

    print(f"\nFound {len(markets)} markets:\n")
    for m in markets:
        formatted = format_market_for_experiment(m)
        print(f"Title: {formatted['title'][:60]}...")
        print(f"  Prob: {formatted['core_data']['current_prob']}")
        print(f"  Volume: ${formatted['core_data']['volume_usd']:,.0f}")
        print(f"  Days: {formatted['core_data']['days_until_resolution']}")
        print(f"  URL: {formatted['url']}")
        print()
