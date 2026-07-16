# Acceptance Checklist

# Global Standards
- [x] 原典哈希不变
- [x] 输出 ID/hash 稳定
- [x] 版权和生产边界不放宽
- [x] 血缘完整、无断链
- [x] focused tests 与 data supply chain gate 通过
- [x] quick CI 通过

# Task Package Checklists
## TP-01
- [x] 数据契约字段齐全
- [x] 输入、输出和风险边界明确
- Verify: JSON 解析和任务文档 strict 校验。
- Gate: 不放宽版权、生产和分发状态。

## TP-02
- [x] CLI 支持生成和 `--validate-only`
- [x] 使用临时目录和原子替换
- [x] 只使用标准库
- Verify: 合成 fixture 连续生成两次的记录 ID 和内容哈希一致。
- Gate: 不覆盖输入，不静默跳过坏 UTF-8 或血缘错误。

## TP-03
- [x] 正常、重复、坏 UTF-8和输出冲突路径测试
- [x] README/AGENTS 同步
- Verify: focused pytest 通过。
- Gate: 测试不访问网络、不读取私有 raw。

## TP-04
- [x] 14 本生成成功
- [x] manifest 和 `files.sha256` 可复核
- [x] overlap/quality 报告生成
- Verify: build 与 `--validate-only` 对真实数据通过。
- Gate: 14/14 文档、零血缘错误、原文件哈希不变。

## TP-05
- [x] diff review 无阻断
- [x] quick CI 通过
- [x] 任务状态和证据更新
- Verify: quick CI、task strict、git diff/status。
- Gate: 无 BLOCK、无 ignored 正文进入提交。
