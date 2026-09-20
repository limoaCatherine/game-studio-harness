# 技能索引

仓库根 `skills/` 是唯一真相。共 106 条。改一处后 `python -m gsh sync`。

## 导演与收口

| ID | 解决什么 |
|---|---|
| `route-task` | 接到诉求后分析需要哪些事件/职种/外接，写加载计划、现行卡并生成会话能力名单。触发：定档、转向、插队、并行、工作模式、Plan、点名、现行卡、子代理。 |
| `assemble-craft-flow` | 计划里已有多个事件时，按菜单推荐序排出执行顺序并写回会话。触发：拼装、执行单、flow、assemble-craft-flow、推荐序。 |
| `doctor` | 自主迭代时扫技能/职种/外接配置缺口，给出最小补齐或可新部署动作。触发：doctor、缺口扫描、最小部署、激活失败、catalog 对齐。 |
| `verify-gate` | 关项前按档位只核核心证据并写验证报告；证据深度随档位渐进，不逐步全验。 |
| `sync-state` | 对齐工作项、会话卡、计划与产物索引，让下一手看到当前真实进度。触发：状态同步、sync-state、会话卡对齐、事实源。 |
| `artifacts-append` | 把本任务产物路径和摘要追加进索引，供验证和交接引用。触发：产物登记、index.jsonl、登记产物、验证引用路径。 |
| `handoff-pack` | 换职种或换会话时打包：目标、已做决策、产物路径、未决项、建议下一手点名。触发：交接、换岗、换会话、handoff、下一手。 |
| `collab-protocol` | 问清目标、关键分叉给选项、分段推进、正式路径写入前先获准。触发：协作、先问再写、分段批准、选项利弊。 |
| `status-digest` | 汇总工作项/交付包的事实进度、阻塞与需决策项，生成周报与下一手可引用的状态摘要。触发：平台周报、状态摘要、阻塞摘要、status digest、红灯计数。 |

## 记忆与晋升

| ID | 解决什么 |
|---|---|
| `memory-retrieve` | 开工前按问题检索已批准决策、既往产物和会话记录，把读到的条目列出来。触发：检索决策、读canon、找既往结论、开工前记忆。 |
| `promote-canon` | 把已批准的稳定事实写入决策库，带上来源和适用范围。触发：写入canon、晋升事实、已批准事实入库。 |
| `promote-adr` | 把技术选型写成决策记录：背景、选项、选择、后果。触发：ADR、架构决策、技术选型写入、晋升决策记录。 |

## 写隔离与目录

| ID | 解决什么 |
|---|---|
| `write-isolation` | 任何正式面写入先落到隔离根：表沙箱、代码 worktree、引擎 Sandbox、资产 _Dev；沙箱目录不进 git；晋升须人准且只回写记录集。触发：沙盒、隔离、正式面、晋升、worktree、写级别、surfaces、git忽略、沙箱忽略。 |
| `file-pack-layout` | 规划并执行工作区/资源文件的存放分包：按用途落目录、隔离第三方与草稿、产出搬家清单与对照表，避免乱丢找不到。触发：文件乱丢、目录结构、分包、归档、文件夹规划、Assets布局、Content布局、存放规范、找不到文件、repo layout、file pack。 |

## 表格

| ID | 解决什么 |
|---|---|
| `excel-read` | 只读工作簿：定位区域、取值/公式/样式、截图。写前预检与写后回读。触发：读表、回读、预检、get-values、查公式、Excel 现状。 |
| `excel-format` | 格式层：先认表再切线；定级→列角色→非序号六位小数→零显零占位用横杠→左对齐居中。写完必跑。触发：颜色、排版、层级、format-range。 |
| `excel-com-write` | 经确认范围→沙盒改值/公式/插删行→必交排版→diff 只合记录格→获准晋升→回读。写前走读取层。触发：改产品表、沙盒写入、插行、表格连接器晋升、表写入配方。 |
| `tunable-table-diff` | 对比沙盒与正式数值表，分级变更风险并安全晋升或回滚。触发：表diff、数值晋升、tunable diff、改表对比。 |
| `data-readiness-check` | 数值框架簿与战斗模拟数据就绪硬闸。触发：多场景平衡、战斗模拟、表工具重跑、dry-run、框架簿路径、公式参数表头。 |
| `deliverable-sheets` | 按需填写决策、开放问题、进度、交接摘要等通用表，并与产物一起登记。触发：决策表、开放问题、进度表、交接摘要、通用表。 |
| `personal-server-table-sync` | 改完配表后同步到本机个人服：导表→output→后台重载/必要时重启。触发：同步个人服、导表到本地服、Luban 个人服、改表后开服。 |

