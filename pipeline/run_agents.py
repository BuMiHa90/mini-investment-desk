"""Goi lan luot agent 01 -> 02 -> 03 qua Claude API.

- System prompt cua moi agent lay tu PROMPT.md trong thu muc agent tuong ung
  (phan sau dau '---' dau tien).
- Agent 03 duoc bat server-side web search de tu bo sung du lieu nganh.
- Agent 01: KHONG can web search nua cho breadth / khoi ngoai / index
  contribution / basis phai sinh — 4 truong nay duoc fetch_data.py tu fetch
  truc tiep tu 4 API cong khai (xem agent_desk_missing_fields.md) va dua san
  vao market_data_md. Chi con 3 truong thuc su chua co nguon API on dinh
  (ceiling_floor_count, matched_value_hose, global/fx/policy/sentiment) +
  truong nao fetch loi trong lan chay nay van nam trong missing_fields va
  agent ap fallback nhu cu — KHONG bat web_search cho agent 01 vi se lam
  cham pipeline ma khong giai quyet duoc 3 truong con thieu nay.
- Output cua agent truoc duoc dua nguyen van lam message cho agent sau
  (cac agent duoc thiet ke de doc khoi Handoff trong bao cao).
"""

from __future__ import annotations

import os
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parents[1]

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 16000
MAX_CONTINUATIONS = 6  # gioi han vong lap pause_turn cua server-side web search

AGENT_DIRS = {
    "01": "01_Market_Regime_Agent",
    "02": "02_Strategy_Selector_Agent",
    "03": "03_Sector_Rotation_Agent",
}


def load_system_prompt(agent_key: str) -> str:
    text = (ROOT / AGENT_DIRS[agent_key] / "PROMPT.md").read_text(encoding="utf-8")
    # PROMPT.md = phan huong dan + '---' + system prompt that
    _, _, body = text.partition("\n---\n")
    return body.strip() if body.strip() else text


def call_agent(system: str, user_message: str, web_search: bool = False) -> str:
    client = anthropic.Anthropic()
    kwargs = {}
    if web_search:
        kwargs["tools"] = [
            {"type": "web_search_20260209", "name": "web_search", "max_uses": 8}
        ]

    messages = [{"role": "user", "content": user_message}]
    response = None
    for _ in range(MAX_CONTINUATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            thinking={"type": "adaptive"},
            messages=messages,
            **kwargs,
        )
        if response.stop_reason == "pause_turn":
            # server-side tool dang chay do dang — gui lai de tiep tuc
            messages = messages + [{"role": "assistant", "content": response.content}]
            continue
        break

    return "".join(b.text for b in response.content if b.type == "text").strip()


def run_pipeline_agents(market_data_md: str, report_date: str) -> dict[str, str]:
    """Tra ve dict {'01': report_md, '02': ..., '03': ...}."""
    reports: dict[str, str] = {}

    msg01 = (
        f"Ngay bao cao: {report_date} (du lieu phien gan nhat ben duoi, da gom san "
        "breadth / khoi ngoai / index contribution / basis phai sinh tu API tu dong).\n\n"
        f"{market_data_md}\n\n"
        "Cac truong con lai trong missing_fields o tren: KHONG can web search de bo "
        "sung (chua co nguon API thay the on dinh hoac vua fetch loi lan nay). Ghi ro "
        "trong bao cao la 'Chua co du lieu - cho nguon thay the, se duoc bo sung sau' "
        "va ap dung quy tac fallback nhu khi khong tim duoc. KHONG xoa missing_fields "
        "khoi du lieu dau vao — con nguoi se tim nguon va bo sung lai sau."
    )
    reports["01"] = call_agent(load_system_prompt("01"), msg01, web_search=False)

    msg02 = (
        f"Day la MARKET REGIME REPORT ngay {report_date} tu Market Regime Agent. "
        "Hay chon chien thuat theo dung quy trinh.\n\n" + reports["01"]
    )
    reports["02"] = call_agent(load_system_prompt("02"), msg02, web_search=False)

    msg03 = (
        f"Day la STRATEGY SELECTION REPORT ngay {report_date} tu Strategy Selector. "
        "Du lieu nganh chua duoc cung cap san — hay tu thu thap hieu suat/thanh khoan "
        "cac nhom nganh chinh (5 va 20 phien) qua web search, ghi ro nguon. "
        "Thieu truc Flow thi ap fallback (khong xep Strong).\n\n" + reports["02"]
    )
    reports["03"] = call_agent(load_system_prompt("03"), msg03, web_search=True)

    return reports
