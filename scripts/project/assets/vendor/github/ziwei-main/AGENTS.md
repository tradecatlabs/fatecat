# Repository Guidelines

## 项目结构与模块组织
- `packages/core`：承载紫微斗数的算法、国际化资源，并在 `src/__tests__` 维护领域测试。
- `packages/react`：React 绑定，包含 `src/components`、共享上下文，以及用于演示的 `playground/`。
- `packages/react-hooks`：集中存放包装核心引擎的独立 Hook，实验性实现也放在此处。
- `packages/ziwei`：对外的聚合入口，导出验证的稳定 API。
- `apps/`：应用外壳（目前为空）；测试覆盖率报告写入仓库根目录的 `coverage/`。

## 构建、测试与开发命令
- `pnpm install`：安装依赖并刷新多包工作区的符号链接。
- `pnpm build`：调用 `moon :build`，按依赖图编译所有包。
- `pnpm test`：本地执行 Vitest 套件，可追加 `--run` 加速单次运行。
- `pnpm coverage`：生成基于 V8 的覆盖率数据并写入 `coverage/`。
- `pnpm test:analytics`：CI 使用的 Vitest 流程，产出 `test-report.junit.xml`。
- `pnpm biome format --write`：格式化暂存文件，与预提交钩子保持一致。
- `pnpm biome check`：执行 Biome Lint，确保风格与规范一致。
- `pnpm tsgo --noEmit`：与预提交相同的 TypeScript 类型检查。

## 代码风格与命名约定
- 遵循 Biome 配置：两个空格缩进、100 字符行宽、字符串使用双引号。
- 模块保持 ESM，公共导出在文件末尾集中列出。
- 组件、类型、枚举使用 `PascalCase`；函数、变量、Hook 使用 `camelCase`。
- 测试就近维护在 `__tests__/`，文件命名为 `feature.test.ts`。
- 交由 Biome 自动整理导入，除非格式化无法处理，否则不要手动排序。

## 测试指引
- 优先使用 Vitest 编写单元测试，将确定性逻辑放在 `packages/core/src/__tests__`。
- React 相关改动在 `packages/react/src/components/__tests__` 添加组件测试，可结合 React Testing Library。
- 持续关注覆盖率，提交前检查 `coverage/lcov-report/index.html` 了解缺口。

## 提交与合并请求规范
- 所有开发必须在功能分支进行，禁止直接推送到 `main`，仅允许通过 GitHub PR 合并。
- 保持提交标题的句式风格，可附带问题编号，如 `Add React component library for ZiWei (#137)`。
- 修改发布包时运行 `pnpm changeset`，提交对应的版本记录。
- 推送前请执行 `pnpm biome check`、`pnpm tsgo --noEmit` 以及相关 `pnpm test*`，避免 CI 重跑。
- PR 说明需概述意图、列出测试结果，对 UI 变更附截图或演示链接。
