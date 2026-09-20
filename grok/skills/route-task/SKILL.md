---
name: route-task
description: 接到诉求后分析需要哪些事件/职种/外接，写加载计划、现行卡并生成会话能力名单。触发：定档、转向、插队、并行、工作模式、Plan、点名、现行卡、子代理。
---

# 任务定档与加载计划

流程见第一层。本层是导演：点名、写现行卡、定写级别、拼第三层，不设运行时硬闸。

## 导演面（不只四条）

| 面 | 做什么 |
|---|---|
| 点名 | 只注入本轮真要用的 skill/craft/mcp，防灌 |
| 现行卡 | 下一手不靠聊天：目标、上一步、进度、禁改、下一手 |
| 试错 | 失败路径写进现行卡或 scratch，不污染正式面 |
| 正式面地图 | 读 `.harness/surfaces.json`，分清官方根与隔离根 |
| 通用沙盒 | 表/代码/引擎/资产一律先写隔离根，见 `write-isolation` |
| 晋升 | 人准后只回写记录集，禁止整文件覆盖正式面 |
| 记忆 | `retrieve_keys` 命中才读 canon/adr，不扫全库 |
| 范围禁改 | `forbid` 与写级别写进计划与现行卡 |
| 收口 | 按档位只核核心证据 |
| 并行所有权 | 各会话各卡；互不依赖时开子代理，不请人切产品多开 |
| 子代理 | 适当多用。岗位职责不同时优先按职种各开一只，主会话点名与收口 |

## 怎么分析、怎么点名

1. **复述**：目标、交付物、范围边界。不清先问清。
2. **拆成要做的事**：把诉求拆成 1～N 个可执行事件。
3. **对照菜单选 id**  
   打开 `~/.cursor/harness/catalog.json`。  

   对每一件事：
   - 读技能/职种的 **description 与标题**，看谁最贴。
   - **事件技能**：事怎么做 → 点 `skill`。
   - **职种**：需要该职种主路径或换角色视角 → 点 `craft`。  
     点了职种只注入职种正文 + `craft_open`（第一步），路径其余技能做到那一步再打开。  
     同一诉求里岗位职责不同（多个 craft，或要换角色视角做完整一段）→ **优先各开子代理**，不要主会话串演多个岗位。
   - **外接**：开场就要用的才点 `mcp`。过程中新用到的直接调，不必为放行改计划。
   - 菜单里没有合适 id：先走 doctor，再按任务补技能/职种/外接后重新定档。
4. **每项写为何**：`why` 至少 8 字。对不上就换 id。
5. **定档位**（收口只核核心证据）：

| 说法 | `tier` | 建议 `verify_kind` | 验证粒度 |
|---|---|---|---|
| 讨论 | `Discuss` | `none` | 不写报告 |
| 短活 | `T0` | `smoke` | 1 条主产物 |
| 已知配方 | `T1` | `schema` 或 `smoke` | 主产物 + 关键约束 |
| 多职种 | `T2` | `playtest` 或 `schema` | 再加跨职种接口；各职种优先子代理 |
| 硬闸 | `T3` | `build` / `release` | 再加构建或发版输出 |

6. **写加载计划**：`.harness/sessions/<会话>/loadplan.json`  
   - 必填：`session_id`、`tier`、`items`、`verify_kind`、`intent`、`work_mode`；有工作项则写 `bead_id`。  
   - 建议：`write_class`（`read` / `sandbox` / `promote` / `destroy`）、`retrieve_keys`、`forbid`。  
   - 每项：`kind`（`skill` / `mcp` / `craft` / `memory_plane` / `formula`）、`id`、`why`。  
   - `intent` / `work_mode` 按下表选，不得虚构产品能力。
7. **生成名单**：跑生成脚本。确认 `activated.json` 只含点名项，职种未预展开全路径；同目录写出 `current.md`。
8. 多事件再走拼装。收口走验证技能。
9. **中途改口径**：先改计划再动手。转向只改受影响项；插队开新会话，旧件 progress 写已停。

## 意图与工作模式

