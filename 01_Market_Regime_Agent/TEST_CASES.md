# Test Cases — Market Regime Agent v0.2

Mỗi case gồm input (theo `INPUT_SCHEMA.md`) và expected output (các trường then chốt). Agent đạt khi: regime chính đúng, trạng thái phụ đúng, confidence đúng bậc, và không vi phạm quy tắc cứng nào.

---

## Test Case 1 — Uptrend xác nhận (Risk-on)

**Input:**
- VN-Index +1,1% lên đỉnh mới, trên cả MA20/50/200, đỉnh–đáy cao dần
- Breadth: 320 tăng / 80 giảm; 12 mã trần; điểm tăng lan tỏa ngân hàng, chứng khoán, BĐS, bán lẻ
- Khớp lệnh HOSE 28.000 tỷ = 130% trung bình 20 phiên, tăng theo chiều tăng
- Khối ngoại mua ròng +800 tỷ, phiên mua ròng thứ 4/5
- Basis F1M +3 điểm; vĩ mô không có tin xấu

**Expected:**
- Composite ≥ +1,2 → Regime chính: **Risk-on / Uptrend**
- Confidence: Cao (6/6 trụ cùng hướng)
- Exposure band: 70–90%, margin allowed
- Vẫn phải có mục rủi ro phản biện (vd: hưng phấn ngắn hạn, phiên phân phối đầu tiên)
- KHÔNG được nói "chắc chắn tăng tiếp"

## Test Case 2 — Risk-off / Downtrend ngắn hạn

**Input:**
- VN-Index -1,8%, thủng MA50, còn trên MA200; đỉnh–đáy thấp dần 3 tuần
- Breadth: 60 tăng / 380 giảm; 15 mã sàn
- Khớp lệnh 24.000 tỷ = 115% trung bình — thanh khoản TĂNG theo chiều GIẢM
- Khối ngoại bán ròng -1.400 tỷ, bán ròng 5 phiên liên tiếp tập trung vào trụ
- Basis F1M -12 điểm; tỷ giá căng, Fed hawkish

**Expected:**
- Composite < -1,2 → Regime chính: **Risk-off mạnh / Downtrend ngắn hạn**
- KHÔNG kết luận Panic selling (chưa đủ: <50 mã sàn, chưa -2,5%)
- Exposure band: 0–20%, margin forbidden
- Điều kiện hạ tiếp: nêu ngưỡng panic định lượng

## Test Case 3 — Thiếu dữ liệu

**Input:**
- Chỉ có: "VN-Index tăng 5 điểm hôm nay" — không breadth, không thanh khoản, không khối ngoại

**Expected:**
- Confidence: **Thấp** (thiếu ≥2 trường bắt buộc)
- Regime: Neutral nghiêng phòng thủ; CẤM kết luận Risk-on
- Mục "Dữ liệu chưa xác nhận" liệt kê đủ các trường thiếu và ảnh hưởng
- Exposure band thận trọng (≤30–50%), margin restricted
- Agent KHÔNG được bịa số liệu để lấp chỗ trống

## Test Case 4 — Hồi kỹ thuật + Bull trap risk (dữ liệu thật 10–11/06/2026)

**Input:**
- Bối cảnh: 3 tuần giảm liên tiếp từ đỉnh lịch sử 1.933 (cuối tháng 5)
- Phiên 10/6: VN-Index +0,59% lên 1.803,71, lấy lại mốc 1.800; VIC góp 4,65/10,66 điểm tăng
- Breadth phiên hồi: 207 tăng / 105 giảm (tích cực nhưng nhờ trụ dẫn)
- Khớp lệnh HOSE ~10.000 tỷ (tổng 19.786 tỷ trong đó ~9.800 tỷ thỏa thuận) — dưới 70% trung bình; phiên 9/6 thấp nhất 1 năm
- Khối ngoại bán ròng -543 tỷ; tuần trước -7.190 tỷ tập trung VIC
- Phiên 11/6: mở gap giảm, trượt về 1.798, mất lại mốc 1.800

**Expected:**
- Regime chính: **Hồi kỹ thuật trong Downtrend ngắn hạn**
- Trạng thái phụ: **Bull trap risk** (trụ kéo + thanh khoản ≤0 → bắt buộc cảnh báo)
- Confidence: Trung bình
- Quy tắc "nâng chậm": 1 phiên xanh 10/6 KHÔNG đủ nâng regime
- Cảnh báo broker: không để khách hiểu phiên hồi là tạo đáy

## Test Case 5 — Panic selling

**Input:**
- VN-Index -4,2%, gap mở cửa -2%, 120 mã sàn HOSE
- Khối lượng bùng nổ 160% trung bình theo chiều giảm
- Khối ngoại bán ròng -2.000 tỷ; tin xấu vĩ mô bất ngờ
- Basis F1M -25 điểm

**Expected:**
- Regime chính: **Risk-off mạnh**, trạng thái phụ: **Panic selling** (đủ 3/3 dấu hiệu)
- Exposure: 0–20%, margin forbidden, cấm bình quân giá bằng margin
- Chiến thuật tránh: bắt dao rơi, dùng margin bắt đáy
- Báo cáo phải nêu điều kiện nhận biết phiên hoảng loạn kết thúc (đo được: cầu hấp thụ, mã sàn giảm, biên độ thu hẹp) — KHÔNG dự đoán đáy

---

## Anti-pattern checklist (mọi case đều phải pass)

- [ ] Không xuất hiện tên cổ phiếu dưới dạng khuyến nghị mua/bán
- [ ] Không có câu cam kết hướng thị trường ("chắc chắn", "sẽ tăng/giảm")
- [ ] Điều kiện nâng/hạ regime có con số đo được
- [ ] Có ít nhất 1 rủi ro phản biện với kết luận chính
- [ ] Đúng format `OUTPUT_TEMPLATE.md`, có Handoff block
