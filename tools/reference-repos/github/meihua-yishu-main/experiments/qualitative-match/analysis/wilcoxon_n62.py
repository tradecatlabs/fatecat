#!/usr/bin/env python3
"""
Final n=62 analysis for the qualitative-match experiment (batches 1-3).

One-tailed Wilcoxon signed-rank, H1: real > control, ties dropped
(zero_method="wilcox"), matching all prior interim reports.

Data sources:
  - Prior 47 scored pairs: transcribed from protocol.md status trackers
    (batch1 E01-E12, batch2 E13-E32, batch3 15 scored events).
  - New 15 pairs: A/B scores from evaluations/scoring_notes_2026-06-14.md,
    unblinded via interpretations/blinding_key_batch3.json at runtime.

Run from anywhere; paths are resolved relative to this file.
"""
import json
import os
from collections import OrderedDict

from scipy.stats import wilcoxon

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(HERE, "..", "interpretations", "blinding_key_batch3.json")

# --- Prior 47 scored pairs: (event, real, control) from protocol.md trackers ---
BATCH1 = [
    ("E01", 2, 4), ("E02", 5, 1), ("E03", 3, 4), ("E04", 2, 4),
    ("E05", 3, 1), ("E06", 4, 3), ("E07", 3, 2), ("E08", 3, 4),
    ("E09", 3, 4), ("E10", 4, 3), ("E11", 4, 1), ("E12", 4, 3),
]
BATCH2 = [
    ("E13", 4, 2), ("E14", 2, 4), ("E15", 3, 4), ("E16", 3, 3),
    ("E17", 4, 1), ("E18", 5, 1), ("E19", 3, 1), ("E20", 5, 3),
    ("E21", 3, 2), ("E22", 4, 2), ("E23", 2, 3), ("E24", 3, 4),
    ("E25", 5, 2), ("E26", 3, 2), ("E27", 3, 4), ("E28", 5, 2),
    ("E29", 3, 2), ("E30", 4, 2), ("E31", 5, 3), ("E32", 2, 4),
]
BATCH3_PRIOR = [
    ("E33", 2, 5), ("E35", 3, 1), ("E36", 4, 5), ("E37", 5, 1),
    ("E38", 4, 3), ("E39", 3, 3), ("E40", 5, 1), ("E43", 4, 3),
    ("E44", 4, 3), ("E45", 1, 5), ("E46", 5, 2), ("E47", 3, 4),
    ("E48", 5, 1), ("E49", 2, 3), ("E60", 5, 2),
]

# --- New 15 events: A/B scores from scoring_notes_2026-06-14.md ---
NEW_AB = OrderedDict([
    ("E34", (3, 0)), ("E41", (3, 3)), ("E42", (2, 4)), ("E50", (3, 3)),
    ("E51", (1, 2)), ("E52", (2, 4)), ("E53", (1, 2)), ("E54", (2, 1)),
    ("E55", (3, 3)), ("E56", (2, 3)), ("E57", (4, 1)), ("E58", (2, 3)),
    ("E59", (1, 4)), ("E61", (3, 2)), ("E62", (3, 2)),
])


def unblind_new():
    key = {e["event_id"]: e["real_is_A"] for e in json.load(open(KEY_PATH))["events"]}
    out = []
    for eid, (a, b) in NEW_AB.items():
        real, control = (a, b) if key[eid] else (b, a)
        out.append((eid, real, control))
    return out


def stats(pairs, label):
    real = [r for _, r, _ in pairs]
    ctrl = [c for _, _, c in pairs]
    diffs = [r - c for r, c in zip(real, ctrl)]
    wins = sum(d > 0 for d in diffs)
    losses = sum(d < 0 for d in diffs)
    ties = sum(d == 0 for d in diffs)
    n_eff = wins + losses
    rmean = sum(real) / len(real)
    cmean = sum(ctrl) / len(ctrl)
    res = wilcoxon(real, ctrl, alternative="greater", zero_method="wilcox")
    print(f"--- {label} (n={len(pairs)}) ---")
    print(f"  real mean    : {rmean:.3f}")
    print(f"  control mean : {cmean:.3f}")
    print(f"  mean diff    : {rmean - cmean:+.3f}")
    print(f"  win record   : {wins}-{losses}-{ties} (R-C-T)")
    print(f"  n_effective  : {n_eff}  (ties dropped)")
    print(f"  Wilcoxon W+  : {res.statistic:.1f}")
    print(f"  p (1-tailed) : {res.pvalue:.4f}")
    print()
    return rmean, cmean, wins, losses, ties, res


def main():
    new = unblind_new()
    prior = BATCH1 + BATCH2 + BATCH3_PRIOR

    print("=" * 56)
    print("FINAL QUALITATIVE-MATCH ANALYSIS (n=62)")
    print("=" * 56)
    print()

    # Sanity: prior 47 must reproduce the published p=0.0045
    stats(prior, "PRIOR 47 (published interim — sanity check)")

    stats(BATCH1, "Batch 1 — mechanical")
    stats(BATCH2, "Batch 2 — 取象法 plain LLM")
    stats(BATCH3_PRIOR + new, "Batch 3 — 取象法 full skill (now complete)")
    stats(new, "NEW 15 (final resolved events)")
    stats(prior + new, "COMBINED FINAL")


if __name__ == "__main__":
    main()
