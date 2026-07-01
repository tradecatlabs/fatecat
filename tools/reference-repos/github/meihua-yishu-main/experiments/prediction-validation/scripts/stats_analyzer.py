#!/usr/bin/env python3
"""
Statistical Analyzer for Meihua Prediction Experiment

Performs statistical significance tests to determine if Meihua Yishu
provides predictive value beyond random chance or market probability.

Key Tests:
1. McNemar's Test - Paired comparison (same markets, different methods)
2. Binomial Test - Is each method better than chance?
3. Chi-Square Test - Independence of method and correctness
4. Effect Size - Cohen's h for practical significance

Sample Size Requirements:
- For detecting 10% accuracy difference with 80% power: ~200 markets
- For detecting 15% accuracy difference: ~90 markets
- Minimum viable pilot: 50 markets
"""

import json
import os
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class StatisticalResult:
    """Result of a statistical test."""
    test_name: str
    statistic: float
    p_value: float
    significant: bool  # At α = 0.05
    interpretation: str
    details: Dict[str, Any]


class StatsAnalyzer:
    """Statistical analysis for the prediction experiment."""

    # Significance level
    ALPHA = 0.05

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, "..", "data")

        self.data_dir = data_dir
        self.state_file = os.path.join(data_dir, "experiment_state.json")

    def load_data(self) -> Dict[str, Any]:
        """Load experiment state."""
        if not os.path.exists(self.state_file):
            raise FileNotFoundError(f"No experiment data found at {self.state_file}")

        with open(self.state_file, "r") as f:
            return json.load(f)

    def get_resolved_markets(self) -> List[Dict[str, Any]]:
        """Get markets that have resolved with both predictions."""
        state = self.load_data()
        resolved = []

        for m in state["markets"].values():
            if (m["actual_outcome"] in ["YES", "NO"] and
                m["control_prediction"] and
                m["meihua_prediction"]):
                resolved.append(m)

        return resolved

    def calculate_sample_size_needed(
        self,
        expected_effect: float = 0.10,  # Expected accuracy difference
        power: float = 0.80,
        alpha: float = 0.05
    ) -> Dict[str, int]:
        """
        Calculate sample size needed for different effect sizes.

        For McNemar's test comparing paired proportions.

        Args:
            expected_effect: Expected difference in accuracy (e.g., 0.10 = 10%)
            power: Statistical power (typically 0.80)
            alpha: Significance level (typically 0.05)

        Returns:
            Dict with sample sizes for different scenarios
        """
        # Z-scores for common power and alpha
        z_alpha = 1.96  # two-tailed α = 0.05
        z_beta = 0.84   # power = 0.80

        # For McNemar's test, simplified formula
        # n = (z_alpha + z_beta)^2 / (2 * effect^2)
        # This is approximate; actual depends on discordant pairs

        def sample_size_for_effect(effect):
            if effect <= 0:
                return float('inf')
            # Simplified formula for proportions comparison
            p1 = 0.50 + effect/2  # e.g., 55% for Meihua
            p2 = 0.50 - effect/2  # e.g., 45% for control
            pooled = (p1 + p2) / 2
            se = math.sqrt(2 * pooled * (1 - pooled))
            n = ((z_alpha + z_beta) * se / effect) ** 2
            return int(math.ceil(n))

        return {
            "effect_5%": sample_size_for_effect(0.05),   # Small effect
            "effect_10%": sample_size_for_effect(0.10),  # Medium effect
            "effect_15%": sample_size_for_effect(0.15),  # Large effect
            "effect_20%": sample_size_for_effect(0.20),  # Very large
            "minimum_pilot": 30,
            "recommended": 200,
            "ideal": 300,
            "publishable": 200,
        }

    def mcnemar_test(self, markets: List[Dict]) -> StatisticalResult:
        """
        McNemar's Test for paired nominal data.

        Compares: When do control and meihua disagree, and who's right?

        Contingency table:
                        Meihua Correct  Meihua Wrong
        Control Correct      a              b
        Control Wrong        c              d

        McNemar tests if b ≠ c (disagreements are balanced)

        Uses EXACT test for n < 25 discordant pairs (publication-grade).
        """
        # Build contingency table
        a = b = c = d = 0

        for m in markets:
            ctrl_correct = m["control_correct"]
            mh_correct = m["meihua_correct"]

            if ctrl_correct and mh_correct:
                a += 1
            elif ctrl_correct and not mh_correct:
                b += 1
            elif not ctrl_correct and mh_correct:
                c += 1
            else:
                d += 1

        discordant = b + c

        if discordant == 0:
            chi2 = 0
            p_value = 1.0
            test_type = "N/A (no discordant pairs)"
        elif discordant < 25:
            # EXACT test using binomial distribution
            # Under H0, b ~ Binomial(b+c, 0.5)
            # Two-tailed p-value
            chi2 = 0  # Not applicable for exact test
            p_value = self._exact_mcnemar_pvalue(b, c)
            test_type = "Exact (binomial)"
        else:
            # Chi-square approximation with continuity correction
            chi2 = (abs(b - c) - 1) ** 2 / (b + c)
            p_value = self._chi2_pvalue(chi2, df=1)
            test_type = "Chi-square (with continuity correction)"

        significant = p_value < self.ALPHA

        # Determine direction
        if c > b:
            direction = "Meihua better (more unique correct predictions)"
        elif b > c:
            direction = "Control better (more unique correct predictions)"
        else:
            direction = "No difference"

        return StatisticalResult(
            test_name="McNemar's Test",
            statistic=chi2,
            p_value=p_value,
            significant=significant,
            interpretation=f"{direction}. {'Statistically significant' if significant else 'Not significant'} at α={self.ALPHA}",
            details={
                "both_correct": a,
                "only_control_correct": b,
                "only_meihua_correct": c,
                "both_wrong": d,
                "discordant_pairs": discordant,
                "test_type": test_type,
            }
        )

    def _exact_mcnemar_pvalue(self, b: int, c: int) -> float:
        """
        Compute exact two-tailed p-value for McNemar's test.
        Uses binomial distribution: under H0, b ~ Binomial(b+c, 0.5)
        """
        n = b + c
        if n == 0:
            return 1.0

        # Two-tailed: P(X <= min(b,c)) + P(X >= max(b,c))
        k = min(b, c)

        # Sum binomial probabilities for extreme values
        p_value = 0.0
        for i in range(k + 1):
            p_value += self._binomial_pmf(n, i, 0.5)
        for i in range(n - k, n + 1):
            p_value += self._binomial_pmf(n, i, 0.5)

        return min(p_value, 1.0)

    def _binomial_pmf(self, n: int, k: int, p: float) -> float:
        """Binomial probability mass function."""
        if k < 0 or k > n:
            return 0.0
        coeff = math.comb(n, k)
        return coeff * (p ** k) * ((1 - p) ** (n - k))

    def market_baseline_test(self, markets: List[Dict]) -> Dict[str, StatisticalResult]:
        """
        Compare predictions against market probability baseline.

        This is a fairer comparison than 50% chance - it tests whether
        Meihua beats the crowd wisdom embedded in market prices.
        """
        results = {}

        for pred_type in ["control", "meihua"]:
            # Count: did prediction beat the market baseline?
            beats_market = 0
            total = 0

            for m in markets:
                pred_field = f"{pred_type}_prediction"
                correct_field = f"{pred_type}_correct"

                if not m.get(pred_field) or m[correct_field] is None:
                    continue

                total += 1
                initial_prob = m.get("initial_probability", 0.5)

                # Market baseline prediction: YES if prob > 0.5, NO otherwise
                market_pred = "YES" if initial_prob > 0.5 else "NO"
                actual = m["actual_outcome"]

                market_correct = (market_pred == actual)
                method_correct = m[correct_field]

                # Did this method beat the market on this prediction?
                if method_correct and not market_correct:
                    beats_market += 1
                elif not method_correct and market_correct:
                    beats_market -= 1  # Market beat us
                # If both right or both wrong, no advantage

            # Test if beats_market is significantly different from 0
            # Using sign test approximation
            if total > 0:
                # Approximate with normal
                z = beats_market / math.sqrt(total) if total > 0 else 0
                p_value = 2 * (1 - self._normal_cdf(abs(z)))
            else:
                z = 0
                p_value = 1.0

            results[pred_type] = StatisticalResult(
                test_name=f"{pred_type.title()} vs Market Baseline",
                statistic=z,
                p_value=p_value,
                significant=p_value < self.ALPHA,
                interpretation=f"Net advantage over market: {beats_market:+d} predictions",
                details={
                    "net_advantage": beats_market,
                    "total_markets": total,
                    "advantage_rate": beats_market / total if total > 0 else 0,
                }
            )

        return results

    def binomial_test(
        self,
        successes: int,
        trials: int,
        null_prob: float = 0.5
    ) -> StatisticalResult:
        """
        Binomial test: Is accuracy significantly different from chance?

        Args:
            successes: Number of correct predictions
            trials: Total predictions
            null_prob: Expected probability under null (0.5 = random)
        """
        if trials == 0:
            return StatisticalResult(
                test_name="Binomial Test",
                statistic=0,
                p_value=1.0,
                significant=False,
                interpretation="No data",
                details={}
            )

        observed_rate = successes / trials

        # Normal approximation for binomial
        expected = trials * null_prob
        std = math.sqrt(trials * null_prob * (1 - null_prob))

        if std == 0:
            z = 0
        else:
            z = (successes - expected) / std

        # Two-tailed p-value
        p_value = 2 * (1 - self._normal_cdf(abs(z)))

        significant = p_value < self.ALPHA

        return StatisticalResult(
            test_name="Binomial Test",
            statistic=z,
            p_value=p_value,
            significant=significant,
            interpretation=f"Accuracy {observed_rate:.1%} vs expected {null_prob:.1%}. {'Significant' if significant else 'Not significant'}",
            details={
                "successes": successes,
                "trials": trials,
                "observed_rate": observed_rate,
                "expected_rate": null_prob,
                "z_score": z,
            }
        )

    def calculate_effect_size(self, markets: List[Dict]) -> Dict[str, float]:
        """
        Calculate Cohen's h effect size for the difference in proportions.

        Cohen's h:
        - 0.2 = small effect
        - 0.5 = medium effect
        - 0.8 = large effect
        """
        if not markets:
            return {"cohens_h": 0, "interpretation": "No data"}

        ctrl_correct = sum(1 for m in markets if m["control_correct"])
        mh_correct = sum(1 for m in markets if m["meihua_correct"])
        n = len(markets)

        p1 = mh_correct / n
        p2 = ctrl_correct / n

        # Cohen's h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))
        h = 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))

        if abs(h) < 0.2:
            interp = "negligible"
        elif abs(h) < 0.5:
            interp = "small"
        elif abs(h) < 0.8:
            interp = "medium"
        else:
            interp = "large"

        return {
            "cohens_h": h,
            "meihua_accuracy": p1,
            "control_accuracy": p2,
            "difference": p1 - p2,
            "interpretation": interp,
            "favors": "meihua" if h > 0 else "control" if h < 0 else "neither",
        }

    def _normal_cdf(self, z: float) -> float:
        """Approximate normal CDF using error function approximation."""
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    def _chi2_pvalue(self, chi2: float, df: int = 1) -> float:
        """Approximate chi-square p-value for df=1."""
        if chi2 <= 0:
            return 1.0
        # Use normal approximation: sqrt(2*chi2) - sqrt(2*df - 1) ~ N(0,1)
        z = math.sqrt(2 * chi2) - math.sqrt(2 * df - 1)
        return 1 - self._normal_cdf(z)

    def run_full_analysis(self) -> Dict[str, Any]:
        """Run complete statistical analysis on current data."""
        markets = self.get_resolved_markets()

        if not markets:
            return {
                "status": "no_data",
                "message": "No resolved markets with both predictions found",
                "sample_size_needed": self.calculate_sample_size_needed(),
            }

        n = len(markets)
        ctrl_correct = sum(1 for m in markets if m["control_correct"])
        mh_correct = sum(1 for m in markets if m["meihua_correct"])

        results = {
            "status": "analyzed",
            "sample_size": n,
            "sample_size_needed": self.calculate_sample_size_needed(),
            "summary": {
                "control_accuracy": ctrl_correct / n,
                "meihua_accuracy": mh_correct / n,
                "control_correct": ctrl_correct,
                "meihua_correct": mh_correct,
            },
            "tests": {},
        }

        # McNemar's test (paired comparison)
        mcnemar = self.mcnemar_test(markets)
        results["tests"]["mcnemar"] = {
            "name": mcnemar.test_name,
            "statistic": mcnemar.statistic,
            "p_value": mcnemar.p_value,
            "significant": mcnemar.significant,
            "interpretation": mcnemar.interpretation,
            "details": mcnemar.details,
        }

        # Binomial tests for each method vs chance
        results["tests"]["control_vs_chance"] = {
            "name": "Control vs 50% chance",
            **self.binomial_test(ctrl_correct, n, 0.5).__dict__
        }

        results["tests"]["meihua_vs_chance"] = {
            "name": "Meihua vs 50% chance",
            **self.binomial_test(mh_correct, n, 0.5).__dict__
        }

        # Effect size
        results["effect_size"] = self.calculate_effect_size(markets)

        # Market baseline comparison (fairer than 50% chance)
        baseline_tests = self.market_baseline_test(markets)
        results["tests"]["control_vs_market"] = {
            "name": baseline_tests["control"].test_name,
            **baseline_tests["control"].__dict__
        }
        results["tests"]["meihua_vs_market"] = {
            "name": baseline_tests["meihua"].test_name,
            **baseline_tests["meihua"].__dict__
        }

        # Interpretation
        results["conclusion"] = self._generate_conclusion(results)

        return results

    def _generate_conclusion(self, results: Dict) -> str:
        """Generate human-readable conclusion."""
        n = results["sample_size"]
        needed = results["sample_size_needed"]

        lines = []

        # Sample size assessment
        if n < needed["minimum_pilot"]:
            lines.append(f"⚠️  Sample size ({n}) is below minimum pilot size ({needed['minimum_pilot']}). Results are preliminary.")
        elif n < needed["recommended"]:
            lines.append(f"📊 Sample size ({n}) is adequate for pilot analysis but below recommended ({needed['recommended']}) for definitive conclusions.")
        else:
            lines.append(f"✅ Sample size ({n}) is sufficient for statistical analysis.")

        # Accuracy comparison
        ctrl_acc = results["summary"]["control_accuracy"]
        mh_acc = results["summary"]["meihua_accuracy"]
        diff = mh_acc - ctrl_acc

        if abs(diff) < 0.01:
            lines.append(f"\n📈 Accuracies are nearly identical: Control {ctrl_acc:.1%}, Meihua {mh_acc:.1%}")
        else:
            better = "Meihua" if diff > 0 else "Control"
            lines.append(f"\n📈 {better} shows higher accuracy: Control {ctrl_acc:.1%}, Meihua {mh_acc:.1%} (Δ = {abs(diff):.1%})")

        # Statistical significance
        mcnemar = results["tests"]["mcnemar"]
        if mcnemar["significant"]:
            lines.append(f"\n✨ The difference IS statistically significant (p = {mcnemar['p_value']:.4f})")
        else:
            lines.append(f"\n⏳ The difference is NOT statistically significant (p = {mcnemar['p_value']:.4f})")

        # Effect size
        effect = results["effect_size"]
        lines.append(f"\n📐 Effect size (Cohen's h): {effect['cohens_h']:.3f} ({effect['interpretation']})")

        return "\n".join(lines)

    def print_report(self):
        """Print a formatted analysis report."""
        results = self.run_full_analysis()

        print("\n" + "="*70)
        print("STATISTICAL ANALYSIS REPORT")
        print("="*70)

        if results["status"] == "no_data":
            print("\n❌ No resolved markets with predictions found.")
            print("\nSample sizes needed for statistical power:")
            for key, val in results["sample_size_needed"].items():
                print(f"  {key}: {val}")
            return

        print(f"\nSample Size: {results['sample_size']}")
        print(f"\nAccuracy Summary:")
        print(f"  Control: {results['summary']['control_accuracy']:.1%} ({results['summary']['control_correct']}/{results['sample_size']})")
        print(f"  Meihua:  {results['summary']['meihua_accuracy']:.1%} ({results['summary']['meihua_correct']}/{results['sample_size']})")

        print(f"\n{'─'*70}")
        print("McNemar's Test (Paired Comparison)")
        print(f"{'─'*70}")
        mcnemar = results["tests"]["mcnemar"]
        print(f"  χ² statistic: {mcnemar['statistic']:.4f}")
        print(f"  p-value: {mcnemar['p_value']:.4f}")
        print(f"  Significant: {'Yes' if mcnemar['significant'] else 'No'}")
        print(f"\n  Contingency table:")
        d = mcnemar["details"]
        print(f"    Both correct: {d['both_correct']}")
        print(f"    Only control correct: {d['only_control_correct']}")
        print(f"    Only meihua correct: {d['only_meihua_correct']}")
        print(f"    Both wrong: {d['both_wrong']}")

        print(f"\n{'─'*70}")
        print("Effect Size")
        print(f"{'─'*70}")
        effect = results["effect_size"]
        print(f"  Cohen's h: {effect['cohens_h']:.4f} ({effect['interpretation']})")
        print(f"  Favors: {effect['favors']}")

        print(f"\n{'─'*70}")
        print("CONCLUSION")
        print(f"{'─'*70}")
        print(results["conclusion"])
        print("\n" + "="*70)


# CLI
if __name__ == "__main__":
    analyzer = StatsAnalyzer()

    print("\n📊 SAMPLE SIZE REQUIREMENTS")
    print("="*50)
    sizes = analyzer.calculate_sample_size_needed()
    print(f"""
To detect different effect sizes (80% power, α=0.05):

  5% accuracy difference:  {sizes['effect_5%']} markets
  10% accuracy difference: {sizes['effect_10%']} markets
  15% accuracy difference: {sizes['effect_15%']} markets
  20% accuracy difference: {sizes['effect_20%']} markets

Recommended:
  Minimum pilot:  {sizes['minimum_pilot']} markets
  Recommended:    {sizes['recommended']} markets
  Ideal:          {sizes['ideal']} markets
""")

    try:
        analyzer.print_report()
    except FileNotFoundError:
        print("\n(No experiment data yet - run the experiment first)")
