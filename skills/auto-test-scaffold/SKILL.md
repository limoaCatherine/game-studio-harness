---
name: auto-test-scaffold
description: "搭测试目录、可注入夹具、CI 失败非0钩与片状 quarantine 政策。触发：测试脚手架、test scaffold、CI 接线。"
---

# 自动化测试脚手架怎么搭

## 何时用

- 仓库从零接测试或目录混乱
- CI 无测试钩或失败被忽略
- 夹具依赖本机手动档，结果不可重复
- 需要与故事 slug 追溯

## 怎么做

### 1. 定目录与命名

1. 落地目录示例：`tests/unit/<system>/`、`tests/integration/<system>/`、`tests/smoke/`。
2. 命名含系统 slug 与故事/缺陷 id 片段（如 `combat_skill_cd_test`），便于追溯。
3. 写「新用例放哪」五步约定进 `tests/README`；自动测进上述分层，手工清单 markdown 另放。
4. 回归清单文件位置约定（如 `tests/regression-suite.md`）与 `regression-pack` 对齐。
5. 清理历史错放用例：搬迁或标 DEPRECATED，不留双份真相。

**做到**：unit/smoke/regression 三类路径存在；命名含系统 slug+故事/缺陷片段可举例；错放已迁或 DEPRECATED。

### 2. 夹具与隔离

1. 准备可检入的最小测试数据夹具（JSON/二进制最小档）；用相对仓库根路径；不读生产玩家档、不用整包玩家档拷贝。
2. 时间、随机、网络做成可注入接口（clock/rng/http fake）；提供 `TestClock.advance(ms)` 一类钩子示例；同步用显式等待/回调。
3. 每测前清理副作用：静态单例、临时文件、环境变量；同机连跑两次结果一致；失败用例可单独复跑。
4. 集成测需要服务时：用本地 fake/docker 文档化启动命令，或标「需服务」非永久 skip 策略。

**做到**：同机连跑两次结果一致；夹具无绝对路径硬编码；失败用例可单独复跑。

### 3. 接 CI 钩

1. CI job：unit 与 smoke 分 job；失败 exit≠0；上传 JUnit/日志；本地脚本参数与 CI 对齐。
2. 故意弄红一条测验证流水线会红；验证后复原。
3. 分支保护项写清「所需检查 job 名」；PR 跑 unit，nightly 跑 integration+smoke。
4. CI 产物保留天数与路径写清；矩阵：PR 轻、nightly 重。

**做到**：故意弄红 exit≠0 能阻断；JUnit/日志可下载；本地脚本参数=CI 命令。

### 4. 片状 quarantine 政策

1. quarantine 标记含原因+Owner+截止日期；重试上限（如 CI 自动重试 ≤1）写清；超限仍红则进 quarantine。
2. 逾期未修：自动改回失败或日报暴露；恢复需连续绿 N 次并留日志。
3. 片状列表可检索（单文件或看板）；周扫一次；到期扫描可用标签脚本或 CI 步。
4. 片状率超过阈值（向用户索取）开专项；主路径用例保持可失败可见。

**做到**：片状 skip 有标记+期限+Owner；主路径用例未永久 skip；列表可检索。

## 做到

- 目录与命名约定落地；夹具可重复、可注入
- CI 失败非 0 且日志可取；本地与 CI 命令一致
- quarantine 政策可执行

## 失败回哪一步

- 目录混乱、命名无 slug、手工清单冒充自动目录 → 回步骤 1
- 夹具绝对路径、读生产档、sleep 同步、连跑不一致 → 回步骤 2
- CI 忽略失败、无产物、本地≠CI → 回步骤 3
- 永久 skip、无 Owner/期限、片状率失控 → 回步骤 4

下一步常接：`case-automation-map` → 填用例；提测前 `ci-smoke`。
