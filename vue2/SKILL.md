---
name: frontend-avatar
description: 当你（大模型）收到开发或修改 Vue 2 前端组件、表单、弹窗或表格页面的任务时，请激活此技能。该技能包含了项目历史约定的深度定制 UI 组件库（ef- 类组件）、弹窗逻辑编排规则及状态字典的结构约束。
---

# Frontend Avatar (项目前端开发规约分身)

## 技能触发条件 (When to use this skill)

当你被要求编写或修改涉及界面的业务代码（尤其是后台管理列表、数据表、弹窗操作等场景）时，应当优先遵循本项目设定的这套高标准最佳实践，以确保代码带有“强烈的工程化整洁度”和与历史架构的高度契合。

## 架构说明与基本倾向 (Core Architecture & Preferences)

- **核心框架**: Vue 2 (Options API 为主)。
- **UI 组件库**: 基于 Element UI 深度定制封装的 `ef-` 开头系列组件（如 `ef-dialog`, `ef-table`, `ef-condition`, `ef-pagination` 等）。在书写代码时，遇到此类对应场景，强制使用 `ef-` 组件替代 `el-` 基础组件。
- **状态管理**: 借助 Vuex 按需通过 `mapState` 注入（例如 `mapState('core', ['desktopSvc'])`）。
- **国际化与鉴权**: 
  - 核心业务路由与文案严格使用 `$t('key')`；国际化变量寻找顺序：先查 `src/locales/langs/zh`，若字典失配，则前往 `src/locales/langs/zh/zxt.js`及其对应英文版提取后追加。
  - 组件与核心操作显示级别优先采用无侵入的权限指令约束：`v-perm="$perm.perm.xxx"`（复杂逻辑或不可用指令处再退化为 `v-if="$perm.hasPerm(...)"`）。

## 业务痛点实现范式 (Implementation Paragdigms)

### 1. 状态与副作用管理防散乱化
- 页面级别变量必须归拢合并。例如加载状态必定结构化在 `loadings: { table: false, submit: false }` 中。
- API Promise 的回收统一使用 `.finally(() => { this.loadings.xx = false })` 在结束周期进行复位。

### 2. 拒斥内联式弹窗控制 (Programmatic Modals Required)
坚决反对并在审查阶段拒绝通过父组件维护大量的 `v-if` / `visible.sync` 控制弹层。必须一律使用基于原型的抽象层实现：
- 使用 `this.$modal({ title, component: () => import('...'), data: { rowData } })` 控制。
- 对其结果的接收利用 Promise 句柄 `.then(() => { this.$emit('change', 'action') })`。

### 3. 操作按钮池的管理化机制
面对超过 3 个的行操作按钮，必须强制执行抽离逻辑：
- 在单独剥离出去的 `xx-operate.vue` 中配置 `operations` 数组（管理名称、隐藏参数、禁用条件）。
- 利用常量阈值 `DISPLAY_COUNT`，使用 `slice` 截断，将后半部分无缝衔接到 `<el-dropdown>` 的【更多操作】下拉框中。

## 组件速查检索与开发路由 (Snippet Routing)
遇到具体组件或业务需求时，**你必须（MUST）** 仅单独调阅下方匹配的特定文件以提取封装骨架，严禁依靠预训练知识强行生成原生 Element UI 标签：

- => 涉及顶部表单联合检索栏：立即读取 `references/ef-condition.md`
- => 涉及数据表格挂载与翻页：立即读取 `references/ef-table.md`
- => 涉及编程式弹窗骨架新建：立即读取 `references/ef-dialog.md`
- => 需要在界面渲染特殊的悬浮或失效解释时：立即读取 `references/help-popover.md`
- => 涉及需要用到预置业务状态字段解释时：立即读取 `references/status-dictionary.md`

【警告】一旦确定命中上述组件需求，立即查阅文件并套用其中的示例进行代码产出。
