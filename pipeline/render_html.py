"""Render 3 bao cao markdown thanh 1 trang HTML dashboard.

- docs/index.html      : bao cao moi nhat
- docs/archive/<date>.html : luu vinh vien tung ngay
"""

from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIVE = DOCS / "archive"

REGIME_COLORS = {
    "RISK_ON": "#1a7f37",
    "UPTREND_CAUTIOUS": "#2da44e",
    "NEUTRAL": "#9a6700",
    "SIDEWAY": "#9a6700",
    "DIVERGENT": "#bf8700",
    "TECH_BOUNCE": "#bc4c00",
    "BULL_TRAP_RISK": "#cf222e",
    "RISK_OFF": "#cf222e",
    "DOWNTREND_ST": "#cf222e",
    "PANIC": "#82071e",
}

PAGE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daily Desk Report — {date}</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; background: #f6f8fa; color: #1f2328; line-height: 1.55; }}
  header {{ background: #0d1117; color: #fff; padding: 20px 24px; }}
  header h1 {{ margin: 0 0 6px; font-size: 1.35rem; }}
  header .meta {{ color: #9aa4b2; font-size: .9rem; }}
  .badges {{ margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; }}
  .badge {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-weight: 600; font-size: .85rem; color: #fff; }}
  main {{ max-width: 980px; margin: 0 auto; padding: 16px; }}
  details {{ background: #fff; border: 1px solid #d0d7de; border-radius: 8px; margin: 14px 0; overflow: hidden; }}
  details > summary {{ cursor: pointer; padding: 14px 18px; font-weight: 700; font-size: 1.02rem; background: #f0f3f6; list-style: none; }}
  details > summary::before {{ content: "▸ "; }}
  details[open] > summary::before {{ content: "▾ "; }}
  .report {{ padding: 6px 22px 18px; }}
  .report table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: .9rem; }}
  .report th, .report td {{ border: 1px solid #d0d7de; padding: 6px 9px; text-align: left; vertical-align: top; }}
  .report th {{ background: #f0f3f6; }}
  .report h1 {{ font-size: 1.2rem; }} .report h2 {{ font-size: 1.05rem; margin-top: 22px; }}
  .report code {{ background: #eff1f3; padding: 1px 5px; border-radius: 4px; }}
  .disclaimer {{ background: #fff8c5; border: 1px solid #d4a72c66; border-radius: 8px; padding: 12px 16px; font-size: .85rem; margin: 18px 0; }}
  .archive-list {{ font-size: .9rem; }}
  footer {{ text-align: center; color: #6e7781; font-size: .8rem; padding: 24px; }}
  @media (max-width: 600px) {{ .report {{ padding: 4px 10px 12px; }} }}
</style>
</head>
<body>
<header>
  <h1>📊 Mini Investment Desk — Báo cáo đầu ngày</h1>
  <div class="meta">Dữ liệu phiên {date} · tạo tự động lúc ~6h30 sáng hôm sau · LPBS internal</div>
  <div class="badges">{badges}</div>
</header>
<main>
  <div class="disclaimer"><strong>Lưu ý:</strong> Báo cáo do hệ thống AI tạo tự động để hỗ trợ broker nội bộ,
  chỉ có giá trị trong ngày, không phải khuyến nghị đầu tư cho khách hàng cuối và không cam kết lợi nhuận.
  Mọi tư vấn cho khách phải qua đánh giá của broker. Dữ liệu nguồn miễn phí, có thể có độ trễ/sai số.</div>
  {sections}
  {archive_block}
</main>
<footer>Mini Investment Desk Agent System v1 · pipeline 01→03 tự động · 04→05 chạy theo yêu cầu</footer>
</body>
</html>
"""

SECTION_TITLES = {
    "01": "1 · MARKET REGIME — Thị trường đang chơi theo luật nào?",
    "02": "2 · STRATEGY — Hôm nay đánh kiểu gì hay đứng ngoài?",
    "03": "3 · SECTOR — Tiền đang ở nhóm ngành nào?",
}


def _extract(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None


def _badges(reports: dict[str, str]) -> str:
    badges = []
    regime = _extract(r"Regime code:\*{0,2}\s*\[?([A-Z_]+)", reports.get("01", ""))
    if regime:
        color = REGIME_COLORS.get(regime, "#57606a")
        badges.append(f'<span class="badge" style="background:{color}">Regime: {regime}</span>')
    strat = _extract(r"Strategy code:\*{0,2}\s*\[?([A-Z_]+)", reports.get("02", ""))
    if strat:
        badges.append(f'<span class="badge" style="background:#0969da">Chiến thuật: {strat}</span>')
    margin = _extract(r"Margin:\*{0,2}\s*\[?(allowed|restricted|forbidden)", reports.get("02", "") or reports.get("01", ""))
    if margin:
        mcolor = {"allowed": "#1a7f37", "restricted": "#9a6700", "forbidden": "#cf222e"}[margin]
        badges.append(f'<span class="badge" style="background:{mcolor}">Margin: {margin}</span>')
    return "".join(badges) or '<span class="badge" style="background:#57606a">Chưa parse được handoff</span>'


def _md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def render(reports: dict[str, str], report_date: str) -> Path:
    DOCS.mkdir(exist_ok=True)
    ARCHIVE.mkdir(exist_ok=True)

    sections = []
    for key in ("01", "02", "03"):
        if key not in reports:
            continue
        is_open = " open" if key in ("01", "02") else ""
        sections.append(
            f"<details{is_open}><summary>{SECTION_TITLES[key]}</summary>"
            f'<div class="report">{_md(reports[key])}</div></details>'
        )

    # danh sach archive (toi da 30 ngay gan nhat)
    archived = sorted(ARCHIVE.glob("*.html"), reverse=True)[:30]
    links = " · ".join(f'<a href="archive/{p.name}">{p.stem}</a>' for p in archived)
    archive_block = (
        f'<details><summary>📁 Báo cáo các ngày trước</summary>'
        f'<div class="report archive-list">{links or "Chưa có"}</div></details>'
    )

    html = PAGE_TMPL.format(
        date=report_date,
        badges=_badges(reports),
        sections="\n".join(sections),
        archive_block=archive_block,
    )

    # archive page tro ve archive/<file> tu thu muc archive/ -> sua link tuong doi
    archive_html = html.replace('href="archive/', 'href="')
    (ARCHIVE / f"{report_date}.html").write_text(archive_html, encoding="utf-8")
    out = DOCS / "index.html"
    out.write_text(html, encoding="utf-8")
    return out
