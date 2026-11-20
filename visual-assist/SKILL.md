---
name: visual-assist
description: 当用户要求提供或实现可视化辅助、交互式说明页、流程图、架构图、时间线、对比页或可打开的本地演示页面时，生成、验证并发布可访问的 HTML 可视化制品。显式调用写法：/visual-assist <页面目标>。
---

# 可视化辅助页面（visual-assist）

用户要求“提供/实现可视化辅助”、交互式说明页、流程图、架构图、时间线、对比页或可打开的本地演示页面时使用本 skill。显式调用：`/visual-assist <页面目标>`（等效于点名本 skill）。

## 职责边界

- 本 skill 负责**生成、验证并发布**一个可视化 HTML 制品；不负责随意管理本地服务器。
- **禁止**自行计算端口或哈希、扫描端口、启动替代服务（miniserve / `python -m http.server` / `npx serve` / Vite 等）、安装服务依赖、或拼接猜测的 localhost 地址。
- 发布只能走下面的“发布”流程，端口与服务生命周期完全由脚本拥有。

## 实施前：需求判断

动手前先从现有上下文形成最低实现契约（内部检查，不逐项盘问用户）：页面帮助谁完成什么、事实来源是什么、最合适的可视化形式、是否需要交互、是否为低风险辅助制品。

**直接实施**（不再追问）的任一条件：

- 显式命令已给出目标，且所需事实已在上下文或工作区材料中；
- 主题和页面形式已指定，合理默认不会改变结论或用户意图；
- 页面是低风险辅助制品，不用于公开发布或关键决策；采用的默认值在最终回复中简短声明。

**才允许提问**：缺失材料会决定页面展示什么事实；同一描述对应截然不同的目标；页面支撑关键决策或对外发布；涉及个人信息、凭据、安全或不可逆操作；用户点名的资料无法定位。提问时只问**一个合并的关键问题**并附推荐默认。不得为配色、字体、动画、圆角等低风险设计偏好阻塞工作。

## 制品规范

- 路径：`.agents/visuals/YYYY-MM-DD-<topic>.html`（相对当前项目根）；同日同主题默认覆盖，仅当用户明确要求保留版本时追加后缀。
- 页面是纯静态制品：使用相对或内嵌资源，不依赖项目开发服务器路由；不修改业务源码或项目构建配置。
- 内容结构：标题 → 一句话目标/结论 → 主要可视化 → 图例/阅读指引（确有需要时）→ 事实来源、假设与生成时间（涉及事实、数据或推断时）。不为“好看”添加空洞的仪表盘、卡片或动效。

## 静态依赖本地化（强制）

- 所有第三方静态依赖（Tailwind、Vue、ECharts 等）**先下载到 `.agents/visuals/static/`**，页面只引用本地相对路径 `static/<文件名>`，**禁止运行时从线上拉取**，避免每次访问都重新请求 CDN。
- 文件名固定为 `<库名>-<精确版本>.<扩展名>`；文件已存在则**直接复用，不重复下载**。
- **来源优先级**：① jsdelivr（`https://cdn.jsdelivr.net/npm/<pkg>@<version>/<file>`）；② GitHub（`https://cdn.jsdelivr.net/gh/<user>/<repo>@<tag>/<file>` 或 `https://raw.githubusercontent.com/<user>/<repo>/<tag>/<file>`）；③ 其它源（unpkg、官方站点等）仅作兜底。选定后把精确 URL 记入 HTML 注释。
- 固定版本清单（除非用户指定其它版本）：

| 库 | 本地文件名 | 首选下载源 |
|---|---|---|
| Tailwind | `static/tailwind-3.4.17.js` | `https://cdn.tailwindcss.com/3.4.17`（Play 版无 jsdelivr/GitHub 分发，唯一官方源） |
| Vue | `static/vue-3.5.13.global.prod.js` | `https://cdn.jsdelivr.net/npm/vue@3.5.13/dist/vue.global.prod.js` |
| ECharts | `static/echarts-5.6.0.min.js` | `https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js` |

- 下载示例：

  ```sh
  mkdir -p .agents/visuals/static
  curl -fL -o .agents/visuals/static/tailwind-3.4.17.js https://cdn.tailwindcss.com/3.4.17
  curl -fL -o .agents/visuals/static/vue-3.5.13.global.prod.js https://cdn.jsdelivr.net/npm/vue@3.5.13/dist/vue.global.prod.js
  ```

- 其它库同样先下载、版本化命名后再引用；HTML 注释中列明本地依赖的名称、版本与实际下载源 URL。
- 下载失败时按来源优先级换下一个源重试一次；仍失败且本地无缓存时，可临时改引对应 CDN 地址，并在最终回复中注明“依赖未能本地化”；用户要求离线可用时改用内联等价样式（同一套主题令牌）。

## 样式与固定主题（强制）

所有页面**必须使用 Tailwind CSS（本地静态文件，固定版本）**并采用下方固定主题，保证任何 harness、任何项目产出的页面风格一致：

