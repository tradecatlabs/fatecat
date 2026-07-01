# Qualitative Match Experiment Protocol

**Started**: 2026-02-24
**Predecessor**: prediction-validation (binary, N=100, 51% result)

## What This Tests

The previous experiment forced Meihua into binary YES/NO and got coin-flip results. This experiment tests the actual claim: do hexagrams describe the **qualitative character** of situations better than random?

## Design

Three batches, tested separately due to different casting methods:

### Batch 1 (E01-E12)
- 12 upcoming events (Feb 27 - Mar 15, 2026)
- **Casting method**: Mechanical text-based (character count → trigram numbers)
- Control seed: `20260224`
- Each event gets 2 hexagram interpretations (real + control, blinded A/B)

### Batch 2 (E13-E32)
- 20 upcoming events (Mar 8 - Apr 12, 2026)
- **Casting method**: 取象法 (imagery-based — analyze event title semantics → map to bagua類象)
- Control seed: `20260305`, blinding seed: `20260306`
- Each event gets 2 hexagram interpretations (real + control, blinded A/B)
- Full skill output recorded for each real hexagram (取象理由, 體用, 策略, 爻位風險)

### Shared
- Interpretations written BEFORE events happen
- Blinded evaluation AFTER events resolve
- Wilcoxon signed-rank test on paired scores
- Batches analyzed separately, then combined if methods prove comparable

## Batch 1 Status Tracker

| Event | Cast | Interpreted | Resolved | Narrated | Scored |
|-------|------|------------|----------|----------|--------|
| E01 Apple Launch | Done | Done | Done (Mar 2-4) | Done | R=2, C=4 |
| E02 Lunar Eclipse | Done | Done | Done (Mar 3) | Done | R=5, C=1 ⭐ |
| E03 SpaceX Starship | Done | Done | Done (delayed) | Done | R=3, C=4 |
| E04 Tariff Challenge | Done | Done | Done (~Mar 7) | Done | R=2, C=4 |
| E05 Iran-US Crisis | Done | Done | Done (~Mar 10) | Done | R=3, C=1 |
| E06 Ukraine-Russia Talks | Done | Done | Done (~Mar 10) | Done | R=4, C=3 |
| E07 CL R16 Draw | Done | Done | Done (Feb 27) | Done | R=3, C=2 |
| E08 World Baseball Classic | Done | Done | Done (Mar 5-18) | Done | R=3, C=4 |
| E09 Oscars | Done | Done | Done (Mar 15) | Done | R=3, C=4 |
| E10 March Madness | Done | Done | Done (Mar 15) | Done | R=4, C=3 |
| E11 SOTU Aftermath | Done | Done | Done (Mar 3) | Done | R=4, C=1 ⭐ |
| E12 Blizzard/Polar Vortex | Done | Done | Done (~Mar 7) | Done | R=4, C=3 |

## Batch 2 Status Tracker

| Event | Domain | Cast | Interpreted | Resolved | Narrated | Scored |
|-------|--------|------|------------|----------|----------|--------|
| E13 F1 Australian GP | Sports | Done | Done | Done (Mar 8) | Done | R=4, C=2 |
| E14 Colombia Election | Politics | Done | Done | Done (Mar 8) | Done | R=2, C=4 |
| E15 WGA Awards | Culture | Done | Done | Done (Mar 8) | Done | R=3, C=4 |
| E16 Georgia Special Election | Politics | Done | Done | Done (Mar 10) | Done | R=3, C=3 |
| E17 Pixar Hoppers Box Office | Culture | Done | Done | Done (Mar 8) | Done | R=4, C=1 ⭐ |
| E18 NVIDIA GTC Keynote | Technology | Done | Done | Done (Mar 17) | Done | R=5, C=1 ⭐ |
| E19 FOMC Rate Decision | Economy | Done | Done | Done (Mar 18) | Done | R=3, C=1 |
| E20 EU Council Summit | International | Done | Done | Done (Mar 19-20) | Done | R=5, C=3 |
| E21 Project Hail Mary Premiere | Culture | Done | Done | Done (Mar 20) | Done | R=3, C=2 |
| E22 World Indoor Athletics | Sports | Done | Done | Done (Mar 20-22) | Done | R=4, C=2 |
| E23 South Australia Election | Politics | Done | Done | Done (Mar 21) | Done | R=2, C=3 |
| E24 UN Fraud Summit | International | Done | Done | Done (Mar 16-17) | Done | R=3, C=4 |
| E25 Miami Open Tennis Final | Sports | Done | Done | Done (Mar 29) | Done | R=5, C=2 ⭐ |
| E26 F1 Japanese GP Suzuka | Sports | Done | Done | Done (Mar 29) | Done | R=3, C=2 |
| E27 NCAA Championship Game | Sports | Done | Done | Done (Apr 6) | Done | R=3, C=4 |
| E28 Masters Golf | Sports | Done | Done | Done (Apr 12) | Done | R=5, C=2 ⭐ |
| E29 Peru Presidential Election | Politics | Done | Done | Done (Apr 12) | Done | R=3, C=2 |
| E30 Hungary Parliamentary Election | Politics | Done | Done | Done (Apr 12) | Done | R=4, C=2 |
| E31 NASA Artemis II | Science/Space | Done | Done | Done (Apr 1-10) | Done | R=5, C=3 ⭐ |
| E32 ISRO Gaganyaan Test | Science/Space | Done | Done | Done (Apr 10 IADT-02) | Done | R=2, C=4 |

