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
<title>@@OG_TITLE@@</title>
<meta name="description" content="@@OG_DESC@@">
<!-- Open Graph: thuoc tinh xem truoc khi chia se len Zalo/Facebook/chat -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Mini Investment Desk · LPBS">
<meta property="og:title" content="@@OG_TITLE@@">
<meta property="og:description" content="@@OG_DESC@@">
<meta property="og:url" content="https://bumiha90.github.io/mini-investment-desk/">
<meta property="og:locale" content="vi_VN">
<meta property="article:published_time" content="@@OG_DATE_ISO@@">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="@@OG_TITLE@@">
<meta name="twitter:description" content="@@OG_DESC@@">
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

@@BROKER_BLOCK@@

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
    """Lay noi dung 1 muc '## heading' (den heading cung cap hoac cao hon).

    Cho phep tien to danh so truoc ten muc (vd '## VII. TÓM TẮT...', '## 2. ...',
    emoji) — agent thuong danh so La Ma / so / emoji nen phai bo qua.
    """
    # tien to: so La Ma, so Arab, dau cham, emoji, khoang trang — truoc heading text
    prefix = r"(?:[IVXLCDM0-9]+[.)]\s*|[^\w\s#]+\s*)*"
    m = re.search(
        rf"^#{{2,4}}\s*{prefix}{heading_regex}[^\n]*\n(.*?)(?=^#{{1,4}}\s|\Z)",
        text,
        re.S | re.M,
    )
    if not m:
        return None
    body = m.group(1).strip()
    # bo dong bang markdown (| ... |) va dong gach ngang
    lines = []
    for ln in body.splitlines():
        s = ln.strip()
        if not s or set(s) <= set("-|: "):
            continue
        s = re.sub(r"^[-*>]\s*", "", s)  # bullet
        s = s.replace("**", "").replace("*", "").replace("`", "")  # bo markdown
        s = re.sub(r"^#+\s*", "", s)  # sot dau heading
        lines.append(s.rstrip("."))
    joined = " · ".join(lines)
    return " ".join(joined.split()) or None


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


def _desk_meta(text: str) -> dict:
    """Doc khoi <!--DESK_META ... --> (key: value moi dong) neu agent co xuat.
    Day la nguon dang tin cay nhat — khong phu thuoc cach trinh bay than bao cao."""
    m = re.search(r"<!--\s*DESK_META\s*(.*?)-->", text, re.S | re.I)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            v = v.strip().strip("[]").strip()
            if v and v.lower() not in ("none", "n/a", "-"):
                out[k.strip().lower()] = v
    return out


_MARGIN_VN = [
    (r"forbidden|cấm|không sử dụng|không dùng|không margin|no margin", "forbidden"),
    (r"restricted|hạn chế|thận trọng", "restricted"),
    (r"allowed|được phép|cho phép", "allowed"),
]


def _norm_margin(raw: str | None) -> str | None:
    if not raw:
        return None
    low = raw.lower()
    for pat, val in _MARGIN_VN:
        if re.search(pat, low):
            return val
    return None


