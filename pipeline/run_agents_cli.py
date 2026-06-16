"""Goi agent 01 -> 02 -> 03 qua Claude Code CLI (headless, dung goi thue bao
thay vi API key). Cung interface voi run_agents.py.

Yeu cau: da dang nhap `claude` mot lan tren may (credentials luu o ~/.claude).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .run_agents import AGENT_DIRS, load_system_prompt  # tai su dung

ROOT = Path(__file__).resolve().parents[1]

CLAUDE_EXE = os.environ.get(
    "CLAUDE_CLI", str(Path.home() / ".local" / "bin" / "claude.exe")
)
CLI_MODEL = os.environ.get("CLAUDE_CLI_MODEL", "sonnet")
TIMEOUT_S = 1500  # 25 phut/agent (web search co the cham)


def call_agent(system: str, user_message: str, web_search: bool = False) -> str:
    cmd = [
        CLAUDE_EXE,
        "-p",
        "--model", CLI_MODEL,
        "--system-prompt", system,
    ]
    if web_search:
        cmd += ["--allowedTools", "WebSearch,WebFetch", "--max-turns", "10"]

    r = subprocess.run(
        cmd,
        input=user_message,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT_S,
        cwd=str(ROOT),
    )
    if r.returncode != 0:
        raise RuntimeError(
            f"claude CLI loi (exit {r.returncode}): {(r.stderr or r.stdout)[:500]}"
        )
    return r.stdout.strip()


def run_pipeline_agents(market_data_md: str, report_date: str) -> dict[str, str]:
    reports: dict[str, str] = {}

    msg01 = (
        f"Ngay bao cao: {report_date} (du lieu phien gan nhat ben duoi).\n\n"
        f"{market_data_md}\n\n"
        "Cac truong con thieu o tren: hay tu thu thap qua web search tu nguon "
        "cong khai (bai tong ket phien CafeF/Vietstock, du lieu khoi ngoai...), "
        "ghi ro nguon va do tre. Truong nao khong tim duoc thi ap quy tac fallback. "
        "Chi tra ve noi dung bao cao markdown, khong them loi dan."
    )
    print("      agent 01 (regime, co web search)...")
    reports["01"] = call_agent(load_system_prompt("01"), msg01, web_search=True)

    msg02 = (
        f"Day la MARKET REGIME REPORT ngay {report_date} tu Market Regime Agent. "
        "Hay chon chien thuat theo dung quy trinh. Chi tra ve bao cao markdown.\n\n"
        + reports["01"]
    )
    print("      agent 02 (strategy)...")
    reports["02"] = call_agent(load_system_prompt("02"), msg02, web_search=False)

    msg03 = (
        f"Day la STRATEGY SELECTION REPORT ngay {report_date} tu Strategy Selector. "
        "Du lieu nganh chua duoc cung cap san — hay tu thu thap hieu suat/thanh khoan "
        "cac nhom nganh chinh (5 va 20 phien) qua web search, ghi ro nguon. "
        "Thieu truc Flow thi ap fallback (khong xep Strong). Chi tra ve bao cao markdown.\n\n"
        + reports["02"]
    )
    print("      agent 03 (sector, co web search)...")
    reports["03"] = call_agent(load_system_prompt("03"), msg03, web_search=True)

    return reports
