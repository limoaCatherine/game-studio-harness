# L4 档案柜

第四层承认模型没有可靠的长期记忆，因此把状态与已批准事实写成文件。业务根以 `.harness` 为库。

## 处理什么

- 正式面 ↔ 隔离根对照（`surfaces.json`）
- 当前行（`state.json`）与只追加流水（`tasks.jsonl`）
- 现行卡与会话目录
- 已批准事实（`canon/`）与决策（`adr/`）按键打开
- 验证报告与产物索引

## 解决什么

没有档案柜：换窗口就丢进度；沙箱试错覆盖正式表；口头讨论被当成 canon；关项没有证据链。

## 路径

仓库示例脚手架：`studio/.harness/`（空数据、占位路径）。安装时只把**缺失**文件合并进业务根。

| 表 | 路径 |
|---|---|
| 当前行 | `.harness/state.json` |
| 正式面地图 | `.harness/surfaces.json` |
| 默认地图模板 | `harness/surfaces.default.json` |
| 任务流水 | `.harness/memory/tasks.jsonl` |
| 已批准事实 | `.harness/memory/canon/` |
| 决策 | `.harness/memory/adr/` |
| 进度摘要 | `.harness/memory/status/` |
| 产物索引 | `.harness/artifacts/index.jsonl` |
| 验证报告 | `.harness/artifacts/<工作项>/verify-report.json` |
| 代码隔离 | `.harness/worktrees/` |
| 会话 | `.harness/sessions/<id>/` |

## 缺席崩溃模式

| 模块 | 缺席时 |
|---|---|
| `surfaces.json` | 不知道官方根与隔离根；默认写级别无法落地 |
| `write-isolation` 技能 | 代理直写正式 xlsx / 主仓 / 引擎资源 |
| `state.json` | 换 IDE 不知道当前会话 |
| `tasks.jsonl` | 无审计流水；进度被改写而不是追加 |
| `canon/` | 口头想法指导下游；或开场扫描全库撑爆窗口 |
| `verify-report.json` | L1 结束钩子无法关项；口头绿 |
| `studio/.harness` 示例 | 新业务根没有可复制的空结构 |

## 写隔离牙齿

- 表：同级 `sandbox/` 副本 + changeset，晋升只回写记录格
- 代码：`.harness/worktrees/`，人准后再合并
- 引擎：sandbox 根，禁止把试错盘当官方 Content
- 资产：`_Dev/`，不进发版包
- `**/sandbox/` 与中文 `**/沙箱/` 应进各仓 `.gitignore`
