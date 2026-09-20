# Architecture

GSH uses a four-layer file contract for the **full game-production pipeline**. The agent executes inside a named roster, writes to the isolation surface, and stops at human gates for pillars, scope, promotion, and ship. The thesis is bounded autonomy, auditable diffs, and human gates — not unattended ship.

Read “Design philosophy”, then “Three things to understand first” in the root [README.en.md](../../README.en.md) (full-pipeline coverage / human–AI boundaries / capability curve) before drilling into this folder. 中文：[README.md](README.md).

What each layer does, and which command you run:

- [L1 constitution](l1-constitution.md) — per-turn tax: read order, write isolation, close, secrets, destructive gates
- [L2 director](l2-director.md) — request becomes a loadplan; named ids; a craft opens only step one
- [L3 capability](l3-capability.md) — 35 crafts / 106 skills / MCP purpose stubs; open one step at a time
- [L4 filing](l4-filing.md) — current card, audit log, verify report; promotion still needs a human
- [Cross-harness](cross-harness.md) — one content source, written as each tool’s complete native tree
- [Adapters](../adapters/README.md)
- [MCP policy](../mcp-policy.md)
- [Install](../install.md)
- [Release](../release.md)
- [Docs map](../README.md)
