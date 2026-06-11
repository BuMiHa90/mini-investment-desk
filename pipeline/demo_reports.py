"""Bao cao mau (demo) de xem truoc giao dien — noi dung mo phong output that
cua agent 01-03 theo boi canh thi truong 11/06/2026. Khong phai du lieu tu van."""

DEMO = {
    "01": """# MARKET REGIME REPORT — 11/06/2026

## Scorecard

| Trụ cột | Trọng số | Điểm (-2..+2) | Căn cứ chính (1 dòng) |
|---|---|---|---|
| Trend | 25% | -1 | Dưới MA20 (1.858) và MA50 (1.831), còn trên MA200 (1.749); đỉnh–đáy thấp dần từ 1.933 |
| Breadth | 20% | 0 | 168 tăng / 145 giảm — cân bằng, chưa lan tỏa (nguồn: tổng kết phiên CafeF) |
| Liquidity | 20% | -1 | Khối lượng 56,5% trung bình 20 phiên — cạn kiệt rõ rệt |
| Flows | 15% | -1 | Khối ngoại bán ròng ~-540 tỷ, lũy kế 5 phiên ~-7.000 tỷ tập trung trụ |
| Volatility/Phái sinh | 10% | -1 | Basis F1M chiết khấu ~-8 điểm |
| Macro/Sentiment | 10% | 0 | Fed giữ lãi suất; tỷ giá còn căng; tâm lý thận trọng đứng ngoài |
| **Composite** | | **-0,70** | |

## Kết luận

- **Trạng thái thị trường chính:** Risk-off / Downtrend ngắn hạn — đang trong nhịp hồi kỹ thuật
- **Trạng thái phụ:** Bull trap risk — phiên hồi 10/6 nhờ trụ kéo, thanh khoản dưới 70% trung bình
- **Mức độ tự tin:** Trung bình — đủ trường bắt buộc nhưng tín hiệu trái chiều giữa Trend và Breadth
- **So với phiên trước:** Giữ nguyên — 1 phiên xanh đơn lẻ không đủ điều kiện nâng regime

## Dữ liệu ủng hộ

- VN-Index 1.798,61 (-0,28%), mất lại mốc 1.800 trong phiên
- Giảm 6,59% trong 20 phiên từ đỉnh lịch sử 1.933 (19/5)
- Khối lượng khớp chỉ 410 triệu đơn vị = 56,5% trung bình 20 phiên
- Khối ngoại bán ròng phiên thứ 6 liên tiếp

## Dữ liệu chưa xác nhận / còn thiếu

- GTGD khớp lệnh tách thỏa thuận — dùng khối lượng tổng làm proxy, có thể lệch
- Số mã trần/sàn chính xác — chưa tìm được nguồn cập nhật sau 15h30

## Rủi ro chính trong ngày

- Nhịp hồi tắt thanh khoản → quay lại kiểm định đáy 1.780; thủng kèm khối lượng là tín hiệu xấu
- Đáo hạn phái sinh 18/6 có thể gây biến động trụ VN30

## Khuyến nghị khung (không phím mã)

- **Tỷ trọng cổ phiếu tham khảo:** 10–30%, không margin
- **Chiến thuật phù hợp:** Chờ xác nhận; tận dụng nhịp hồi để hạ tỷ trọng/margin
- **Chiến thuật nên tránh:** Mua đuổi phiên hồi; bắt đáy bằng margin; breakout

## Điều kiện chuyển trạng thái

- **Nâng regime khi:** Lấy lại 1.830 (MA50) với khớp lệnh >100% trung bình 20 phiên VÀ breadth >250 mã tăng, giữ được 2 phiên
- **Hạ regime khi:** Thủng 1.780 kèm khối lượng >120% trung bình, hoặc >30 mã sàn

## Cảnh báo cho broker

- Khách dễ hiểu nhầm phiên hồi lấy lại 1.800 là "tạo đáy xong". Chưa có bằng chứng dòng tiền — hồi trong downtrend với thanh khoản cạn là setup bull trap kinh điển. Không để khách FOMO.

## Handoff cho Strategy Selector

- **Regime code:** TECH_BOUNCE
- **Trạng thái phụ:** BULL_TRAP_RISK
- **Exposure band:** 10–30%
- **Margin:** forbidden
- **Ràng buộc chiến lược:** chỉ chiến lược phòng thủ, cấm mua đuổi, cấm breakout
""",
    "02": """# STRATEGY SELECTION REPORT — 11/06/2026

## Market regime đầu vào

- **Regime code:** TECH_BOUNCE
- **Trạng thái phụ:** BULL_TRAP_RISK
- **Confidence:** Trung bình
- **Exposure band / Margin:** 10–30% / forbidden

## Chiến thuật chính hôm nay

- **WAIT — Không giao dịch / chờ xác nhận** (Risk Tier 0)

## Vì sao chọn chiến thuật này

- Sub-state BULL_TRAP_RISK ghi đè regime chính → tra ma trận theo dòng thận trọng hơn: cấm toàn bộ chiến thuật mua mới
- Phiên hồi không có thanh khoản (56,5% trung bình) — không có bằng chứng dòng tiền quay lại
- Confidence Trung bình → loại mọi chiến thuật Tier 3 khỏi vị trí chính

## Chiến thuật phụ (nếu có)

- **DERISK — Giảm tỷ trọng / hạ margin:** dành cho khách đang kẹt hàng hoặc còn margin — tận dụng nhịp hồi về vùng 1.800–1.830 để đưa tỷ trọng về ≤30% và margin về 0

## Chiến thuật KHÔNG nên dùng (bị cấm hôm nay)

- **BREAKOUT:** không có nền tích lũy, mọi nhịp vượt kháng cự trong downtrend thanh khoản cạn đều rủi ro bull trap
- **PULLBACK_BUY:** không có uptrend để pullback — đây là hồi trong downtrend
- **MEAN_REVERSION:** chưa có tín hiệu cạn cung đo được; "đã giảm nhiều" không phải điều kiện kích hoạt
- **TREND_FOLLOW chiều mua:** ngược xu hướng chính

## Điều kiện được hành động (kích hoạt)

- Index lấy lại 1.830 (MA50) với khớp lệnh >100% trung bình 20 phiên, giữ 2 phiên liên tiếp
- Breadth >250 mã tăng/phiên và điểm tăng không dồn vào <5 mã trụ

## Điều kiện phải đứng ngoài / vô hiệu

- Thủng 1.780 kèm khối lượng tăng → chuyển hẳn sang DERISK/CASH, chờ tín hiệu panic/cạn cung
- Hồi tiếp nhưng thanh khoản vẫn <80% trung bình → tiếp tục WAIT, không nâng tỷ trọng

## Thời gian nắm giữ phù hợp

- Không mở vị thế mới. Việc hạ tỷ trọng (DERISK) thực hiện trong 1–3 phiên tới khi index trong vùng 1.800–1.830

## Tỷ trọng tham khảo

- Danh mục hiện có: đưa về ≤30%, ưu tiên giảm hàng yếu/beta cao trước. Vị thế mới: 0%

## Có nên dùng margin không

- **Không.** Margin forbidden từ regime — đặc biệt cấm bình quân giá bằng margin

## Loại khách phù hợp

- Tất cả các tệp khách đều phù hợp với WAIT; khách kẹt hàng/margin cao phù hợp với DERISK

## Loại khách KHÔNG phù hợp

- Không có — nhưng khách T+ chuyên nghiệp đòi "đánh hồi" phải được cảnh báo đây là setup rủi ro cao, lệnh nhỏ, tự chịu kỷ luật cắt 1–2%

## Cảnh báo cho broker

- Hôm nay câu hỏi nguy hiểm nhất từ khách là "thị trường xanh rồi, vào được chưa?". Câu trả lời: chưa — hồi không có tiền. Điều kiện vào lại rất cụ thể: 1.830 + khớp lệnh >100% trung bình + 2 phiên giữ được. Trước đó, mọi nhịp tăng là cơ hội GIẢM chứ không phải mua.

## Handoff

- **Strategy code:** WAIT
- **Secondary code:** DERISK
- **Cho Sector Rotation Agent:** chỉ chạy map quan sát — đánh dấu nhóm giữ giá tốt nhất để theo dõi; xếp hạng nhóm nên giảm trước cho khách kẹt hàng
- **Cho Stock Watchlist Agent:** KHÔNG chạy watchlist mua hôm nay; chỉ xuất danh sách "Nên tránh"
- **Exposure ceiling:** 30%
- **Margin:** forbidden
""",
    "03": """# SECTOR ROTATION REPORT — 11/06/2026

## Strategy Context

- **Strategy code đầu vào:** WAIT (phụ: DERISK)
- **Chế độ map:** Quan sát + xếp hạng nhóm nên giảm trước (không khuyến nghị mua)

## Sector Map

### Strong Sectors

| Ngành | RS (5p / 20p vs Index) | Flow | Ghi chú 1 dòng |
|---|---|---|---|
| — | — | — | Chế độ WAIT: không xếp nhóm Strong khuyến nghị mua |

### Improving Sectors

| Ngành | RS | Flow | Điều kiện xác nhận để lên Strong (đo được) |
|---|---|---|---|
| Điện | +1,2% / +2,8% vs Index | GTGD 95% TB20 | Giữ giá tốt nhất thị trường — theo dõi, chỉ xét khi regime nâng |
| Dược | +0,8% / +1,9% vs Index | GTGD 88% TB20 | Phòng thủ điển hình, thanh khoản mỏng — không phù hợp danh mục lớn |

### Weak Sectors

| Ngành | RS | Flow | Dấu hiệu rút tiền |
|---|---|---|---|
| Chứng khoán | -2,1% / -9,4% | GTGD 60% TB20 | Beta cao, giảm sâu hơn index, tiền rút rõ |
| Thép | -1,8% / -8,1% | GTGD 55% TB20 | Khối ngoại bán ròng HPG 4/5 phiên (bằng chứng dòng tiền, không phải khuyến nghị) |

### Avoid Chasing

| Ngành | Lý do định lượng | Rủi ro nếu mua đuổi |
|---|---|---|
| BĐS (nhóm trụ V) | Hồi +3% trong 2 phiên nhưng 80% mức tăng từ 1 trụ; GTGD ngành 70% TB20 | Trụ ngừng kéo là mất hết mức tăng — đúng cấu trúc bull trap của regime |

## Evidence

- Toàn bộ 10 nhóm theo dõi đều có GTGD dưới trung bình 20 phiên — không nhóm nào đạt Flow+
- Điện/dược giữ giá tốt nhất nhưng là phòng thủ co cụm, không phải dòng tiền mới vào
- Thứ tự ưu tiên GIẢM cho khách kẹt hàng: chứng khoán → thép → BĐS đầu cơ (beta cao, thanh khoản kém trước)

## Risks

- Map dựa trên dữ liệu hồi phục mới 2 phiên — phân hóa có thể đảo nhanh quanh đáo hạn phái sinh 18/6
- Thiếu dữ liệu tự doanh theo ngành → trục Flow chỉ dựa khối ngoại + GTGD

## Handoff To Stock Watchlist

- **Preferred sector filters:** KHÔNG có — chế độ WAIT, không chạy watchlist mua
- **Excluded sector filters:** Toàn bộ; đặc biệt BĐS trụ kéo (avoid chasing), chứng khoán/thép (weak)
- **Liquidity note:** Toàn thị trường thanh khoản cạn — mọi lệnh lớn đều khó khớp giá tốt
- **Missing data:** Tự doanh theo ngành; độ rộng nội ngành chỉ ước tính từ tổng kết phiên
""",
}
