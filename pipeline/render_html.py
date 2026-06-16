"""Render 3 bao cao markdown thanh 1 trang HTML theo phong cach "Ban tin TTCK"
(Be Vietnam Pro, navy #122B4D, xanh #1E6FD9, nen #EDF0F5).

- docs/index.html          : bao cao moi nhat
- docs/archive/<date>.html : luu vinh vien tung ngay
"""

from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIVE = DOCS / "archive"

# ---------------------------------------------------------------- mapping ---

REGIME_LABELS = {
    "RISK_ON": ("Risk-on / Uptrend xác nhận", "#178A50"),
    "UPTREND_CAUTIOUS": ("Uptrend thận trọng", "#178A50"),
    "NEUTRAL": ("Neutral / Trung tính", "#B97A0F"),
    "SIDEWAY": ("Sideway / Đi ngang", "#B97A0F"),
    "DIVERGENT": ("Phân hóa", "#B97A0F"),
    "TECH_BOUNCE": ("Hồi kỹ thuật trong downtrend", "#B97A0F"),
    "BULL_TRAP_RISK": ("Rủi ro bull trap", "#D6453D"),
    "RISK_OFF": ("Risk-off", "#D6453D"),
    "DOWNTREND_ST": ("Downtrend ngắn hạn", "#D6453D"),
    "PANIC": ("Hoảng loạn", "#8C231D"),
}

STRATEGY_HEADLINES = {
    "WAIT": "Đứng ngoài — chờ xác nhận",
    "CASH": "Giữ tiền — bảo toàn vốn",
    "DERISK": "Hạ tỷ trọng, giảm margin",
    "T_PLUS": "Trading ngắn T+ chọn lọc",
    "SIDEWAY_SWING": "Swing trong biên sideway",
    "PULLBACK_BUY": "Mua pullback trong uptrend",
    "BREAKOUT": "Đánh breakout có điều kiện",
    "TREND_FOLLOW": "Đi theo xu hướng",
    "SECTOR_ROTATION": "Xoay vòng nhóm ngành",
    "MEAN_REVERSION": "Đánh hồi kỹ thuật — rủi ro cao",
    "EVENT_DRIVEN": "Giao dịch theo sự kiện",
}

MARGIN_LABELS = {
    "allowed": ("Được phép", "#178A50"),
    "restricted": ("Hạn chế", "#B97A0F"),
    "forbidden": ("Cấm", "#D6453D"),
}

SECTIONS = [
    ("01", "§ 01", "Market Regime — Thị trường đang chơi theo luật nào?",
     "Scorecard 6 trụ cột · quy tắc hạ nhanh nâng chậm · output của Market Regime Agent"),
    ("02", "§ 02", "Chiến thuật — Hôm nay đánh kiểu gì hay đứng ngoài?",
     "Ma trận regime → playbook · điều kiện kích hoạt và vô hiệu đo được · Strategy Selector Agent"),
    ("03", "§ 03", "Dòng tiền ngành — Tiền đang ở đâu, cấm đuổi nhóm nào?",
     "Ma trận RS × Flow · Strong / Improving / Weak / Avoid Chasing · Sector Rotation Agent"),
]

WEEKDAYS = ["THỨ HAI", "THỨ BA", "THỨ TƯ", "THỨ NĂM", "THỨ SÁU", "THỨ BẢY", "CHỦ NHẬT"]

# --------------------------------------------------------------- template ---

