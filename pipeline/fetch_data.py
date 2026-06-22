"""Lay du lieu thi truong qua vnstock va tinh san cac chi so ky thuat
ma Market Regime Agent can (tru Trend + mot phan Liquidity).

Ngoai vnstock, module nay con goi truc tiep 4 nguon API cong khai da kiem
chung (xem agent_desk_missing_fields.md) de tu bo sung breadth, khoi ngoai
rong, tru/keo diem (index contribution) va basis phai sinh — KHONG can agent
web-search nua cho 4 truong nay. Cac goi nay duoc cache theo report_date
trong data/cache/<date>_extra.json: lan chay dau tien trong ngay (thuong la
buoi chieu, luc thi truong con dang giao dich) se fetch va luu cache; lan
chay sau (buoi toi, thi truong da dong cua, so lieu khong doi) chi doc lai
cache, khong fetch lai — tranh goi API thua va giam rui ro bi rate-limit/
chan bot.

Cac truong con lai chua co nguon API on dinh (ceiling_floor_count,
matched_value_hose, global_overnight/fx_rates/domestic_policy/sentiment_note)
van duoc liet ke trong missing_fields de agent tu web-search bo sung hoac
ap fallback.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"

# Project tin tuc (cung tai khoan Github, chay truoc 7h00, out o du-lieu/*.json)
NEWS_PROJECT_DIR = Path("F:/Hai BUi/Agent tổng hợp tin tức")

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
_HTTP_TIMEOUT = 15


def _history(symbol: str, days: int = 450):
    from vnstock.api.quote import Quote

    q = Quote(symbol=symbol, source="VCI")
    end = date.today().isoformat()
    start = (date.today() - timedelta(days=days)).isoformat()
    df = q.history(start=start, end=end, interval="1D")
    df = df.sort_values("time").reset_index(drop=True)
    return df


def _ma(series, n: int):
    if len(series) < n:
        return None
    return round(float(series.tail(n).mean()), 2)


def _pct(a: float, b: float) -> float:
    return round((a / b - 1) * 100, 2)


# ------------------------------------------------------------ extra fetchers --
# 4 nguon API cong khai da kiem chung thay the cho web-search (xem
# agent_desk_missing_fields.md). Moi ham tu try/except va tra None neu loi —
# 1 nguon loi khong duoc lam fail ca pipeline, chi ha confidence o agent.


def fetch_breadth() -> dict | None:
    """So ma tang/giam/dung gia HOSE (advancers_decliners). Nguon: CafeF."""
    try:
        r = requests.get(
            "https://cafef.vn/du-lieu/ajax/mobile/smart/ajaxdorongthitruong.ashx",
            params={"centerID": "HOSE"},
            headers={"User-Agent": _UA},
            timeout=_HTTP_TIMEOUT,
        )
        r.raise_for_status()
        rows = r.json().get("Data") or []
        if not rows:
            return None
        last = rows[-1]
        return {
            "up": last["TotalStockUp"],
            "down": last["TotalStockDown"],
            "nochange": last["TotalStockNochange"],
            "pct_up": last["PercentStockUp"],
            "pct_down": last["PercentStockDown"],
            "as_of_time": last["Time"],
            "source": "cafef.vn ajaxdorongthitruong (HOSE)",
        }
    except Exception as exc:  # noqa: BLE001
        print(f"      [extra] fetch_breadth loi: {exc}")
        return None


def fetch_foreign_net(report_date: str) -> dict | None:
    """Khoi ngoai rong phien va luy ke 5 phien (VND). Nguon: CafeF msh-appdata."""
    try:
        d = datetime.strptime(report_date, "%Y-%m-%d").strftime("%Y%m%d")
        r = requests.get(
            f"https://msh-appdata.cafef.vn/rest-api/api/v1/OverviewOrgnizaztion/0/{d}/15",
            params={"symbol": "VNINDEX"},
            headers={"User-Agent": _UA},
            timeout=_HTTP_TIMEOUT,
        )
        r.raise_for_status()
        rows = r.json() or []
        if not rows:
            return None
        net_today = float(rows[0]["netVal"])
        net_5d = round(sum(float(x["netVal"]) for x in rows[:5]))
        return {
            "net_today_vnd": net_today,
            "net_5d_vnd": net_5d,
            "unit": "VND",
            "source": "msh-appdata.cafef.vn OverviewOrgnizaztion (VNINDEX)",
        }
    except Exception as exc:  # noqa: BLE001
        print(f"      [extra] fetch_foreign_net loi: {exc}")
        return None


def fetch_index_contribution(report_date: str, top: int = 10) -> list | None:
    """Top ma tru/keo diem VNIndex. Nguon: Vietstock (token CSRF + POST).

    Vietstock co the bat anti-bot tuy IP/session — neu loi (302/4xx/timeout)
    ham tra None, agent se ap fallback nhu khi khong co du lieu.
    """
    try:
        with requests.Session() as s:
            s.headers.update({"User-Agent": _UA})
            page = s.get(
                "https://finance.vietstock.vn/ket-qua-giao-dich?tab=cp-anh-huong",
                timeout=_HTTP_TIMEOUT,
            )
            page.raise_for_status()
            m = re.search(
                r'id=__CHART_AjaxAntiForgeryForm[^>]*>\s*<input[^>]*name=["\']?'
                r'__RequestVerificationToken["\']?[^>]*value=["\']?([^"\' >]+)',
                page.text,
            )
            if not m:
                return None
            token = m.group(1)

            from_date = (
                datetime.strptime(report_date, "%Y-%m-%d") - timedelta(days=31)
            ).strftime("%Y-%m-%d")
            resp = s.post(
                "https://finance.vietstock.vn/data/TopStockInfluence",
                data={
                    "fromDate": from_date,
                    "toDate": report_date,
                    "catID": 1,
                    "top": top,
                    "type": 0,
                    "__RequestVerificationToken": token,
                },
                headers={
                    "Referer": "https://finance.vietstock.vn/ket-qua-giao-dich?tab=cp-anh-huong",
                    "X-Requested-With": "XMLHttpRequest",
                },
                timeout=_HTTP_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            if not isinstance(data, list) or not data:
                return None
            return [
                {
                    "code": x["StockCode"],
                    "change_pct": x["PerChange"],
                    "influence_index": x["InfluenceIndex"],
                }
                for x in data
            ]
    except Exception as exc:  # noqa: BLE001
        print(f"      [extra] fetch_index_contribution loi (co the bi anti-bot): {exc}")
        return None


def _vietstock_ohlc(symbol: str) -> dict | None:
    end = int(datetime.now().timestamp())
    start = end - 30 * 86400
    r = requests.get(
        "https://api.vietstock.vn/tvnew/history",
        params={
            "symbol": symbol,
            "resolution": "1D",
            "from": start,
            "to": end,
            "countback": 2,
        },
        headers={"User-Agent": _UA, "Referer": "https://stockchart.vietstock.vn/"},
        timeout=_HTTP_TIMEOUT,
    )
    r.raise_for_status()
    j = r.json()
    if j.get("s") != "ok" or not j.get("c"):
        return None
    return {"close": float(j["c"][-1]), "time": j["t"][-1]}


def fetch_f1_basis() -> dict | None:
    """Basis giua VN30F1M va VN30. Nguon: api.vietstock.vn/tvnew/history."""
    try:
        vn30 = _vietstock_ohlc("VN30")
        f1 = _vietstock_ohlc("VN30F1M")
        if not vn30 or not f1:
            return None
        basis = round(f1["close"] - vn30["close"], 2)
        return {
            "vn30_close": vn30["close"],
            "f1_close": f1["close"],
            "basis": basis,
            "basis_pct": round(basis / vn30["close"] * 100, 2),
            "source": "api.vietstock.vn/tvnew/history (VN30, VN30F1M)",
        }
    except Exception as exc:  # noqa: BLE001
        print(f"      [extra] fetch_f1_basis loi: {exc}")
        return None


def fetch_ceiling_floor() -> dict | None:
    """So ma tang tran / giam san HOSE, kem tong KLGD va GTGD. Nguon: CafeF PriceHistory.ashx.

    Cung tra ve TotalStockUp/Down/Nochange nen co the dung lam backup cho breadth
    neu fetch_breadth() bi loi.
    """
    try:
        r = requests.get(
            "https://cafef.vn/du-lieu/Ajax/PriceHistory/PriceHistory.ashx",
            params={"centerid": "1"},
            headers={"User-Agent": _UA},
            timeout=_HTTP_TIMEOUT,
        )
        r.raise_for_status()
        j = r.json()
        if not j.get("Success"):
            return None
        d = j["Data"]
        return {
            "ceiling": int(d["TotalKichtran"]),
            "floor": int(d["TotalKichsan"]),
            "up": int(d["TotalStockUp"]),
            "down": int(d["TotalStockDown"]),
            "nochange": int(d["TotalStockNochange"]),
            "total_volume": int(d["Volume"]),
            "total_value_bil": float(d["TotalValue"]),  # don vi: ty VND
            "source": "cafef.vn PriceHistory.ashx (HOSE centerid=1)",
        }
    except Exception as exc:  # noqa: BLE001
        print(f"      [extra] fetch_ceiling_floor loi: {exc}")
        return None


def fetch_agreements_trading() -> dict | None:
    """Tong KLGD va GTGD thoa thuan VNINDEX. Nguon: 24hmoney agreements-trading-history.

    Lay agreements_vol va agreements_val. Ket hop voi tong tu fetch_ceiling_floor()
    se tinh duoc khop lenh = tong - thoa thuan.
    """
    try:
        r = requests.get(
            "https://api-finance-t19.24hmoney.vn/v1/web/indices/agreements-trading-history",
            params={
                "device_id": "web1782126832vtsa2om3p04je0swryh0ketx9nqw8568282",
                "device_name": "INVALID",
                "device_model": "Windows 10",
                "network_carrier": "INVALID",
                "connection_type": "INVALID",
                "os": "Chrome",
                "os_version": "149.0.0.0",
                "access_token": "INVALID",
                "push_token": "INVALID",
                "locale": "vi",
                "browser_id": "web1782126832vtsa2om3p04je0swryh0ketx9nqw8568282",
                "code": "10",
            },
            headers={"User-Agent": _UA},
            timeout=_HTTP_TIMEOUT,
        )
        r.raise_for_status()
        j = r.json()
        if j.get("status") != 200 or not j.get("data"):
            return None
        d = j["data"][0]
        return {
            "agreements_vol": int(d["total_vol"]),
            "agreements_val": int(d["total_val"]),  # don vi: VND
            "agreements_transactions": int(d["total_transactions"]),
            "agreements_symbols": int(d["total_symbol"]),
            "source": "api-finance-t19.24hmoney.vn agreements-trading-history (code=10 VNINDEX)",
        }
    except Exception as exc:  # noqa: BLE001
        print(f"      [extra] fetch_agreements_trading loi: {exc}")
        return None


def fetch_from_news_project(today: str) -> dict | None:
    """Doc du lieu tu project 'Agent tong hop tin tuc' (chay luc 7h, truoc project nay).

    Doc file du-lieu/{today}.json; neu khong co thi thu lui 1-2 ngay (nghi le / loi).
    Tra ve dict chua:
      - global_overnight: items cua muc §01 (thi truong quoc te)
      - fx_rates: USD/VND va lai qua dem LNH (tu chi_so hoac §05)
      - domestic_policy: items cua muc §05 (vi mo & tien te)
      - sentiment_note: truong danh_gia (nhan dinh tong hop cua desk)
    """
    du_lieu_dir = NEWS_PROJECT_DIR / "du-lieu"
    if not du_lieu_dir.exists():
        print(f"      [news] Khong tim thay thu muc {du_lieu_dir}")
        return None

    # Tim file gần nhất: hôm nay → lui tối đa 3 ngày (ngày nghỉ / lỗi)
    candidate = None
    today_dt = datetime.strptime(today, "%Y-%m-%d")
    for delta in range(4):
        d = (today_dt - timedelta(days=delta)).strftime("%Y-%m-%d")
        p = du_lieu_dir / f"{d}.json"
        if p.exists():
            candidate = p
            break

    if not candidate:
        print(f"      [news] Khong co file nao trong vong 3 ngay truoc {today}")
        return None

    try:
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"      [news] Loi doc {candidate.name}: {exc}")
        return None

    global_overnight = None
    domestic_policy = None
    for muc in data.get("muc", []):
        so = muc.get("so")
        if so == "01":
            global_overnight = muc.get("items", [])
        elif so == "05":
            domestic_policy = muc.get("items", [])

    # Trich xuat fx_rates: uu tien §05, fallback chi_so
    fx_rates: dict = {}

    def _try_extract_fx(items: list, key_field: str, val_field: str) -> None:
        for item in items:
            label = str(item.get(key_field, "")).lower()
            val = item.get(val_field)
            note = item.get("y_nghia") or item.get("ghi_chu") or ""
            if not fx_rates.get("usdvnd") and ("usd" in label or "tỷ giá" in label):
                fx_rates["usdvnd"] = {"value": val, "note": note}
            if not fx_rates.get("overnight_rate") and (
                "liên ngân" in label or "lãi qua đêm" in label or "lnh" in label
            ):
                fx_rates["overnight_rate"] = {"value": val, "note": note}

    if domestic_policy:
        _try_extract_fx(domestic_policy, "chi_tieu", "gia_tri")
    _try_extract_fx(data.get("chi_so", []), "ten", "gia_tri")

    print(f"      [news] Doc thanh cong {candidate.name} (ngay tin: {data.get('ngay')}, phien: {data.get('phien')})")
    return {
        "global_overnight": global_overnight,
        "fx_rates": fx_rates if fx_rates else None,
        "domestic_policy": domestic_policy,
        "sentiment_note": data.get("danh_gia"),
        "news_date": data.get("ngay"),
        "news_phien": data.get("phien"),
        "news_source_file": candidate.name,
    }


def fetch_extra_fields(report_date: str, force_refresh: bool = False) -> dict:
    """Goi 4 nguon tren, co cache theo report_date.

    Cache file: data/cache/<report_date>_extra.json. Lan chay dau trong ngay
    (chieu, thi truong dang mo) fetch va luu cache; lan chay sau (toi, thi
    truong da dong cua) doc lai cache — khong fetch lai.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{report_date}_extra.json"

    if not force_refresh and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            print(f"      [extra] dung lai cache {cache_path.name} (khong fetch lai)")
            return cached
        except Exception:
            pass  # cache hong -> fetch lai

    extra = {
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "breadth": fetch_breadth(),
        "foreign_net": fetch_foreign_net(report_date),
        "index_contribution": fetch_index_contribution(report_date),
        "f1_basis": fetch_f1_basis(),
        "ceiling_floor": fetch_ceiling_floor(),
        "agreements": fetch_agreements_trading(),
        "news": fetch_from_news_project(report_date),
    }
    cache_path.write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")
    return extra


