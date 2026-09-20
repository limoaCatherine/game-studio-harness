---
name: diagram-pack
description: "按图种选工具并落盘：环/流程图写 Mermaid，树/大纲用 xmind，画布精修用 excalidraw，协作白板用 miro。触发：流程图、系统循环、mermaid、excalidraw、脑图、xmind、画布、miro、块连线、架构图。"
---

# 图怎么选工具并落盘

## 何时用

- 要画系统循环、流程图、时序、架构块连线
- 要画树、大纲、会议脑图
- 要出手绘风、可继续拖的本地画布
- 要把图画到在线白板给人看

**不替代**：`economy-loop-analysis` / `systems-index-map` 管内容怎么拆；本技能管**用哪支笔、落到哪类文件**。

## 分流（只走本轮那一层）

| 图种 | 点名 | 落盘 | 禁区 |
|---|---|---|---|
| 环 / 流程 / 时序 | 本技能 | `.harness/artifacts/<工作项>/*.md` 或 `*.mmd` 里的 Mermaid | 不要用 `xmind` 硬画流程图 |
| 树 / 大纲 / 会议脑图 | `xmind` | `.xmind` | 不要用 relationship 当流程箭头 |
| 画布精修 / 手绘块 | `excalidraw` | `.excalidraw`，需要静图再 `export_diagram` → SVG | 不要从空坐标手摆每个元素 |
| 协作分享白板 | `miro` | Miro 板 | 日常环图不要烧免费档 100 次/日 |

Mermaid **不是 MCP**。写在 Markdown 围栏里即可被宿主渲染；需要可拖画布时，把同一份 Mermaid 交给 `excalidraw` 的 `import_mermaid`。

## 怎么做

### 1. 锁定图种与路径

1. 复述要交付的是环、树、画布还是分享板；一种主产物，其余最多作派生。
2. 路径落到业务根 `.harness/artifacts/<工作项>/`，文件名用中文短名 + 图种后缀。
3. 开场要用的 MCP 可写进加载计划；过程中要用再调，不必等重生名单。
4. 不合格：图种未定就开画 → 停。

**做到**：图种、主路径、派生（若有）写清。

### 2. 按图种出主产物

**环 / 流程 / 时序（默认）**

1. 用 `flowchart` / `sequenceDiagram`；方向默认 `TB`，横向泳道才用 `LR`。
2. 节点用短中文标签；边写触发或代价，不写散文。
3. 环要能顺着箭头走回起点；旁路单独标，不和主环抢编号。
4. 落盘后在对话里再贴同一份围栏，方便当场看。

**树 / 大纲**

1. 调 `xmind`：附着主题 + 宿主自动布局。
2. 只表达从属，不表达流转。流转另出 Mermaid 或画布。

**画布精修**

1. 调 `excalidraw`：优先 `create_flowchart` / `create_architecture_diagram` / `import_mermaid`。
2. `output_path` 必须是本机绝对路径，指向步骤 1 的 artifacts。
3. 改已有图用 `read_diagram` → `modify_diagram`，不要重画覆盖未确认稿。

**协作白板**

1. 确认 `miro` 已 OAuth（菜单里该 MCP 为已连接）。未登录则在 why 写缺口，改出本地 Mermaid / `.excalidraw`。
2. 整图写入，少打往返；免费档按「一天 1～2 张整图」估次数。

**做到**：主产物路径可打开；派生不抢主文件名。

### 3. 验收

1. 流程：任意节点能沿箭头走到终点或回到环入口。
2. 树：折叠父节点后子树仍在同一枝上。
3. 画布：`.excalidraw` 能拖到 [excalidraw.com](https://excalidraw.com) 继续改。
4. 白板：板里能看到本轮写入的块，而不是空板。

**做到**：对应图种的一条验收过了才能交。

## 完成检查

- [ ] 只走了一种主图种
- [ ] 产物在 artifacts 且路径可打开
- [ ] 未用 XMind 冒充流程图
- [ ] `miro` 未登录时未假装已写板

## 工具锚

- MCP：`excalidraw`（`${HARNESS_APPS}\mcp\excalidraw-mcp`）、`xmind`、`miro`（`https://mcp.miro.com/`）
- 菜单：`~/.cursor/mcp.json` → 刷新菜单
- 点名：`route-task`「图怎么点」