PAGE_TMPL = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Báo cáo chiến lược @@DATE_DOT@@ — Mini Investment Desk</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Be Vietnam Pro',system-ui,sans-serif;background:#EDF0F5;color:#122B4D;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:#1E6FD9;text-decoration:none}a:hover{text-decoration:underline}
.khung{max-width:1100px;margin:0 auto;padding:0 20px}
.topbar{background:#fff;border-bottom:3px solid #122B4D}
.topbar .khung{display:flex;justify-content:space-between;align-items:center;padding-top:14px;padding-bottom:14px;gap:12px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px}
.brand .logo{width:30px;height:30px;border-radius:50%;background:#122B4D;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px}
.brand .ten{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.brand .phu{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#1E6FD9;font-weight:600}
.tieude-bar{font-size:18px;font-weight:800;color:#122B4D}
.meta-bar{text-align:right;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#5B6B80;font-weight:600;line-height:1.8}
.meta-bar b{color:#122B4D}
.hero{background:#fff;border-bottom:1px solid #DDE3EC}
.hero .khung{display:grid;grid-template-columns:minmax(220px,1fr) 2fr;gap:32px;padding-top:34px;padding-bottom:34px}
.badge-ngay{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#1E6FD9;border:1.5px solid #1E6FD9;padding:5px 12px;border-radius:4px;margin-bottom:14px}
.hero h1{font-size:44px;line-height:1.1;font-weight:800;color:#122B4D;letter-spacing:-.01em}
.hero .diem-nhan{font-size:21px;font-weight:700;line-height:1.4;margin-bottom:10px}
.hero .diem-nhan .xanh{color:#1E6FD9}
.hero .dande{font-size:14.5px;color:#44546A;font-style:italic}
.metrics{background:#fff;padding:6px 0 26px}
.metrics .khung{display:grid;grid-template-columns:repeat(auto-fit,minmax(152px,1fr));gap:14px}
.mcard{border:1px solid #DDE3EC;border-radius:8px;padding:14px 16px;background:#fff}
.mcard .nhan{font-size:10px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:#5B6B80;margin-bottom:6px}
.mcard .so{font-size:23px;font-weight:800;color:#122B4D;letter-spacing:-.01em;line-height:1.15}
.mcard .phu{font-size:13px;font-weight:700;margin-top:3px}
.mcard .chu{margin-top:9px;font-size:11px;color:#5B6B80;border-left:3px solid #DDE3EC;padding:2px 0 2px 9px;font-style:italic;line-height:1.45}
.canhbao{padding:18px 0 0}
.canhbao .hop{background:#FDF6E3;border:1px solid #E8D9A8;border-radius:8px;padding:12px 18px;font-size:12.5px;color:#7A4E05;font-style:italic}
.noidung{padding:26px 0 8px}
.sec{background:#fff;border:1px solid #DDE3EC;border-radius:10px;padding:22px 26px;margin-bottom:18px}
.sec .dau{display:flex;align-items:baseline;gap:10px;margin-bottom:4px}
.sec .so-sec{font-size:13px;font-weight:800;color:#1E6FD9;letter-spacing:.06em}
.sec h2{font-size:19px;font-weight:800;color:#122B4D}
.sec .ghichu-sec{font-size:11px;color:#8593A6;font-style:italic;margin-bottom:12px}
.report-md{font-size:13.5px;color:#2C3E55}
.report-md h1{display:none}
.report-md h2{font-size:14px;font-weight:800;color:#122B4D;letter-spacing:.02em;text-transform:uppercase;margin:20px 0 8px;padding-bottom:5px;border-bottom:2px solid #E4E9F0}
.report-md h3{font-size:13px;font-weight:800;color:#1E6FD9;margin:14px 0 6px}
.report-md p{margin:7px 0}
.report-md ul{list-style:none;margin:4px 0}
.report-md li{padding:7px 0 7px 18px;border-bottom:1px dashed #E4E9F0;position:relative}
.report-md li:last-child{border-bottom:none}
.report-md li::before{content:"";position:absolute;left:2px;top:14px;width:7px;height:7px;border-radius:50%;background:#1E6FD9}
.report-md table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}
.report-md th{background:#F2F5FA;color:#122B4D;font-weight:800;text-align:left;padding:8px 10px;border-bottom:2px solid #122B4D;font-size:12px;letter-spacing:.03em}
.report-md td{padding:8px 10px;border-bottom:1px dashed #E4E9F0;vertical-align:top;color:#2C3E55}
.report-md tr:last-child td{border-bottom:none}
.report-md strong{color:#122B4D}
.report-md code{background:#F2F5FA;padding:1px 6px;border-radius:4px;font-size:12px}
.quote{padding:10px 0 26px}
.quote .hop{background:#E7F0FC;border-radius:10px;padding:26px 32px;display:flex;gap:18px;align-items:flex-start}
.quote .dau-nhay{font-size:52px;font-weight:800;color:#1E6FD9;line-height:.8;font-family:Georgia,serif}
.dg-tieude{font-size:11px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#1E6FD9;margin-bottom:7px}
.quote p{font-size:16.5px;font-style:italic;font-weight:500;color:#0F4187;line-height:1.65}
.quote .ai{margin-top:8px;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:#1E6FD9;font-style:normal}
.luutru{padding:0 0 26px}
.luutru .hop{background:#fff;border:1px solid #DDE3EC;border-radius:10px;padding:18px 26px}
.luutru .tieu{font-size:11px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#5B6B80;margin-bottom:8px}
.luutru .links{font-size:13px;line-height:2}
.chantrang{background:#122B4D;color:#fff;margin-top:14px}
.chantrang .khung{padding-top:22px;padding-bottom:22px}
.chantrang .hang{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}
.chantrang .brand-ft{font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:13px}
.chantrang .mota-ft{font-size:11px;color:#9FB2CC;font-style:italic}
.chantrang .nguon{margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,.15);font-size:11px;color:#9FB2CC;line-height:2}
@media(max-width:760px){.hero .khung{grid-template-columns:1fr;gap:18px}.hero h1{font-size:32px}.tieude-bar{display:none}}
</style>
</head>
<body>

<header class="topbar"><div class="khung">
  <div class="brand"><div class="logo">MD</div><div><div class="ten">Mini Investment Desk</div><div class="phu">Daily strategy desk · LPBS</div></div></div>
  <div class="tieude-bar">— Báo cáo chiến lược đầu ngày —</div>
  <div class="meta-bar"><b>@@WEEKDAY@@ · @@DATE_DOT@@</b><br>Pipeline 01→03 tự động trước giờ giao dịch</div>
</div></header>

<div class="hero"><div class="khung">
  <div><span class="badge-ngay">Dữ liệu phiên · @@DATE_DOT@@</span><h1>@@HEADLINE@@</h1></div>
  <div>
    <div class="diem-nhan">@@VNI_LINE@@ — <span class="xanh">@@REGIME_LINE@@</span></div>
    <p class="dande">@@LEAD@@</p>
  </div>
</div></div>

<div class="metrics"><div class="khung">@@METRIC_CARDS@@</div></div>

<div class="canhbao"><div class="khung"><div class="hop"><strong>Lưu ý:</strong> Báo cáo do hệ thống AI tạo tự động để hỗ trợ broker nội bộ, chỉ có giá trị trong ngày, không phải khuyến nghị đầu tư cho khách hàng cuối và không cam kết lợi nhuận. Mọi tư vấn cho khách phải qua đánh giá của broker.</div></div></div>

<main class="noidung"><div class="khung">@@SECTIONS@@</div></main>

<div class="quote"><div class="khung"><div class="hop"><div class="dau-nhay">"</div><div><div class="dg-tieude">Cảnh báo cho broker hôm nay</div><p>@@BROKER_QUOTE@@</p><div class="ai">— Strategy Selector Agent · @@DATE_DOT@@ · điều khách dễ hiểu sai nhất hôm nay</div></div></div></div></div>

<div class="luutru"><div class="khung"><div class="hop"><div class="tieu">📁 Báo cáo các ngày trước</div><div class="links">@@ARCHIVE_LINKS@@</div></div></div></div>

<footer class="chantrang"><div class="khung">
  <div class="hang"><span class="brand-ft">Mini Investment Desk Agent System</span><span class="mota-ft">Pipeline 5 agent: Regime → Strategy → Sector → Watchlist → Risk · 01–03 chạy tự động mỗi sáng, 04–05 chạy theo yêu cầu trưởng phòng</span></div>
  <div class="nguon">Dữ liệu giá: vnstock (VCI) · Breadth, khối ngoại, vĩ mô, tin tức: agent tự thu thập qua web search có ghi nguồn trong từng báo cáo · Model: Claude (Anthropic) · Báo cáo không nêu khuyến nghị mã cụ thể — watchlist (agent 04) và risk review (agent 05) chỉ chạy nội bộ khi có người duyệt.</div>
</div></footer>
</body>
</html>
"""

# ----------------------------------------------------------------- helpers --

def _extract(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None


def _extract_section(heading_regex: str, text: str) -> str | None:
    """Lay noi dung 1 muc '## heading' (den heading tiep theo)."""
    m = re.search(rf"##\s*{heading_regex}\s*\n(.*?)(?=\n##\s|\Z)", text, re.S)
    if not m:
        return None
    body = m.group(1).strip()
    bullets = [re.sub(r"^[-*]\s*", "", ln).strip() for ln in body.splitlines() if ln.strip()]
    joined = " · ".join(b.rstrip(".") for b in bullets if b)
    return " ".join(joined.split())


def _field(label: str, text: str, value_re: str = r"[^\n|\]]+") -> str | None:
    """Bat 1 truong Handoff du o dang 'Key: value', '| Key | value |',
    '**Key:** value' hay 'Key | value'. label la regex cho ten truong."""
    # tach bo ** va [ ] o value
    pat = (
        rf"{label}\s*\**\s*[:|]\s*\**\s*\[?\s*({value_re})"
    )
    m = re.search(pat, text, re.I)
    if not m:
        return None
    return m.group(1).strip().strip("*[]").strip()


def _code(label: str, text: str) -> str | None:
    v = _field(label, text, r"[A-Za-z][A-Za-z0-9_ /]+")
    if not v:
        return None
    # chuan hoa: vd "RISK OFF" -> "RISK_OFF", lay token dau neu co ' — '
    v = v.split("—")[0].split("(")[0].strip()
    return v.upper().replace(" ", "_").replace("-", "_").rstrip("_")


def _md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def _mcard(label: str, value: str, sub: str = "", sub_color: str = "#5B6B80", note: str = "") -> str:
    sub_html = f'<div class="phu" style="color:{sub_color}">{sub}</div>' if sub else ""
    note_html = f'<div class="chu">{note}</div>' if note else ""
    return (
        f'<div class="mcard"><div class="nhan">{label}</div>'
        f'<div class="so">{value}</div>{sub_html}{note_html}</div>'
    )


def _fmt_vn(x: float) -> str:
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------------------------------------------------------ render --

def render(reports: dict[str, str], report_date: str, snapshot: dict | None = None) -> Path:
    DOCS.mkdir(exist_ok=True)
    ARCHIVE.mkdir(exist_ok=True)

    r01, r02 = reports.get("01", ""), reports.get("02", "")

    regime = _code(r"Regime code", r01) or _code(r"Regime code", r02) or "?"
    sub_state = _code(r"Trạng thái phụ", r01)
    confidence = (
        _field(r"Mức độ tự tin", r01, r"Thấp|Trung bình|Cao")
        or _field(r"Confidence", r01, r"Thấp|Trung bình|Cao|THẤP|TRUNG BÌNH|CAO")
        or _field(r"Confidence", r02, r"Thấp|Trung bình|Cao|THẤP|TRUNG BÌNH|CAO")
    )
    if confidence:
        confidence = confidence.capitalize() if confidence.isupper() else confidence
    exposure = (
        _field(r"Exposure (?:band|ceiling)", r02)
        or _field(r"Exposure (?:band|ceiling)", r01)
        or _field(r"Tỷ trọng tham khảo", r02)
    )
    margin = _field(r"Margin", r02, r"allowed|restricted|forbidden") or _field(
        r"Margin", r01, r"allowed|restricted|forbidden"
    )
    margin = margin.lower() if margin else None
    # strategy: uu tien dong "Strategy code", roi "Chiến thuật chính được chọn",
    # cuoi cung heading "### XXX —" dau tien trong muc chien thuat chinh
    strategy = (
        _code(r"Strategy code", r02)
        or _code(r"Chiến thuật chính được chọn", r02)
        or _extract(r"###\s+([A-Z_]{3,})\b", r02)
        or "?"
    )
    secondary = _code(r"Secondary code", r02)
    if secondary in ("NONE", "KHÔNG", "KHONG"):
        secondary = None

    regime_label, regime_color = REGIME_LABELS.get(regime, (regime, "#5B6B80"))
    headline = STRATEGY_HEADLINES.get(strategy, "Báo cáo chiến lược đầu ngày")

    # hero
    if snapshot:
        v = snapshot["vnindex"]
        chg = v["change_pct"]
        vni_line = f"VN-Index {_fmt_vn(v['close'])} ({'+' if chg >= 0 else ''}{str(chg).replace('.', ',')}%)"
    else:
        vni_line = "VN-Index"
    regime_line = regime_label + (f" · cảnh báo {REGIME_LABELS.get(sub_state, (sub_state, ''))[0].lower()}" if sub_state and sub_state != regime else "")

    lead = _extract_section(r"Vì sao chọn chiến thuật này", r02) or _extract_section(r"Kết luận", r01) or ""
    lead = (lead[:420] + "…") if len(lead) > 420 else lead

    # metric cards
    cards = []
    if snapshot:
        v = snapshot["vnindex"]
        chg = v["change_pct"]
        cards.append(_mcard(
            "VN-Index", _fmt_vn(v["close"]),
            f"{'▲' if chg >= 0 else '▼'} {'+' if chg >= 0 else ''}{str(chg).replace('.', ',')}%",
            "#178A50" if chg >= 0 else "#D6453D",
            f"5 phiên {str(v['perf_5d_pct']).replace('.', ',')}% · 20 phiên {str(v['perf_20d_pct']).replace('.', ',')}%",
        ))
        liq = snapshot["liquidity"]
        pct = liq["volume_vs_avg20_pct"]
        cards.append(_mcard(
            "Thanh khoản", f"{str(pct).replace('.', ',')}%",
            "so trung bình 20 phiên", "#D6453D" if pct < 80 else ("#B97A0F" if pct < 100 else "#178A50"),
            "khối lượng tổng (proxy)",
        ))
    cards.append(_mcard("Regime", regime.replace("_", " "), regime_label, regime_color,
                        f"trạng thái phụ: {sub_state}" if sub_state else ""))
    cards.append(_mcard("Chiến thuật", strategy.replace("_", " "), headline, "#1E6FD9",
                        f"phụ: {secondary}" if secondary and secondary != "NONE" else ""))
    if margin:
        m_label, m_color = MARGIN_LABELS[margin]
        cards.append(_mcard("Margin", m_label, margin, m_color, ""))
    if exposure:
        cards.append(_mcard("Tỷ trọng tham khảo", exposure, f"confidence: {confidence}" if confidence else "", "#5B6B80", ""))

    # sections
    secs = []
    for key, num, title, note in SECTIONS:
        if key not in reports:
            continue
        secs.append(
            f'<section class="sec"><div class="dau"><span class="so-sec">{num}</span>'
            f"<h2>{title}</h2></div>"
            f'<div class="ghichu-sec">{note}</div>'
            f'<div class="report-md">{_md(reports[key])}</div></section>'
        )

    broker_quote = (
        _extract_section(r"Cảnh báo cho broker", r02)
        or _extract_section(r"Cảnh báo cho broker", r01)
        or "Chưa trích xuất được cảnh báo — đọc trực tiếp mục Cảnh báo trong báo cáo chiến thuật."
    )

    # archive links
    archived = sorted(ARCHIVE.glob("*.html"), reverse=True)
    links = " · ".join(f'<a href="archive/{p.name}">{p.stem}</a>' for p in archived[:40]) or "Chưa có"

    d = report_date.split("-")  # YYYY-MM-DD
    date_dot = f"{d[2]}.{d[1]}.{d[0]}"
    import datetime as _dt

    weekday = WEEKDAYS[_dt.date(int(d[0]), int(d[1]), int(d[2])).weekday()]

    html = (
        PAGE_TMPL
        .replace("@@DATE_DOT@@", date_dot)
        .replace("@@WEEKDAY@@", weekday)
        .replace("@@HEADLINE@@", headline)
        .replace("@@VNI_LINE@@", vni_line)
        .replace("@@REGIME_LINE@@", regime_line)
        .replace("@@LEAD@@", lead)
        .replace("@@METRIC_CARDS@@", "".join(cards))
        .replace("@@SECTIONS@@", "\n".join(secs))
        .replace("@@BROKER_QUOTE@@", broker_quote)
        .replace("@@ARCHIVE_LINKS@@", links)
    )

    (ARCHIVE / f"{report_date}.html").write_text(
        html.replace('href="archive/', 'href="'), encoding="utf-8"
    )
    out = DOCS / "index.html"
    out.write_text(html, encoding="utf-8")
    return out
