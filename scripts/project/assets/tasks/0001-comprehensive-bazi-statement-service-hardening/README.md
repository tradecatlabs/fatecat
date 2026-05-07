# Task Overview
- Task ID: `0001`
- Slug: `comprehensive-bazi-statement-service-hardening`
- Objective: `综合八字陈述服务加固：锁定节气边界、默认报告结构、证据化陈述、输入隐私、多端同源输出、典籍引用与质量门禁`
- Status: `In Progress`

## In Scope
- 只加固当前生产方向：综合八字默认报告与同源服务链路。
- 建立节气、月令、立春年界、起运边界的 golden 回归项目。
- 锁定 Markdown 默认输出结构，并把非综合八字体系移出默认报告。
- 为八字核心结论补齐 evidence 契约，明确依据来源与权重边界。
- 加固 Web、API、Bot 同源输出、输入契约、隐私示例、质量门禁与服务化文档。

## Out of Scope
- 不实现紫微、六爻、梅花、奇门、大六壬、西方占星、塔罗、铁板神数等新体系。
- 不把 raw 书籍、Drive zip 或版权未复核资料直接接入生产运行链路。
- 不重写成熟历法库；节气项目先做 golden 校验与回归门禁。
- 不允许前端、API、Bot 各自拼装报告结构。

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 节气 golden 回归
  │  ├─ TP-01.01 [leaf] [P0] 盘点交节时间 raw 表
  │  ├─ TP-01.02 [leaf] [P0] 构建节气 golden fixture
  │  ├─ TP-01.03 [leaf] [P0] 节气与月令边界测试
  │  └─ TP-01.04 [leaf] [P0] 起运边界回归
  ├─ TP-02 [branch] [P0] 综合八字输出结构锁定
  │  ├─ TP-02.01 [leaf] [P0] 审计当前 report profile
  │  ├─ TP-02.02 [leaf] [P0] 锁定综合八字默认块
  │  └─ TP-02.03 [leaf] [P0] 报告结构快照测试
  ├─ TP-03 [branch] [P0] 八字核心证据化
  │  ├─ TP-03.01 [leaf] [P0] 定义 evidence schema
  │  ├─ TP-03.02 [leaf] [P0] 核心结论 evidence mapper
  │  └─ TP-03.03 [leaf] [P1] 证据渲染与可见性
  ├─ TP-04 [branch] [P0] 权重与边界治理
  │  ├─ TP-04.01 [leaf] [P0] 独立体系 capability 边界
  │  └─ TP-04.02 [leaf] [P1] 权重策略测试
  ├─ TP-05 [branch] [P0] 输入契约与隐私治理
  │  ├─ TP-05.01 [leaf] [P0] 输入 schema 与错误响应
  │  └─ TP-05.02 [leaf] [P0] 隐私与示例脱敏回归
  ├─ TP-06 [branch] [P0] Web/API/Bot 同源输出
  │  ├─ TP-06.01 [leaf] [P0] 报告 profile 单一真相源
  │  └─ TP-06.02 [leaf] [P0] Markdown 复制一致性
  ├─ TP-07 [branch] [P1] 八字典籍引用层
  │  ├─ TP-07.01 [leaf] [P1] 典籍来源与版权边界审计
  │  ├─ TP-07.02 [leaf] [P1] 小型规则索引种子
  │  └─ TP-07.03 [leaf] [P1] 规则引用接入 evidence
  ├─ TP-08 [branch] [P0] 质量门禁加固
  │  ├─ TP-08.01 [leaf] [P0] pytest 门禁扩展
  │  └─ TP-08.02 [leaf] [P0] acceptance 脚本更新
  ├─ TP-09 [branch] [P1] 服务化文档同步
  │  ├─ TP-09.01 [leaf] [P1] README/SKILL 生产边界更新
  │  └─ TP-09.02 [leaf] [P1] playbook 与架构文档更新
  └─ TP-10 [branch] [P0] 交付控制与 closeout
     ├─ TP-10.01 [leaf] [P0] 生成交付证据
     └─ TP-10.02 [leaf] [P0] 任务 closeout

