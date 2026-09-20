---
name: combat-feel-checklist
description: "用帧预览、输入缓冲窗、Hitstop 帧与镜头震动强度检查战斗手感，短片作证据。触发：战斗手感、打击感、hitstop、input buffer、camera shake。"
---

# 战斗手感怎么查与改

## 何时用

- 技能发飘/过肉，需落到帧与反馈参数而非形容词
- 输入缓冲、取消窗、Hitstop 有争议
- 镜头震动/闪白超预算要可配置降级
- 数值已定但手感未过，需分流反馈 vs 数值

## 边界

格斗/动作公开资料把 startup/active/recovery、hitstun/blockstun、hitstop、i-frame、输入缓冲当作可测帧数据；命中停顿与镜头反馈宜在权威确认后加强，避免纯预测反馈在回滚时“假打”。本清单只验收反馈轴，不改伤害数字。

## 怎么做

### 1. 建可测检查轴与抽检名单

**做**
1. 固定六轴：`feel_startup_feedback|feel_hitstop_flash|feel_hurt_read|feel_cancel_armor|feel_cam_shake|feel_audio_hook`；每轴写通过/失败样子须录像可辨。
2. 打开手感预算表（或向用户索取）：`hitstop_ticks_cap|shake_stack_cap|input_buffer_ticks|vfx_clutter_cap`；无数字不开评。
3. 抽检名单：每武器/职业至少普攻、小技能、大招、位移各一；向用户索取 `skill_id` 列表。
4. 工具面：引擎 Timeline 帧 scrubber、输入调试 overlay、Camera Shake 强度读数、短录屏（5～10s）。
5. 检查卡写入任务备注：轴、预算数字、抽检 `skill_id`；换人复检用同一卡。
6. 声明本清单不管伤害高低；跳字异常分流 `skill-numeric-pass`。
7. 对照：预算表路径、上一版检查卡版本号。
8. 失败→回本步：轴或缺预算数字。

**做到**：轴与预算数字齐；抽检 skill_id 可点名；工具面已就绪。

### 2. 逐技能量帧与缓冲

**做**
1. 对目标 `skill_id`：帧 scrubber 读前摇/判定/后摇；对照表字段 `startup_ticks|active_ticks|recovery_ticks`；差 >1 tick 记入偏帧表。
2. 命中瞬间量 Hitstop：停顿 ticks 写入 `skill_id|hitstop_ticks`；超预算标红；无停顿/无闪白记失败。
3. 输入缓冲：读「键按下→被接受」间隔；对照声明 `input_buffer_ticks`；窗外仍吞输入或窗内丢输入分别记。
4. 取消/霸体：对照 skill-kit 取消点；声明有但动画无 Notify → 标 `hook_missing`，返工动画事件钩子。
5. 受击方必评：至少一类人形敌 + 一类特殊体型；无受击方向/僵直可读性记失败。
6. 多段技能逐段勾反馈；缺段单独成行。每条失败附短片 `feel/<skill_id>_<axis>.mp4`；无证据的「发飘」不入库。
7. 跳字过大但 Hitstop/受击正常 → 分流 numeric，不在本表改伤害。
8. 不合格回步骤 1：检查卡缺轴导致采不到读数。

**做到**：问题落到 `skill_id+轴+帧/ms 读数+短片`；数值与反馈已分流。

### 3. 镜头震动与改法归属

**做**
1. 读 Camera Shake：振幅/频率/时长或 Intensity 曲线；同屏叠加用调试计数器。
2. 超预算降级：减振幅、加触发冷却、合并同帧多次触发；降级须可配（表字段或资产参数）。
3. 优先级：受击不可读 > 无命中 Hitstop > 取消窗缺失 > 震动过激 > 音频缺失。
4. 每修项写归属：改动画事件帧 / VFX 钩子 / Hitstop 字段 / Camera Shake 资产 / 音频事件。
5. 同问题跨多 skill：抽公共钩子修，避免逐技能补丁漂移。
6. Hitstop/取消字段落产品表 → 沙盒表格写入；动画/VFX 记片段版本号。
7. 输出优先级表：`skill_id|axis|reading|priority|fix|owner`；可延后项写为何不挡里程碑。
8. 失败→回步骤 2：无读数则先重量帧。

**做到**：超预算有可配降级；每修项有归属与优先级。

### 4. 回归抽检与返工路由

**做**
1. 修完后用同一检查卡+同一机位重录；对比 Hitstop、缓冲窗、震动读数是否回预算内。
2. 残留分流：动画事件钩子 / VFX 钩子 / `skill-numeric-pass` / `combat-flow-design` / `client-combat-frame-debug`。
3. 修法引入新打扰：回步骤 3 再降级，不宣称手感已过。
4. 未修残留不得标通过；可延后必须写里程碑理由。
5. 回归包至少含：一条普攻 Hitstop、一条取消窗、一条受击方向、一条震动降级后抽检。
6. 读数回退恶化：回到步骤 2 重量帧。
7. 工具信号：前后读数 diff 表、短片路径列表。

**做到**：抽检有前后读数对比；残留有去向 Skill；预算未回退恶化。

## 工具锚

- 战斗流程 / 手感对照表 `.xlsx` 与公式文档 `.md`
- 客户端调试叠加日志；必要时空放进 `.harness/artifacts/`
- 配置表回读（表仓或 `excel` COM 写入后的 sheet）

## 失败回哪一步

- 轴/预算/抽检名单缺 → 回步骤 1
- 帧差或缓冲无法量化 → 回步骤 2
- 超预算无降级或无归属 → 回步骤 3
- 回归缺前后对比或读数回退 → 回步骤 2/4

下一步常接：动画/VFX 钩子；`client-combat-frame-debug`；数值回 `skill-numeric-pass`。

## 细则

### A. 帧数据与网络手感

1. 本地验收固定逻辑 tick（如 60Hz 上限），关闭动态帧率干扰采样。
2. 若项目有 rollback/预测：Hitstop/震屏优先在 `hit_confirmed` 后触发，减少假打；预测层只做轻反馈。
3. 记录 `frame_advantage` 相关读数仅作手感参考，不在本清单改数值 TTK。
4. i-frame 窗：对照 `iframe_ticks` 与受击盒关闭；过长标风险，过短标「闪避无用」。
5. 弱网抽测：开网络工具固定延迟档，缓冲窗是否仍可信；不可信记给 `client-combat-frame-debug`。

### B. 证据与分流模板

失败行模板：`skill_id|axis|reading|budget|clip_path|owner_skill|priority`
分流：动画事件 / VFX / numeric / flow 预算 / 客户端帧调试——一行只指向一个下游 Skill。