def build_market_snapshot() -> dict:
    vni = _history("VNINDEX")
    vn30 = _history("VN30")

    last = vni.iloc[-1]
    prev = vni.iloc[-2]
    close = float(last["close"])

    ma20 = _ma(vni["close"], 20)
    ma50 = _ma(vni["close"], 50)
    ma200 = _ma(vni["close"], 200)

    vol = vni["volume"].astype(float)
    vol_today = float(vol.iloc[-1])
    vol_avg20 = float(vol.iloc[-21:-1].mean())

    recent20 = vni.tail(20)
    recent60 = vni.tail(60)

    snapshot = {
        "data_date": str(last["time"])[:10],
        "vnindex": {
            "open": float(last["open"]),
            "high": float(last["high"]),
            "low": float(last["low"]),
            "close": close,
            "change_pct": _pct(close, float(prev["close"])),
            "perf_5d_pct": _pct(close, float(vni["close"].iloc[-6])),
            "perf_20d_pct": _pct(close, float(vni["close"].iloc[-21])),
        },
        "vn30": {
            "close": float(vn30["close"].iloc[-1]),
            "change_pct": _pct(
                float(vn30["close"].iloc[-1]), float(vn30["close"].iloc[-2])
            ),
        },
        "moving_averages": {
            "ma20": ma20,
            "ma50": ma50,
            "ma200": ma200,
            "above_ma20": ma20 is not None and close > ma20,
            "above_ma50": ma50 is not None and close > ma50,
            "above_ma200": ma200 is not None and close > ma200,
        },
        "liquidity": {
            # vnstock chi co tong khoi luong (khong tach khop lenh / thoa thuan)
            "volume_today": vol_today,
            "volume_avg20": round(vol_avg20),
            "volume_vs_avg20_pct": round(vol_today / vol_avg20 * 100, 1),
            "note": "Khoi luong TONG (chua tach thoa thuan) - chi la proxy, can doi chieu GTGD khop lenh tu nguon khac",
        },
        "swing_structure": {
            "high_20d": float(recent20["high"].max()),
            "high_20d_date": str(
                recent20.loc[recent20["high"].idxmax(), "time"]
            )[:10],
            "low_20d": float(recent20["low"].min()),
            "low_20d_date": str(recent20.loc[recent20["low"].idxmin(), "time"])[:10],
            "high_60d": float(recent60["high"].max()),
            "low_60d": float(recent60["low"].min()),
        },
        "missing_fields": [],
    }

    report_date = snapshot["data_date"]
    extra = fetch_extra_fields(report_date)
    snapshot["breadth"] = extra.get("breadth")
    snapshot["foreign_flows"] = extra.get("foreign_net")
    snapshot["index_contribution"] = extra.get("index_contribution")
    snapshot["f1_basis"] = extra.get("f1_basis")
    snapshot["ceiling_floor"] = extra.get("ceiling_floor")
    snapshot["extra_fetched_at"] = extra.get("fetched_at")

    # Du lieu tu project tin tuc (chay 7h, doc sau khi project do hoan thanh)
    news = extra.get("news")
    if news:
        snapshot["global_overnight"] = news.get("global_overnight")
        snapshot["fx_rates"] = news.get("fx_rates")
        snapshot["domestic_policy"] = news.get("domestic_policy")
        snapshot["sentiment_note"] = news.get("sentiment_note")
        snapshot["news_meta"] = {
            "date": news.get("news_date"),
            "phien": news.get("news_phien"),
            "source_file": news.get("news_source_file"),
        }
    else:
        snapshot["global_overnight"] = None
        snapshot["fx_rates"] = None
        snapshot["domestic_policy"] = None
        snapshot["sentiment_note"] = None
        snapshot["news_meta"] = None

    # Tinh khop lenh = tong - thoa thuan (neu co du ca 2 nguon)
    cf = extra.get("ceiling_floor")
    ag = extra.get("agreements")
    snapshot["agreements"] = ag
    if cf and ag:
        total_val_vnd = cf["total_value_bil"] * 1e9
        matched_vol = cf["total_volume"] - ag["agreements_vol"]
        matched_val_vnd = total_val_vnd - ag["agreements_val"]
        snapshot["matched_trading"] = {
            "matched_vol": matched_vol,
            "matched_val_bil": round(matched_val_vnd / 1e9, 2),
            "agreements_vol": ag["agreements_vol"],
            "agreements_val_bil": round(ag["agreements_val"] / 1e9, 2),
            "total_vol": cf["total_volume"],
            "total_val_bil": cf["total_value_bil"],
        }
    else:
        snapshot["matched_trading"] = None

    # Bao ro cac truong loi lan nay de agent ha confidence.
    if snapshot["breadth"] is None:
        snapshot["missing_fields"].append(
            "advancers_decliners (so ma tang/giam HOSE) — loi khi fetch lan nay, xem log"
        )
    if snapshot["foreign_flows"] is None:
        snapshot["missing_fields"].append(
            "foreign_net_today / foreign_net_5d (khoi ngoai rong) — loi khi fetch lan nay, xem log"
        )
    if snapshot["index_contribution"] is None:
        snapshot["missing_fields"].append(
            "index_contribution (tru keo diem) — loi khi fetch lan nay (co the bi anti-bot Vietstock), xem log"
        )
    if snapshot["f1_basis"] is None:
        snapshot["missing_fields"].append(
            "f1_basis (basis VN30F1M) — loi khi fetch lan nay, xem log"
        )
    if cf is None:
        snapshot["missing_fields"].append(
            "ceiling_floor_count (so ma tran/san) — loi khi fetch lan nay, xem log"
        )
    if ag is None:
        snapshot["missing_fields"].append(
            "agreements_trading (thoa thuan HOSE) — loi khi fetch lan nay, xem log"
        )
    if snapshot["matched_trading"] is None:
        snapshot["missing_fields"].append(
            "matched_value_hose (GTGD khop lenh) — can ca ceiling_floor va agreements de tinh, xem log"
        )
    if snapshot["global_overnight"] is None:
        snapshot["missing_fields"].append(
            "global_overnight / fx_rates / domestic_policy / sentiment_note"
            " — project tin tuc chua chay hoac chua co file ngay hom nay (chay sau 7h00)"
        )
    return snapshot


