---
name: terrain-gaea-pass
description: "用 Gaea 程序化地形并导出供场景模块衔接。触发：地形、Gaea、heightmap、地形图、开放世界地块。"
needs_mcp: gaea
---

# 地形（Gaea）怎么出图衔接场景

## 何时用

- 开放世界/大地图需要程序化高度图与掩码
- 灰盒分区已定，要替换为可导出色图/高度
- 地形节点图要可复现、可版本化

## 勾选主路径

### 1. 环境与工程

- [ ] `gaea.check_gaea_status`：确认 Gaea/Swarm 路径就绪
- [ ] MCP 根：`${HARNESS_APPS}\mcp\gaea-mcp\`
- [ ] `gaea.list_projects` 看已有 `.terrain`；新地块 `create_terrain`
- [ ] 锁定世界单位、高度范围、导出分辨率（向用户索取档，不猜）

### 2. 搭节点图

- [ ] `list_node_types` → `add_node` / `connect_nodes` / `set_node_property`
- [ ] `read_terrain_graph` / `get_node_details` 复核连线
- [ ] 掩码（雪/沙/岩/草）分输出；命名进导出表
- [ ] 禁止无文档改种子导致不可复现；种子写入工作卡

### 3. 构建与产物

- [ ] `build_terrain`（Swarm CLI）；失败读日志，不假装成功
- [ ] 产物：高度图/色图/掩码路径列入 `terrain_exports.csv`（可用 `excelMCP`）
- [ ] 可选 `cloudcompare` 对位扫描/参考网格
- [ ] 植被代理交 `treeit`（**launch-only**，人工出树）

### 4. 场景衔接

- [ ] `environment-artist` / `env-asset-checklist`：地形块与模块网格接缝
- [ ] `ldtk`/`tiled` 若有 2D 分层数据，与高度分区对齐
- [ ] `gamedev-mcp` 导入地形；走主路径胶囊；LOD/流式边界试进出
- [ ] `export-naming-gate` → `import-validate`

## 做到

- [ ] `.terrain` 图可 `read_terrain_graph` 复述
- [ ] build 产物路径稳定；种子/分辨率在卡上
- [ ] 引擎内无炸缝；流式进出无 Missing
- [ ] 植被若需要：treeit 产物已入库或债项显式

## 失败回哪一步

- status 失败/Swarm 缺失 → 回 1
- 节点口连错 → 回 2
- build 失败 → 回 2/3
- 引擎接缝/Missing → 回 4→`env-asset-checklist`

## 工具锚点（live mcp.json）

| Key | 工具（已知） |
|-----|-------------|
| `gaea` | check_gaea_status, get_gaea_version, list_projects, build_terrain, list_node_types, read_terrain_graph, get_node_details, create_terrain, add_node, remove_node, connect_nodes, disconnect_port, set_node_property |
| `treeit` | launch-only |
| `cloudcompare` | tools/list |
| `ldtk` / `tiled` / `magicavoxel` | 分层/块辅助 |
| `gamedev-mcp` / `excelMCP` / `everything-search` | 衔接与表 |