def _md(text: str) -> str:
    # an khoi DESK_META khoi noi dung hien thi (no la HTML comment nen browser
    # da an, nhung loai bo cho sach)
    text = re.sub(r"<!--\s*DESK_META.*?-->", "", text, flags=re.S | re.I)
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
    meta = {**_desk_meta(r01), **_desk_meta(r02)}  # 02 ghi de 01 neu trung khoa

    def pick(key, *fallbacks):
        if meta.get(key):
            return meta[key]
        for fb in fallbacks:
            if fb:
                return fb
        return None

    regime = (
        pick("regime", _code(r"Regime code", r01), _code(r"Regime code", r02)) or "?"
    ).upper().replace(" ", "_")
    sub_state_raw = pick("sub_state", _code(r"Trạng thái phụ", r01))
    sub_state = sub_state_raw.upper().replace(" ", "_") if sub_state_raw else None

    confidence = pick(
        "confidence",
        _field(r"Mức độ tự tin", r01, r"Thấp|Trung bình|Cao|THẤP|TRUNG BÌNH|CAO"),
        _field(r"Confidence", r02, r"Thấp|Trung bình|Cao|THẤP|TRUNG BÌNH|CAO"),
    )
    if confidence:
        confidence = confidence.capitalize() if confidence.isupper() else confidence

    exposure = pick(
        "exposure",
        _field(r"Exposure (?:band|ceiling)", r02),
        _field(r"Exposure (?:band|ceiling)", r01),
        _field(r"Exposure Band", r02),
        _field(r"Tỷ trọng tham khảo", r02),
    )

    margin = _norm_margin(
        pick(
            "margin",
            _field(r"Margin(?:\s*Status)?", r02),
            _field(r"Margin(?:\s*Status)?", r01),
        )
    )

    strategy = (
        pick(
            "strategy",
            _code(r"Strategy code", r02),
            _code(r"Chiến thuật chính được chọn", r02),
            _extract(r"CHIẾN THUẬT CHÍNH[:\s]*\**\s*([A-Z_]{3,})", r02),
            _extract(r"###[^\n]*?\b([A-Z_]{3,})\b[^\n]*?—", r02),
        )
        or "?"
    ).upper().replace(" ", "_")
    secondary_raw = pick(
        "secondary",
        _code(r"Secondary code", r02),
        _extract(r"CHIẾN THUẬT PHỤ[:\s]*\**\s*([A-Z_]{3,})", r02),
    )
    secondary = secondary_raw.upper().replace(" ", "_") if secondary_raw else None
    if secondary in ("NONE", "KHÔNG", "KHONG", "?"):
        secondary = None

    regime_label, regime_color = REGIME_LABELS.get(regime, (regime.replace("_", " ").title(), "#5B6B80"))
    headline = meta.get("headline") or STRATEGY_HEADLINES.get(strategy)
    if not headline:
        headline = f"{regime_label} — đọc kỹ trước phiên"

    # hero
    if snapshot:
        v = snapshot["vnindex"]
        chg = v["change_pct"]
        vni_line = f"VN-Index {_fmt_vn(v['close'])} ({'+' if chg >= 0 else ''}{str(chg).replace('.', ',')}%)"
    else:
        vni_line = "VN-Index"
    regime_line = regime_label + (f" · cảnh báo {REGIME_LABELS.get(sub_state, (sub_state, ''))[0].lower()}" if sub_state and sub_state != regime else "")

    # lead (doan dan hero): meta -> heading rieng (KHONG dung mac broker de tranh
    # trung noi dung khung canh bao) -> tu sinh tu regime+strategy
    lead = pick(
        "lead",
        _extract_section(r"Vì sao chọn", r02),
        _extract_section(r"Kết luận", r01),
        _extract_section(r"Nhận định", r01),
    )
    if not lead:
        strat_txt = STRATEGY_HEADLINES.get(strategy, strategy.replace("_", " ").lower())
        ex_txt = f", tỷ trọng tham khảo {exposure}" if exposure else ""
        mg_txt = " · không dùng margin" if margin == "forbidden" else ""
        lead = (
            f"Trạng thái thị trường: {regime_label}. Chiến thuật ưu tiên hôm nay: "
            f"{strat_txt}{ex_txt}{mg_txt}. Chi tiết căn cứ xem các mục bên dưới."
        )
    lead = (lead[:460] + "…") if len(lead) > 460 else lead

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

    broker_quote = pick(
        "broker_note",
        _extract_section(r"Cảnh báo cho broker", r02),
        _extract_section(r"CẢNH BÁO CHO BROKER[^\n#]*", r02),
        _extract_section(r"TÓM TẮT CHO BROKER[^\n#]*", r02),
        _extract_section(r"Cảnh báo cho broker", r01),
    )
    if broker_quote and len(broker_quote) > 600:
        broker_quote = broker_quote[:600] + "…"

    # archive links
    archived = sorted(ARCHIVE.glob("*.html"), reverse=True)
    links = " · ".join(f'<a href="archive/{p.name}">{p.stem}</a>' for p in archived[:40]) or "Chưa có"

    d = report_date.split("-")  # YYYY-MM-DD
    date_dot = f"{d[2]}.{d[1]}.{d[0]}"
    import datetime as _dt

    weekday = WEEKDAYS[_dt.date(int(d[0]), int(d[1]), int(d[2])).weekday()]

    if broker_quote and len(broker_quote.strip()) >= 20:
        broker_block = (
            '<div class="quote"><div class="khung"><div class="hop">'
            '<div class="dau-nhay">"</div><div>'
            '<div class="dg-tieude">Cảnh báo cho broker hôm nay</div>'
            f"<p>{broker_quote}</p>"
            f'<div class="ai">— Strategy Selector Agent · {date_dot} · điều khách dễ hiểu sai nhất hôm nay</div>'
            "</div></div></div></div>"
        )
    else:
        broker_block = ""

    # Open Graph: tieu de + mo ta cho the xem truoc khi share (Zalo/FB/chat)
    og_title = f"Báo cáo desk {date_dot} · {headline}"
    og_bits = [f"Phiên {date_dot}", regime_label]
    if strategy and strategy != "?":
        og_bits.append(f"Chiến thuật: {STRATEGY_HEADLINES.get(strategy, strategy.replace('_',' '))}")
    if exposure:
        og_bits.append(f"Tỷ trọng {exposure}")
    og_desc = " · ".join(og_bits)
    og_desc = re.sub(r'["\n<>]', " ", og_desc)[:200]
    og_title = re.sub(r'["\n<>]', " ", og_title)[:90]

    html = (
        PAGE_TMPL
        .replace("@@OG_TITLE@@", og_title)
        .replace("@@OG_DESC@@", og_desc)
        .replace("@@OG_DATE_ISO@@", report_date)
        .replace("@@DATE_DOT@@", date_dot)
        .replace("@@WEEKDAY@@", weekday)
        .replace("@@HEADLINE@@", headline)
        .replace("@@VNI_LINE@@", vni_line)
        .replace("@@REGIME_LINE@@", regime_line)
        .replace("@@LEAD@@", lead)
        .replace("@@METRIC_CARDS@@", "".join(cards))
        .replace("@@SECTIONS@@", "\n".join(secs))
        .replace("@@BROKER_BLOCK@@", broker_block)
        .replace("@@ARCHIVE_LINKS@@", links)
    )

    (ARCHIVE / f"{report_date}.html").write_text(
        html.replace('href="archive/', 'href="'), encoding="utf-8"
    )
    out = DOCS / "index.html"
    out.write_text(html, encoding="utf-8")
    return out
