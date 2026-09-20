# Game Studio Harness

# 第一层

定档 → 制作 → 结案。同一未关目标续同一会话。

开场读序：本规则 → `.harness/sessions/<会话>/current.md` → 名单里点名的技能/职种正文 → 计划 `retrieve_keys` 命中的 canon/adr。不要把菜单全文灌进上下文。开场钩子注入现行卡摘要与点名列表。

## 名单

`activated.json` 只决定**开场先注入哪些正文**，不是运行时防火墙。

1. 计划里点名的 `skill` / `craft` / `mcp`，id 在 catalog 中则进入对应列表。
2. 已点名 skill 的 `needs_mcp` 并入 `mcp_allow`（开场提示，不挡调用）。
3. 已点名 craft **不预展开** `uses_skills`：不把路径上全部技能写入 `skills`，也不把它们的 `needs_mcp` 灌进 `mcp_allow`。只写 `craft_open`（路径第一步）供开场知道下一手打开谁。
4. 开场只读名单里的正文。过程中缺技能或外接：当场打开或调用，不必先改计划重生名单。

新增 skill / craft / mcp 后刷新菜单，再生成名单。开场发现菜单旧于源则刷新。
写新 skill 时把常用外接写进 frontmatter `needs_mcp`。
写新 mcp 时把键写进 `mcp.json`，刷新菜单补用途桩。
菜单无 id：先 doctor。

## 会话

- **续**：同一聊天且同一 `bead_id` / 同一未关交付 → 改计划增量，再生成名单。
- **转向**：同一未关交付、口径变了 → 先改计划再动手，禁止沿旧名单做完。
- **插队**：先放下当前交付 → 新会话做新件；旧件不关，进度写已停。
- **新**：新工作项或另一件交付 → 新会话目录（短名）。
- **并行**：互不依赖的两件 → 各开会话；由代理按需开子代理。不请人切产品多开。
- **讨论**：口头即可。要留点名则写计划且 `verify_kind=none`，只出口头或选项。

## 定档

复述目标、交付、边界；不清先问。
一件事一个主事件，或一条职种主路径，二者只取其一。工具按本轮真实动作点，防灌。
why ≥ 8 字。写 `.harness/sessions/<会话>/loadplan.json`，必填另加 `intent`、`work_mode`，建议加 `write_class`。再生成名单（会写现行卡），确认后再制作。工作模式见定档技能。

## 制作

点了职种走其主路径，路径上的事件**按步打开**，不预读整条路径。
只点了事件则只做该段。
岗位职责不同时优先按职种开子代理，主会话点名与收口。
写级别默认 `sandbox`：改正式面前先落到隔离根。晋升须人准，且只回写记录集。
不可逆破坏须本轮明确授权。密钥留在密钥管理处。

## 结案

有交付则写一份验证结论，按档位核核心证据。`verdict` 为通过后再关项。
通过后更新 `.harness/state.json`、现行卡进度，并往 `tasks.jsonl` 追加一行。

## 第四层

业务根以 `.harness` 为库。读当前行，写回当前行；流水只追加。不是知识图谱。

| 表 | 路径 |
|---|---|
| 当前行 | `.harness/state.json` |
| 现行卡 | `.harness/sessions/<会话>/current.md` |
| 正式面地图 | `.harness/surfaces.json` |
| 任务流水 | `.harness/memory/tasks.jsonl` |
| 已批准事实 | `.harness/memory/canon/` |
| 决策 | `.harness/memory/adr/` |
| 进度摘要 | `.harness/memory/status/` |
| 产物索引 | `.harness/artifacts/index.jsonl` |

开场读现行卡与当前行。生成名单写入会话、现行卡与工作项。当前行走 `sessions` 保留其它会话摘要。结案追加流水。
日期与时刻只写进当前行与任务流水。

## 正文

技能、职种、规则、MCP 说明只写可复用做法。当次诉求写在 `why`、现行卡与产物。
四层已封版。改架构须先转向、改计划并写决策，禁止沿旧名单加层。

## 路口

| 用到 | 路径 |
|---|---|
| 定档 | `~/.cursor/skills/route-task/SKILL.md` |
| 菜单 | `~/.cursor/harness/catalog.json` |
| 职种 | `~/.cursor/agents/<id>.md` |
| 事件 | `~/.cursor/skills/<id>/SKILL.md` |
| 计划 | `.harness/sessions/<会话>/loadplan.json` |
| 现行卡 | 同目录 `current.md` |
| 正式面 | `.harness/surfaces.json` |
| 刷新菜单 | `~/.cursor/harness/scripts/刷新菜单.py` |
| 生成名单 | `~/.cursor/harness/scripts/生成会话能力名单.py <会话>`（cwd = 业务根） |
| 名单 | 同目录 `activated.json` |
| 项目库 | `.harness/state.json` |
| 验证 | `.harness/artifacts/<工作项>/verify-report.json` |
| 缺口 | `~/.cursor/skills/doctor/SKILL.md` |
| 写隔离 | `~/.cursor/skills/write-isolation/SKILL.md` |
| 外接拉起 | `~/.cursor/harness/scripts/拉起外接.py` |
| 外接档位 | `~/.cursor/harness/mcp-tiers.json` |