- **必须**：先按“静态依赖本地化”下载 `static/tailwind-3.4.17.js`，`<head>` 中原样包含下面的模板块；布局与样式一律使用 Tailwind 工具类。
- **禁止**：引入其他 UI/CSS 框架（Bootstrap、Element、Ant 等）、手写全局样式表、自造配色、直接引用线上 CDN。
- **可选**：图表/关系可视化库（ECharts 等）同样先本地化到 `static/` 再引用，颜色服从主题令牌。
- **固定浅色主题**：不做暗色切换；正文、卡片、语义色只用下列令牌。

```html
<script src="static/tailwind-3.4.17.js"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          brand: { 50:'#eef2ff',100:'#e0e7ff',500:'#6366f1',600:'#4f46e5',700:'#4338ca' },
          ok: '#059669', warn: '#d97706', risk: '#e11d48',
        },
        fontFamily: {
          sans: ['system-ui','-apple-system','Segoe UI','PingFang SC','Microsoft YaHei','sans-serif'],
          mono: ['ui-monospace','SFMono-Regular','Consolas','monospace'],
        },
        boxShadow: { card: '0 1px 3px rgb(15 23 42 / 0.08)' },
      },
    },
  }
</script>
```

主题令牌约定：

| 用途 | 令牌 |
|---|---|
| 页面背景 | `bg-slate-50` |
| 卡片/面板 | `bg-white rounded-xl shadow-card`，内边距 `p-5` 以上 |
| 主文字 / 次文字 | `text-slate-800` / `text-slate-500` |
| 主色（标题强调、选中态、主按钮） | `text-brand-600` / `bg-brand-600` |
| 语义色（成功/警告/风险） | `text-ok` / `text-warn` / `text-risk`，色块用对应 `bg-*` 加 `text-white` |
| 页面容器 | `max-w-5xl mx-auto px-6 py-8` |
| 控件圆角 | `rounded-lg`；代码与数值 `font-mono` |

依赖加载失败兜底（紧跟在上述脚本之后，原样保留）：

```html
<script>
  window.addEventListener('DOMContentLoaded', function () {
    if (!window.tailwind) {
      var b = document.createElement('div');
      b.textContent = '样式依赖（static/tailwind）加载失败：内容仍可阅读，但排版未按主题渲染。';
      b.setAttribute('style', 'position:sticky;top:0;padding:8px 16px;background:#fef3c7;color:#92400e;font:14px system-ui;z-index:9999');
      document.body.prepend(b);
    }
  });
</script>
```

用户明确要求“离线可用/无外网”时：不得使用 CDN，改用内联等价样式并遵循同一套令牌（色值见上方 `tailwind.config`）。

## 页面质量基线

- 按关系选择形式：步骤/分支→流程图；时间顺序→时间线；层级与依赖→架构图/树；方案权衡→对比表/矩阵；状态演变→状态机；趋势→图表；复杂关系图须同时提供结构化文字列表。
- 字号：正文 `text-base`（16px）起、辅助文本 `text-sm`（14px）起；层级用 `text-2xl`/`text-xl` 标题与留白表达。
- 色彩语义一致（见主题令牌），颜色不作为状态的唯一表达，需辅以文字或图标；宽屏多列、窄屏单列（`grid` + 响应式断点）；关键内容不依赖悬停；交互元素键盘可达并有可见焦点（`focus-visible:ring`）；动效仅用于状态与反馈并尊重 `prefers-reduced-motion`。

## 事实与安全

- 只可视化用户提供的、工作区确认的或明确标注为“假设”的信息；不把推测画成已确认结论。
- 不嵌入密钥、令牌、个人信息或未脱敏日志；不向 CDN 或第三方 API 发送工作区数据。

## 发布（原样运行本 skill 自带脚本）

生成并通过静态检查后，运行本 skill 自带的脚本（本 SKILL.md 所在目录下），**同时传入项目绝对路径和入口 HTML**：

```sh
python3 <skill-dir>/scripts/preview-server.py <项目绝对路径> <入口HTML路径>
```

- 入口路径可写工作区相对路径（如 `.agents/visuals/2026-11-19-x.html`）或绝对路径；
- 原样执行，不修改、不复述其内部逻辑，也不自行计算端口；
- 脚本输出 `url=http://localhost:<port>/<文件名>`——该 URL 由脚本在服务端拼好并验证过可达；
- **最终回复只准原样引用脚本输出的 `url=` 行，禁止用 `origin=` 自行拼接任何路径**（服务根目录就是 `.agents/visuals`，URL 中不含 `.agents/visuals/` 前缀）；
- 脚本退出码非 0（含无 python3、端口被外来服务占用、入口校验失败、URL 验证失败）时**不做任何变通**：不换端口、不换服务器、不安装依赖；
- 此时降级交付：仍交付已生成的 HTML 文件路径，说明“预览发布不可用，文件为自包含 HTML，可由用户在浏览器直接打开”。不提供任何未经验证或猜测的 URL。

## 交付格式

- 发布成功：预览 URL（链接形式）+ HTML 文件路径（项目内路径）+ 一句话页面用途。
- 发布失败：HTML 文件路径 + 一句降级说明。
- 生成后先做静态检查：文件存在、`<title>` 与核心内容完整、无失效的外链资源引用。

## 不触发

- 用户只要文字解释、普通代码修改或图片时，不创建辅助页面；
- 普通前端开发任务（用户要求开发的产品页面本身）不套用本 skill，除非用户同时要求可视化辅助。
