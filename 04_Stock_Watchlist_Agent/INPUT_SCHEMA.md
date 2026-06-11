# Input Schema — Stock Watchlist Agent v0.2

Input là Handoff của agent 02 + `SECTOR ROTATION REPORT` của agent 03 + dữ liệu cổ phiếu. Trường **bắt buộc** thiếu thì áp fallback bên dưới.

## 1. Từ Strategy Selector Agent (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| strategy_code | Chiến thuật chính | PULLBACK_BUY |
| secondary_code | Chiến thuật phụ | T_PLUS hoặc NONE |
| watchlist_directive | Mục "Cho Stock Watchlist Agent" trong Handoff | "Lọc cổ phiếu còn uptrend chờ pullback về MA20" |
| exposure_ceiling | Trần tỷ trọng | 50% |
| margin_status | allowed / restricted / forbidden | restricted |

## 2. Từ Sector Rotation Agent (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| preferred_sectors | Ngành ưu tiên lọc | Bán lẻ, Chứng khoán |
| excluded_sectors | Ngành loại trừ + Avoid Chasing | Ngân hàng (weak), BĐS (avoid chasing) |
| sector_liquidity_note | Lưu ý thanh khoản từ agent 03 | Né nhóm thanh khoản cạn |

## 3. Universe & dữ liệu cổ phiếu (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| stock_universe | Danh sách mã được phép xét | VN30 + watchlist nội bộ phòng |
| price_data | Giá đóng cửa, vị trí so MA20/50, cấu trúc đỉnh–đáy, hỗ trợ/kháng cự gần nhất | MWG: trên MA50, điều chỉnh về MA20 tại 62.5 |
| volume_data | GTGD khớp lệnh TB20, volume các phiên điều chỉnh/bứt phá | TB20 = 85 tỷ; volume cạn dần khi điều chỉnh |
| listing_status | Diện cảnh báo/kiểm soát nếu có | Không |

## 4. Bối cảnh (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| stock_events | KQKD, cổ tức, phát hành, tin trọng yếu theo mã (kèm ngày) | FPT công bố KQKD 15/6 |
| client_constraints | Ràng buộc tệp khách | Né mã biến động cao |
| hot_stocks_clients_ask | Mã khách đang hỏi nhiều (để xếp vào Nên tránh nếu nguy hiểm) | Mã X trần 3 phiên do tin đồn |

## Meta

| Field | Mô tả |
|---|---|
| report_date | Ngày báo cáo (bắt buộc) |
| missing_data_note | Ghi chú dữ liệu thiếu |

## Quy tắc fallback khi thiếu dữ liệu

1. Không có Handoff agent 02 → không chạy; trả lời yêu cầu chạy pipeline từ bước 1–2 trước.
2. Không có sector map agent 03 → chỉ được xét universe theo cổng thanh khoản + setup, ghi rõ "chưa có bộ lọc ngành — độ tin cậy giảm", và tối đa 3 mã nhóm hành động.
3. Mã thiếu price_data hoặc volume_data → tối đa vào nhóm Quan sát, ghi rõ thiếu gì.
4. Universe không được cung cấp → mặc định VN30 + VNMidcap (ghi rõ giả định); KHÔNG tự thêm mã ngoài hai rổ này.
5. Không rõ listing_status → ghi chú "chưa kiểm tra diện cảnh báo/kiểm soát" vào rủi ro của mã.
