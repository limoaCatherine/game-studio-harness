---
name: skill-kit-design
description: "定定位、槽位职责、资源与冷却结构，交付可填系数的技能包骨架。触发：技能包、skill kit、技能组设计。"
---

# 技能包怎么搭骨架

## 何时用

- 新角色/职业技能组要设计
- 技能职责重叠或真空
- 资源轴与技能不匹配
- 要给数值/动画/VFX 的槽位骨架

## 边界

能力系统公开实践普遍把「元数据/费用/冷却」「编排（施放/取消窗）」「命中冲击」「表现层」拆开；动画 Notify 只报时间窗，不直接结算伤害。本技能只定职责与字段骨架，系数交给 `skill-numeric-pass`，命中权威交给服务器侧。

## 怎么做

### 1. 定定位与对手问题

**做**
1. 定位句：输出/控制/生存/辅助主次 + 非目标（明确不做 X）；写入 `kit/<kit_id>_brief.md`，`kit_id` 用 `snake_case`。
2. 对手问题表列：`gap_id|problem|owner_slot|notes`——突进/消耗/爆发/驱散/逃生；每条「谁的问题」一列。
3. 打开 `combat-flow-design` 的 `resource_axis.csv` 与可读性预算；超预算先砍技能数/同屏特效，不靠数值压感。
4. `rg -n "否决|anti-example" pillars/` 对读支柱；撞否决→改定位或升级决策。
5. 两套重心（更爆发/更持续）+利弊；用户选定后冻 `kit_focus∈{burst,sustain,hybrid}`。
6. 对照工具：表格连接器打开资源轴；版本库看 brief 是否已有同 `kit_id`。
7. 失败→回本步：定位撞支柱或资源轴未冻——先裁决再分槽。

**做到**：brief 含定位/非目标/对手问题；资源轴路径可指；`kit_focus` 已选定。

### 2. 分配技能槽职责（槽位表）

**做**
1. `kit/<kit_id>_slots.csv` 列：`slot_id|duty|cadence|effect_type|channel_hint|non_goal`（`slot_id` 如 `slot_basic|slot_skill_a|slot_ult|slot_passive|slot_mobility`）。
2. 重叠检查：两槽 `duty` 同义→合并或改；真空：对手问题无人答→补槽或改定位；可用表公式或脚本扫重复 `duty`。
3. 两套结构（少而全能/多而专精）+利弊；用户选定冻 `slots_version`。
4. 被动/光环：触发条件字段 `trigger_cond`、霸体 `super_armor?`、是否占可读预算写入文档。
5. `effect_type` 供 numeric 挂公式通道（如 `damage_phys|cc_stun|heal|shield`）；本步系数列留空。
6. 用能力编辑器/技能调试列表核槽位数与 csv 行数一致；不一致先对齐再往下。
7. 不合格信号：编辑器多出幽灵槽、或 csv 有行但无 `skill_id` 绑定计划。
8. 失败→回步骤 1：真空/重叠无法在槽内消化——回改定位。

**做到**：csv 无重叠无真空；`slots_version` 冻结；每槽 `effect_type` 可挂；编辑器槽数=表行数。

### 3. 资源、冷却与连招骨架（字段级）

**做**
1. 每技能字段（名级，不填样例秒当正式数）：`cost_res|cooldown_field|precond|cancel_window_field|combo_window_field|startup_ticks|active_ticks|recovery_ticks`。
2. 标准循环图（mermaid/白板）：`open→loop→burst→escape`；标退化键（只会普攻能否活/交机制）。
3. 对照资源轴：循环内消耗总和 vs 回复；用计算器或表公式验是否可持续；不可持续→回调职责或资源。
4. 动画/特效/音效钩子空槽名列表 `kit/<kit_id>_hooks.txt`（Anim Notify / Socket 名）；本步不填死时长。
5. 连招三岔：`combo_success|combo_fail|combo_interrupt`——无岔口标 `brittle=true`。
6. 与 `combat-modeling` 预留事件名：`ev_skill_cast|ev_skill_cancel|ev_skill_interrupt`；`rg` 确认未与旧事件撞名。
7. 检查：循环图每节点能指到 `slot_id`；钩子名可被动画 Owner 检索。
8. 失败→回步骤 2：冷却字段与槽节奏矛盾或循环不可持续——改职责/字段。

**做到**：字段级资源/冷却齐全；循环含退化；钩子列表可指；三岔齐全或已标脆；事件名无撞车。

### 4. 交付数值与表现接口

**做**
1. 交 `skill-numeric-pass` 表头：`skill_id|slot_id|duty|cost_res|cd_field|effect_type|channel`；系数列空；沙盒走表格写入配方。
2. 禁改职责 vs 可调数值分栏写入 brief；禁改变更须重开 kit。
3. 表现接口：钩子名、Socket、是否需新动画——交 anim/vfx Owner；记路径与责任人。
4. Play 模式或技能调试面板点每个槽一次，确认事件名出现在战斗日志/Console。
5. 冻本版职责；仅允许调数值字段直到下次 kit 变更；版本号写入 `slots_version`。
6. 抽检：任选一槽走读「slot→事件→钩子→通道」能指到表行。
7. 失败→回步骤 3：调试面板无事件或钩子名 Missing——补钩子/事件名再交 numeric。

**做到**：numeric 可直接填系数；禁改/可调分栏可见；每槽日志有事件信号；职责冻结。

## 失败回哪一步

- 定位/资源轴未冻 → 回步骤 1
- 槽重叠真空或版本未冻 → 回步骤 2
- 循环不可持续/事件撞名 → 回步骤 3
- 调试无事件或接口缺字段 → 回步骤 3/4

下一步常接：`skill-numeric-pass`；`combat-feel-checklist`；`combat-flow-design`。

## 细则

### A. 槽位与事件接代码

1. `slot_id|duty|cadence|effect_type|channel_hint` 稳定英文；系数列空交 numeric。
2. 循环图含退化键；资源消耗总和 vs 回复用表公式验可持续。
3. 事件名 `ev_skill_cast|ev_skill_cancel|ev_skill_interrupt` 与 modeling 对齐，`rg` 防撞。
4. 调试面板每槽点一次见日志事件；钩子列表交 anim/vfx。
5. 禁改职责 vs 可调数值分栏；禁改变更重开 kit。
