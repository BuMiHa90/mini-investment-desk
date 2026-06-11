"""Entry point: python -m pipeline.run_pipeline [--mock]

Quy trinh: fetch du lieu -> agent 01 -> 02 -> 03 -> render HTML.
--mock: bo qua API (khong can ANTHROPIC_API_KEY), dung bao cao gia de test render.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

from . import fetch_data, render_html

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"

MOCK_REPORTS = {
    "01": (
        "# MARKET REGIME REPORT — {d}\n\n## Kết luận (MOCK)\n\n"
        "- Đây là báo cáo giả để test render.\n\n## Handoff cho Strategy Selector\n\n"
        "- **Regime code:** SIDEWAY\n- **Exposure band:** 30–50%\n- **Margin:** restricted\n"
    ),
    "02": (
        "# STRATEGY SELECTION REPORT — {d}\n\n## Chiến thuật chính hôm nay (MOCK)\n\n"
        "- SIDEWAY_SWING\n\n## Handoff\n\n- **Strategy code:** SIDEWAY_SWING\n"
        "- **Margin:** restricted\n"
    ),
    "03": (
        "# SECTOR ROTATION REPORT — {d}\n\n## Sector Map (MOCK)\n\n"
        "| Ngành | RS | Flow | Ghi chú |\n|---|---|---|---|\n| Bán lẻ | RS+ | Flow+ | mock |\n"
    ),
}


def main() -> int:
    mock = "--mock" in sys.argv

    print("[1/4] Lay du lieu thi truong (vnstock)...")
    try:
        snapshot, market_md = fetch_data.fetch()
        report_date = snapshot["data_date"]
        print(f"      OK — phien {report_date}, VN-Index {snapshot['vnindex']['close']}")
    except Exception:
        traceback.print_exc()
        print("      LOI lay du lieu — pipeline van chay, agent se tu web-search va ha confidence.")
        from datetime import date

        report_date = date.today().isoformat()
        market_md = (
            "KHONG LAY DUOC du lieu tu vnstock trong lan chay nay. "
            "Hay tu thu thap toan bo du lieu phien gan nhat qua web search, "
            "ghi ro nguon; neu khong du truong bat buoc thi ap fallback va ha confidence."
        )

    print("[2/4] Chay agent 01 -> 02 -> 03...")
    if mock:
        reports = {k: v.format(d=report_date) for k, v in MOCK_REPORTS.items()}
        print("      (mock mode — khong goi API)")
    else:
        from . import run_agents

        reports = run_agents.run_pipeline_agents(market_md, report_date)

    print("[3/4] Luu bao cao markdown...")
    day_dir = REPORTS_DIR / report_date
    day_dir.mkdir(parents=True, exist_ok=True)
    for key, text in reports.items():
        (day_dir / f"{key}.md").write_text(text, encoding="utf-8")

    print("[4/4] Render HTML...")
    out = render_html.render(reports, report_date)
    print(f"      Xong: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
