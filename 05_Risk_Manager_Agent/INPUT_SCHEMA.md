# Input Schema — Risk Manager Agent v0.2

Input chính là `STOCK WATCHLIST REPORT` của agent 04 + bối cảnh pipeline. Trường **bắt buộc** thiếu thì áp fallback bên dưới.

## 1. Từ Stock Watchlist Agent (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| watchlist_items | Toàn bộ bảng "Có thể hành động nếu xác nhận" (đủ 7 trường mỗi mã) | MWG: pullback MA20, kích hoạt..., stop... |
| watch_only_items | Bảng "Chỉ quan sát" (chỉ rà nếu được yêu cầu) | FPT chờ KQKD |
| avoid_items | Bảng "Nên tránh" (đối chiếu nhất quán) | VHM — avoid chasing |
| handoff_concerns | Khối Handoff To Risk Manager | "Soi kỹ mã D — mean reversion rủi ro cao" |

## 2. Bối cảnh pipeline (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| market_regime | Regime code + confidence từ agent 01 | DIVERGENT, confidence Cao |
| strategy_code | Chiến thuật chính + phụ từ agent 02 | SECTOR_ROTATION + T_PLUS |
| exposure_ceiling | Trần tỷ trọng | 50% |
| margin_status | allowed / restricted / forbidden | restricted |
| sector_map_summary | Tóm tắt Strong/Excluded từ agent 03 | Strong: bán lẻ; Excluded: ngân hàng, BĐS |

## 3. Hồ sơ khách (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| client_risk_profile | Tệp khách áp dụng báo cáo này | Thận trọng / cân bằng / chấp nhận rủi ro |
| client_margin_usage | Tình trạng margin hiện tại của tệp khách | Nhiều khách đang margin cao |
| client_holdings_note | Khách đang kẹt hàng nhóm nào | Kẹt BĐS từ đỉnh |

## 4. Rủi ro sự kiện (không bắt buộc nhưng nên có)

| Field | Mô tả | Ví dụ |
|---|---|---|
| event_risks | Sự kiện 1–5 phiên tới theo mã và toàn thị trường | FPT KQKD 15/6; đáo hạn F1M 18/6 |
| market_event_note | Sự kiện vĩ mô | Họp Fed 17–18/6 |

## Meta

| Field | Mô tả |
|---|---|
| report_date | Ngày báo cáo (bắt buộc) |
| missing_data_note | Ghi chú dữ liệu thiếu |

## Quy tắc fallback khi thiếu dữ liệu

1. Không có watchlist từ agent 04 → không có gì để rà; trả lời yêu cầu chạy pipeline bước 1–4 trước. KHÔNG tự tạo ý tưởng để đánh giá.
2. Thiếu market_regime / strategy_code → không kiểm tra được Cổng 1 → mọi ý tưởng tối đa Conditional Pass, ghi rõ "chưa xác minh nhất quán pipeline".
3. Thiếu hồ sơ khách → đánh giá suitability theo tệp khách bảo thủ nhất (khách mới, không margin) và ghi rõ giả định.
4. Thiếu lịch sự kiện → ghi "chưa kiểm tra rủi ro sự kiện" vào mọi quyết định Pass (tự động thành Conditional nếu mã có KQKD theo mùa đang đến gần).
5. Mã nào trong watchlist thiếu 1 trong 7 trường → Reject tại Cổng 2, không xét tiếp.
