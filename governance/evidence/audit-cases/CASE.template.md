---
id: CASE-9999
slug: project-specific-pattern
title: 项目特有问题模式
type: audit-case
status: draft
owner: engineering
last_reviewed: 2026-07-15
severity: WARN
root_cause_class: project_specific_pattern
review_profiles:
  - correctness
reviewer_prompts:
  - reviewers/critical-review-audit-prompt.md
trigger_signals:
  - project signal
audit_questions:
  - 审查者必须确认什么？
automation_candidate: 描述可实现的扫描、测试或 Gate。
project_safe: false
---

# CASE-9999 项目特有问题模式

## Problem Pattern

说明复发问题形态。

## Why It Recurs

说明工程机制根因。

## Audit Questions

- 列出可执行审计问题。

## Evidence To Request

- 列出必须获取的证据。

## Finding Template

- Severity: WARN
- Category: project-specific
- Evidence: 具体文件、命令或测试证据。
- Risk: 忽略问题的影响。
- Minimal Fix: 最小永久修复。
- Verification: 可执行验证方式。

## Gate Suggestion

说明何时 `BLOCK`，何时只记为 `WARN`。

## Automation Candidate

说明自动发现方式。

## Privacy Boundary

说明为何该案例只能存在于项目 overlay。