## Workflow

1. **Phase 1**: Select events + cast hexagrams (DONE — both batches)
2. **Phase 2**: Write blinded interpretations (DONE — both batches)
3. **Phase 3**: Wait for events to resolve (Feb 27 - Apr 12)
4. **Phase 4**: Write factual narratives (blinded narrator, no hexagram access)
5. **Phase 5**: Score interpretations (blinded evaluator, 0-5 scale)
6. **Phase 6**: Unblind + statistical analysis (Wilcoxon signed-rank)

## Files

```
qualitative-match/
├── protocol.md                          (this file)
├── events/
│   └── event_registry.json              (12 batch 1 events)
├── hexagrams/
│   ├── casting_records.json             (batch 1: real + control + blinding)
│   ├── random_seed.txt                  (batch 1 seed: 20260224)
│   ├── casting_records_batch2.json      (batch 2: real + control + blinding)
│   ├── random_seed_batch2.txt           (batch 2 seed: 20260305)
│   └── generate_batch2.py              (batch 2 generation script)
├── interpretations/
│   ├── E01_A.md ... E12_B.md            (24 batch 1 blinded interpretations)
│   ├── E13_A.md ... E32_B.md            (40 batch 2 blinded interpretations)
│   ├── blinding_key.json                (batch 1 — SEALED until evaluation)
│   └── blinding_key_batch2.json         (batch 2 — SEALED until evaluation)
├── evaluations/                         (empty until Phase 5)
└── analysis/                            (empty until Phase 6)
```

## Key Dates

### Batch 1
- **Feb 27**: Champions League draw (first event!)
- **Mar 2-4**: Apple launch, Lunar eclipse, SOTU aftermath
- **Mar 5-11**: World Baseball Classic, Blizzard aftermath
- **Mar 7-9**: SpaceX Starship, Tariff challenges
- **Mar 10**: Iran-US crisis, Ukraine-Russia talks
- **Mar 15**: Oscars + March Madness Selection Sunday

### Batch 2
- **Mar 8**: F1 Australian GP, Colombia election, WGA Awards, Pixar Hoppers
- **Mar 10**: Georgia special election
- **Mar 16-17**: UN Fraud Summit
- **Mar 17-19**: NVIDIA GTC, FOMC rate decision, EU Council summit
- **Mar 20-21**: Project Hail Mary, World Indoor Athletics, South Australia election
- **Mar 29**: Miami Open final, F1 Japanese GP
- **Mar 30**: ISRO Gaganyaan test flight
- **Apr 1**: NASA Artemis II launch
- **Apr 6**: NCAA championship game
- **Apr 12**: Masters Golf, Peru election, Hungary election (last events)

## FINAL Results (2026-06-14, 62/62 events scored — experiment closed)

| Metric | Batch 1 | Batch 2 | Batch 3 | Combined |
|--------|---------|---------|---------|----------|
| Events scored | 12/12 | 20/20 | 30/30 | **62/62** |
| Real mean | 3.33 | 3.55 | 2.93 | **3.21** |
| Control mean | 2.83 | 2.55 | 2.70 | **2.68** |
| Mean diff | +0.50 | +1.00 | +0.23 | **+0.53** |
| Win record | 7-5 | 13-6-1T | 14-12-4T | **34-23-5T** |
| Wilcoxon p (one-tailed) | 0.260 | **0.011** | 0.268 | **0.021** |

**The effect peaked at p=0.0045 (n=47, 2026-05-02) then weakened to p=0.021 once the final 15 events resolved.** The final 15 — scored under a stricter split-role protocol (separate blinded narrator + separate blinded scorer subagents) — regressed against the hypothesis (real 2.20 vs control 2.60). Completed batch 3 (full skill) is null (p=0.27); only batch 2 (plain-LLM 取象法) is individually significant. The full-skill wrapper did **not** beat plain prompting.

See `analysis/final_results_n62.md` for the full writeup, caveats, and standout cases.
See `analysis/wilcoxon_n62.py` to reproduce (re-derives the n=47 p=0.0045 as a sanity check).
See `evaluations/interim_report_2026-05-02.md` (peak snapshot), `..._2026-04-15.md`, `..._2026-03-18.md` for the trajectory.

