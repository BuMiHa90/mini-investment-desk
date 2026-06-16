# Missing fields — trạng thái nguồn dữ liệu

Đã kiểm chứng 4/7 nguồn dưới đây bằng cách gọi thật (Python `requests`) và
**đã code thẳng vào `pipeline/fetch_data.py`** — agent 01 KHÔNG cần web search
cho 4 trường này nữa, `build_market_snapshot()` tự fetch và đưa sẵn vào
`market_data_md`. 3 trường còn lại chưa có nguồn API ổn định, vẫn nằm trong
`missing_fields` để agent áp fallback / tự web search nếu được bật.

## Cache theo phiên (chiều fetch, tối tái dùng)

`fetch_extra_fields(report_date)` cache kết quả 4 nguồn vào
`data/cache/<report_date>_extra.json`. Lần chạy đầu trong ngày (thường là
buổi chiều, lúc thị trường còn mở) fetch trực tiếp và lưu cache; lần chạy
sau cùng ngày (buổi tối, thị trường đã đóng cửa — số liệu không đổi) chỉ đọc
lại cache, KHÔNG gọi lại API. Dùng `force_refresh=True` nếu cần ép fetch lại
trong cùng ngày. Cache không commit vào git (`data/cache/` trong `.gitignore`).

Mỗi nguồn tự `try/except` độc lập trong `fetch_data.py` — 1 nguồn lỗi (ví dụ
Vietstock chặn bot) không làm fail cả pipeline, chỉ field đó trả `None` và
được thêm vào `missing_fields` của lần chạy đó để agent hạ confidence.

## ĐÃ XÁC THỰC — code trong `fetch_data.py`

### advancers_decliners (số mã tăng/giảm HOSE) → `fetch_breadth()`
GET `https://cafef.vn/du-lieu/ajax/mobile/smart/ajaxdorongthitruong.ashx?centerID=HOSE`
Trả về mảng `Data` theo từng mốc thời gian trong phiên; lấy phần tử cuối
(`TotalStockUp/Down/Nochange`, `PercentStockUp/Down`) làm số liệu tính đến
thời điểm chạy.

### foreign_net_today / foreign_net_5d (khối ngoại ròng) → `fetch_foreign_net()`
GET `https://msh-appdata.cafef.vn/rest-api/api/v1/OverviewOrgnizaztion/0/<yyyymmdd>/15?symbol=VNINDEX`
(`<yyyymmdd>` = `report_date` định dạng lại). Trả về list 15 phiên gần nhất,
mỗi phần tử có `netVal` (VND). `net_today` = phần tử đầu, `net_5d` = tổng 5
phần tử đầu.

### index_contribution (trừ/kéo điểm) → `fetch_index_contribution()`
Bước 1: GET `https://finance.vietstock.vn/ket-qua-giao-dich?tab=cp-anh-huong`,
giữ session (`requests.Session`) để cookie antiforgery đi kèm, parse token
trong form `__CHART_AjaxAntiForgeryForm`.
Bước 2: POST `https://finance.vietstock.vn/data/TopStockInfluence` với
`fromDate`, `toDate`, `catID=1`, `top=10`, `type=0`, `__RequestVerificationToken`
+ header `Referer`, `X-Requested-With: XMLHttpRequest`, dùng cùng session
(cookie) ở bước 1. Trả về top N mã ảnh hưởng VNIndex (`StockCode`,
`PerChange`, `InfluenceIndex`, ...).

**Lưu ý vận hành:** endpoint này từng trả 302 khi test bằng `curl` trần (có
thể do anti-bot dựa trên TLS/session fingerprint), nhưng chạy ổn định qua
`requests.Session` của Python (đã test thực tế, có dữ liệu). Nếu một ngày nào
đó Vietstock siết bot mạnh hơn và hàm bắt đầu trả `None` liên tục, cần xem
log lỗi và có thể phải thêm header/cookie giống browser hơn hoặc đổi nguồn.

### f1_basis (basis VN30F1M vs VN30) → `fetch_f1_basis()`
GET `https://api.vietstock.vn/tvnew/history?symbol=VN30&resolution=1D&from=...&to=...&countback=2`
(và lặp lại với `symbol=VN30F1M`), cần header `User-Agent` + `Referer:
https://stockchart.vietstock.vn/`. Lấy giá đóng cửa gần nhất mỗi mã, basis =
`f1_close - vn30_close`.

## CHƯA CÓ NGUỒN — vẫn skip, agent tự web search/fallback

- `ceiling_floor_count` (số mã trần/sàn)
- `matched_value_hose` (GTGD khớp lệnh tách thỏa thuận)
- `global_overnight / fx_rates / domestic_policy / sentiment_note`
