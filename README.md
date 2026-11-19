# my skills

跨 agent 通用技能集合。每个子目录是一个独立技能（`SKILL.md` + 可选脚本），
支持 Claude Code、OpenCode、Codex、GitHub Copilot、Cursor、DSH 等。

## 技能列表

| 目录 | 名称 | 用途 |
|---|---|---|
| `vue2/` | `frontend-avatar-vue2` | Vue 2 前端开发规约分身（ef- 组件库、弹窗编排、状态字典） |
| `visual-assist/` | `visual-assist` | 可视化辅助页面：生成、验证并发布可访问的 HTML 可视化制品 |

## 安装

```sh
git clone https://github.com/hibiscustoyou1/my-frontend-avatar-skill
cd my-frontend-avatar-skill
sh install.sh
```

- 规范副本安装到 `~/.agents/skills/<name>`（Codex / Cursor / Copilot /
  OpenCode agent 兼容层 / DSH 原生读取）；
- Claude Code（`~/.claude/skills`）、OpenCode（`~/.config/opencode/skills`）、
  Copilot（`~/.copilot/skills`）、Codex（`~/.codex/skills`）为符号链接；
- 只装一个技能：`ONLY=visual-assist sh install.sh`；
- 跳过某 harness：`SKIP_CLAUDE=1 sh install.sh` 等；
- 项目级安装：把对应技能目录复制进项目的 `.agents/skills/` 即可。

## visual-assist 说明

- 显式调用：`/visual-assist <页面目标>`；命中“可视化辅助 / 交互式说明页 /
  流程图 / 架构图 / 时间线 / 对比页 / 本地演示页面”时自动加载。
- 制品落在项目 `.agents/visuals/YYYY-MM-DD-<topic>.html`，默认单文件自包含，
  允许固定版本的 CDN（Vue / Tailwind / D3 等）。
- 预览发布由技能自带 `scripts/preview-server.py` 完成（仅依赖 python3）：
  端口 = `38700 + DJB2(项目绝对路径) % 301`，健康端点复用已有服务，仅绑定
  127.0.0.1；脚本失败时降级交付文件路径，绝不猜测 URL。
- 技能零依赖：不引用任何 harness 私有工具。
