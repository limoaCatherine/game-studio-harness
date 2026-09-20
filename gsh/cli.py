# -*- coding: utf-8 -*-
"""python -m gsh  入口：setup / sync / verify / doctor / uninstall。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gsh import __version__
from gsh.commands import doctor, setup, studio, sync, uninstall, verify


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gsh",
        description="Game Studio Harness CLI — 安装、点名、续上、职种下一步、关项。",
    )
    p.add_argument("--version", action="version", version=f"gsh {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--workspace", help="业务根（将放 .harness）")
        sp.add_argument(
            "--tools",
            default="all",
            help="cursor,claude,codex,... 或 all（全部原生适配器）或 legacy（cursor+claude+codex+grok+deepseek）",
        )
        sp.add_argument("--profile", default="full", choices=("minimal", "core", "full"))
        sp.add_argument("--isolate-root", help="探测根：所有家目录改落到此树下")
        sp.add_argument("--cursor-home", help="兼容旧开关；请改用 --isolate-root")
        sp.add_argument("--cursor-only", action="store_true", help="不建业务根")
        sp.add_argument(
            "--pack-root",
            help="pack 根（skills/agents/…）；默认 GSH_PACK_ROOT、git 检出、或 wheel 内 gsh/pack_data",
        )
        sp.add_argument("--yes", action="store_true", help="非交互，跳过确认")

    s = sub.add_parser("setup", help="引导或脚本化安装")
    add_common(s)
    s.add_argument("--write-mcp", action="store_true", help="仅当目标没有 mcp.json 时从示例创建占位文件")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--guided", action="store_true", help="交互选择工具与档位")

    sy = sub.add_parser("sync", help="从仓库根真相源重投影到已安装适配器")
    add_common(sy)
    sy.add_argument("--dry-run", action="store_true")

    v = sub.add_parser("verify", help="架构完整性、唯一 ID、职种不预展开、无密钥、投影一致")
    add_common(v)

    d = sub.add_parser("doctor", help="诊断漂移、缺文件、密钥痕迹、各工具原生能力")
    add_common(d)

    u = sub.add_parser("uninstall", help="按 install-state 撤掉 GSH 投影（不删用户 mcp.json）")
    add_common(u)
    u.add_argument("--dry-run", action="store_true")

    m = sub.add_parser("menu", help="导演菜单：按 id 检索职种/技能，不灌 catalog 全文")
    add_common(m)
    m.add_argument("--kind", default="all", choices=("all", "craft", "skill"))
    m.add_argument("-q", "--query", default="", help="检索词，例如 ttk / 经济 / qa")

    st = sub.add_parser("status", help="当前会话、职种进度、验证报告")
    add_common(st)
    st.add_argument("--session", help="会话短名；默认 LATEST")

    rs = sub.add_parser("resume", help="打印现行卡与下一手")
    add_common(rs)
    rs.add_argument("--session", help="会话短名；默认 LATEST")

    nx = sub.add_parser("next", help="把职种路径推到下一步并改写现行卡")
    add_common(nx)
    nx.add_argument("--session", help="会话短名；默认 LATEST")
    nx.add_argument("--craft", help="职种 id；默认名单里的第一条")

    cl = sub.add_parser("close", help="写出验证报告并登记关项")
    add_common(cl)
    cl.add_argument("--session", help="会话短名；默认 LATEST")
    cl.add_argument("--kind", default="smoke", help="smoke|schema|playtest|build|release")
    cl.add_argument("--evidence", default="", help="证据路径，逗号分隔")
    cl.add_argument("--command", default="python -m gsh close")
    cl.add_argument("--notes", default="")
    cl.add_argument("--verdict", default="pass", choices=("pass", "fail"))

    ac = sub.add_parser("activate", help="根据 loadplan 生成名单与现行卡")
    add_common(ac)
    ac.add_argument("session", help="会话短名")

    # 兼容旧入口：python -m gsh --workspace X  视为 setup
    return p


def _legacy_isolate(args: argparse.Namespace) -> Path | None:
    if getattr(args, "isolate_root", None):
        return Path(args.isolate_root)
    if getattr(args, "cursor_home", None):
        print("warning: --cursor-home is legacy; prefer --isolate-root", file=sys.stderr)
        return Path(args.cursor_home).parent / "_isolate_from_cursor_home"
    return None


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # 允许 `python -m gsh --workspace X` 无子命令，视为 setup
    if argv and not argv[0].startswith("-") and argv[0] not in {
        "setup",
        "sync",
        "verify",
        "doctor",
        "uninstall",
        "menu",
        "status",
        "resume",
        "next",
        "close",
        "activate",
    }:
        pass
    elif argv and (argv[0].startswith("-") or not argv):
        if "--version" in argv or "-h" in argv or "--help" in argv:
            return build_parser().parse_args(argv) or 0
        argv = ["setup", *argv]

    parser = build_parser()
    args = parser.parse_args(argv)
    isolate = _legacy_isolate(args)
    pack = Path(args.pack_root).resolve() if args.pack_root else None

    if args.cmd == "setup":
        return setup.run(
            workspace=Path(args.workspace) if args.workspace else None,
            tools_raw=args.tools,
            profile=args.profile,
            isolate=isolate,
            cursor_only=args.cursor_only,
            write_mcp=args.write_mcp,
            dry=args.dry_run,
            guided=args.guided,
            yes=args.yes,
            pack=pack,
        )
    if args.cmd == "sync":
        return sync.run(
            workspace=Path(args.workspace) if args.workspace else None,
            tools_raw=args.tools,
            profile=args.profile,
            isolate=isolate,
            cursor_only=args.cursor_only,
            dry=args.dry_run,
            pack=pack,
        )
    if args.cmd == "verify":
        return verify.run(
            workspace=Path(args.workspace) if args.workspace else None,
            tools_raw=args.tools,
            isolate=isolate,
            cursor_only=args.cursor_only,
            pack=pack,
        )
    if args.cmd == "doctor":
        return doctor.run(
            workspace=Path(args.workspace) if args.workspace else None,
            tools_raw=args.tools,
            isolate=isolate,
            pack=pack,
        )
    if args.cmd == "uninstall":
        return uninstall.run(isolate=isolate, dry=args.dry_run, yes=args.yes)
    if args.cmd == "menu":
        return studio.run_menu(kind=args.kind, query=args.query, pack=pack)
    if args.cmd == "status":
        return studio.run_status(
            workspace=Path(args.workspace) if args.workspace else None,
            session=args.session,
            pack=pack,
        )
    if args.cmd == "resume":
        return studio.run_resume(
            workspace=Path(args.workspace) if args.workspace else None,
            session=args.session,
            pack=pack,
        )
    if args.cmd == "next":
        return studio.run_next(
            workspace=Path(args.workspace) if args.workspace else None,
            session=args.session,
            craft=args.craft,
            pack=pack,
        )
    if args.cmd == "close":
        return studio.run_close(
            workspace=Path(args.workspace) if args.workspace else None,
            session=args.session,
            kind=args.kind,
            evidence=args.evidence,
            command=args.command,
            notes=args.notes,
            verdict=args.verdict,
            pack=pack,
        )
    if args.cmd == "activate":
        return studio.run_activate(
            workspace=Path(args.workspace) if args.workspace else None,
            session=args.session,
            pack=pack,
        )
    parser.error(f"unknown command {args.cmd}")
    return 2
