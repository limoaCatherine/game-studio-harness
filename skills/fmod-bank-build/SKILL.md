---
name: fmod-bank-build
description: "用 FMOD Studio / fmodstudiocl 做工程诊断、Bank 构建与 GUID 导出。触发：FMOD、Bank、音频中间件、fmodstudiocl、声音打包。"
needs_mcp: fmod-cli
---

# FMOD Bank 怎么构建

## 何时用

- 开放世界默认音频中间件是 FMOD（不是把 DAW 当运行时）
- 需要可重复的 Bank 构建与 GUID 导出，而不是只开 GUI

## 主路径

### 1. 确认宿主与工程

1. 读 `fmod-cli.status`（或 `fmod-studio` 若仅 TCP）：确认 `fmodstudiocl.exe` 与 Studio 路径在 `${HARNESS_APPS}\Audio\FMOD\`。
2. `fmod-cli.list_projects` 找到目标 `.fspro`；没有则在 `_mcp-projects` 建工程约定目录。
3. 人机：事件/混音仍在 Studio GUI 编辑；CLI 不替代做声。
4. 需要实时遥控 Studio 时再开 `fmod-studio`（宿主要听 3664）；CLI 构建不依赖该 TCP。
5. 核对平台名与银行名与游戏工程约定表一致。

### 2. 诊断

1. 跑 `fmod-cli.diagnostic(project)`。
2. 退出码非 0：把 stderr 尾部写进产物；修工程后再构建。
3. 警告策略：是否 `-ignore-warnings` 必须书面记录。
4. 完成信号：diagnostic 干净或豁免单齐。

### 3. 构建 Bank

1. `fmod-cli.build_banks(project, banks?, platforms?=Desktop, export_guids?)`。
2. 指定银行/平台，避免全量误构建。
3. `fmod-cli.list_bank_outputs` 核 `.bank` mtime/体积。
4. 需要 GUID 文本时 `export_guids`。
5. 脚本化批量改工程用 `run_script`（JS），先在副本工程试。
6. 完成信号：目标 bank 齐、guid 齐、日志可回放。

### 4. 交接引擎

1. Bank 拷贝到引擎约定内容目录（只进隔离根或地图里的正式面；不写第三方插件根）。
2. `import-validate` / `gamedev-mcp` 抽事件可播。
3. 失败回 FMOD 工程，不在引擎里硬改 bank。

## 完成勾选

- [ ] diagnostic 通过或豁免
- [ ] 目标平台 bank 已构建且 mtime 新
- [ ] guid 导出（若需要）
- [ ] 引擎抽事件可闻/可触发
- [ ] 人机编辑边界写进交接