## 方向与范围

| ID | 解决什么 |
|---|---|
| `pillar-define` | 定 3～5 条可检验体验支柱与像/不像反例，供全组引用否决功能。触发：支柱、pillar、设计支柱、反例、否决清单。 |
| `scope-cut-decision` | 在支柱约束下出保/砍/延后表，写清利弊、回滚与影响职种。触发：砍范围、scope cut、保什么砍什么、里程碑瘦身。 |
| `feature-gdd-slice` | 按节共写单功能 GDD：读上下文→八节骨架→逐节 Context/Options/Draft→冲突扫描与验收证据。触发：GDD、功能切片、系统设计、写规则、retrofit、空洞节补写、接口公式验收。 |
| `feature-vertical-slice` | 锁定验证问题与 3–5 分钟范围，打通主路径+失败态并试玩裁决。触发：竖切、vertical slice、最小可玩、切片演示。 |
| `experience-critique` | 按支柱对垂直切片打可执行批注（保/砍/改），指向具体物件而非空话。触发：体验评审、切片批注、fantasy 冲突、体验验收。 |
| `milestone-plan` | 用容量表、依赖板与日历排里程碑：成功证据、关键路径、缓冲与中段预演。触发：里程碑、版本计划、milestone plan。 |
| `risk-register-update` | 在风险台账表识别/重估风险，写可观测信号、缓解与复查日并按级排序。触发：风险台账、risk register、风险更新。 |
| `dependency-map` | 用边表/图工具映射系统依赖契约，跑环检测算法并输出并行组与裁剪扇出。触发：依赖图、dependency map、循环依赖、拓扑排序。 |
| `systems-index-map` | 从概念枚举显式/隐式系统，分层画依赖并产出可设计顺序的系统索引表。触发：系统索引、systems index、功能分解、map systems、隐式系统漏列、队首该设计谁。 |
| `rule-feasibility-check` | 把 GDD 规则拆成能力点，对照引擎/联机/工具链判定可行或降级方案。触发：规则可行性、能不能做、引擎能力、联机权威、降级方案、条件可行。 |

## 战斗与数值

| ID | 解决什么 |
|---|---|
| `combat-modeling` | 建战斗对象生命周期表、状态机与事件载荷，冻结结算管线顺序并对齐端权威。触发：战斗建模、战斗实体、状态机、事件载荷、combat model。 |
| `combat-flow-design` | 定可入库的战斗流程骨架：标准步骤 id、时间模型、资源轴、判定公式语法与胜负条件，供代码管线与配表直接引用。触发：战斗流程、combat flow、步骤名标准化、判定公式、接代码。 |
| `combat-feel-checklist` | 用帧预览、输入缓冲窗、Hitstop 帧与镜头震动强度检查战斗手感，短片作证据。触发：战斗手感、打击感、hitstop、input buffer、camera shake。 |
| `skill-kit-design` | 定定位、槽位职责、资源与冷却结构，交付可填系数的技能包骨架。触发：技能包、skill kit、技能组设计。 |
| `skill-numeric-pass` | 按技能包填写系数、对齐公式项，做档位对照与异常扫描。触发：技能数值、技能系数、skill numeric。 |
| `attribute-framework` | 定义属性主键、派生关系、快照与上下限，供公式与成长引用。触发：属性框架、属性表、一级二级属性。 |
| `attr-family-sync` | 新增或重排一层属性时，按读取→改动→格式→读取覆盖受影响表，并同步下游主键。触发：加属性、属性族、多层主键同步、同步配表。 |
| `damage-formula-pass` | 选定伤害/治疗通道、冻结运算顺序与钳制，并给出可解析表达式语法需要与验算槽。触发：伤害公式、damage formula、结算式、表达式语法。 |
| `counter-matrix-pass` | 定义克制轴、填矩阵、检查循环与强度并映射到公式修饰。触发：克制、属性相克、counter matrix。 |
| `progression-curve` | 定成长锚与曲线形状，落表字段与累计/差分验算槽，扫异常档并用 excel-com-write 改表。触发：成长曲线、升级曲线、进度节奏、累计代价。 |

