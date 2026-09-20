# Game Studio Harness

跨工具入口。技能/职种/规则/钩子/运行时的唯一真相在仓库根 `skills/` `agents/` `rules/` `hooks/` `harness/`。各工具目录只是投影。Cursor 才有钩子运行时；其它工具按本文件约定工作。

定档 → 制作 → 结案。同一未关目标续同一会话。

开场读序：本文件 → `.harness/sessions/<会话>/current.md` → 名单里点名的技能/职种正文 → 计划 `retrieve_keys` 命中的 canon/adr。不要把菜单全文灌进上下文。

## 名单

`activated.json` 只决定开场先注入哪些正文，不是运行时防火墙。

1. 计划里点名的 `skill` / `craft` / `mcp`，id 在 catalog 中则进入对应列表。
2. 已点名 skill 的 `needs_mcp` 并入 `mcp_allow`。
3. 已点名 craft **不预展开** `uses_skills`。只写 `craft_open`（路径第一步）。
4. 开场只读名单里的正文。过程中缺技能或外接：当场打开或调用。

## 写隔离

写级别默认 `sandbox`。改正式面前先落到 `.harness/surfaces.json` 里的隔离根。晋升须人准，且只回写记录集。禁止整文件覆盖正式面。密钥不进仓库。

## 会话

- 续：同一聊天且同一未关交付 → 改计划增量，再生成名单。
- 转向：口径变了 → 先改计划再动手。
- 新：新工作项 → 新会话目录。
- 并行：互不依赖的两件 → 各开会话；岗位不同时按职种开子代理。

## 定档

复述目标、交付、边界。写 `.harness/sessions/<短名>/loadplan.json`，必填 `session_id` `tier` `items` `verify_kind` `intent` `work_mode`。再生成名单。

```text
python %USERPROFILE%\.gsh\harness\scripts\生成会话能力名单.py <短名>
```

## 四层

宪法 → 定档 → 技能/职种/外接 → 业务根档案柜。四层已封版。改架构须转向、改计划、写决策。
