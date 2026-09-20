# L4 档案柜

第四层是业务根上的文件事实。换会话、换工具，先读这里。

| 文件 | 作用 |
|---|---|
| `.harness/surfaces.json` | 正式面与隔离根 |
| `.harness/state.json` | 当前会话、进度 |
| `.harness/sessions/<id>/current.md` | 现行卡 |
| `.harness/sessions/LATEST` | 指针（`_` 开头的探测会话不写） |
| `.harness/memory/tasks.jsonl` | 只追加流水 |
| `.harness/artifacts/<bead>/verify-report.json` | `gsh close` 写出的关项报告 |
| `.harness/templates/verify-report.json` | 报告模板 |

```bash
python -m gsh resume --workspace /path/to/studio
python -m gsh close --kind smoke --evidence <产物>
```

晋升正式面仍然要人准，且只回写记录集。关项必须写出 `verify-report.json`；没有人准，隔离面草稿不能当成已发版。
