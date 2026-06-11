"""Lay du lieu thi truong qua vnstock va tinh san cac chi so ky thuat
ma Market Regime Agent can (tru Trend + mot phan Liquidity).

Cac truong khong lay duoc tu API (breadth, khoi ngoai, phai sinh, vi mo)
duoc liet ke ro trong missing_fields de agent tu web-search bo sung.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


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
        "missing_fields": [
            "advancers_decliners (so ma tang/giam HOSE)",
            "ceiling_floor_count (so ma tran/san)",
            "index_contribution (tru keo diem)",
            "matched_value_hose (GTGD khop lenh tach thoa thuan)",
            "foreign_net_today / foreign_net_5d (khoi ngoai rong)",
            "f1_basis (basis VN30F1M)",
            "global_overnight / fx_rates / domestic_policy / sentiment_note",
        ],
    }
    return snapshot


def snapshot_to_markdown(s: dict) -> str:
    v = s["vnindex"]
    ma = s["moving_averages"]
    liq = s["liquidity"]
    sw = s["swing_structure"]

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
        "## Truong du lieu CON THIEU (can tu thu thap qua web search, ghi ro nguon):",
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
