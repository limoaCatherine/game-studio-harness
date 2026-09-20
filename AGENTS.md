# Game Studio Harness

定档 → 制作 → 结案。同一未关目标续同一会话。

开场读序：本文件 → `.harness/sessions/<会话>/current.md` → 名单里点名的技能/职种正文 → 计划 `retrieve_keys` 命中的 canon/adr。不要把菜单全文灌进上下文。

`activated.json` 只决定开场先注入哪些正文，不是运行时防火墙。职种不预展开。写级别默认 sandbox。晋升须人准，只回写记录集。

思路拆解：`docs/architecture.md`。技能正文在 `core/`。本机菜单脚本：`~/.gsh/harness/scripts/生成会话能力名单.py`。
