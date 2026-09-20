# Cookbook：战斗数值竖切

定档 → 点战斗数值职种 → 按步前进 → 沙箱改表 → `gsh close` → 人准晋升。

## 0. 准备

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m gsh setup --tools cursor --profile core --workspace "$PWD/../studio-root" --yes
```

在业务根填 `.harness/surfaces.json` 的 `<tables-root>`。

## 1. 定档

```bash
cd /path/to/studio-root
python -m gsh menu --kind craft -q 战斗数值
```

写 `.harness/sessions/combat-ttk/loadplan.json`：

```json
{
  "session_id": "combat-ttk",
  "bead_id": "bead-ttk",
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
python -m gsh activate combat-ttk
python -m gsh resume
```

`activated.json` 里 `crafts` 只有职种 id；`craft_open` 是第一步；`craft_path` 记下整条路径与步号。

## 2. 制作

读 `agents/combat-numeric-designer.md`，打开 `craft_open` 指向的技能（通常是 `combat-modeling`）。锚点空则先问制作方。

沙箱改表：`excel-read` → 隔离副本 → `excel-com-write` → 回读。做完这一步：

```bash
python -m gsh next --craft combat-numeric-designer
```

现行卡会改成下一步（例如 `attribute-framework`）。不要一次打开整条 `uses_skills`。

## 3. 关项

```bash
python -m gsh close --kind schema --evidence .harness/sandbox/ttk-notes.md
```

报告落到 `.harness/artifacts/bead-ttk/verify-report.json`。人准后只回写正式表的记录格。

换工具续上：`python -m gsh status`。
