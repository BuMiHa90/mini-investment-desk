"""Goi agent 01 -> 02 -> 03 qua Claude Code CLI (headless, dung goi thue bao
thay vi API key). Cung interface voi run_agents.py.

Yeu cau: da dang nhap `claude` mot lan tren may (credentials luu o ~/.claude).

Agent 01: KHONG can web search nua cho breadth / khoi ngoai / index
contribution / basis phai sinh — 4 truong nay duoc fetch_data.py tu fetch
truc tiep tu 4 API cong khai (xem agent_desk_missing_fields.md), co cache
theo report_date (data/cache/<date>_extra.json) de lan chay buoi toi tai su
dung ket qua da fetch buoi chieu, khong fetch lai. Chi con 3 truong thuc su
chua co nguon API on dinh (ceiling_floor_count, matched_value_hose,
global/fx/policy/sentiment) + truong nao fetch loi lan nay van nam trong
missing_fields va agent ap fallback nhu cu.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

from .run_agents import AGENT_DIRS, DESK_META_INSTRUCTION, load_system_prompt  # tai su dung

ROOT = Path(__file__).resolve().parents[1]

CLAUDE_EXE = os.environ.get(
    "CLAUDE_CLI", str(Path.home() / ".local" / "bin" / "claude.exe")
)
CLI_MODEL = os.environ.get("CLAUDE_CLI_MODEL", "sonnet")
TIMEOUT_S = 1500  # 25 phut/agent (web search co the cham)

# Mot lan dung session limit thi cho toi gio reset roi thu lai. Toi le tinh
# tu gio cao diem (toi) hay dung mat vai phut. Chi tu cho neu reset gan, de
# task khong vuot ExecutionTimeLimit.
SESSION_LIMIT_MAX_WAIT_S = 20 * 60  # cho toi da 20 phut toi gio reset
SESSION_LIMIT_RETRIES = 2


def _seconds_until_reset(msg: str) -> int | None:
    """Tu thong bao 'resets 8:40pm (Asia/Saigon)' suy ra so giay can cho.
    Tra None neu khong parse duoc."""
    m = re.search(r"resets?\s+(\d{1,2})(?::(\d{2}))?\s*([ap]m)", msg, re.I)
    if not m:
        return None
    hh = int(m.group(1)) % 12
    if m.group(3).lower() == "pm":
        hh += 12
    mm = int(m.group(2) or 0)
    now = datetime.now()
    target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)  # gio reset da qua trong ngay -> ngay mai
    return int((target - now).total_seconds())


def _is_session_limit(text: str) -> bool:
    return "session limit" in text.lower() or "hit your session" in text.lower()


def call_agent(system: str, user_message: str, web_search: bool = False) -> str:
    cmd = [
        CLAUDE_EXE,
        "-p",
        "--model", CLI_MODEL,
        "--system-prompt", system,
    ]
    if web_search:
        cmd += ["--allowedTools", "WebSearch,WebFetch", "--max-turns", "10"]

    for attempt in range(SESSION_LIMIT_RETRIES + 1):
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
        if r.returncode == 0:
            return r.stdout.strip()

        err = (r.stderr or r.stdout) or ""
        # Neu dung session limit va con luot thu: cho toi gio reset roi thu lai
        if _is_session_limit(err) and attempt < SESSION_LIMIT_RETRIES:
            wait = _seconds_until_reset(err)
            if wait is not None and 0 < wait <= SESSION_LIMIT_MAX_WAIT_S:
                print(
                    f"      [session limit] cho {wait + 30}s toi gio reset roi thu lai "
                    f"(lan {attempt + 1}/{SESSION_LIMIT_RETRIES})..."
                )
                time.sleep(wait + 30)  # buffer 30s sau gio reset
                continue
        raise RuntimeError(
            f"claude CLI loi (exit {r.returncode}): {err[:500]}"
        )

    raise RuntimeError("claude CLI: het luot thu lai sau session limit")


def run_pipeline_agents(market_data_md: str, report_date: str) -> dict[str, str]:
    reports: dict[str, str] = {}

    msg01 = (
        f"Ngay bao cao: {report_date} (du lieu phien gan nhat ben duoi, da gom san "
        "breadth / khoi ngoai / index contribution / basis phai sinh tu API tu dong).\n\n"
        f"{market_data_md}\n\n"
        "Cac truong con lai trong missing_fields o tren: KHONG can web search de bo "
        "sung (chua co nguon API thay the on dinh hoac vua fetch loi lan nay). Ghi ro "
        "trong bao cao la 'Chua co du lieu - cho nguon thay the, se duoc bo sung sau' "
        "va ap dung quy tac fallback nhu khi khong tim duoc. KHONG xoa missing_fields "
        "khoi du lieu dau vao — con nguoi se tim nguon va bo sung lai sau. Chi tra ve "
        "noi dung bao cao markdown, khong them loi dan."
    )
    print("      agent 01 (regime, breadth/khoi ngoai/phai sinh da co san tu API)...")
    reports["01"] = call_agent(load_system_prompt("01"), msg01, web_search=False)

    msg02 = (
        f"Day la MARKET REGIME REPORT ngay {report_date} tu Market Regime Agent. "
        "Hay chon chien thuat theo dung quy trinh. Chi tra ve bao cao markdown.\n\n"
        + reports["01"]
        + "\n\n"
        + DESK_META_INSTRUCTION
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
