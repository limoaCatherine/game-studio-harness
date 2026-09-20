---
name: combat-modeling
description: "建战斗对象生命周期表、状态机与事件载荷，冻结结算管线顺序并对齐端权威。触发：战斗建模、战斗实体、状态机、事件载荷、combat model。"
---

# 战斗对象与管线怎么建模

## 何时用

- 战斗对象/状态机未建模或隐式状态横行
- 事件载荷与结算顺序有争议
- Buff/召唤物/投射物流转与销毁不清
- 需给服务器权威与客户端预测对齐的边界

## 怎么做

### 1. 枚举对象生命周期表

**做**
1. 列对象类并给稳定类型 ID：`Unit` / `Projectile` / `Area` / `Summon` / `Trap` / `DoTZone`（按项目裁剪）；口头称呼回指 type_id。
2. 每类填生命周期表列：`type_id | 创建条件/事件 | 附着规则 | tick 挂点 | 销毁条件 | 主人死亡行为 | 数量上限与替换策略 | 权威(ServerOnly/ClientPredict)`。
3. tick 挂点与 `combat-flow-design` 推进单位交叉勾选（输入后/移动后/结算后）；不一致当场改表。
4. 召唤物/陷阱：最大存活时间或回合、超限替换（FIFO/优先级）、主人死亡时 Destroy 或 Orphan——无销毁条件不得过本步。
5. 输出 `combat/object_lifecycle.md`（或表）；缺权威列向程序确认槽，不猜。
6. 表缺列或 type_id 冲突：停在本步补齐销毁条件，再进状态机。

**做到**：每类有 type_id+创建/销毁+权威+tick 挂点；召唤物销毁条件可执行。

### 2. 状态集、转换表与事件载荷

**做**
1. 状态集至少：`Alive` / `CrowdControlled` / `Invulnerable` / `Dead` / `Untargetable`（按适用）；每状态写进入/退出事件名（与代码/表一致，如 `OnEnter_Invulnerable`）。
2. 转换表：`event_name → from → to → 副作用`（清 Buff、停移动、关碰撞）；搜技能/Buff 文档「无敌/霸体/死亡」无 ID 的补进表或删逻辑依赖。
3. 事件载荷模板（字段名，不编数值）：`DamageRequest{src,tgt,channel,snapshot_id}`、`HealRequest{...}`、`BuffApply{buff_id,stacks,dur}`、`BuffDispel{...}`、`MoveImpulse{...}`、`SpawnObject{type_id,...}`；至少 5 个高频样例供订阅方核对。
4. 与战斗状态枚举 / 协议交叉：控制态/无敌是否同一套状态 ID；冲突并列请用户裁。
5. 载荷字段名与现有代码枚举/协议对照（grep 事件名）；对不上则改文档名或开接口任务，事件名与代码枚举统一，冲突改文档或开接口任务。
6. 隐式状态扫到：回到本步补转换表；隐式状态补进转换表。

**做到**：转换无隐式状态；≥5 事件载荷字段可订阅；状态 ID 与协议一致或矛盾已列。

### 3. 结算管线顺序与同帧规则

**做**
1. 冻结默认序（可调但唯一）：`Input → Move → SkillCast → HitResolve → DamageFormula → BuffTick/Jump → DeathCleanup`；写入 `combat/pipeline_vN.md` 带版本号。
2. 同帧冲突写死：死亡 vs 治疗谁先、多段命中合并/分发、破盾瞬间护盾与血的扣减序；给 2 套选项+利弊，用户选定后冻结。
3. 与 `damage-formula-pass` 快照规则交叉：管线取数时机不得与「施放锁定/命中取值」声明矛盾；矛盾回公式或回本步改序。
4. 投射物/区域：`spawn_frame | hit_frame | destroy_frame` 落在管线哪一段，写入对象表旁注。
5. 边界走读：破盾瞬间、致死治疗赛跑、召唤物与主人同死——歧义点修表后再往下。
6. 改序必须附影响面（技能/投射物/区域列表）；无影响面不得升版本。

**做到**：管线版本可复现；同帧规则明确；与公式快照无矛盾。

### 4. 模型图交付与权威对齐

**做**
1. 整理对象-状态-事件-管线为一张模型图（或等价边表）；节点名= type_id/状态 ID/事件名，模型图节点名= type_id/状态 ID/事件名。
2. 影响产品表字段列清单（对象类型、状态 ID、事件名）；变更走 `excel-com-write` → `tunable-table-diff`。
3. 与服务器权威、客户端预测各确认一次边界；不一致立项（ADR 或接口单），权威边界不一致先立项，不并行两套。
4. 未决接口三列：`缺什么 | 卡谁 | 是否阻塞本里程碑`；藏段落里不算交付。
5. 模型图版本号写入技能/Buff 表头旁注；旧理解填表发现后回到步骤 2/3 升版。
6. 抽检：任选 1 技能走读「事件名→载荷→管线段→权威」能指到表行；指不到则返工对应步。

**做到**：程序/数值共用同一模型图；表字段可指；未决可见；权威无双轨。

## 失败回哪一步

- 生命周期缺销毁/权威/tick → 回步骤 1
- 隐式状态或事件载荷对不上代码 → 回步骤 2
- 管线与公式快照矛盾或同帧规则未冻 → 回步骤 3
- 模型图/权威双轨或抽检指不到表行 → 回步骤 2/3 升版

下一步常接：`server-combat-authority-check`；手感 `combat-feel-checklist`；流程状态 id 见 `combat-flow-design`。

## 细则

### A. 命中窗与冲击分离

1. 动画 Notify / 时间轴事件只发射 `ev_hit_window_open|ev_hit_window_close`；禁止在 Notify 回调里直接扣血。
2. 命中检测组件在 `active` 窗内做扫掠/插值（prev_pos→curr_pos），降低高速挥砍漏判；同 `attack_uid`+`target_id` 入 `hit_once_set`。
3. 冲击结果（伤害、击退、受击反应）走 `cf_hit_resolve`→`cf_damage_calc`；表现事件 `cf_emit_present` 只订阅结果。
4. 对照：调试绘制 hitbox 与 hurtbox；日志打印 window open/close tick。
5. 不合格：Notify 内结算或无去重 → 回对象表权威列与管线序。

### B. 预测与权威边界字段

1. 每类对象填 `authority`：结算类默认 `server_only`；纯表现拖尾可 `client_predict`。
2. 客户端可预测字段清单：`anim,vfx,local_input_buffer`；不可预测：`hp,death,loot,cooldown_commit`。
3. 预测失败：写和解策略 `rollback_present|snap_correct`；与 `server-combat-authority-check` 同文案。
4. 随机：种子来源写在模型旁注 `rng_seed_at∈{room,round,cast}`；同种子可回放。
5. 检查：篡改客户端伤害包必须被服驳回（联调用例）。

### C. 同帧冲突决策表

| 冲突 | 选项 A | 选项 B | 冻结字段 |
|---|---|---|---|
| 致死 vs 治疗同帧 | 先伤后疗 | 先疗后伤 | `same_frame_heal_vs_lethal` |
| 多段命中 | 合并一次跳字 | 分段结算 | `multi_hit_mode` |
| 破盾瞬间 | 先扣盾再溢血 | 按比例分摊 | `shield_break_overflow` |

用户选定后写入 `pipeline_vN.md`；改表必须附影响面列表。
