#!/usr/bin/env python3
"""
Market Selector

Randomly selects eligible markets from Polymarket for the experiment.
No human judgment - purely random selection from filtered pool.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import os

from polymarket_client import PolymarketClient, format_market_for_experiment


class MarketSelector:
    """Selects eligible markets for the Meihua experiment."""

    # Exclusion keywords (markets to skip)
    EXCLUDE_KEYWORDS = [
        "sports", "nfl", "nba", "mlb", "nhl", "soccer", "football",
        "game", "match", "score", "winner", "playoff", "championship",
        "celebrity", "kardashian", "taylor swift",
        "this market", "polymarket",  # Self-referential
    ]

    # Minimum thresholds
    MIN_VOLUME = 1000  # $1,000 minimum volume
    MIN_PROBABILITY = 0.15  # Not too one-sided
    MAX_PROBABILITY = 0.85  # Not too one-sided
    MIN_DAYS = 3  # At least 3 days to resolution
    MAX_DAYS = 60  # Not too far out

    def __init__(self):
        self.client = PolymarketClient()

    def fetch_eligible_markets(self, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch markets that meet basic criteria from API."""
        now = datetime.now()

        markets = self.client.get_markets(
            limit=limit,
            closed=False,
            volume_min=self.MIN_VOLUME,
            end_date_min=now + timedelta(days=self.MIN_DAYS),
            end_date_max=now + timedelta(days=self.MAX_DAYS),
            order="volume",
            ascending=False,
        )

        return markets

    def is_eligible(self, market: Dict[str, Any]) -> tuple[bool, str]:
        """
        Check if a market is eligible for the experiment.
        Returns: (is_eligible, reason)
        """
        # Must have a question
        question = market.get("question", "").lower()
        if not question:
            return False, "No question"

        # Check exclusion keywords
        for keyword in self.EXCLUDE_KEYWORDS:
            if keyword in question:
                return False, f"Excluded keyword: {keyword}"

        # Must have order book enabled (tradeable)
        if not market.get("enableOrderBook"):
            return False, "Order book disabled"

        # Must be active and not closed
        if market.get("closed"):
            return False, "Market closed"
        if not market.get("active", True):
            return False, "Market inactive"

        # Check probability range
        prob = None
        if market.get("lastTradePrice"):
            prob = float(market["lastTradePrice"])
        elif market.get("bestAsk"):
            prob = float(market["bestAsk"])

        if prob is not None:
            if prob < self.MIN_PROBABILITY:
                return False, f"Probability too low: {prob:.2f}"
            if prob > self.MAX_PROBABILITY:
                return False, f"Probability too high: {prob:.2f}"

        return True, "Eligible"

    # Category mapping for stratification
    CATEGORY_KEYWORDS = {
        "politics": ["election", "president", "congress", "senate", "vote", "trump", "biden", "political", "government"],
        "crypto": ["bitcoin", "ethereum", "crypto", "btc", "eth", "token", "blockchain"],
        "finance": ["stock", "market", "fed", "interest rate", "inflation", "gdp", "economic"],
        "tech": ["ai", "openai", "google", "apple", "microsoft", "tech", "software", "spacex"],
        "science": ["climate", "research", "study", "scientific", "nasa", "space"],
        "legal": ["court", "lawsuit", "legal", "trial", "judge", "conviction"],
        "entertainment": ["movie", "oscar", "grammy", "award", "show", "netflix"],
        "world": ["china", "russia", "ukraine", "war", "international", "foreign"],
    }

    def categorize_market(self, market: Dict[str, Any]) -> str:
        """Categorize a market based on its title and tags."""
        title = market.get("question", "").lower()
        tags = [t.get("label", "").lower() for t in market.get("tags", [])]
        text = title + " " + " ".join(tags)

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return category

        return "other"

    def select_random(
        self,
        n: int = 20,
        seed: Optional[int] = None,
        exclude_ids: Optional[List[str]] = None,
        stratify: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Randomly select N eligible markets with optional stratification.

        Args:
            n: Number of markets to select
            seed: Random seed for reproducibility
            exclude_ids: Market IDs to exclude (already in experiment)
            stratify: If True, balance selection across categories

        Returns:
            List of formatted market data
        """
        if seed is not None:
            random.seed(seed)

        exclude_ids = exclude_ids or []

        # Fetch candidates
        print(f"Fetching markets from Polymarket...")
        raw_markets = self.fetch_eligible_markets(limit=300)
        print(f"Fetched {len(raw_markets)} markets from API")

        # Filter eligible and categorize
        eligible_by_category: Dict[str, List] = {}
        for m in raw_markets:
            market_id = m.get("id") or m.get("conditionId")
            if market_id in exclude_ids:
                continue

            is_elig, reason = self.is_eligible(m)
            if is_elig:
                category = self.categorize_market(m)
                if category not in eligible_by_category:
                    eligible_by_category[category] = []
                eligible_by_category[category].append(m)

        total_eligible = sum(len(v) for v in eligible_by_category.values())
        print(f"Found {total_eligible} eligible markets (excluding {len(exclude_ids)} already selected)")
        print(f"Categories: {', '.join(f'{k}({len(v)})' for k, v in eligible_by_category.items())}")

        selected = []

        if stratify and len(eligible_by_category) > 1:
            # Stratified sampling: equal from each category
            categories = list(eligible_by_category.keys())
            per_category = max(1, n // len(categories))
            remainder = n % len(categories)

            random.shuffle(categories)  # Randomize which categories get remainder

            for i, cat in enumerate(categories):
                cat_n = per_category + (1 if i < remainder else 0)
                cat_markets = eligible_by_category[cat]
                cat_sample = min(cat_n, len(cat_markets))
                selected.extend(random.sample(cat_markets, cat_sample))

            # If we still need more, fill from any category
            while len(selected) < n:
                all_remaining = [m for cat in eligible_by_category.values() for m in cat if m not in selected]
                if not all_remaining:
                    break
                selected.append(random.choice(all_remaining))

            print(f"Stratified selection: {len(selected)} markets across {len(categories)} categories")
        else:
            # Simple random sample
            all_eligible = [m for cat in eligible_by_category.values() for m in cat]
            if len(all_eligible) < n:
                print(f"Warning: Only {len(all_eligible)} eligible markets available")
                n = len(all_eligible)
            selected = random.sample(all_eligible, n)
            print(f"Randomly selected {n} markets")

        # Format for experiment
        formatted = [format_market_for_experiment(m) for m in selected]

        # Report category distribution
        cat_dist = {}
        for m in formatted:
            cat = m['meihua_inputs']['direction_based']['category']
            cat_dist[cat] = cat_dist.get(cat, 0) + 1
        print(f"Final distribution: {cat_dist}")

        return formatted


# CLI
if __name__ == "__main__":
    import sys

    selector = MarketSelector()

    n = 10  # Default
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except:
            pass

    print(f"\n=== Market Selection ===\n")
    markets = selector.select_random(n=n)

    print(f"\n=== Selected Markets ===\n")
    for i, m in enumerate(markets, 1):
        print(f"{i}. {m['title'][:70]}...")
        prob = m['core_data']['current_prob']
        vol = m['core_data']['volume_usd']
        days = m['core_data']['days_until_resolution']
        print(f"   Prob: {prob:.1%} | Vol: ${vol:,.0f} | Days: {days}")
        print()
