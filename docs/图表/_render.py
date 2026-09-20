# -*- coding: utf-8 -*-
"""生成示意/清单计数图。曲线是架构对比模型；雷达与条形按本仓职种/技能/外接清单计分。"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = '"Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'


def polyline(xs, ys, x0, y0, x1, y1, xmin, xmax, ymin, ymax) -> str:
    pts = []
    for x, y in zip(xs, ys):
        px = x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
        py = y1 - (y - ymin) / (ymax - ymin) * (y1 - y0)
        pts.append(f"{px:.1f},{py:.1f}")
    return " ".join(pts)


def svg_head(w: int, h: int, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <rect width="100%" height="100%" fill="#f6f8fb"/>
  <defs>
    <linearGradient id="hero" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1f6feb"/><stop offset="100%" stop-color="#8250df"/>
    </linearGradient>
  </defs>
  <style>
    .title {{ font: 600 18px/1.3 {FONT}; fill: #1f2328; }}
    .sub {{ font: 12px/1.4 {FONT}; fill: #656d76; }}
    .tick, .axis {{ font: 11px/1.2 {FONT}; fill: #656d76; }}
    .leg {{ font: 12px/1.2 {FONT}; fill: #1f2328; }}
    .lab {{ font: 11px/1.2 {FONT}; fill: #1f2328; }}
    .num {{ font: 700 22px/1 {FONT}; fill: #1f2328; }}
    .cap {{ font: 12px/1.3 {FONT}; fill: #656d76; }}
  </style>
'''


def chart(path: Path, title: str, subtitle: str, xlabel: str, ylabel: str,
          series: list[tuple[str, str, list[float], list[float]]], ymin: float, ymax: float) -> None:
    W, H = 840, 420
    L, R, T, B = 72, 800, 78, 352
    xs_all = [x for _, _, xs, _ in series for x in xs]
    xmin, xmax = min(xs_all), max(xs_all)
    grid = []
    for i in range(5):
        y = ymin + (ymax - ymin) * i / 4
        py = B - (y - ymin) / (ymax - ymin) * (B - T)
        grid.append(
            f'<line x1="{L}" y1="{py:.1f}" x2="{R}" y2="{py:.1f}" stroke="#e6e8eb" stroke-width="1"/>'
            f'<text x="{L - 10}" y="{py + 4:.1f}" text-anchor="end" class="tick">{y:g}</text>'
        )
    xticks = []
    for i in range(5):
        x = xmin + (xmax - xmin) * i / 4
        px = L + (x - xmin) / (xmax - xmin) * (R - L)
        xticks.append(
            f'<line x1="{px:.1f}" y1="{B}" x2="{px:.1f}" y2="{B + 6}" stroke="#8b939c"/>'
            f'<text x="{px:.1f}" y="{B + 22}" text-anchor="middle" class="tick">{x:g}</text>'
        )
    lines, legend = [], []
    for i, (name, color, xs, ys) in enumerate(series):
        pts = polyline(xs, ys, L, T, R, B, xmin, xmax, ymin, ymax)
        lines.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" points="{pts}"/>'
        )
        legend.append(
            f'<rect x="{L + i * 210}" y="388" width="14" height="3" fill="{color}"/>'
            f'<text x="{L + 20 + i * 210}" y="393" class="leg">{name}</text>'
        )
    path.write_text(
        svg_head(W, H, title)
        + f'<text x="{L}" y="28" class="title">{title}</text>'
        + f'<text x="{L}" y="48" class="sub">{subtitle}</text>'
        + "".join(grid)
        + f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="#8b939c"/>'
        + f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="#8b939c"/>'
        + "".join(xticks)
        + f'<text x="24" y="{(T + B) / 2:.0f}" transform="rotate(-90 24 {(T + B) / 2:.0f})" text-anchor="middle" class="axis">{ylabel}</text>'
        + f'<text x="{(L + R) / 2:.0f}" y="378" text-anchor="middle" class="axis">{xlabel}</text>'
        + "".join(lines) + "".join(legend) + "</svg>\n",
        encoding="utf-8",
    )


def radar(path: Path) -> None:
    axes = [
        "体验支柱 / GDD",
        "战斗与数值",
        "经济 / 活服",
        "叙事文案",
        "美术 DCC",
        "客户端引擎",
        "服务端权威",
        "QA 矩阵",
        "写隔离 / 档案柜",
        "多工具适配",
    ]
    series = [
        ("通用编程助手", "#8b939c", [2.0, 1.2, 0.8, 1.5, 0.6, 2.4, 1.4, 2.0, 1.0, 1.2]),
        ("48h 黑客马拉松技能包", "#cf222e", [2.6, 2.0, 1.4, 2.2, 1.8, 3.4, 1.6, 2.2, 1.2, 2.4]),
        ("引擎向 GameStudio 类仓", "#fb8f44", [3.6, 2.4, 2.0, 3.4, 3.2, 4.6, 2.2, 3.6, 2.0, 4.6]),
        ("本仓（清单计分）", "#1f6feb", [4.6, 4.8, 4.7, 4.2, 4.6, 4.0, 4.7, 4.6, 4.9, 4.8]),
    ]
    W, H = 920, 560
    cx, cy, r = 360, 300, 190
    n = len(axes)
    rings = []
    for k in range(1, 6):
        rr = r * k / 5
        pts = []
        for i in range(n):
            ang = -math.pi / 2 + i * 2 * math.pi / n
            pts.append(f"{cx + rr * math.cos(ang):.1f},{cy + rr * math.sin(ang):.1f}")
        rings.append(f'<polygon fill="none" stroke="#d0d7de" points="{" ".join(pts)}"/>')
    spokes, labels = [], []
    for i, name in enumerate(axes):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        spokes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d0d7de"/>')
        lx, ly = cx + (r + 28) * math.cos(ang), cy + (r + 28) * math.sin(ang)
        anchor = "middle"
        if math.cos(ang) > 0.35:
            anchor = "start"
        elif math.cos(ang) < -0.35:
            anchor = "end"
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="lab">{name}</text>')

    def poly(vals: list[float], color: str, opacity: str) -> str:
        pts = []
        for i, v in enumerate(vals):
            ang = -math.pi / 2 + i * 2 * math.pi / n
            rr = r * (v / 5.0)
            pts.append(f"{cx + rr * math.cos(ang):.1f},{cy + rr * math.sin(ang):.1f}")
        return (
            f'<polygon fill="{color}" fill-opacity="{opacity}" stroke="{color}" stroke-width="2" points="{" ".join(pts)}"/>'
        )

    body = [poly(vals, color, "0.10" if i < 3 else "0.22") for i, (_, color, vals) in enumerate(series)]
    legend = []
    for i, (name, color, _) in enumerate(series):
        legend.append(
            f'<rect x="700" y="{120 + i * 28}" width="14" height="14" rx="2" fill="{color}"/>'
            f'<text x="722" y="{132 + i * 28}" class="leg">{name}</text>'
        )
    path.write_text(
        svg_head(W, H, "制作流程覆盖雷达")
        + '<text x="40" y="32" class="title">全制作流程覆盖雷达</text>'
        + '<text x="40" y="54" class="sub">按本仓 35 职种 / 106 技能 / 36 外接清单计分，对照公开的通用助手、Jam 包与引擎向 GameStudio 类仓。不是第三方评测、不是实测 SLA。</text>'
        + "".join(rings) + "".join(spokes) + "".join(body) + "".join(labels) + "".join(legend)
        + "</svg>\n",
        encoding="utf-8",
    )


def bars(path: Path) -> None:
    rows = [
        ("制作 / 创意方向", 4, "#8250df"),
        ("系统 / 战斗 / 数值 / 经济", 11, "#1f6feb"),
        ("叙事 / 文案 / UX", 4, "#1a7f37"),
        ("角色 / 场景 / 技美 / 动画", 9, "#bf3989"),
        ("客户端 / 服务端 / 工具", 6, "#cf222e"),
        ("测试五岗", 5, "#9a6700"),
    ]
    W, H = 840, 420
    L, T = 220, 80
    max_v = 12
    bars_s = []
    for i, (name, val, color) in enumerate(rows):
        y = T + i * 48
        w = 520 * val / max_v
        bars_s.append(
            f'<text x="208" y="{y + 18}" text-anchor="end" class="lab">{name}</text>'
            f'<rect x="{L}" y="{y}" width="{w:.1f}" height="26" rx="4" fill="{color}"/>'
            f'<text x="{L + w + 8:.1f}" y="{y + 18}" class="leg">{val}</text>'
        )
    path.write_text(
        svg_head(W, H, "职种覆盖")
        + '<text x="40" y="32" class="title">35 个职种如何铺满制作流水线</text>'
        + '<text x="40" y="54" class="sub">计数来自 cursor/agents/*.md 清单。一条职种主路径，不预展开整条技能。</text>'
        + "".join(bars_s)
        + '<text x="220" y="390" class="axis">职种数量（制作人 4 · 策划 11 · 叙事UX 4 · 美术 9 · 程序 6 · 测试 5）</text>'
        + "</svg>\n",
        encoding="utf-8",
    )


def jam(path: Path) -> None:
    hours = [0, 8, 16, 24, 36, 48]
    generic = [8, 18, 24, 28, 30, 31]
    ours = [12, 28, 44, 58, 70, 78]
    chart(
        path,
        "48 小时黑客马拉松可覆盖工作面（示意模型）",
        "同一支小队、同一套代理：通用助手停在写代码；本仓按职种拆开后能同时推进策划、表、美术挂点、权威与验收。",
        "Jam 已过小时",
        "已覆盖工作面（相对指数）",
        [
            ("一个通用编程助手", "#8b939c", hours, generic),
            ("本仓：职种拆分 + 点名注入", "#1f6feb", hours, ours),
        ],
        0,
        90,
    )


def compare(path: Path) -> None:
    items = [
        ("引擎代码技能堆", 3, 5, 3),
        ("制作操作系统（定档/结案）", 5, 2, 2),
        ("写隔离 + 记录集晋升", 5, 2, 1),
        ("Excel / 配表生产", 5, 1, 0),
        ("DCC / 音频 / 关卡外接", 5, 3, 1),
        ("服务端战斗权威", 5, 2, 1),
        ("活服 / 商业化 / 经济", 5, 2, 1),
        ("多工具适配", 5, 5, 3),
    ]
    W, H = 920, 480
    L, T = 260, 78
    body = []
    colors = ("#1f6feb", "#fb8f44", "#8b939c")
    names = ("本仓", "引擎向公开仓", "通用 Superpowers 类")
    for i, (label, a, b, c) in enumerate(items):
        y = T + i * 44
        body.append(f'<text x="248" y="{y + 16}" text-anchor="end" class="lab">{label}</text>')
        for j, val in enumerate((a, b, c)):
            x = L + j * 200
            w = 36 * val
            body.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="3" fill="{colors[j]}" fill-opacity="0.9"/>'
                f'<text x="{x + w + 6}" y="{y + 16}" class="tick">{val}</text>'
            )
    legend = []
    for i, (name, color) in enumerate(zip(names, colors)):
        legend.append(
            f'<rect x="{260 + i * 180}" y="440" width="14" height="14" rx="2" fill="{color}"/>'
            f'<text x="{280 + i * 180}" y="452" class="leg">{name}</text>'
        )
    path.write_text(
        svg_head(W, H, "能力对照")
        + '<text x="40" y="32" class="title">和公开顶级 harness 仓比什么</text>'
        + '<text x="40" y="54" class="sub">对照 GameStudio / YJack 一类引擎技能堆，以及 Superpowers 一类通用编程方法论。分数是架构定位，不是下载量或评测榜。</text>'
        + "".join(body) + "".join(legend) + "</svg>\n",
        encoding="utf-8",
    )


def kpi(path: Path) -> None:
    cards = [
        ("35", "职种 / 子代理", "从创意总监到测试负责人"),
        ("106", "事件技能", "一件事一份正文，按步打开"),
        ("36", "制作外接", "Excel 核心，其余懒接"),
        ("5", "AI 编程工具", "Cursor · Claude · Codex · Grok · DSH"),
    ]
    W, H = 840, 220
    body = ['<text x="40" y="36" class="title">本仓清单，不是营销口号</text>']
    for i, (n, cap, sub) in enumerate(cards):
        x = 40 + i * 200
        body.append(
            f'<rect x="{x}" y="58" width="184" height="130" rx="10" fill="#fff" stroke="#d0d7de"/>'
            f'<text x="{x + 16}" y="100" class="num">{n}</text>'
            f'<text x="{x + 16}" y="128" class="leg">{cap}</text>'
            f'<text x="{x + 16}" y="154" class="cap">{sub}</text>'
        )
    path.write_text(svg_head(W, H, "清单 KPI") + "".join(body) + "</svg>\n", encoding="utf-8")


def pipeline(path: Path) -> None:
    stages = [
        ("1 定方向", "支柱 / 砍范围 / 竖切"),
        ("2 定规则", "系统索引 / GDD / 可行性"),
        ("3 定数字", "属性 / 公式 / 物价 / 成长"),
        ("4 定体验", "关卡 / 叙事 / UX / 文案"),
        ("5 出资产", "原画 / 模型 / 绑定 / 动画 / 特效 / 音频"),
        ("6 进引擎", "导入 / LOD / Shader / 帧同步"),
        ("7 上权威", "服务端结算 / 反作弊 / 存档"),
        ("8 能验收", "用例 / 兼容 / 性能 / 发版"),
        ("9 能运营", "活动 / 邮件 / 商业化 KPI"),
    ]
    W, H = 920, 300
    parts = ['<text x="40" y="32" class="title">一条游戏制作流水线，而不是一堆代码技能</text>',
             '<text x="40" y="54" class="sub">九段都能点到职种主路径。引擎向公开仓通常在 6 段最厚；本仓在 3 / 7 / 9 段明显更厚。</text>']
    for i, (title, sub) in enumerate(stages):
        x = 28 + (i % 9) * 98
        y = 86
        lines = []
        for j, word in enumerate(sub.replace(" / ", "/").split("/")):
            lines.append(f'<text x="{x + 8}" y="{y + 62 + j * 16}" class="cap">{word.strip()}</text>')
        parts.append(
            f'<rect x="{x}" y="{y}" width="90" height="170" rx="8" fill="#fff" stroke="#1f6feb"/>'
            f'<rect x="{x}" y="{y}" width="90" height="8" fill="url(#hero)"/>'
            f'<text x="{x + 8}" y="{y + 36}" class="leg">{title}</text>'
            + "".join(lines)
        )
    path.write_text(svg_head(W, H, "全流程") + "".join(parts) + "</svg>\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    xs = list(range(1, 9))
    chart(
        OUT / "上下文占用.svg",
        "会话上下文占用（示意模型）",
        "全量灌入随轮次接近窗口顶；点名注入把增长率压在可工作区间。不是某工作室实测。",
        "会话轮次",
        "相对占用（%）",
        [
            ("全量灌入技能/职种/外接", "#cf222e", xs, [18, 28, 41, 55, 70, 84, 94, 99]),
            ("本架构：只注入点名正文", "#1f6feb", xs, [14, 17, 20, 23, 26, 29, 32, 35]),
        ],
        0,
        100,
    )
    chart(
        OUT / "冷启动时延.svg",
        "外接发现阶段时延（示意模型）",
        "核心直连保持可握手；其余懒接，避免 Unity / 大工具表堵死开场。",
        "已注册外接数量",
        "发现阶段秒数",
        [
            ("全部外接启动即连", "#cf222e", [4, 8, 16, 24, 32, 36], [3, 8, 18, 32, 48, 58]),
            ("核心直连 + 其余懒接", "#1a7f37", [4, 8, 16, 24, 32, 36], [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]),
        ],
        0,
        60,
    )
    chart(
        OUT / "正式面风险.svg",
        "正式面误写累积风险（示意模型）",
        "直接改正式面随会话叠加；隔离根默认写、人准后只回写记录集，风险接近持平。",
        "并行会话数",
        "不可逆误写相对风险",
        [
            ("代理直接写正式面", "#cf222e", [1, 2, 3, 4, 5, 6], [1.0, 2.3, 4.0, 6.2, 8.8, 11.5]),
            ("沙盒默认 + 记录集晋升", "#8250df", [1, 2, 3, 4, 5, 6], [0.3, 0.4, 0.5, 0.55, 0.6, 0.65]),
        ],
        0,
        12,
    )
    radar(OUT / "覆盖雷达.svg")
    bars(OUT / "职种覆盖.svg")
    jam(OUT / "黑客马拉松.svg")
    compare(OUT / "能力对照.svg")
    kpi(OUT / "清单KPI.svg")
    pipeline(OUT / "全流程.svg")
    print("wrote 9 charts")


if __name__ == "__main__":
    main()
