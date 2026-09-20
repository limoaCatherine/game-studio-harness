---
name: excel-read
description: "只读工作簿：定位区域、取值/公式/样式、截图。写前预检与写后回读。触发：读表、回读、预检、get-values、查公式、Excel 现状。"
needs_mcp: excelMCP
---

# 读取

## 何时用

- 本轮只查询、预检或回读，不改写
- 改值/公式已点 `excel-com-write` 时，写前 get 与写后回读在该技能内完成，不必再点本层

## 怎么做

1. 正式表被锁也可以读。`xlsx_probe` 取证据，不要问关表。
2. 看 `com_health`。先 `file list`。只复用本轮仍可见且 COM 能调通的会话。`isExcelVisible=false` 或 COM 报未知接口/unavailable/timeout：`close save=false`，不要复用。`crowded`/`overloaded` 或清残留：`xlsx_com_hygiene diagnose`，再 `reap_automation confirm=true`（不杀桌面窗）。未清干净不要新开 COM。
3. 能开 COM：没有可复用的可见会话再 `open`。IRM 先 `test`。`range` get-used-range / get-current-region 定区，再 get-values / get-formulas。样式用 `range_format` get-style。版面用 `screenshot`。只读结束：`close` 且 `save:false`，再 `xlsx_release`。工具表没有 `xlsx_release`：关掉隐藏会话后 `diagnose`；无可见审阅窗则 reap `/automation`。
4. COM 不可用或只要文件快读：`xlsx_read_data`、`xlsx_get_workbook_metadata`、`xlsx_get_range_style`。不要为了复用去碰残留 COM。结束后仍收口隐藏 automation。文件通路无截图、无实时计算值（只有公式或上次缓存）。
5. 沙箱审阅窗仍开着，且人已准晋升、接着说话且不再看窗、或明确说合/关/继续：按写侧同一拍释放（`xlsx_release keep_visible=false`；无该工具则关审阅会话和所有 `isExcelVisible=false`，再 diagnose，无可见窗则 reap）。不要问「还开着看吗」。释放指 COM，不是删沙箱文件。禁止对正式簿 `show=true`。

本层不调用任何写接口、不克隆、不 merge。