先判意图，再写计划。默认留在制作；只有做法分叉才申请切 Plan。

| 用户在做什么 | `intent` | 会话 | 默认 `work_mode` |
|---|---|---|---|
| 同一件接着做 | `continue` | 同目录，计划可不动 | `agent` |
| 同一件改口径 | `steer` | 同目录，改计划增量 | `agent`；做法分叉改 `plan` |
| 上一件未完，先做另一件 | `park` | 新目录做新件 | `agent` |
| 另一件交付 | `new` | 新目录 | 按档位 |
| 两件互不依赖都要 | `parallel` | 各件各目录 | `agent` |
| 只要选项、先不定 | `discuss` | 口头或 `verify_kind=none` | `agent` |

`work_mode`：

| 值 | 何时 | 代理怎么做 |
|---|---|---|
| `agent` | 已知做法；改数字/路径/口径但不换做法 | 留在制作。若人在 Plan 且方案已冻，申请切回 Agent |
| `plan` | 多种做法、架构、范围不清、转向推翻做法 | 写完计划后申请切到 Plan，等人确认。不能静默切 |

申请切 Plan / Agent 时用一句话说清为何；Ask、Debug 没有可切入口，不请人切。  
转向时禁止沿旧名单把上一稿做完。插队不关旧项。

## 子代理

自己判断何时开，不必等人准，也不写入 `work_mode`。**适当多用**；岗位职责不同时优先开，产出更稳。

**优先开**

- 岗位职责不同：已点多个 craft，或要换角色视角做完整一段 → 一职种一只子代理，主会话不串演
- 两件以上互不依赖，且不抢同一正式面
- 大范围检索/勘察，主线还要继续做别的

**何时不开**

- 同一岗位、同一正式面的连续步骤
- 单文件或单针查找
- 后一步必须吃前一步产物，且没有可交接的中间件
- 只为了「看起来在并行」

**怎么和 skill / mcp / craft 拼接**

1. 子代理不自动继承本会话名单。提示词写清：先打开哪些 skill、用哪些 mcp、正式面与隔离根、禁改。
2. 点了职种：`subagent_type` 用职种 id。只给该职种正文 + 路径第一步；其余技能做到那步再打开，与主会话同一条。
3. 外接按提示调用，不灌全量工具表。缺的当场调，不必先改名单。
4. 主会话收口：对结果、写现行卡、关项。子代理不改当前行指针。

改产品表点 `excel-com-write`，并遵守 `write-isolation`。  
`Discuss` 档只出选项。

## 定档指针

开放世界美术 / 音频路径用 `mcp.json` 现网键：

| 场景 | 优先 skill | 优先 mcp | 边界 |
|---|---|---|---|
| 地形 | `terrain-gaea-pass` | `gaea` | 图节点/工程文件级 |
| 树木植被 | `env-asset-checklist` | `treeit` | 文件/工作区级；无 GUI 遥控 |
| 角色建模/材质 | `character-asset-checklist` | `blender-mcp` `materialpilot` `meshlab` | |
| 绑定 | `bind-rig-checklist` → `skin-weight-pass` | `accurig` `blender-mcp` | AccuRIG=文件/工作区，非 GUI 自动绑骨 |
| 动捕参考 | 动画相关 skill | `rokoko` | 文件/工作区级 + Listen 探针；GUI 重定向仍人做 |
| 音频 Bank | `audio-fmod-checklist` / `fmod-bank-build` | **`fmod-cli`**（主）`fmod-studio`（辅，需 Studio TCP） | 事件编辑在 Studio GUI |
| 关卡 2D | 关卡相关 | `ldtk` `tiled` | 文件级 |
| 体素草案 | | `magicavoxel` | 文件级 |
| 引擎抽检 | `import-validate` | `gamedev-mcp` | 写在正式面地图的 engine 隔离根 |

仍为 launch-only（勿写成可代工）：`pureref` `rokoko` `materialize` `xnormal` `meshroom` `audacity`。

mcp id 必须是 `mcp.json` 的键；缺键先 doctor。
