# L2 定档

第二层是导演，不是工人。它把模糊诉求变成可审计的上下文边界、写级别和收口证据。

## 处理什么

- 复述目标、交付、范围；不清先问
- 对照 `catalog.json` 点名 `skill` / `craft` / `mcp`，禁止现场发明 ID
- 定 `tier`（Discuss / T0 / T1 / T2 / T3）与 `write_class`（read / sandbox / promote / destroy）
- 写 `loadplan.json`，生成 `activated.json` 与 `current.md`
- 职种只打开 `craft_open`（路径第一步）

## 解决什么

没有定档，模型会拿到诉求就改表、同时扮演多个岗位、用最后一步的口径做第一步、把口头范围当成合同。

## 路径

| 模块 | 路径 |
|---|---|
| 导演技能 | `skills/route-task/SKILL.md` |
| 名单生成器 | `harness/scripts/生成会话能力名单.py` |
| 执行单 | `harness/scripts/建议执行单.py` → `.harness/sessions/<id>/flow.json` |
| 计划 | `.harness/sessions/<id>/loadplan.json` |
| 名单 | `.harness/sessions/<id>/activated.json` |
| 现行卡 | `.harness/sessions/<id>/current.md` |
| 会话指针 | `.harness/sessions/LATEST` |

## 缺席崩溃模式

| 模块 | 缺席时 |
|---|---|
| `route-task` | 无导演面：不复述、不点名、不定档、不写现行卡 |
| `生成会话能力名单.py` | 计划只是聊天记录；开场无法注入可审计名单 |
| `activated.json` | 钩子不知道点了谁；`craft_open` 丢失，职种被当成技能清单 |
| `current.md` | 压缩上下文或换窗口后失忆；下一手靠猜 |
| `建议执行单.py` | 多事件时先跑收口再做制作 |
| `LATEST` | 开场钩子读错会话，注入过期现行卡 |

## 职种不预展开

点名 `combat-numeric-designer` 只注入职种正文 + 第一步（通常是 `combat-modeling`）。路径上的 `damage-formula-pass`、`excel-com-write` 做到那一步再打开。生成器若把全部 `uses_skills` 写入 `skills`，视为回归失败。
