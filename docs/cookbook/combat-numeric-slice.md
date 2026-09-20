# Cookbook：战斗数值竖切（端到端）

一条游戏向路径：定档 → 点战斗数值职种 → 只打开第一步 → 沙箱改表 → 验证报告 → 人准晋升。

## 0. 准备

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m gsh setup --tools cursor --profile core --workspace "$PWD/../studio-root" --isolate-root "$PWD/../gsh-probe" --yes
python -m gsh verify --tools cursor --workspace "$PWD/../studio-root" --isolate-root "$PWD/../gsh-probe"
```

在业务根填 `.harness/surfaces.json` 的 `<tables-root>`。不要把真实工作室盘符提交回本仓。

## 1. 定档

打开 `skills/route-task/SKILL.md`。写 `.harness/sessions/combat-ttk/loadplan.json`：

```json
{
  "session_id": "combat-ttk",
  "tier": "T1",
  "verify_kind": "schema",
  "intent": "new",
  "work_mode": "agent",
  "write_class": "sandbox",
  "items": [
    {
      "kind": "craft",
      "id": "combat-numeric-designer",
      "why": "本轮只定 TTK 锚点与公式顺序，不改技能幻想。"
    }
  ]
}
```

```bash
python harness/scripts/生成会话能力名单.py combat-ttk
```

检查 `activated.json`：`crafts` 只有职种 id；`craft_open` 是路径第一步；`skills` **没有**整条 `uses_skills`。

## 2. 制作

读职种正文 `agents/combat-numeric-designer.md`，再打开 `craft_open` 指向的技能（通常是 `combat-modeling`）。锚点空则停填表。

改表走 `excel-read` → 沙箱副本 → `excel-com-write` → `excel-format` → 回读。正式 xlsx 禁止整文件覆盖。

## 3. 验证与关项

按 T1 核主产物 + 关键约束，写 `.harness/artifacts/<bead>/verify-report.json`，`verdict` 必须是 `pass`。然后 `sync-state`、`artifacts-append`。人准后才 `promote` 回写记录格。

## 4. 若缺模块会怎样

- 无 `route-task`：直接改正式表
- 无名单生成器：职种被当成 8 个技能一次性灌进窗口
- 无 `surfaces.json`：沙箱路径靠猜
- 无验证报告：Cursor 结束钩子拒绝关项；其它工具只会在宪法里警告
