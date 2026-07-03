# Acceptance

## Required

- `scripts/multi-surface-semantic-diff.py/.sh` 存在，并能对 bazi/ziwei 输出 `status=passed`。
- `contracts/fate/delivery/multi-surface-semantic-diff.json` 登记 required surfaces、partial surface boundary、external pending 和 privacy boundary。
- `contracts/fate/delivery/registry.json` 顶层登记 `multiSurfaceSemanticDiffGate`。
- `scripts/local-ci.sh` quick profile 调用 `multi-surface-semantic-diff.sh`，summary 记录 artifact 路径。
- API/Web/Bot 标准 Markdown bazi 路径统一使用 capability 引擎。
- 回归测试覆盖输出不保存完整 Markdown 正文、registry/local-ci/AGENTS wiring 和 capability 接线。

## Evidence Commands

```bash
bash scripts/multi-surface-semantic-diff.sh --output-json /tmp/fatecat-multi-surface-semantic-diff.json --pretty
python3 -m pytest -q tests/regression/test_multi_surface_semantic_diff.py
python3 -m ruff check scripts/multi-surface-semantic-diff.py tests/regression/test_multi_surface_semantic_diff.py
bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0090.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0090
```

## External Pending

- 真实 Telegram Bot live smoke：外部连通验证待执行。
- 真实 HF Space hosted Web live diff：外部连通验证待执行。
- 公网 API/HF/真实浏览器兼容性：外部连通验证待执行。
