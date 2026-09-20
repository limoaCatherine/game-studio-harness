---
name: write-isolation
description: 任何正式面写入先落到隔离根：表沙箱、代码 worktree、引擎 Sandbox、资产 _Dev；沙箱目录不进 git；晋升须人准且只回写记录集。触发：沙盒、隔离、正式面、晋升、worktree、写级别、surfaces、git忽略、沙箱忽略。
---

# 写隔离（通用，不绑 Excel）

## 何时用

- 本轮会改表、代码、引擎试验物、美术草稿或任何「正式面」
- 定档写了 `write_class`，或现行卡写级别不是 `read`

## 怎么做

### 1. 认正式面

1. 打开 `.harness/surfaces.json`（无则从 `~/.cursor/harness/surfaces.default.json` 拷一份再改路径）。
2. 按 `kind` 找到本轮要动的面：`excel` / `git` / `engine` / `draft` / 其他。
3. 记下 `official` 与 `sandbox`。没有对应行 → 先补地图，再动手。

**做到**：知道官方根和隔离根。

### 2. 按写级别落笔

| `write_class` | 允许 |
|---|---|
| `read` | 只读正式面 |
| `sandbox` | 只写隔离根（默认） |
| `promote` | 人准后把记录集写回正式面对应格子/路径 |
| `destroy` | 本轮明确授权的不可逆操作 |

1. 表：正式表同级 `沙箱/<名>.sandbox-时间戳.xlsx`，禁止直连正式簿。交审时改成 `<名>.sandbox-<会话短名>.xlsx`（会话短名 = 会话目录名），changeset 同步改名；见 `excel-com-write`。交审只 `show=true` 开沙箱，禁止对正式簿开可见 COM 窗。审阅完（人已准晋升、接着说话且不再看窗、或明确说合/关/继续）当拍释放沙箱 COM 窗，不要问「还开着看吗」。「释放沙箱」不是删 `沙箱/*.xlsx` 或 changeset。
2. 代码：隔离 worktree / `.harness/worktrees/`，不要在主工作区试错后假装没动过正式文件。
3. 引擎：只写地图里 `kind=engine` 的隔离根。
4. 资产草稿：只写地图里 `kind=draft` 的隔离根，不进发包集合。

**做到**：本轮产生的文件都在隔离根。

### 沙箱不进 git

1. 每个会落 `沙箱/` 的 git 仓，根 `.gitignore` 必须有一行 `**/沙箱/`。没有就补。父目录忽略不传给子仓。
2. 禁止 `git add` 沙箱路径、changeset、shadow。新克隆出来的副本默认不入库。
3. 已跟踪：`git rm -r --cached -- <沙箱相对路径>`，不要把文件加回去。不替人 commit，除非人明确要求。
4. `xlsx_sandbox_clone` 之后用 `git check-ignore -v -- <副本路径>` 抽查；没命中就先补忽略再继续写。
5. 释放沙箱窗不是删文件，也不是把沙箱提交进库。

**做到**：沙箱路径已被忽略；未把沙箱文件 add 进库。

### 3. 晋升

1. 列出记录集：哪些格、哪些路径、什么 diff。
2. 等人准。不准则停在沙盒。
3. 只回写记录集，禁止整文件覆盖正式面。表晋升走 `xlsx_merge_changeset`，只合 changeset 格子，不写 rollback，不用 rollback 拷回。禁止在正式面同级新建 `*.rollback-*`、`版本/`、`*.xlsx-shadow.xlsx`。晋升前若沙箱窗还占着文件：先释放再 merge。晋升后不要再 `show=true` 重开沙箱，除非人明确还要看。禁止对正式簿 `show=true`。
4. 回读正式面，把结果写进现行卡。

**做到**：正式面变更可指到记录集。

## 完成检查

- [ ] 用的是地图里的隔离根，不是临时另开的杂目录
- [ ] `promote` 有人准与记录集
- [ ] 现行卡写明写级别与禁改
- [ ] 审阅完已释放 COM / 审阅窗，沙箱文件与 changeset 仍在
- [ ] 本仓 `.gitignore` 含 `**/沙箱/`；沙箱路径 `git check-ignore` 命中；未 `git add` 沙箱文件
