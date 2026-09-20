# L2 定档

第二层把模糊诉求变成可执行的一轮：目标、点名 id、写级别、验证种类。点名集合是本轮防火墙；未点名的职种仍留在完整菜单（35 / 106），不预展开进上下文。

日常命令：

```bash
python -m gsh menu --kind craft -q ttk
# 写 .harness/sessions/<id>/loadplan.json
python -m gsh activate <id>
python -m gsh status
```

| 文件 | 作用 |
|---|---|
| `skills/route-task/SKILL.md` | 导演做法 |
| `loadplan.json` | 本轮合同 |
| `activated.json` | 点名集合 + `craft_open` + `craft_path` |
| `current.md` | 换工具也能读的现行卡 |
| `flow.json` | `建议执行单.py` 排出制作在前、收口在后 |

点名职种时，生成器只打开路径第一步，并把整条 `uses_skills` 写进 `craft_path`。后面的步骤用 `python -m gsh next` 前进。