## 经济与商业化

| ID | 解决什么 |
|---|---|
| `economy-loop-analysis` | 把核心产销循环拆成节点与有向边，找出断裂/滞留并决定改哪些表字段。触发：经济循环、产销闭环、核心循环、循环断裂。 |
| `sink-source-map` | 枚举货币/材料实体，列出 Source/Sink，算净流量并对齐上限与表字段。触发：产销地图、source sink、水龙头水槽。 |
| `price-curve-pass` | 选锚、建档位价带、扫描永不值/唯一解并映射调价字段。触发：物价、价格曲线、Teq、商店定价。 |
| `inflation-stress` | 定义多情景、投影库存/购买力、设计熔断选项并写出可复述结论。触发：通胀、压力测试、购买力、熔断。 |
| `iap-catalog-check` | 核对 IAP/礼包/通行证 SKU、价格档、内容物、限购与商店 ID 对照。触发：IAP 目录、SKU、礼包、通行证、商店后台、限购刷新。 |
| `monetization-kpi-pass` | 冻结商业化 KPI 口径、观测窗口与不伤支柱的禁区后再设计付费点。触发：商业化 KPI、ARPU、转化率、付费底线、观测窗口。 |

## 叙事关卡体验

| ID | 解决什么 |
|---|---|
| `narrative-beat-sheet` | 把故事节拍落成可挂门闸的 beat 表，对齐任务/对白/玩法触发。触发：节拍表、beat sheet、叙事结构、故事门闸、幕与 beat。 |
| `quest-spec` | 写可执行任务规格：状态机、目标键、奖励、失败与回滚、本地化键。触发：任务案、quest spec、任务状态机、接取完成条件、任务奖励。 |
| `dialogue-pass` | 按节点意图润色对白，控字数/声口/可跳过，并过设定禁词。触发：对白、dialogue、对话润色、声口、跳过策略、字幕字数。 |
| `lore-consistency-check` | 对照世界观圣经扫设定冲突、命名漂移与时间线矛盾。触发：世界观一致性、lore check、设定打架、Canon 冲突、时间线。 |
| `copy-pass` | 统一 UI/物品/系统短文案的术语、长度与语气。触发：文案、copy、UI文案、物品描述。 |
| `level-goals-spec` | 写清关卡主/可选/失败目标、教学点与时长预算，并与叙事 beat 挂钩。触发：关卡目标、level goals、胜负条件、教学点、一局时长、失败重试。 |
| `blockout-pass` | 用灰盒验证尺度/动线/门控/视线，玩家视角实测后再进美术替换。触发：灰盒、白盒、blockout、graybox、动线、门控、尺度校验。 |
| `encounter-script` | 编排遭遇波次/触发/重置/教学序，控制同屏预算与失败可读性。触发：遭遇脚本、encounter、波次、刷新、脱战重置、教学遭遇。 |
| `pacing-pass` | 用峰谷图对照战斗/解谜/叙事密度，实测时长并插入喘息点。触发：节奏、pacing、峰谷、过长砍支线、连续高压、安全区。 |
| `ux-flow-spec` | 画关键用户流：进入/操作/反馈/离开，含五态与异常流节点 ID。触发：UX 流图、交互流程、信息架构、五态、异常流。 |
| `ux-review-pass` | 对照流图走查迷失/误触/反馈弱，分级阻塞与抛光并回修。触发：可用性评审、UX review、热区、误操作、走查。 |
| `ui-kit-spec` | 在 Figma/设计 token/引擎 UI 库分层盘点控件，定义变体×尺寸×状态合同。触发：UI Kit、组件库、设计系统UI。 |
| `ui-screen-pass` | 按流程落单屏信息层级、kit 组件引用、多态与跳转。触发：UI屏、界面稿、screen pass。 |
| `ui-logic-pass` | 定义屏的状态机、事件、数据绑定与错误处理。触发：UI逻辑、界面状态机、ui logic。 |

## 美术音频技美

