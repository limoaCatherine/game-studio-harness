---
name: combat-flow-design
description: 定可入库的战斗流程骨架：标准步骤 id、时间模型、资源轴、判定公式语法与胜负条件，供代码管线与配表直接引用。触发：战斗流程、combat flow、步骤名标准化、判定公式、接代码。
---

# 战斗流程怎么定骨架（可接代码）

本技能产出必须能进代码与配表：**步骤用稳定英文 id**，**判定用可解析公式语法**，中文只作说明，不进标识符。

## 何时用

- 新战斗系统或大改时间/资源/判定管线
- 步骤名口语化、无法映射状态机或表主键
- 判定公式写法不统一，客户端/服务器/数值对不齐
- 关卡与数值对一局结构理解不一致

## 标准标识约定（全局）

| 种类 | 语法 | 例 |
|---|---|---|
| 步骤/状态 id | `snake_case`，前缀 `cf_` | `cf_startup` `cf_active` `cf_recovery` |
| 事件 id | `snake_case`，前缀 `ev_` | `ev_hit_confirmed` `ev_whiff` |
| 资源 id | `snake_case`，前缀 `res_` | `res_stamina` |
| 属性主键 | 与属性框架一致 | `atk_phys` `hp_max` |
| 公式 | 纯函数表达式，字段用 `{attr}` / `{res}` / 字面量 | `max(0, {atk_phys} * {skill_coeff} - {def_phys})` |
| 时间 | 仿真 tick（整数），禁止用渲染帧口语代替字段 | `startup_ticks` `active_ticks` |

禁止：中文当字段名、空格/驼峰混用当表主键、用「大概一下」描述窗口。

## 怎么做

### 1. 写 brief 与成功标准（可测）

**做**
1. 读支柱与（若有）遭遇目标；写 ≥3 条成功标准，每条绑定测量：战斗日志计数、tick 秒表、调试 overlay。
2. 禁改区表：`attribute-framework` / 关卡预算 / 网络权威 / 既有 `skill-kit`——标 `locked` 或 `open`。
3. 模式：`mode=new|extend|audit`；`audit` 默认不改产品表。
4. 输出路径：`combat/flow_<flow_id>_brief.md`（`flow_id` 为 `snake_case`）。
5. 自检：`rg -n "success|locked|mode=" combat/flow_<flow_id>_brief.md` 无空槽。
6. 失败→回本步：成功标准无测量面或禁改空。

**做到**：brief 含 `flow_id`、≥3 条可测标准、禁改表、mode。

### 2. 冻结时间模型（标准字段）

**做**
1. 选定 `time_model` ∈ `realtime_fixed_tick|semi_realtime|turn|timeline_pause`；写入 `time_model_version`。
2. 冻结推进单位：`tick_hz`（如 30/60）与字段：
   - `startup_ticks` / `active_ticks` / `recovery_ticks`
   - `hitstun_ticks` / `blockstun_ticks` / `iframe_ticks`
3. 管线阶段顺序（代码必须同序，id 固定）：

```text
cf_input_collect
→ cf_validate_actor
→ cf_skill_timeline
→ cf_hitbox_window
→ cf_target_filter
→ cf_hit_resolve
→ cf_damage_calc
→ cf_apply_effects
→ cf_emit_present
```

4. 权威边界：伤害结算只在 `cf_damage_calc`+权威侧；表现只订 `cf_emit_present` 事件，不改 HP。
5. 去重：同一 `attack_uid` 对同一 `target_id` 在窗口内只结算一次（`hit_once_set`）。
6. 失败→回步骤 1：与禁改「网络权威」冲突则改模型或升级决策。

**做到**：`time_model_version` 冻结；上列阶段 id 写入骨架；未冻结不得填技能前摇字段。

### 3. 资源轴（表字段）

**做**
1. 写 `combat/resource_axis.csv` 列：

```text
res_id,attr_key,cap_src,regen_per_tick,persist_ooc,empty_effect,ui_always_on
```

2. `attr_key` 必须存在于属性框架；缺则先补框架。
3. 产品表列 vs 运行时字段分界写入清单；改产品表走表格写入配方。
4. 同窗口资源总负担上限向用户索取；超限先砍技能包结构。
5. 验证：耗尽后释放应走 `cf_validate_actor` 失败；日志关键字 `reject_reason=res_empty`。
6. 失败→回步骤 2。

**做到**：csv 每行合法；空资源释放实验符合预期。

### 4. 判定与伤害公式（标准语法）

**做**
1. 判定管线只用下列事件 id（可增补但必须登记）：
   - `ev_hit_confirmed` / `ev_whiff` / `ev_blocked` / `ev_iframe_ignore`
2. 命中条件公式字段（布尔表达式，可进配置）：

```text
hit_gate = in_range({dist}, {range_max})
         && facing_ok({attacker_yaw}, {target_pos})
         && not in_iframe({target_id})
         && not already_hit({attack_uid}, {target_id})
```

3. 伤害公式（纯函数，结果写入 `damage_out`）：

```text
damage_out = max(0,
  ({base_damage} * {skill_coeff} * {zone_coeff})
  * (1 - {mitigation})
  + {flat_bonus}
)
mitigation = clamp({def_score} / ({def_score} + {def_k}), 0, 0.9)
```

4. 公式里每个 `{token}` 必须映射到：属性主键、技能表列、或运行时常量；输出 `combat/formula_<flow_id>.json`：

```json
{
  "flow_id": "example",
  "hit_gate": "…",
  "damage_out": "…",
  "tokens": { "base_damage": "skill.base_damage", "atk_phys": "attr.atk_phys" }
}
```

5. 版本字段 `formula_version`；变更要可 diff。
6. 失败→回属性框架或缺列：token 无法解析则不许标通过。

**做到**：公式文件可被校验器解析；无中文标识符；`formula_version` 有值。

### 5. 节奏模板与胜负 id

**做**
1. 四段模板 id：`seg_open` / `seg_pressure` / `seg_release` / `seg_close`；每段：`pressure_band`、`new_info_budget`、`exit_cond_id`。
2. `exit_cond_id` / `win_cond_id` / `fail_cond_id` 用 `snake_case`，供 `encounter-script` 引用。
3. 可读性预算：`max_onscreen_threats`、`max_vfx_disturb`；超限降级策略写入骨架旁注。
4. 一页骨架：`time_model + resource_axis + stages + formulas + segments + winlose`。
5. 与 `skill-kit-design` 的释放窗字段对齐（`startup_ticks` 等同名）。
6. 失败→回步骤 3/4：缺资源或公式 token。

**做到**：≥1 个遭遇可引用 `flow_id`；胜负 id 可指；无中文主键。

### 6. 接入代码管线自检

**做**
1. 对照清单：阶段 id 表、事件 id 表、公式 token 表、资源 csv、cond id 表。
2. 用仓库或工具链里已有命名检查（若有）跑一遍；没有则人工 `rg` 中文/空格字段名。
3. 调试：打开 hitbox overlay + damage log；同一 `attack_uid` 不得双计。
4. 登记产物路径到产物索引。
5. 失败→回对应步骤；不把「口算过」当通过。

**做到**：自检清单全勾；日志无双计；产物已登记。

下一步常接：`skill-kit-design`；`combat-modeling`；`encounter-script`；`combat-feel-checklist`。

## 参考类型（非原文）

- 固定 tick 伤害管线与去重 / 权威结算
- 帧数据：startup/active/recovery、hitstun、i-frame
- 规则层与表现层分离（rules → outcome → present events）
