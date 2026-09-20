# -*- coding: utf-8 -*-
"""生成示意曲线图 SVG。数据为架构对比模型，不是某工作室实测。"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent


def polyline(xs, ys, x0, y0, x1, y1, xmin, xmax, ymin, ymax) -> str:
    pts = []
    for x, y in zip(xs, ys):
        px = x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
        py = y1 - (y - ymin) / (ymax - ymin) * (y1 - y0)
        pts.append(f"{px:.1f},{py:.1f}")
    return " ".join(pts)


def chart(
    path: Path,
    title: str,
    subtitle: str,
    xlabel: str,
    ylabel: str,
    series: list[tuple[str, str, list[float], list[float]]],
    ymin: float,
    ymax: float,
) -> None:
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
    lines = []
    legend = []
    for i, (name, color, xs, ys) in enumerate(series):
        pts = polyline(xs, ys, L, T, R, B, xmin, xmax, ymin, ymax)
        lines.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" points="{pts}"/>'
        )
        legend.append(
            f'<rect x="{L + i * 210}" y="388" width="14" height="3" fill="{color}"/>'
            f'<text x="{L + 20 + i * 210}" y="393" class="leg">{name}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
  <rect width="100%" height="100%" fill="#fbfcfd"/>
  <style>
    .title {{ font: 600 18px/1.3 "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #1f2328; }}
    .sub {{ font: 12px/1.4 "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #656d76; }}
    .tick, .axis {{ font: 11px/1.2 "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #656d76; }}
    .leg {{ font: 12px/1.2 "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #1f2328; }}
  </style>
  <text x="{L}" y="28" class="title">{title}</text>
  <text x="{L}" y="48" class="sub">{subtitle}</text>
  {''.join(grid)}
  <line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="#8b939c"/>
  <line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="#8b939c"/>
  {''.join(xticks)}
  <text x="24" y="{(T + B) / 2:.0f}" transform="rotate(-90 24 {(T + B) / 2:.0f})" text-anchor="middle" class="axis">{ylabel}</text>
  <text x="{(L + R) / 2:.0f}" y="378" text-anchor="middle" class="axis">{xlabel}</text>
  {''.join(lines)}
  {''.join(legend)}
</svg>
'''
    path.write_text(svg, encoding="utf-8")


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
        "Cursor 发现阶段时延（示意模型）",
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
    print("wrote 3 charts")


if __name__ == "__main__":
    main()
