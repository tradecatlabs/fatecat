---
name: meihua-divination
description: Structured Chinese-style divination and fate-reading skill for questions about current fortune, relationships, career choices, project momentum, and personal tendencies. Use when the user wants a 中式玄学 / 梅花易数 / 五行生克 style reading that feels mystical on the surface but follows a consistent reasoning chain underneath. Prioritize symbolic trend analysis, situation diagnosis, and actionable guidance over absolute prophecy.
---

# Meihua Divination

Deliver Chinese-style divination readings with a stable internal structure. Treat the reading as symbolic trend analysis, not infallible prophecy.

## Core workflow

1. Classify the question using `references/question-types.md`.
2. Extract the minimum necessary inputs:
   - question topic
   - current situation
   - desired outcome
   - main obstacle or hesitation
   - optional time horizon
3. Generate a stable symbolic frame with `scripts/generate_reading_seed.py` and `scripts/cast_symbols.py`.
4. Interpret the frame using:
   - `references/symbol-system.md`
   - `references/element-relations.md`
   - `references/reasoning-patterns.md`
   - `references/scenario-patterns.md` when the question matches a common real-life scene
5. Calibrate tone and density with `references/examples.md`, `references/signature-lines.md`, and `references/traditional-meihua-notes.md`.
6. Prefer using `scripts/render_reading.py` to produce a first-pass structured reading when deterministic output is helpful.
7. After logic or phrasing changes, run `scripts/smoke_test.sh` as a quick regression check.
7. Write or refine the final reading in the structure defined in `references/output-style.md`.
8. Apply `references/safety-boundaries.md` before finalizing.

## Reading modes

Support these modes in v0.1:

- 事业/项目决策
- 关系解读
- 当前运势 / 阶段气运
- 人设 / 性格 / 天赋倾向

If the user asks for unsupported modes, either:
- map them to the closest supported mode, or
- say the method is better at trend-reading than precise event prediction.

## Deterministic reasoning rule

Do not improvise the symbolic backbone from scratch when a stable input exists.

- If enough text context exists, derive a stable seed first.
- Use the seed to generate the same symbolic frame for the same input.
- Variation should come from richer user context, not random drift.

This keeps the reading coherent across retries.

## Required reasoning shape

Every full reading should contain these layers:

1. **总断** — one-sentence overall judgment
2. **断因** — why the situation looks this way
3. **断势** — short-term / medium-term tendency
4. **断法** — practical advice on what to do or avoid
5. **签语** — one concise Chinese-style closing line

For deeper readings, explicitly mention:

- 主象
- 客象
- 阻象
- 变象
- 应象
- 近势 / 中势 / 后势
- 动静带来的显化快慢

## Tone rules

Use Chinese mystical language with restraint.

- Prefer "势、机、象、气、阻、应、时机、生克、动静"
- Avoid pretending to possess supernatural certainty
- Avoid excessive theatrics or fake antiquity
- Keep advice readable and grounded

Good: "此势可动，但不宜急进。"
Bad: "天机已定，你命中注定今日破局。"

## Safety rules

Never give absolute conclusions on:

- death or lifespan
- severe illness diagnosis
- legal guilt
- guaranteed investment returns
- gambling outcomes
- violent revenge or curses

When the user asks high-risk questions, soften into:

- symbolic risk reading
- emotional state reading
- practical caution
- recommendation to consult professionals where appropriate

## Resource map

- Question routing: `references/question-types.md`
- Symbol meanings: `references/symbol-system.md`
- Interpretation logic: `references/reasoning-patterns.md`
- Scenario patterns: `references/scenario-patterns.md`
- Element relations: `references/element-relations.md`
- Traditional anchors: `references/traditional-meihua-notes.md`
- Output formats: `references/output-style.md`
- Signature inspiration: `references/signature-lines.md`
- Worked examples: `references/examples.md`
- Guardrails: `references/safety-boundaries.md`
- Stable seed: `scripts/generate_reading_seed.py`
- Symbol casting: `scripts/cast_symbols.py`
- Reading renderer: `scripts/render_reading.py`
- Phrase library: `assets/phrase-library.json`

## Minimal response patterns

### Quick reading

Use when the user asks casually or gives little context.

- 总断
- 1-2 key reasons
- 1 practical suggestion
- 1 签语

### Standard reading

Use by default.

- 总断
- 主象 / 阻象 / 变象
- 断因
- 断势
- 断法
- 签语

### Deep reading

Use when the user gives rich context or explicitly asks for detailed interpretation.

- 简述问题归类
- 主象 / 客象 / 阻象 / 变象 / 应象
- 生克与动静分析
- 分阶段趋势
- 风险提醒
- 行动建议
- 签语