| ID | 解决什么 |
|---|---|
| `style-anchor` | 用参考板/取色器/并排比对写出一句视觉规则、色形材边界与拒收标准并版本化。触发：风格锚点、美术风格、视觉宪法、Art Bible切片。 |
| `concept-key-art` | 按风格锚点写 Brief、剪影选型并产出可进 3D 的主视觉与三视图。触发：概念图、主视觉、三视图、角色设定、关键原画。 |
| `character-asset-checklist` | 按档位完成角色建模、UV、贴图、LOD 并导入引擎验收。触发：角色模型、角色资产、高模低模、角色贴图、角色LOD。 |
| `env-asset-checklist` | 按网格定模块尺寸与枢轴，做接缝/碰撞/材质复用后试摆再导出。触发：场景模型、模块化场景、环境资产、接缝。 |
| `anim-set-checklist` | 列出最小可玩与完整动作集，核对片段存在与技术约束后收包。触发：动画集、动作列表、Locomotion、动画收包。 |
| `anim-event-hook` | 建事件字典、在关键帧植入 Notify/事件并对齐逻辑与特效。触发：动画事件、Hit帧、AnimNotify、攻击判定帧。 |
| `bind-rig-checklist` | 对照骨架模板装 IK/约束与 Socket，并用极端姿验绑定。触发：绑定、骨架、Rig、IK、挂点Socket。 |
| `skin-weight-pass` | 按极端姿刷权重，卡影响骨上限与压缩预览后交动画。触发：蒙皮、权重、Skinning、飞肉、塌陷。 |
| `lod-budget-pass` | 订各级面数比与切换距离，扫覆盖并实机标定同屏策略。触发：LOD预算、LOD距离、减面、同屏模型预算。 |
| `shader-budget-note` | 盘点变体与关键字，订白名单/指令上限并合并超标材质。触发：Shader预算、材质变体、关键字膨胀、移动端指令。 |
| `vfx-budget-pass` | 订 Overdraw/粒子上限，测热区并做保可读的降级。触发：特效预算、Overdraw、Fillrate、粒子上限。 |
| `vfx-skill-hook` | 按 Timeline/Notify 帧与 Socket 名挂技能特效，核粒子预算与 Overdraw，并处理打断清理。触发：特效挂点、技能VFX、Socket、Notify帧、overdraw、粒子预算。 |
| `audio-fmod-checklist` | 用 FMOD Studio / Audacity / ffmpeg 完成音频事件入库与试听校验。触发：音频、FMOD、音效、BGM、混音、Audacity。 |
| `fmod-bank-build` | 用 FMOD Studio / fmodstudiocl 做工程诊断、Bank 构建与 GUID 导出。触发：FMOD、Bank、音频中间件、fmodstudiocl、声音打包。 |
| `export-naming-gate` | 按 Domain/Type/Name/Variant/LOD 扫描导出物、批量改名并同步引用。触发：命名规范、导出命名、资源改名、命名扫描。 |
| `export-pipeline-fix` | 用好坏金样跑导出器，查依赖/命名失败可读性与幂等。触发：导出校验、资源管线、export pipeline。 |
| `import-validate` | 按导入预设入库，机检缩放/材质/LOD 后试播并固定可引用路径。触发：导入校验、FBX导入、资源入库检查。 |
| `terrain-gaea-pass` | 用 Gaea 程序化地形并导出供场景模块衔接。触发：地形、Gaea、heightmap、地形图、开放世界地块。 |

## 工程与测试

