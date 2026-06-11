# Input Schema — Strategy Selector Agent v0.2

Input chính là `MARKET REGIME REPORT` của `01_Market_Regime_Agent` (tối thiểu là khối Handoff). Các nhóm còn lại bổ sung ngữ cảnh. Trường **bắt buộc** thiếu thì áp quy tắc fallback bên dưới.

## 1. Từ Market Regime Agent (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| regime_code | Mã regime từ Handoff | RISK_OFF, SIDEWAY, TECH_BOUNCE |
| sub_state | Trạng thái phụ nếu có | Bull trap risk, Phân hóa |
| regime_confidence | Mức tự tin của regime | Thấp / Trung bình / Cao |
| exposure_band | Band tỷ trọng từ Handoff | 10–30% |
| margin_status | Trạng thái margin từ Handoff | allowed / restricted / forbidden |
| strategy_constraints | Ràng buộc chiến lược từ Handoff | "chỉ chiến lược phòng thủ, không breakout" |
| key_levels | Hỗ trợ/kháng cự đang theo dõi (từ báo cáo regime) | HT 1.780–1.750; KC 1.811–1.830 |
| liquidity_context | Thanh khoản so trung bình 20 phiên | 65% trung bình, cạn kiệt |

## 2. Tâm lý nhà đầu tư (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| sentiment_state | Trạng thái tâm lý chung | Sợ hãi / thận trọng / hưng phấn cực đoan |
| sentiment_evidence | Căn cứ | Thanh khoản cạn, NĐT đứng ngoài, room chat im ắng |

## 3. Tin tức thị trường (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| market_news | Tin lớn trong ngày/tuần | Fed giữ lãi suất, tin nâng hạng |
| event_calendar | Sự kiện 1–5 phiên tới | Đáo hạn F1M 18/6, review ETF 20/6 |

## 4. Dữ liệu ngành (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| sector_dispersion | Mức phân hóa giữa các ngành | Ngân hàng -1,2% trong khi BĐS +2,1% |
| leading_sectors | Nhóm đang giữ tiền / dẫn dắt | BĐS, bán lẻ |

## 5. Rủi ro & ràng buộc desk (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| key_market_risks | Rủi ro chính từ báo cáo regime | Bull trap, margin call dây chuyền |
| client_constraints | Ràng buộc theo tệp khách của phòng | Đa số khách mới, khẩu vị rủi ro thấp |
| desk_note | Ghi chú riêng của trưởng phòng | Tuần này hạn chế khuyến nghị mới |

## Meta

| Field | Mô tả |
|---|---|
| report_date | Ngày báo cáo (bắt buộc) |
| regime_report_date | Ngày của báo cáo regime đầu vào — nếu cũ hơn 1 phiên phải ghi chú độ trễ |

## Quy tắc fallback khi thiếu dữ liệu

1. Thiếu toàn bộ báo cáo regime → coi confidence là **Thấp** → chiến thuật chính bắt buộc WAIT; ghi rõ "không có báo cáo regime đầu vào".
2. Có regime_code nhưng thiếu confidence → coi là Trung bình (loại Tier 3 khỏi chiến thuật chính).
3. Thiếu exposure_band / margin_status → dùng band thận trọng nhất của regime đó và margin restricted.
4. Báo cáo regime cũ hơn 1 phiên giao dịch → hạ confidence 1 bậc, ghi chú độ trễ vào "Cảnh báo cho broker".
5. Thiếu sentiment / tin tức / dữ liệu ngành → bỏ qua modifier tương ứng, KHÔNG suy diễn thay.
