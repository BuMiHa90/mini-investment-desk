# Input Schema — Sector Rotation Agent v0.2

Input chính là `STRATEGY SELECTION REPORT` của `02_Strategy_Selector_Agent` (tối thiểu khối Handoff) + dữ liệu ngành. Trường **bắt buộc** thiếu thì áp quy tắc fallback bên dưới.

## 1. Từ Strategy Selector Agent (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| strategy_code | Mã chiến thuật chính | SECTOR_ROTATION, PULLBACK_BUY, WAIT |
| secondary_code | Chiến thuật phụ | T_PLUS hoặc NONE |
| sector_directive | Mục "Cho Sector Rotation Agent" trong Handoff | "Tìm nhóm giữ tiền trong phân hóa, xác nhận bằng dòng tiền" |
| exposure_ceiling | Trần tỷ trọng | 50% |
| margin_status | allowed / restricted / forbidden | restricted |

## 2. Dữ liệu ngành (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| sector_performance_5d | Hiệu suất từng ngành 5 phiên + VN-Index cùng kỳ | Ngân hàng +1,2% vs Index +0,5% |
| sector_performance_20d | Hiệu suất từng ngành 20 phiên + Index cùng kỳ | BĐS -3,1% vs Index -1,0% |
| sector_liquidity | GTGD ngành so trung bình 20 phiên của chính ngành đó | Chứng khoán 140% trung bình |
| sector_breadth | % mã tăng trong từng ngành (phiên gần nhất hoặc 5 phiên) | Thép: 8/12 mã tăng |

## 3. Dòng tiền theo ngành (không bắt buộc nhưng nên có)

| Field | Mô tả | Ví dụ |
|---|---|---|
| foreign_flow_sector | Khối ngoại ròng theo ngành (phiên + 5 phiên) | Bán ròng BĐS -800 tỷ/5 phiên |
| prop_flow_sector | Tự doanh theo ngành | Mua ròng ngân hàng |
| leader_contribution | Mức tăng ngành có dồn vào 1–2 trụ không | VIC chiếm 80% mức tăng ngành BĐS |

## 4. Bối cảnh (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| sector_news | Tin tức theo ngành | Giá thép HRC tăng, room tín dụng mới |
| event_calendar | Sự kiện liên quan ngành 1–10 phiên tới | KQKD ngân hàng tuần sau |
| hot_streak_note | Ngành nào đang có chuỗi tăng dài / mã trần | Chứng khoán tăng 6 phiên liên tiếp |

## Meta

| Field | Mô tả |
|---|---|
| report_date | Ngày báo cáo (bắt buộc) |
| missing_data_note | Ghi chú dữ liệu thiếu |

## Nguồn dữ liệu gợi ý (miễn phí)

- Hiệu suất + thanh khoản ngành: Vietstock (thống kê ngành), CafeF, fireant.vn, simplize.vn (sector heatmap).
- Khối ngoại theo ngành/mã: CafeF dữ liệu khối ngoại, bài tổng kết phiên sau 15h30.
- Độ rộng nội ngành: bảng giá theo ngành của các CTCK.

## Quy tắc fallback khi thiếu dữ liệu

1. Không có báo cáo agent 02 → chỉ xuất map quan sát, không khuyến nghị hành động, ghi rõ thiếu đầu vào chiến thuật.
2. Thiếu sector_liquidity / sector_breadth (trục Flow) → chỉ dùng trục RS, KHÔNG được xếp nhóm Strong (tối đa Improving), ghi rõ vào Data gaps.
3. Chỉ có dữ liệu 1 phiên → toàn bộ kết luận gắn nhãn "tín hiệu chưa xác nhận", không có nhóm Strong.
4. Thiếu dòng tiền ngoại/tự doanh → bỏ qua cấu phần đó trong Flow, không suy diễn.
