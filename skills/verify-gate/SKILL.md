---
name: verify-gate
description: 关项前按档位只核核心证据并写验证报告；证据深度随档位渐进，不逐步全验。
---

# 验证

第一层关项只认报告 `verdict` 为 `pass`。「真通过」= 本档位该核的核心证据已打开且相符。

验证报告是关项级一份。中间步骤靠制作自检。

| 档位 | 验证种类 | 核什么 | 大约证据条数 |
|---|---|---|---|
| 讨论 | `none` | 无交付则不写报告 | 0 |
| 短活 | `smoke` | 主产物在、非空、抽一眼内容对 | 1 |
| 已知配方 | `schema` 或 `smoke` | 主产物 + 关键约束 | 1～2 |
| 多职种 | `playtest` 或 `schema` | 上栏 + 跨职种接口 | 2～3 |
| 硬闸 | `build` / `release` | 上栏 + 构建或发版输出 | 3～5 |

## 怎么做

### 1. 定核什么

1. 读加载计划：`bead_id`、`tier`、`verify_kind`、主交付路径。
2. 只列本档位核心项；每项一个已存在路径。
3. `verify_kind=none` 且无交付：停，不写报告。

**做到**：1～5 条核心项。

### 2. 打开证据

1. 逐项打开：在、非空、与预期相符。
2. 改表核回读或 diff；构建看日志或产物路径。
3. 打不开或内容不符 → 本项失败，不凑绿。

**做到**：已打开路径列表。

### 3. 写报告并登记

路径：`.harness/artifacts/<工作项>/verify-report.json`

| 字段 | 写什么 |
|---|---|
| `bead_id` | 工作项编号 |
| `verify_kind` | 与计划一致（不含 `none`） |
| `command` | 本档位核对动作一句 |
| `exit_code` | 全过 `0`，失败 `1` |
| `evidence_paths` | 已打开的核心路径 |
| `verdict` | `pass` / `fail` |
| `notes` | 失败时写哪条不过 |

核心项全过且路径非空 → `pass`。  
随后追加一行到 `.harness/artifacts/index.jsonl`（`ts`、`bead_id`、`skill=verify-gate`、`path`、`summary`）。  
再写 `.harness/state.json` 的 progress，并往 `.harness/memory/tasks.jsonl` 追加一行。短活只登记报告自身。多文件批次或换手再点 `artifacts-append`。

**做到**：报告字段齐全；索引尾部可见本行。

### 4. 关项

仅 `pass` 后关项。`fail` 按 `notes` 回流制作。

## 完成检查

- 档位与 `verify_kind` 对齐
- 证据已打开并写入报告
- 报告已登记进索引
