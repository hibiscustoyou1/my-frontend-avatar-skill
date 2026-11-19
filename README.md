# visual-assist（跨 agent 通用 skill）

一个纯粹、可移植的 Agent Skill：当用户要求“可视化辅助 / 交互式说明页 / 流程图 /
架构图 / 时间线 / 对比页 / 本地演示页面”时，生成、验证并发布可访问的 HTML
可视化制品。

## 结构

```text
visual-assist/
  SKILL.md                  # frontmatter（name/description）+ 全部行为规范
  scripts/preview-server.py # 确定性端口与本地预览服务（仅依赖 python3）
install.sh                  # 一次安装到多个 harness
```

## 安装

```sh
sh install.sh
```

规范副本安装到 `~/.agents/skills/visual-assist`（Codex、Cursor、Copilot、
OpenCode agent 兼容层、DSH 均原生读取该目录），并为以下 harness 创建符号链接：

- Claude Code：`~/.claude/skills/visual-assist`
- OpenCode：`~/.config/opencode/skills/visual-assist`
- Copilot：`~/.copilot/skills/visual-assist`
- Codex：`~/.codex/skills/visual-assist`（可选；`~/.agents` 已覆盖用户级）

跳过某个 harness：`SKIP_CLAUDE=1 sh install.sh` 等。
项目级安装：把 `visual-assist/` 目录复制到项目的 `.agents/skills/`。

## 设计要点

- **零外部依赖**：预览脚本仅用 python3 标准库；没有 python3 时 skill 走降级
  交付（给出 HTML 文件路径，不猜测 URL）。
- **端口确定性**：`38700 + DJB2(工作区绝对路径) % 301`，与 DSH 的
  `visual_assist_publish` 工具共用同一算法和健康端点，可互相复用服务。
- **固定视觉风格**：强制 Tailwind CSS（CDN 固定版本 3.4.17）+ 固定浅色主题
  令牌（indigo 主色 / slate 中性 / emerald-amber-rose 语义色），所有页面
  风格统一；离线场景降级为同令牌的内联样式。
- **agent 不自由发挥**：skill 明确禁止自行算端口、扫描端口、起替代服务或拼
  URL；只能原样运行 skill 自带的脚本。skill 不依赖任何 harness 私有工具
  （端口算法与 DSH 的 `visual_assist_publish` 工具一致，二者若同时存在可
  互相复用已启动的服务，但这是协议兼容，不是依赖）。
