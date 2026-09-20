---
name: systems-index-map
description: "从概念枚举显式/隐式系统，分层画依赖并产出可设计顺序的系统索引表。触发：系统索引、systems index、功能分解、map systems、隐式系统漏列、队首该设计谁。"
---

# 系统索引怎么建

## 何时用

- 概念已有但系统清单混乱
- 不知先设计哪个系统
- 隐式系统（存档/教程/UI）被漏
- 需要给 feature-gdd-slice 的待设计队列

## 怎么做

### 1. 读概念并枚举显式+隐式

**做**
1. 读概念/支柱；`rg -n "系统|System|玩法|economy|combat|save" concept/ pillars/` 抽点名系统进草稿。
2. 隐式检查表强制勾选或 N/A+理由：存档、设置、教程/引导、HUD/菜单壳、活服框架、分析埋点壳——空白=漏。
3. 每系统一行写入 `design/systems_index.csv`：`sys_id|duty|pillar_id|layer|priority|status|owner`。
4. 同义合并、一名多义拆开；冲突并列冲突卡（两名→一 id）。
5. 点名系统 `pillar_id` 不得空；空标「待定支柱」阻塞排序。
6. 失败→回本步：隐式项有空白勾选或待定支柱占 MVP——补齐/挂支柱再分层。

**做到**：csv 含显式+隐式；隐式六项均勾或 N/A；同义已合并；待定支柱可见且不阻塞队首误指。

### 2. 分层与依赖粗分（图）

**做**
1. 层：Foundation（零依赖）/ Core / Feature / Presentation / Polish——写入 csv `layer`。
2. 粗依赖边文件 `design/systems_deps.mmd`（mermaid）或 `.dot`：`A-->B` 表示 A 读 B 的表/事件；发现环则拆/合并/标「需合并设计」。
3. 环未处理不得进可设计队列；选项：抽共享接口/合并系统/降弱依赖——记录选用方案。
4. Presentation（UI 壳）不得标可独立上线 Core，除非弱依赖已声明。
5. 伪 Foundation（实际依赖 Core）降层；导出 PNG/SVG 一页给评审。
6. 失败→回步骤 1：环涉及未入索引的隐式系统——先补行再拆环。

**做到**：分层图可导出；环=0 或有处理记录；Foundation 可零依赖开工。

### 3. 定设计顺序与优先级

**做**
1. 优先级：MVP / 垂直切片 / Alpha / 全量愿景；自动建议后请用户改 csv `priority`。
2. 同优先级内 Foundation→Core→Feature→Presentation；输出「下一个该 design 的 `sys_id`」+一句理由写入索引文首。
3. 低对齐高成本标裁剪候选栏 `cut_candidate`，交 `scope-cut-decision`；不与设计队列混排。
4. 细依赖边交 `dependency-map`；本步只粗到可排序。
5. 队列变更需用户确认；队首指针 `next_design` 字段非空。
6. 失败→回步骤 2：队首仍有未拆环——先拆环再指队首。

**做到**：队首 `sys_id` 可开 `feature-gdd-slice`；裁剪栏分离；排序理由一句可见。

### 4. 发布索引与回写状态

**做**
1. 发布 `design/systems_index.md`（由 csv 渲染或手维）：ID、层、优先级、状态、Owner、下一 design 指针。
2. 队首开 GDD 时回写 `status=in_progress`；完成回写 `done`；用表或 PR 可追踪。
3. 隐式 N/A 集中一节，避免重复争论。
4. 与 `dependency-map` 范围对齐；细边超出标扩展集。
5. 页脚写 `index_version|date`；无版本不得支撑并行排期。
6. `rg sys_id design/ gdd/` 抽查概念/GDD 引用是否指向同一 id。
7. 失败→回步骤 3：版本空或队首指针悬空——补版本/改指针。

**做到**：索引可被 GDD 文首引用；状态可回写；版本/日期非空；sys_id 引用一致。

下一步常接：队首 `feature-gdd-slice`；细依赖 `dependency-map`。
（工具面速查：`rg` 抽系统名、csv 索引、mermaid/dot 依赖图、GDD 文首引用 sys_id、页脚 index_version。）

## 细则

### A. 索引表字段级检查（对照 csv）
1. 打开 `design/systems_index.csv`，确认表头含 `sys_id|duty|pillar_id|layer|priority|status|owner|cut_candidate|next_design`；缺列当场补，不口头记。
2. 用表格工具或 `rg -n "^[^|]+\|" design/systems_index.csv` 数行；显式系统行数应 ≥ 概念文档点名玩法块数，少了回步骤 1 补枚举。
3. 每条 `duty` 限一句可验收职责（动词+对象）；出现「等等/相关」则改写到可测。
4. `layer` 仅允许 Foundation/Core/Feature/Presentation/Polish；非法值标红回步骤 2。
5. 不合格信号：队首 `next_design` 空、或 Foundation 行仍写依赖 Core——回步骤 2 重分层。

### B. 依赖图与环处理（可观察）
1. 在版本库检入 `design/systems_deps.mmd`；本地渲染 PNG 一页进评审目录。
2. 环检测：对每条边做拓扑试排；失败则在备注写「环成员 + 选用方案（抽接口/合并/降弱）」。
3. Presentation 节点不得标「可独立上线」除非弱依赖声明写在 csv 备注。
4. 与 `dependency-map` 范围对齐：粗边留本文件，细边外链并写 `extends: dependency-map`。
5. 不合格回步骤 2：环未处理却已填 `priority=MVP`。

### C. 发布与引用一致性
1. 渲染 `design/systems_index.md` 文首必须含 `index_version` 与日期；无版本禁止并行开多个 GDD。
2. `rg -n "sys_[a-z0-9_]+" gdd/ design/` 抽样 5 处，确认引用的 id 都在 csv。
3. 队首开 `feature-gdd-slice` 当日把该行 `status` 改 `in_progress`；完成改 `done`——用 PR/表历史可追踪。
4. 隐式六项（存档/设置/教程/HUD/活服/埋点）N/A 必须带理由句，空白=漏。
5. 工具信号：csv diff、mermaid 导出图、GDD 文首 `sys_id=` 行。