| ID | 解决什么 |
|---|---|
| `client-bugfix` | 按复现→取证→假说→最小改动→回归点验证修客户端缺陷。触发：修 bug、客户端修复、崩溃修复。 |
| `client-combat-frame-debug` | 对齐动画事件/判定窗/VFX 时间线，用调试 HUD 定位偏差并只修表现。触发：战斗帧、手感、判定窗、技能对齐。 |
| `server-api-contract` | 冻端点字段/错误码/幂等与版本规则，并写契约测。触发：API 契约、接口定稿、协议变更。 |
| `server-combat-authority-check` | 划权威边界，查结算输入/种子，测非法包驳回与回放偏差分类。触发：战斗权威、结算、回放、技能同步。 |
| `anti-cheat-hook-check` | 圈关键写路径、查服务端校验/速率/幂等、测绕过与误杀并补取证日志。触发：反作弊、挂点、校验、篡改。 |
| `save-schema-pass` | 冻存档字段与版本，写迁移、加载校验，坏档隔离演练。触发：存档、save schema、迁移、坏档。 |
| `auto-test-scaffold` | 搭测试目录、可注入夹具、CI 失败非0钩与片状 quarantine 政策。触发：测试脚手架、test scaffold、CI 接线。 |
| `case-automation-map` | 把 GWT/回归用例映射到 pytest/Unity Test/自动化 id，标覆盖缺口与片状信号并排期。触发：自动化映射、用例自动 id、coverage gap、flake。 |
| `test-case-from-gdd` | 从 GDD/AC 抽可测点写 GWT，建追溯矩阵并标自动化候选。触发：写用例、GDD 用例、测试用例生成。 |
| `qa-plan` | 用风险矩阵定本迭代用例量级与环境，写可观察开测/收测条件。触发：测试计划、QA plan、用例规划、开测收测。 |
| `ci-smoke` | 探测测试命令，跑自动冒烟子集与手工核心批，定位红灯来源。触发：CI 冒烟、smoke、提测前自动检。 |
| `compat-smoke` | 定 N/N-1 矩阵，实测旧档升级、协议/资源失败可读且不脏写。触发：兼容、升级、热更、N-1、迁移。 |
| `regression-pack` | 按变更影响与历史缺陷组回归包，执行可检索队列，标缺口并回灌。触发：回归、regression、版本回跑、影响组包。 |
| `bug-report-write` | 把现象写成可复现缺陷单：环境、步骤、期望/实际、证据与严重度。触发：提单、bug、缺陷报告。 |
| `build-gate-checklist` | 盘点构建阻断项：CI job、产物路径、崩溃签名与已知问题预算，产出可修的阻断清单。触发：构建阻断、CI 红灯盘点、产物缺口、known issue budget。 |
| `build-acceptance` | 对目标构建跑主路径验收、对齐版本号、清点已知缺陷处置。触发：验收、acceptance、提测构建核对。 |
| `device-matrix-pass` | 按高中低档必测机跑功能冒烟、热与帧稳，验证降级开关。触发：设备矩阵、机型、低端机、热节流、画质档、降级开关。 |
| `perf-budget-check` | 选代表场景采可复采样本，对照性能预算定位超项并给改法选项。触发：性能预算、profiler、卡顿、帧率、内存。 |
| `platform-cert-smoke` | 按目标店条款要点跑短清单：权限最小化、支付登录沙箱、冷启零崩溃与合规截图。触发：认证、商店审核、平台合规、提审冒烟。 |
| `release-notes-stub` | 从 git log/表 diff/裁剪决议收集变更，分类转写玩家说明并做包内抽检。触发：更新说明、patch notes、版本公告。 |

## 活服与外接

| ID | 解决什么 |
|---|---|
| `liveops-calendar` | 排活服日历：日/周/季节奏、活动撞车消解与容量对齐。触发：活动日历、liveops calendar、档期、赛季、运营节奏。 |
| `event-spec` | 写活动规格：目标/玩法/奖励/开关/埋点与失败补发。触发：活动案、event spec、限时活动、开关表、活动埋点。 |
| `reward-mail-check` | 检查发奖邮件模板、附件校验、补发与过期策略，防重复领取。触发：奖励邮件、发奖、补发、邮件附件、过期清理。 |
| `mcp-autostart` | 启动时按档位拉起外接：核心全量，其余懒接。触发：外接拉起、MCP 挂掉、0 工具、核心档、懒接。 |
| `naming-consistency-check` | 扫描实体/字段/UI 键命名冲突与漂移，给出规范名与替换序。触发：命名一致、rename、术语统一。 |
| `diagram-pack` | 按图种选工具并落盘：环/流程图写 Mermaid，树/大纲用 xmind，画布精修用 excalidraw，协作白板用 miro。触发：流程图、系统循环、mermaid、excalidraw、脑图、xmind、画布、miro、块连线、架构图。 |
| `pipeline-tool-spec` | 定义工具职责、IO/退出码、幂等配置与 CI 测试钩。触发：工具规格、CLI 契约、pipeline tool。 |