def snapshot_to_markdown(s: dict) -> str:
    v = s["vnindex"]
    ma = s["moving_averages"]
    liq = s["liquidity"]
    sw = s["swing_structure"]
    breadth = s.get("breadth")
    flows = s.get("foreign_flows")
    f1 = s.get("f1_basis")
    contrib = s.get("index_contribution")
    cf = s.get("ceiling_floor")
    mt = s.get("matched_trading")
    global_ov = s.get("global_overnight")
    fx = s.get("fx_rates")
    dom_policy = s.get("domestic_policy")
    sentiment = s.get("sentiment_note")
    news_meta = s.get("news_meta")

    def yn(b):
        return "TREN" if b else "DUOI"

    lines = [
        f"## Du lieu phien gan nhat ({s['data_date']}) — nguon vnstock/VCI",
        "",
        f"- VN-Index: O {v['open']} / H {v['high']} / L {v['low']} / C {v['close']} ({v['change_pct']:+}%)",
        f"- VN30: {s['vn30']['close']} ({s['vn30']['change_pct']:+}%)",
        f"- Hieu suat VN-Index: 5 phien {v['perf_5d_pct']:+}% | 20 phien {v['perf_20d_pct']:+}%",
        f"- MA20 = {ma['ma20']} ({yn(ma['above_ma20'])}) | MA50 = {ma['ma50']} ({yn(ma['above_ma50'])}) | MA200 = {ma['ma200']} ({yn(ma['above_ma200'])})",
        f"- Khoi luong phien: {liq['volume_today']:,.0f} = {liq['volume_vs_avg20_pct']}% trung binh 20 phien. LUU Y: {liq['note']}",
        f"- Dinh 20 phien: {sw['high_20d']} ({sw['high_20d_date']}) | Day 20 phien: {sw['low_20d']} ({sw['low_20d_date']})",
        f"- Dinh/Day 60 phien: {sw['high_60d']} / {sw['low_60d']}",
        "",
        "## Breadth, khoi ngoai, phai sinh (nguon API tu dong, khong qua web search)",
        "",
    ]

    if breadth:
        lines.append(
            f"- Breadth HOSE (tinh den {breadth['as_of_time']}): tang {breadth['up']} / "
            f"giam {breadth['down']} / dung gia {breadth['nochange']} "
            f"({breadth['pct_up']}% / {breadth['pct_down']}%). Nguon: {breadth['source']}."
        )
    else:
        lines.append("- Breadth HOSE: KHONG lay duoc lan nay (xem missing_fields).")

    if flows:
        lines.append(
            f"- Khoi ngoai rong phien: {flows['net_today_vnd']:,.0f} {flows['unit']} | "
            f"luy ke 5 phien: {flows['net_5d_vnd']:,.0f} {flows['unit']}. Nguon: {flows['source']}."
        )
    else:
        lines.append("- Khoi ngoai rong: KHONG lay duoc lan nay (xem missing_fields).")

    if f1:
        lines.append(
            f"- Basis phai sinh: VN30 {f1['vn30_close']} | VN30F1M {f1['f1_close']} | "
            f"basis {f1['basis']:+} diem ({f1['basis_pct']:+}%). Nguon: {f1['source']}."
        )
    else:
        lines.append("- Basis VN30F1M: KHONG lay duoc lan nay (xem missing_fields).")

    if contrib:
        top5 = ", ".join(
            f"{x['code']} ({x['change_pct']:+}%, anh huong {x['influence_index']:+})"
            for x in contrib[:5]
        )
        lines.append(f"- Top 5 ma anh huong VN-Index: {top5}. Nguon: Vietstock TopStockInfluence.")
    else:
        lines.append("- Index contribution (tru/keo diem): KHONG lay duoc lan nay (xem missing_fields).")

    if cf:
        lines.append(
            f"- Tran/San HOSE: tang tran {cf['ceiling']} ma | giam san {cf['floor']} ma. "
            f"Tong KL: {cf['total_volume']:,} cp | Tong GTGD: {cf['total_value_bil']:,.2f} ty VND. "
            f"Nguon: {cf['source']}."
        )
    else:
        lines.append("- Tran/San HOSE: KHONG lay duoc lan nay (xem missing_fields).")

    if mt:
        lines.append(
            f"- GTGD khop lenh HOSE: {mt['matched_vol']:,} cp | {mt['matched_val_bil']:,.2f} ty VND. "
            f"(Thoa thuan: {mt['agreements_vol']:,} cp | {mt['agreements_val_bil']:,.2f} ty VND. "
            f"Tong: {mt['total_vol']:,} cp | {mt['total_val_bil']:,.2f} ty VND.)"
        )
    else:
        lines.append("- GTGD khop lenh HOSE: KHONG tinh duoc (can ca ceiling_floor va agreements, xem missing_fields).")

    # Phan du lieu tu project tin tuc
    news_src = f" (tu {news_meta['source_file']}, ban tin ngay {news_meta['date']})" if news_meta else ""
    lines += [
        "",
        f"## Tin tuc & phan tich{news_src}",
        "",
    ]

    if fx:
        usdvnd = fx.get("usdvnd", {})
        lnh = fx.get("overnight_rate", {})
        parts = []
        if usdvnd.get("value"):
            parts.append(f"USD/VND: {usdvnd['value']}")
        if lnh.get("value"):
            parts.append(f"Lai LNH qua dem: {lnh['value']}")
        if parts:
            lines.append(f"- Ty gia & lai suat: {' | '.join(parts)}")
    else:
        lines.append("- Ty gia & lai LNH: chua co (project tin tuc chua chay hoac chua cap nhat).")

    if global_ov:
        lines.append("- Qua dem toan cau (top 5 items):")
        for item in global_ov[:5]:
            name = item.get("ten", "")
            val = item.get("gia_tri") or item.get("text", "")
            change = item.get("thay_doi", "")
            ynghia = item.get("y_nghia", "")
            lines.append(f"  - {name}: {val} {change}. Y nghia: {ynghia}")
    else:
        lines.append("- Qua dem toan cau: chua co (project tin tuc chua chay).")

    if dom_policy:
        lines.append("- Vi mo & tien te (top 4 items):")
        for item in dom_policy[:4]:
            chi_tieu = item.get("chi_tieu", "")
            gia_tri = item.get("gia_tri", "")
            ynghia = item.get("y_nghia", "")
            lines.append(f"  - {chi_tieu}: {gia_tri}. Y nghia: {ynghia}")
    else:
        lines.append("- Vi mo & tien te: chua co (project tin tuc chua chay).")

    if sentiment:
        lines.append(f"- Nhan dinh desk: {sentiment}")
    else:
        lines.append("- Nhan dinh desk: chua co.")

    if s["missing_fields"]:
        lines += [
            "",
            "## Truong du lieu CON THIEU:",
            "",
        ]
        lines += [f"- {f}" for f in s["missing_fields"]]
    return "\n".join(lines)


def fetch(save: bool = True) -> tuple[dict, str]:
    snap = build_market_snapshot()
    md = snapshot_to_markdown(snap)
    if save:
        DATA_DIR.mkdir(exist_ok=True)
        out = DATA_DIR / f"{snap['data_date']}.json"
        out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    return snap, md


if __name__ == "__main__":
    _, md = fetch()
    print(md)
