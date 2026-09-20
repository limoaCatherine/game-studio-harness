---
name: anti-cheat-hook-check
description: "圈关键写路径、查服务端校验/速率/幂等、测绕过与误杀并补取证日志。触发：反作弊、挂点、校验、篡改。"
---

# 反作弊挂点怎么查

## 何时用

- 上线前核货币/战绩/购买是否服务端验
- 改包、加速、重放嫌疑要定挂点
- 校验过严误杀弱网或合法极限操作
- 单机存档防篡改基础要核

## 怎么做

### 1. 圈关键写路径

1. 建表 `anticheat/write_paths.csv`：`path_id|domain(currency/progress/score/purchase/rank/drop)|entry_file:fn|server_check?(Y/N/risk)|mode(online/offline)`；表写入若用表格文件走 `excel-com-write`。
2. 用版本库 CLI / 代码检索扫 `Send|Report|Claim|Rpc` 类结算入口（按仓库改路径），列出客户端直报或可改写点；标终裁嫌疑并行链 `server-combat-authority-check`（本技能不灌战斗权威细则）。
3. 排行/赛季结算、掉落结算各单独成行；单机仅内存值可标 `risk_accepted` + 存档加载校验指针（`save-schema-pass`）；**联机终裁嫌疑不得用 risk_accepted 掩盖**。
4. 扫 `addons|plugins|third_party`；来源不明标红。

**做到**：csv 覆盖六域；每行有 `entry_file:fn`；终裁嫌疑条数可计。

**不合格**：入口无文件锚或联机行空校验 → 回本步补齐。

### 2. 查挂点实现

1. 对每条 `server_check=Y`：记录校验点 `file:fn`、范围检查、速率窗 `N/window`、失败处置（拒/回滚/踢）、原因码字段名。
2. 网络层：抽查 Packet/RPC 入口的大小/类型/值域；位置与战绩读权威字段赋值，不以客户端原样落库。
3. 检索 `Recv|OnRpc|HandlePacket|RateLimit|Idempoten` 抽缺校验调用，开缺口项 `gap_id`。
4. 支付/发奖链路：请求→校验→账本写入；确认幂等键列（`idem_key`/`order_id`），重放不双加。
5. Release 构建扫调试后门/未鉴权管理端点；结果写入扫描文件。

**做到**：每关键动作有可指 `file:fn`+速率窗+失败处置+原因码；支付链路幂等键可指；Release 后门扫描有结果文件。

**不合格**：缺幂等键、无速率窗、Release 仍有未鉴权后门 → 回本步补校验与扫描。

### 3. 绕过面演练

1. 绕过面清单：`tamper_field|replay_reward|clock_skew_cd|mem_currency_sync`；测试环境最小对照，期望拒绝或回滚。
2. 改包：改伤害/货币字段发合法包结构；协议/抓包或 mock 记录请求/响应码。
3. 重放：抓一次合法发奖包原样重放；期望幂等，账本差额=0。
4. 加速：改客户端时钟刷 CD/活动；服务端以服务器时间为准拒绝。
5. 绕过成功→缺陷单（严重度按能否改竞技/付费）；未测面标 `untested`，防护结论只写已测面。

**做到**：四面各有 PASS/FAIL/untested；重放账本差额记录；成功绕过有缺陷 id。

**不合格**：应拦却放过 → 回步骤 2 补校验/幂等后重测该面。

### 4. 误杀与取证日志

1. 误杀用例：弱网重试（断线重发同 `idem_key`）、合法极限 CPS/最短 CD；过严则仅调阈值字段，不关校验。
2. 检测日志必含：`player_id|action|reason_code|key_values|ts|request_id`；在日志平台或本地尾部抽一条能重建请求。
3. 原因码分玩家可见 vs 内部；封禁决策只依据含完整取证字段的检测。
4. 把误杀用例写入回归包（测试标签或手工步骤文件）；阈值回调后必跑。

**做到**：误杀两例有结果；取证六字段齐；回归路径可指；缺字段检测已清零或挂缺口。

**不合格**：无法用日志重建请求 → 回步骤 2 补取证字段后再谈封禁。

## 做到

- 关键写路径表覆盖六域且每行有入口锚
- 挂点含范围、速率窗、失败处置、原因码；支付链路幂等可指
- 绕过面有 PASS/FAIL/untested；误杀两例有结果；Release 后门扫描有记录

## 失败回哪一步

- 关键域缺行或 `server_check` 空 → 回步骤 1
- 挂点找不到入口、缺幂等键 → 回步骤 2
- 期望应拦却放过 → 回步骤 2 补校验后再测步骤 3
- 缺取证字段无法定位误拒 → 回步骤 2 补日志字段后再谈封禁（步骤 4）

下一步常接：`save-schema-pass` / `server-api-contract` / `server-combat-authority-check`。
