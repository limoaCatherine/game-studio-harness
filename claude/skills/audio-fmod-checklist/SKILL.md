---
name: audio-fmod-checklist
description: "用 FMOD Studio / Audacity / ffmpeg 完成音频事件入库与试听校验。触发：音频、FMOD、音效、BGM、混音、Audacity。"
needs_mcp: fmod-studio
---

# 音频（FMOD）怎么入库

## 何时用

- 要接 SFX/BGM/UI 音到 FMOD Studio 工程并进游戏事件
- 波形需裁剪/降噪后才进银行
- 事件名要与动画/技能字典对齐

## 勾选主路径

### 1. 确认 MCP 与工程

- [ ] `fmod-studio`：先 `tools/list`；**Script Server 未开则失败属预期** → 人工开启 FMOD Studio Script Server 后再调
- [ ] 路径锚：`${HARNESS_APPS}\mcp\fmod-studio-mcp\`
- [ ] `audacity`：`status`/`launch`/`open_file` — **launch-only**（不能遥控波形编辑 GUI）
- [ ] `ffmpeg`：批处理转码/响度/切片（用 tools/list 暴露的参数，勿臆造）
- [ ] 事件名字典与 `anim-event-hook` / 技能表对齐；一用途一名

### 2. 波形预处理（human-in-the-loop）

- [ ] `audacity.launch` 或 `open_file(源波)`；人工裁剪、淡入淡出、降噪
- [ ] 导出 WAV/约定格式到音频工作目录；`ffmpeg` 做批量采样率/声道路径统一
- [ ] 响度或峰值超项目档 → 记返工，不静默压爆

### 3. FMOD 事件与银行

- [ ] 在 FMOD Studio 建 Event；参数/snapshot 按项目约定
- [ ] 经 `fmod-studio` MCP 能调的工具做查询/触发（以 tools/list 为准）；不能调则 GUI 完成并在备注写「MCP 边界」
- [ ] 建银行/构建输出路径可指；平台 bank 分档若需要则分列
- [ ] 事件名写入映射表：`event | 用途 | 触发源 | bank`

### 4. 引擎试听与回归

- [ ] `gamedev-mcp` 开代表场景；触发技能/UI 听对齐
- [ ] 与动画事件帧偏差可接受者记录；不可接受回调动画或自改延迟
- [ ] 静音/中断/重叠策略冒烟；失败进问题表
- [ ] 映射表与 bank 路径通知战斗/UI

## 做到

- [ ] 事件名与字典逐字一致；bank 可被游戏加载
- [ ] 源波处理可复述（Audacity/ffmpeg 产物路径）
- [ ] 代表场景试听通过或债项显式
- [ ] 诚实边界：Audacity=launch-only；FMOD 依赖 Script Server

## 失败回哪一步

- Script Server 挂 / tools 空 → 回 1 开服务或改 GUI
- 波形爆/格式错 → 回 2
- 事件名漂/bank Missing → 回 3
- 对帧/中断失败 → 回 4（必要时回 3）

下一步常接：`import-validate`（若引擎另有音频导入闸）。不写技能数值与对白剧本全文。

## 工具锚点（live mcp.json）

| Key | 边界 |
|-----|------|
| `fmod-cli` | 主通路：diagnostic / build_banks / export_guids / list_bank_outputs |
| `fmod-studio` | Studio TCP，需 Studio 进程；人声编辑在 Studio GUI |
| `audacity` | launch-only |
| `ffmpeg` | 转码/切片 |
| `gamedev-mcp` | 试听 |
| `excelMCP` | 映射表（可选） |
| `everything-search` | 定位旧 bank/波 |
