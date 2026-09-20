---
name: excel-com-write
description: "经确认范围→沙盒改值/公式/插删行→必交排版→diff 只合记录格→获准晋升→回读。写前走读取层。触发：改产品表、沙盒写入、插行、表格连接器晋升、表写入配方。"
needs_mcp: excelMCP
---

# 改动层

会话协议以 excelMCP `INSTRUCTIONS.md` 为准。按用途调用工具，不必先过 `mcp_allow` 闸。正式面与隔离根见 `write-isolation` 与 `.harness/surfaces.json`。

## 何时用

- 要把值或公式写入产品工作簿
- 插 / 删 / 移动行或列

## 何时不用

- 只查数 → 点 `excel-read`
- 只改颜色排版 → 点 `excel-format`

本技能已含写前 get 与写后回读，不必为此再点读取技能。写完**必须**按 `excel-format` 排本轮改过的区，不要用「结构没变」跳过。

## 怎么做

### 1. 确认写入范围

1. 范围卡：工作簿、sheet、主键列、允许列、禁改列。
2. 表头与正式簿一致；列增删先人审。
3. `xlsx_probe(正式表)`。`recommend=com` 走 COM；只有占用才走文件通路。不要问关表。
4. 看 `com_health` / `automation_count`。先 `file list`。只复用**本轮还活着、且 `isExcelVisible=true`** 的审阅窗。`isExcelVisible=false`、COM 报未知接口/unavailable/timeout、或会话无操作却占着正式簿：视为残留，`file close save=false`，不要复用。`crowded`/`overloaded` 或清残留：`xlsx_com_hygiene diagnose`，再 `reap_automation confirm=true`。只杀 `/automation -Embedding`，不杀桌面可见 Excel。清完再 `open`，禁止再叠一本。
5. 覆盖前取值/公式：COM `range` get-values / get-formulas，否则 `xlsx_read_data`。结构变更前取样式：COM `range_format` get-style，否则 `xlsx_get_range_style`。

**做到**：范围卡齐全；预检通过；本轮 probe 已落。

### 2. 沙盒写入

1. `xlsx_sandbox_clone(正式表)`。默认落到正式表同级 `沙箱/`，文件名带时间戳。只写沙箱，禁止直连正式簿，不再另建 `版本/`。克隆后确认该仓 `.gitignore` 含 `**/沙箱/`，并对副本路径 `git check-ignore`。未忽略则先按 `write-isolation` 补再写。禁止把沙箱文件 `git add` 进库。
2. 副本未锁用 COM：批量写 `calculation_mode` 手动 → `range` set-values / set-formulas → `calculate` → 自动。只写本轮范围卡里的格子。清内容用 `clear-contents`。插删行/列用 `range_edit`（引用会跟随），并 `xlsx_record_op` 记下 insert/delete 与 `set_cells` / `copy_range`。
3. 正式表占用、COM 不可用：`xlsx_write_data` / `xlsx_apply_formula`。插删用 `xlsx_insert_*` / `xlsx_delete_*`（自动记 op；引用不重写，相关公式要自己改）。每格写入都要进 changeset。
4. `xlsx_format_range` 只传要改的键，禁止默认 `bold=false`。
5. 按 `excel-format` 落到本轮改过的区（已点格式技能则交该技能；没点也要当场打开做完）。
6. 写后抽关键行回读。
7. **交审（做完必须做，不要只报路径）**  
   回读通过后：把沙箱改成 `<正式主名>.sandbox-<会话短名>.xlsx`（会话短名 = `.harness/sessions/<会话>/` 目录名，不是交付内容名）。`.changes.json` 一起改名，并改里头的 `sandbox` 路径。仍只留在正式表同级 `沙箱/`。然后只对**这本沙箱** `file open show=true`，切到本轮 sheet，把窗提到前台。禁止对正式簿 `show=true`。接着 `xlsx_release`（默认 `keep_visible=true`：留下这扇可见窗，关掉其它隐藏会话）。工具表没有 `xlsx_release`：`file close` 掉所有 `isExcelVisible=false` 的会话，再 `xlsx_com_hygiene diagnose`；无可见审阅窗则 `reap_automation confirm=true`。

8. **审阅完就主动释放沙箱**  
   「审阅完」= 人已准晋升、人接着说话且不再看窗、或人明确说合/关/继续。不要再问「还开着看吗」。当拍释放：关掉本轮沙箱审阅 COM 会话（有未存改动先 `save=true`）；`xlsx_release keep_visible=false`（`save_visible` 默认 true）。工具表没有 `xlsx_release`：`file close` 掉审阅会话和所有 `isExcelVisible=false`，再 `xlsx_com_hygiene diagnose`；无可见审阅窗则 `reap_automation confirm=true`。只杀 `/automation -Embedding`，不杀桌面 Excel。人自己关窗后 `/automation` 不会跟着死，必须按本步清。只有人明确说「还开着看」才留窗。  
   「释放沙箱」指 COM / 审阅窗 / 隐藏 automation，**不是**删 `沙箱/*.xlsx` 或 changeset。

**做到**：只改了副本；结构 op 已进 changeset；交审时人看得到沙箱窗；审阅完当拍已释放 COM，沙箱文件仍在。

### 3. 出 diff 与获准

1. 变更单：主键、列、旧→新。
2. 未批不得晋升。

**做到**：变更单已获准。

### 4. 晋升与回读

1. 晋升前：沙箱审阅窗还占着文件则先按第 2.8 步释放，再 `xlsx_merge_changeset`，避免沙箱锁死。
2. `xlsx_merge_changeset`：只把 changeset 记下的格子和结构 op 回写正式主文件。禁止写 `rollback`。禁止全表 diff。禁止整文件覆盖。正式表被锁则写入 `沙箱/<主名>.shadow.xlsx`，不问关表。
3. 合并失败停在沙箱重开，不要用 rollback 拷回正式表。
4. 回读不一致：按主键在沙箱改，再只合记录格。
5. 晋升后回读正式簿（文件通路或隐藏 COM）。不要再 `show=true` 重开沙箱，除非人明确还要看。禁止对正式簿 `show=true`。

**做到**：正式簿目标格与沙盒一致（或已落沙箱 shadow）。正式表同级没有 rollback / 新 shadow 旁路文件。审阅窗已释放，沙箱文件未删。

## 完成检查

- [ ] 范围卡与变更单已获准
- [ ] 本轮改过的区已按 `excel-format` 排过
- [ ] 回读一致
- [ ] 沙箱已改可读名，并已 `show=true` 打开本轮 sheet 给人审（未开正式簿）
- [ ] 审阅完已当拍 `xlsx_release keep_visible=false` 或等价收口；未删沙箱文件/changeset；无可见审阅窗则已清 `/automation`；晋升前已先释放再合记录格，没有 rollback
- [ ] 沙箱路径已被 git 忽略；未把沙箱文件 add 进库

## 不在本文件

- 单元格色码与数字格式见 `excel-format`
- 插入位置由范围卡与主键关系决定