## Requirement Alignment
- 目标: 综合八字陈述服务加固：锁定节气边界、默认报告结构、证据化陈述、输入隐私、多端同源输出、典籍引用与质量门禁。
- approved plan 顶层步骤数: 10
- 编译后节点总数: 35
- 编译后叶子节点数: 25
- 对齐项: 用户明确要求当前准备进服务的是加固和巩固现有综合八字陈述服务体系。
- 对齐项: 用户已确认综合八字范围：八字核心、八字动态运势、八字辅助解释、称骨民俗附录；紫微、黄历择日、占事、西方体系、铁板神数不进默认报告。
- 对齐项: 任务清单已明确 10 项：节气 golden、输出结构锁定、证据化、权重边界、输入契约、隐私、多端同源、典籍引用、质量门禁、服务化文档。
- 计划摘要: 按生产服务地基优先级拆分：先锁节气/报告结构，再补 evidence 与边界治理，然后统一输入隐私和多端输出，最后补典籍引用、质量门禁与服务化文档。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | Foundation | No | - | - | No | No | 解析 1900-2030 交节时间表，建立节气、月令、立春年界和起运边界回归。 |
| TP-01.01 | TP-01 | 2 | P0 | Audit | Yes | - | 1 | Yes | No | 读取 CSV/XLS/XLSX 字段、年份覆盖、时区和精度，产出 normalized schema 设计。 |
| TP-01.02 | TP-01 | 2 | P0 | Build | Yes | TP-01.01 | 2 | No | No | 从 raw 表抽取可提交的小型标准化 fixture 或可复现生成脚本。 |
| TP-01.03 | TP-01 | 2 | P0 | Test | Yes | TP-01.02 | 3 | No | No | 用 golden fixture 锁定节气时刻、月令切换、立春年界和真太阳时入参边界。 |
| TP-01.04 | TP-01 | 2 | P0 | Test | Yes | TP-01.02 | 3 | No | No | 建立 `yun.getStartSolar()` 样本回归，锁定起运年月日时分秒。 |
| TP-02 | ROOT | 1 | P0 | Contract | No | - | - | No | No | 固定默认 Markdown 块，确保非综合八字体系不混入默认报告。 |
| TP-02.01 | TP-02 | 2 | P0 | Audit | Yes | - | 1 | Yes | No | 定位 Web/API/Bot 当前使用的报告 profile 和 Markdown 拼装入口。 |
| TP-02.02 | TP-02 | 2 | P0 | Build | Yes | TP-02.01 | 2 | No | No | 将默认块限定为综合八字核心、动态运势、辅助解释、称骨民俗附录。 |
| TP-02.03 | TP-02 | 2 | P0 | Test | Yes | TP-02.02 | 3 | No | No | 新增 Markdown 结构快照和块可见性测试。 |
| TP-03 | ROOT | 1 | P0 | Contract | No | TP-02.01, TP-02.02, TP-02.03 | - | No | Yes | 为日主、旺衰、调候、格局、用神、干支关系等核心结论补 evidence 字段。 |
| TP-03.01 | TP-03 | 2 | P0 | Design | Yes | TP-02.01, TP-02.02, TP-02.03 | 4 | No | No | 定义 source、basis、weight、visibility、risk、rule_id 等字段。 |
| TP-03.02 | TP-03 | 2 | P0 | Build | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01 | 5 | No | No | 把月令、藏干、透干、五行、合冲刑害、调候、神煞、称骨映射为证据来源。 |
| TP-03.03 | TP-03 | 2 | P1 | Build | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.02 | 6 | No | Yes | 确定 evidence 在 API、Markdown、Web 中的默认显示/隐藏策略。 |
| TP-04 | ROOT | 1 | P0 | Governance | No | TP-02.01, TP-02.02, TP-02.03 | - | No | Yes | 固定八字核心、动态运势、辅助体系、民俗附录的权重层级。 |
| TP-04.01 | TP-04 | 2 | P0 | Governance | Yes | TP-02.01, TP-02.02, TP-02.03 | 4 | No | Yes | 把紫微、黄历择日、占事、西方体系、铁板神数等声明为独立或未来 capability。 |
| TP-04.02 | TP-04 | 2 | P1 | Test | Yes | TP-02.01, TP-02.02, TP-02.03, TP-04.01 | 5 | No | Yes | 为核心/辅助/民俗权重边界添加测试和文档说明。 |
| TP-05 | ROOT | 1 | P0 | Contract | No | TP-02.01, TP-02.02, TP-02.03 | - | No | Yes | 加固姓名、性别、出生日期、时间、地区的必填/可选规则和隐私示例治理。 |
| TP-05.01 | TP-05 | 2 | P0 | Build | Yes | TP-02.01, TP-02.02, TP-02.03 | 4 | No | Yes | 明确缺字段、格式错误、地区解析失败的服务响应，不生成半残报告。 |
| TP-05.02 | TP-05 | 2 | P0 | Test | Yes | TP-02.01, TP-02.02, TP-02.03 | 4 | No | Yes | 统一北京/测试用户示例，禁止真实非北京地区进入前端样例和报告 fixture。 |
| TP-06 | ROOT | 1 | P0 | Integration | No | TP-02.01, TP-02.02, TP-02.03, TP-05.01, TP-05.02 | - | No | No | 确保三端调用同一 report profile，Markdown 复制内容与 API 返回一致。 |
| TP-06.01 | TP-06 | 2 | P0 | Build | Yes | TP-02.01, TP-02.02, TP-02.03, TP-05.01, TP-05.02 | 5 | No | No | 收敛 Web、API、Bot 调用链路到同一 report profile 或同一 renderer。 |
| TP-06.02 | TP-06 | 2 | P0 | Test | Yes | TP-02.01, TP-02.02, TP-02.03, TP-05.01, TP-05.02, TP-06.01 | 6 | No | No | 保证 Web 复制 Markdown 与 API/Bot 产物结构一致。 |
| TP-07 | ROOT | 1 | P1 | Knowledge | No | TP-03.01, TP-03.02, TP-03.03 | - | No | Yes | 从已整理典籍中提炼格局、调候、用神规则索引，支持结论可追溯。 |
| TP-07.01 | TP-07 | 2 | P1 | Audit | Yes | TP-03.01, TP-03.02, TP-03.03 | 7 | No | Yes | 盘点《渊海子平》《三命通会》《子平真诠》《滴天髓》《穷通宝鉴》可用文本与来源状态。 |
| TP-07.02 | TP-07 | 2 | P1 | Build | Yes | TP-03.01, TP-03.02, TP-03.03, TP-07.01 | 8 | No | Yes | 先提炼格局、调候、用神的结构化规则索引种子。 |
| TP-07.03 | TP-07 | 2 | P1 | Integration | Yes | TP-03.01, TP-03.02, TP-03.03, TP-07.02 | 9 | No | Yes | 把可用规则索引接入 evidence，不改变核心算法判断。 |
| TP-08 | ROOT | 1 | P0 | Quality | No | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-02.01, TP-02.02, TP-02.03, TP-05.01, TP-05.02, TP-06.01, TP-06.02 | - | No | No | 把新增回归测试、隐私测试、结构测试和导出包卫生纳入 acceptance。 |
| TP-08.01 | TP-08 | 2 | P0 | Test | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-02.01, TP-02.02, TP-02.03, TP-05.01, TP-05.02, TP-06.01, TP-06.02 | 7 | No | No | 把节气、起运、报告结构、隐私、同源输出测试纳入现有 pytest 目录。 |
| TP-08.02 | TP-08 | 2 | P0 | CI | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-02.01, TP-02.02, TP-02.03, TP-05.01, TP-05.02, TP-06.01, TP-06.02, TP-08.01 | 8 | No | No | 必要时更新 acceptance/preflight，确保新增门禁在本地和 CI 运行。 |
| TP-09 | ROOT | 1 | P1 | Docs | No | TP-02.01, TP-02.02, TP-02.03, TP-04.01, TP-04.02 | - | No | Yes | 更新 README、SKILL、execution playbook 和架构文档，明确当前生产边界。 |
| TP-09.01 | TP-09 | 2 | P1 | Docs | Yes | TP-02.01, TP-02.02, TP-02.03, TP-04.01, TP-04.02 | 6 | No | Yes | 明确当前生产服务只支持综合八字默认报告，其他体系为独立或未来 capability。 |
| TP-09.02 | TP-09 | 2 | P1 | Docs | Yes | TP-02.01, TP-02.02, TP-02.03, TP-04.01, TP-04.02, TP-09.01 | 7 | No | Yes | 同步 execution playbook、AGENTS.md 和相关架构文档。 |
| TP-10 | ROOT | 1 | P0 | Ship | No | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | - | No | No | 完成版本控制、推送、CI、任务 closeout 和交付证据归档。 |
| TP-10.01 | TP-10 | 2 | P0 | Ship | Yes | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | 10 | No | No | 捕获 git delivery evidence、验证命令结果和剩余风险。 |
| TP-10.02 | TP-10 | 2 | P0 | Ship | Yes | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02, TP-10.01 | 11 | No | No | 完成 TODO/STATUS，生成 Task Closeout Packet 并沉淀后续事项。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
