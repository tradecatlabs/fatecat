# Qualitative Match Experiment — Final Results (n=62)
# 梅花易數質性匹配實驗 — 最終結果

**Date**: 2026-06-14
**Status**: Phase 6 complete (batches 1–3 fully resolved, scored, unblinded).
**Events**: 62 of 62 scored. Experiment closed.

---

## Headline

**The effect weakened to p = 0.021 (one-tailed Wilcoxon, n=62) — significant at 0.05 but no longer at 0.01.** The final 15 events, which resolved through late May, **regressed against the hypothesis** (real 2.20 vs. control 2.60, a −0.40 mean difference, 5–7–3 record favoring the control). The 2026-05-02 interim report explicitly warned the result would hold "unless the remaining events regress hard." They regressed hard.

Two things drove the drop, and both matter:

1. **Batch 3 (full-skill 取象法), now complete at n=30, is null** — mean diff +0.23, p = 0.27. Its earlier apparent trend (+0.87 at n=15) was an artifact of which events happened to resolve first.
2. **The final 15 were scored under a stricter protocol** — a *separate* blinded narrator subagent and a *separate* blinded scorer subagent, neither sharing context. Every prior round used **one agent as both narrator and scorer**, an acknowledged leak risk. When that leak was removed, the signal disappeared. This is suggestive, not conclusive (n=15), but it points the same direction the unstarted batch 4 was designed to test.

---

## Final results by batch

| Batch | Method | n | Real | Ctrl | Diff | Record (R–C–T) | p (1-tail) |
|---|---|---:|---:|---:|---:|---|---:|
| 1 | Mechanical (字數→數字) | 12 | 3.33 | 2.83 | +0.50 | 7–5–0 | 0.260 |
| 2 | 取象法 plain LLM | 20 | 3.55 | 2.55 | **+1.00** | 13–6–1 | **0.011** |
| 3 | 取象法 full skill (complete) | 30 | 2.93 | 2.70 | +0.23 | 14–12–4 | 0.268 |
| — *of which: new 15* | (rigorous split-role scoring) | 15 | 2.20 | 2.60 | **−0.40** | 5–7–3 | 0.789 |
| **Combined** | — | **62** | **3.21** | **2.68** | **+0.53** | **34–23–5** | **0.021** |

n_effective (combined) = 57; ties dropped (E16, E39, E41, E50, E55), zero_method="wilcox".

### Trajectory of the combined p-value
| Snapshot | n | Mean diff | p (1-tail) |
|---|---:|---:|---:|
| 2026-03-18 | 19 | +0.58 | 0.139 |
| 2026-04-15 | 37 | +0.78 | 0.011 |
| 2026-05-02 | 47 | +0.83 | 0.0045 |
| **2026-06-14 (final)** | **62** | **+0.53** | **0.021** |

The p-value bottomed out mid-experiment and rose as the harder-to-game (later, stricter-scored) events came in.

---

## What survives and what doesn't

| Claim | Verdict |
|---|---|
| "Real hexagrams describe events better than random" | **Weakly supported** overall (p=0.021), but fragile and method-dependent. |
| "The full meihua-yishu skill matches better than plain LLM 取象法" | **Refuted.** Full-skill batch 3 is null (p=0.27); plain-LLM batch 2 is the only individually-significant batch (p=0.011). The wrapper did not help. |
| "Mechanical character-count casting works" | **Not supported** (p=0.26, as it always was — the weakest method throughout). |
| "The effect strengthens with more data" | **Refuted.** It weakened once the same-agent narrator/scorer leak was removed and batch 3 completed. |

---

## Standout cases (new 15, after unblinding)

### Controls that beat real — the honest losses
- **E34 Assam election** — real (12 否 → 33 遯, "standstill, swallowing shame, dignified retreat") scored **0** against a triumphant BJP landslide; the random control (26 大畜 → 9 小畜, "strong position maintained, opposition defanged") scored 3. The real hexagram described the *losers'* arc.
- **E57 French Open week 1** — the random control (34 大壯 → 54 歸妹, "the ram charges the hedge and entangles its own horns — strength defeats itself") scored **4**, a near-perfect image for a week of top seeds crashing out. Real (24 復 → 27 頤) scored 1.
- **E59 Dell Tech World** — control (8 比 → 2 坤, "alliance under a center becoming the foundation others build on") scored **4** for the "AI Factory" partner-ecosystem platform play. Real (44 姤 → 28 大過, "ridgepole bending under load") scored 1.

### Real hexagrams that landed
- **E42 NHL playoffs R1** — real (3 屯 → 17 隨, "primordial chaos, hard-won partnership from a stumbling start; those who charge alone are swallowed by the storm") scored 4 for an upset-laden round that eliminated three of four top seeds. Control scored 2.
- **E52 Met Gala** — real (38 睽 → 10 履, "treading on a tiger's tail with composure, radiance from proximity to what could consume you") scored 4 for a high-stakes red-carpet spectacle. Control scored 2.
- **E62 UEFA Champions League Final** — real (25 无妄 → 21 噬嗑, "endure first, then bite decisively") scored 3 for a 1–1 final settled only on penalties. Control scored 2.

The round was genuinely mixed; the controls simply hit more of the striking matches this time.

---

## Limitations (fail-loud)

1. **Tautology — still unaddressed.** Real hexagrams are chosen from event semantics (取象法) while controls are drawn uniformly at random. A real-vs-control gap can partly reflect "imagery-loaded text fits events better than arbitrary text," independent of whether the hexagram is *correct*. Batch 4 (displaced 取象法 controls) was designed to kill this critique and **was never run**. Until it is, even the surviving p=0.021 cannot be cleanly attributed to the divination method.
2. **Narrator/scorer leak (now partially measured).** Batches 1–3's first 47 events used one agent as both narrator and scorer. The final 15 split these into separate blinded subagents — and the effect vanished in that subset. This is the single most important caveat: the headline interim significance may have been partly a same-agent artifact.
3. **Single underlying model.** Narrator, scorer, and original caster are all the same model family. No human scorer, no inter-rater reliability.
4. **Event drift.** E54 (Mortal Kombat II) opened May 8 not May 15 (outcome window intact); E61 (Colombia) resolved as a first round into a June 21 runoff, scored on the first-round outcome as designed; all 15 were scoreable. No events were dropped.
5. **Multiple methods pooled.** The combined n=62 mixes three casting methods of differing quality. The combined p leans on batch 2; pooling a null batch 1 and null batch 3 with it is generous to the hypothesis.

---

## Bottom line

The experiment ends **weakly positive and badly weakened from its peak**. The cleanest reading: plain-LLM 取象法 (batch 2) showed a real descriptive-fit effect (p=0.011); the full skill did not improve on it and its complete batch is null; and the effect shrank precisely when the scoring leak was closed. The honest next step is **batch 4** — displaced controls + separated cold-session roles + pre-registered n — which would determine whether anything survives once both the tautology and the leak are controlled. Without it, the strongest defensible claim is "suggestive, not established."

---

## Reproduction

```
python3 analysis/wilcoxon_n62.py
```
Reproduces every table above. The script's first block re-derives the published n=47 result (p=0.0045) as a transcription sanity check; it matches exactly.
