# 三维与 DCC

下列工具都是**懒接**。没装宿主就不要强行变绿。

| id | 要装的软件 | 用法要点 |
|---|---|---|
| `blender-mcp` | [Blender](https://www.blender.org/)；`uvx blender-mcp`（Python 3.11） | 先 `get_scene_info` / 视口截图，再小步改。建模、材质、导入导出按对应 skill。 |
| `cascadeur` | [Cascadeur](https://cascadeur.com/)；本机 HTTP 桥默认 `127.0.0.1:8765` | 已是 HTTP 桥。脚本服务未开时不可挡发现。动画关键帧仍以人工为主。 |
| `meshlab` | [MeshLab](https://www.meshlab.net/) + host MCP | 减面、清重复、看网格信息。批处理写 `run_mlx`。工作目录用环境变量。 |
| `instant-meshes` | Instant Meshes；可选 Blender | 重拓扑/四边面。`BLENDER_EXECUTABLE` 指向本机 Blender。 |
| `accurig` | AccuRIG + host MCP | 文件/工作区级，不是 GUI 全自动绑骨。先 `validate_mesh_input` 再排队。 |
| `rokoko` | Rokoko Studio + host MCP | 文件/工作区 + Listen 探针。重定向仍人做。 |
| `treeit` | TreeIt + host MCP | 树木植被。先 `prepare_workspace` `validate_tree_input`。 |
| `gaea` | QuadSpinner Gaea + `gaea-mcp`（Node/tsx） | 图节点/工程文件级。`GAEA_INSTALL_DIR` `PROJECT_DIR` `OUTPUT_DIR` 换成你的目录。 |
| `materialpilot` | Material Maker + materialpilot MCP | 工具表过百，用到材质图再拉。先 `app_get_status`。 |
| `materialize` | Materialize + host MCP | launch-only：能打开文件，不冒充可全自动代工。 |
| `xnormal` | xNormal + host MCP | 烘焙。launch / 列最近 / 写 bake xml。 |
| `meshroom` | AliceVision Meshroom + host MCP | 摄影测量管线。版本目录不要写进仓，用 `${MESHROOM_EXE}`。 |
| `cloudcompare` | CloudCompare + MCP | 点云距离、ICP、采样。`CLOUDCOMPARE_PATH` 指向 exe。 |
| `renderdoc` | RenderDoc + MCP | 打开 capture 后查 pass、overdraw、shader。先 `open_capture`。 |

## 共同纪律

1. 路径用占位符或 `host-paths.json`，不要把用户名写进 `mcp.json` 后提交。
2. 引擎/资产试验只进 `surfaces.json` 的 sandbox / `_Dev`。
3. launch-only 的宿主（PureRef、部分 host-mcp）能打开就不代表能代工完整 GUI 流程。
