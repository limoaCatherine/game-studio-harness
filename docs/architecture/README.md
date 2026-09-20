# 架构

GSH 用四层文件合同承接**完整游戏制作流水线**。设计逻辑是能力边界隔离、技能蒸馏、任务编排与上下文预算注入。代理在点名集合内按步执行、写入隔离面。人闸负责支柱、范围、晋升与发版，见根 README 的工程实践。

先读仓库根 [README.md](../../README.md) 的「设计哲学」，再读「原则、范围与运行模型」，再下钻本目录。English twin：[README.en.md](README.en.md)。

四层各自做什么、你用哪条命令：

- [L1 宪法](l1-constitution.md) — 每轮固定税：读序、写隔离、关项、密钥与破坏闸
- [L2 定档](l2-director.md) — 诉求写成 loadplan；点名 id；职种只打开第一步
- [L3 能力库](l3-capability.md) — 35 职种 / 106 技能 / MCP 用途桩；按步打开
- [L4 档案柜](l4-filing.md) — 现行卡、流水、验收报告；晋升仍须人准
- [跨工具](cross-harness.md) — 一份内容，写成各工具完整原生树
- [适配器一览](../adapters/README.md)
- [MCP 政策](../mcp-policy.md)
- [安装](../install.md)
- [发版](../release.md)
- [文档地图](../README.md)
