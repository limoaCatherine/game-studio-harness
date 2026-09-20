---
name: vfx-skill-hook
description: "按 Timeline/Notify 帧与 Socket 名挂技能特效，核粒子预算与 Overdraw，并处理打断清理。触发：特效挂点、技能VFX、Socket、Notify帧、overdraw、粒子预算。"
needs_mcp: gamedev-mcp
---

# 技能特效怎么挂

## 何时用

- 技能特效与动画对不齐或相位错位
- Socket/Notify 名缺失或漂移
- 打断后特效残留跟随
- 粒子/Overdraw 超预算要降配

## 怎么做

### 1. 对齐 Notify/Socket 字典

1. 读 `skill-kit`、`anim-event-hook` 事件字典、Socket 表；合并同义异名，缺口标阻塞。
2. 事件名/Socket 名逐字比对（大小写/下划线）；「差不多」一律改到字典正式名。
3. 确认挂点父骨与用途与绑定侧一致；不一致回 `bind-rig-checklist` 修名或偏移。
4. 在 Socket 上临时挂十字/调试球核对朝向与缩放，再换成正式特效。
5. 本批技能列表与优先级向用户确认；先挂竖切技能；字典版本号写入挂接表头。
6. 缺字典条目：停本步补字典，补齐正式名后再挂。

**做到**：Notify/Socket 与字典逐字一致；调试球朝向已核；缺口已补或阻塞。

### 2. 按相位写挂接表（帧号）

1. 挂接表列：`skill_id | phase(前摇/命中/收招) | vfx_asset | socket_name | notify_or_timeline_frame | space(Follow/World) | cleanup(Kill/Detach/Fade)`。
2. 打开 Animation Timeline / Notify 轨道：读触发帧号写入表；以事件帧为正式方案，硬延时只作临时排查。
3. 取消/打断/死亡清理动作必填；无 cleanup 行补齐后再上线。
4. 对照 `vfx-budget-pass`：本技能粒子数峰值、同屏实例预算；超上限则降配或申报后再挂。
5. 地面贴花/预警：生成点（脚底/落点）与生命周期帧数写清。
6. 帧号与判定窗差 >1 帧：回 `anim-event-hook` 改 Notify 或改挂接帧。

**做到**：挂接表完整含帧号与 cleanup；预算内或已申报；正式方案用事件帧。

### 3. 联调：对齐帧、Overdraw、实例计数

1. 同屏播：慢放/逐帧 scrubber 看生成点、朝向、落地帧；对照 Hit Notify 是否同帧。
2. 开 Overdraw/Shader Complexity 视图（引擎约定热力图）：命中闪与大范围粒子标红区是否超项目阈值；超则降粒子数/改材质/缩时。
3. 开特效实例计数（Profiler 自定义或控制台统计）：连放是否泄漏；泄漏修 cleanup 逻辑。
4. 死亡/传送后强制清实例；残留跟随记失败并回步骤 2 补 Kill。
5. 低画质档抽测：降级后关键可读特效（命中闪/预警）仍在。
6. 偏帧/错点/超 Overdraw 列表：修完再往下；修不了标阻塞 Owner。

**做到**：偏帧列表已处理；Overdraw 视图无超标红区或已降配；无实例泄漏。

### 4. 连放/打断复核与表冻结

1. 快速连放、取消、镜像角色、传送各测一轮；实例计数归零。
2. 父子空间切换（手↔背）复核；路径写回挂接表。
3. 多人同屏抽测限流：触发限流时保留关键受击反馈。
4. 冻结本批挂接表版本；与 `anim-event-hook` 字典版本交叉写在表头；改相位/Socket 必须升版并重跑步骤 3。
5. 回归包：连放、打断、死亡、传送、镜像各至少一 skill_id；泄漏清零后再进正片。
6. 清理调试十字/强制生成键；通知 `client-combat-frame-debug` 可对表联调。

**做到**：连放/打断无残留；表已冻结可回归；预算与 Overdraw 合格。

## 做到

- Notify/Socket 与字典对齐无野名；相位→资产→Socket→帧号→cleanup 表齐全
- 打断/死亡/传送实测无残留；实例计数不泄漏
- Overdraw 视图抽检合格或已降配；挂接表版本与动画字典版本交叉；正式方案用事件帧

## 失败回哪一步

- 字典缺口、Socket 名漂 → 回步骤 1（必要时 `bind-rig-checklist` / `anim-event-hook`）
- 缺 cleanup、硬延时当正式、超预算未申报 → 回步骤 2
- 偏帧、Overdraw 超、实例泄漏 → 回步骤 3（泄漏回 2 补 Kill）
- 连放残留、限流误关受击反馈 → 回步骤 2 改 cleanup 或回 3 降 Overdraw

下一步常接：`client-combat-frame-debug`；预算争议回 `vfx-budget-pass`。
## 加厚：技能↔特效挂接表

### A. 表字段（强制）

1. skill_id / anim_id / event_name / frame / socket / vfx_asset / 预算版本 / 降级档引用。
2. 缺事件名或预算版本 → 拒挂；先回 `anim-event-hook`/`vfx-budget-pass`。
3. 同帧多特效：声明排序与是否互斥；避免同 Socket 叠爆。
4. 打断：取消时是否 Kill 特效；用例进冒烟。
5. 左右武器/镜像：Socket 与事件映射写清。

### B. 联调

1. 慢放出招：特效出现帧=事件帧±容差；超容差改挂接或改事件，不改玩法垫时。
2. 低端档播一次降级路径；可读底线（受击/危险区）仍在。
3. 路径变更同步表；旧路径废弃。
4. 与客户端帧调试职种对齐同一字典版本。

**做到加厚**：挂接表无空强制字段；冒烟含打断与低端降级。
## 检查清单（密化）
1. 挂接表强制字段：skill_id、anim_id、event_name、frame、socket、vfx_asset、预算版本、降级引用——缺一拒挂。
2. 冒烟：正常出招、打断取消、低端降级各一条录屏。
3. 同字典版本号与 `anim-event-hook` 交叉打印一次防漂。
4. 路径变更有废弃说明；引用扫描无旧路径。
5. 超预算未申报不得进可玩包。

## 工具锚点（live mcp.json）

- `gamedev-mcp`：事件 Notify / Socket 试播
- `blender-mcp`：网格类特效源
- `ffmpeg`：对帧录像
- `everything-search`：定位旧映射表
- **DoD：** 事件名↔特效资产映射表；对帧误差可接受；导入路径冻结。
