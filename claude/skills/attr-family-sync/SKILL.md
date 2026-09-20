---
name: attr-family-sync
description: "新增或重排一层属性时，按读取→改动→格式→读取覆盖受影响表，并同步下游主键。触发：加属性、属性族、多层主键同步、同步配表。"
needs_mcp: excelMCP
---

# 属性族编排

一次改多张表上的同一组主键时点本技能，代替同时点读取 / 改动 / 格式三层。

## 工作流

1. **口径**（按需打开 `attribute-framework`）：主键、单位、派生 DAG。
2. **读取**：定位插入点；结构变更则 `get-style`。
3. **改动**：插行、写转入与公式（`xlsx_sandbox_clone` 只落 `沙箱/` → 只改该副本 → diff → 获准 → `xlsx_merge_changeset`）。
4. **格式**：按 `excel-format` 落到目标区。
5. **回读**。范围卡含下游主键时补 enum / 属性行 / 文案。个人服导表另点 `personal-server-table-sync`。

## 失败回哪一步

- 缺 DAG 或插入参照 → 步骤 1–2
- 样式不符规范或模板 → 步骤 4
