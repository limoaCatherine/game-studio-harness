---
name: case-automation-map
description: "把 GWT/回归用例映射到 pytest/Unity Test/自动化 id，标覆盖缺口与片状信号并排期。触发：自动化映射、用例自动 id、coverage gap、flake。"
---

# 用例自动化怎么映射

## 何时用

- GWT/回归包要落到具体自动测 id，而非只填「要自动」
- 覆盖缺口与分层边界不清，需要排出本迭代可做项与延期理由
- 单测/集成/UI 自动边界混乱，需按工具面分层
- 要排出本迭代可做 Top N 与延期理由

## 怎么做

### 1. 收集候选用例与现网自动 id

1. 从 `test-case-from-gdd` 产出的 GWT 表、`regression-pack`、关闭缺陷「高复发」列拉取候选；废弃 AC（状态=Obsolete）剔除。
2. 扫现有自动入口：`tests/**/*.py`（pytest 节点 id）、Unity `EditMode`/`PlayMode` 程序集中的 `[Test]`/`[UnityTest]` 全名、Unreal Automation 测试名、或项目 `TestResults/*.xml` 里的 classname+name。
3. 建对照草稿列：`case_id | gwt_title | existing_auto_id | layer_guess`；已有 id 的标 `COVERED`，无则 `GAP`；表写入走 `excel-com-write` 若用 xlsx。
4. 手工耗时用最近一次实测分钟数（QA 笔记或计时表），失败频率高/中/低取近两迭代缺陷标签。
5. 合并重复步骤为夹具候选（同一前置登录/进战斗），写入 `fixtures_candidate` 列；输出存 `qa/automation_map_<sprint>.md` 或表。

**做到**：候选可点名到 case_id；COVERED 挂真实 auto_id；GAP 计数可见。

### 2. 分层、ROI 与工具锚

1. 分层规则落到工具：Logic/边界 → pytest 函数或 Unity EditMode；跨系统状态 → PlayMode / `tests/integration/`；纯 UI 观感 → 慎 UI 自动（Airtest/Appium/Unity UITest）或留手工。
2. ROI 粗算：`月执行次数 × 手工分钟` vs `预计编写+维护人日`；低 ROI 写「不自动」原因一句进表。
3. Feel/演出/手感用例强制手工证据（录像时间码）；真支付/真短信/真推送仅沙箱 mock 或标 `MANUAL_ONLY`。
4. UI 自动候选另答三问：动画依赖高？数据未隔离？月跑<2？任一「是」则降手工。
5. 每行写定：`layer | auto? | target_path_or_id | reason`；GAP 行给出目标 id 命名槽（如 `tests/unit/combat/test_damage_floor.py::test_zero_def`）。

**做到**：每用例有层级+是否自动+目标 id/路径槽+理由；手感路径未计入覆盖率分子。

### 3. 片状信号与稳定性债

1. 读近 14 天 CI：同 auto_id 失败率≥20% 或「红→绿无代码变更」≥2 次 → 标 `FLAKE`；记录 job 名与失败栈首行。
2. 债清单字段：`auto_id | 债类型(真网络/未隔离数据/强时机/缺时钟注入/需真机) | 信号 | 解除动作 | Owner`。
3. 解除定义写死：可注入时钟/随机 + 无真网依赖 + 连续绿 3 次；未解除不得进本迭代 Top。
4. 已知 FLAKE 先 quarantine（`@pytest.mark.flaky` / Unity Explicit）再隔离；同类 UI 自动等解除后再上。
5. 需真机用例标 `device_matrix` 层，挂 `compat-smoke`/`device-matrix-pass` 矩阵格号，不与 EditMode 混跑。

**做到**：FLAKE/债项列表可指到 auto_id；解除定义可判定；Top 不含未解除债。

### 4. 排期地图与覆盖缺口闭环

1. 映射表定稿列：`case_id → layer → priority → Owner → target_auto_id_or_path → status(NEW/EXTEND/DEFER)`；目录对齐 `auto-test-scaffold`。
2. Top N 按 `ROI × 风险`（regression-pack 高风险点加权）排出；与迭代容量对齐。
3. 覆盖缺口报告三行：GAP 总数、本迭代关闭数、DEFER 理由（缺钩子/低 ROI/片状债）。
4. 完成定义：Top N 每条已有测文件路径或 Explicit 延期单号；地图进版本库；变更走增量 diff（加行/改 status），保留历史 id。
5. 落地后抽样跑：新 id 在 CI job 名下出现且非 FLAKE；失败则回步骤 3 标债或回步骤 2 降层。

**做到**：地图可排期；缺口数字闭合；新 id 在约定 CI job 可见。

## 做到

- 候选均有 case_id；COVERED 挂真实 auto_id
- 分层与 ROI/不自动理由齐全；FLAKE 与稳定性债已标且有解除定义
- Top N 有路径或延期单号；地图在版本库；手感与真支付路径不计入覆盖率分子

## 失败回哪一步

- COVERED 无真实 auto_id、耗时拍脑袋 → 回步骤 1
- 手感路径塞进覆盖率分子、目标 id 空槽「稍后补充」 → 回步骤 2
- FLAKE 无解除动作/Owner、未解除进 Top → 回步骤 3
- 地图只在聊天、新 id 未出现在 CI → 回步骤 4

下一步常接：`auto-test-scaffold` → CI job 接入；片状回 `ci-smoke` quarantine 政策。

## 映射表必填列

`case_id,priority,script_id|MANUAL,owner,last_run,result`
自动项必须能指到仓库脚本路径或 CI job 名；标 MANUAL 的要写原因（不稳定/需真机）。
完成：P0/P1 用例 100% 有映射；无「待定」空行。