### Earlier interim trajectory (superseded)
| Snapshot | n | Mean diff | p (1-tail) |
|---|---:|---:|---:|
| 2026-03-18 | 19 | +0.58 | 0.139 |
| 2026-04-15 | 37 | +0.78 | 0.011 |
| 2026-05-02 | 47 | +0.83 | 0.0045 |
| **2026-06-14 final** | **62** | **+0.53** | **0.021** |

## Batch 3 (E33-E62)
- 30 upcoming events (Apr - May 2026)
- **Casting method**: 取象法 via meihua-yishu skill (full skill invocation per event)
- Control seed: `20260318`
- Blinding seed: `20260319`
- Each event gets 2 hexagram interpretations (real + control, blinded A/B)
- Full skill output recorded

### Batch 3 Status Tracker (scored events only)

| Event | Domain | Cast | Interpreted | Resolved | Narrated | Scored |
|-------|--------|------|------------|----------|----------|--------|
| E33 Georgia 14th runoff | Politics | Done | Done | Done (Apr 7) | Done | R=2, C=5 |
| E34 Assam election | Politics | Done | Done | Done (results May 4) | Done | R=0, C=3 |
| E35 Cygnus NG-24 | Science/Space | Done | Done | Done (Apr 11) | Done | R=3, C=1 |
| E36 Djibouti election | Politics | Done | Done | Done (Apr 10) | Done | R=4, C=5 |
| E37 Grand National | Sports | Done | Done | Done (Apr 11) | Done | R=5, C=1 ⭐ |
| E38 Benin election | Politics | Done | Done | Done (Apr 12) | Done | R=4, C=3 |
| E39 NBA Play-In | Sports | Done | Done | Done (Apr 17) | Done | R=3, C=3 (T) |
| E40 Michael MJ biopic | Culture | Done | Done | Done (Apr 17) | Done | R=5, C=1 ⭐ |
| E41 NBA Playoffs R1 | Sports | Done | Done | Done (late Apr) | Done | R=3, C=3 (T) |
| E42 NHL Playoffs R1 | Sports | Done | Done | Done (early May) | Done | R=4, C=2 |
| E43 Adobe Summit | Tech | Done | Done | Done (Apr 19-22) | Done | R=4, C=3 |
| E44 Boston Marathon | Sports | Done | Done | Done (Apr 20) | Done | R=4, C=3 |
| E45 Google Cloud Next | Tech | Done | Done | Done (Apr 22-24) | Done | R=1, C=5 |
| E46 NFL Draft R1 | Sports | Done | Done | Done (Apr 23) | Done | R=5, C=2 ⭐ |
| E47 Chevron Championship | Sports | Done | Done | Done (Apr 26) | Done | R=3, C=4 |
| E48 London Marathon | Sports | Done | Done | Done (Apr 26) | Done | R=5, C=1 ⭐ |
| E49 Devil Wears Prada 2 | Culture | Done | Done | Done (May 1) | Done | R=2, C=3 |
| E50 Kentucky Derby | Sports | Done | Done | Done (May 2) | Done | R=3, C=3 (T) |
| E51 F1 Miami GP | Sports | Done | Done | Done (May 3) | Done | R=1, C=2 |
| E52 Met Gala | Culture | Done | Done | Done (May 4) | Done | R=4, C=2 |
| E53 UK local elections | Politics | Done | Done | Done (May 7) | Done | R=2, C=1 |
| E54 Mortal Kombat 2 | Culture | Done | Done | Done (May 8, drift) | Done | R=1, C=2 |
| E55 FA Cup Final | Sports | Done | Done | Done (May 16) | Done | R=3, C=3 (T) |
| E56 Cape Verde parliament | Politics | Done | Done | Done (May 17) | Done | R=2, C=3 |
| E57 French Open week 1 | Sports | Done | Done | Done (May 18) | Done | R=1, C=4 |
| E58 Google I/O | Tech | Done | Done | Done (May 19) | Done | R=3, C=2 |
| E59 Dell Tech World | Tech | Done | Done | Done (May 18) | Done | R=1, C=4 |
| E61 Colombia round 1 | Politics | Done | Done | Done (May 31, → runoff) | Done | R=2, C=3 |
| E62 UEFA CL Final | Sports | Done | Done | Done (May 30) | Done | R=3, C=2 |
| E60 Starship Flight 12 V3 | Science/Space | Done | Done | Did not launch — static fire only Apr 15 | Done | R=5, C=2 ⭐ |

## Methodology Difference: Batch 1 vs Batch 2 vs Batch 3

| | Batch 1 | Batch 2 | Batch 3 |
|---|---------|---------|---------|
| Casting method | Mechanical (字數/字元數 → 數字) | 取象法 (LLM direct) | 取象法 (full skill invocation) |
| Script used | meihua_calc.py | LLM with bagua-wanwu.md | /meihua-yishu skill |
| Sample size | 12 events | 20 events | 30 events |
| Control seed | 20260224 | 20260305 | 20260318 |
| Extra data recorded | Word/char counts | 取象理由, 策略建議, 爻位風險 | Full skill output |
