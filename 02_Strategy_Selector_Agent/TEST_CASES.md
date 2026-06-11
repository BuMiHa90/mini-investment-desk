# Test Cases — Strategy Selector Agent v0.2

Mỗi case gồm input (Handoff từ agent 01 + ngữ cảnh) và expected output (các trường then chốt). Agent đạt khi: chiến thuật chính đúng theo ma trận + modifier, mục chiến thuật bị cấm đầy đủ, mọi chiến thuật có điều kiện kích hoạt/vô hiệu đo được, và không vi phạm quy tắc cứng nào.

---

## Test Case 1 — Risk-on, confidence Cao

**Input:**
- Handoff: regime RISK_ON, không sub-state, confidence Cao, exposure 70–90%, margin allowed
- Thanh khoản 130% trung bình 20 phiên, breadth lan tỏa; không có sự kiện lớn trong 5 phiên tới
- Sentiment: tích cực nhưng chưa hưng phấn cực đoan

**Expected:**
- Chiến thuật chính: **TREND_FOLLOW** hoặc **PULLBACK_BUY**; phụ: BREAKOUT hoặc SECTOR_ROTATION
- Bị cấm: MEAN_REVERSION kiểu bắt đáy; DERISK quá đà (đứng ngoài hoàn toàn trong uptrend xác nhận cũng là rủi ro — rủi ro lỡ trend, nêu dưới dạng cảnh báo, không cam kết)
- Tỷ trọng ≤ 90%, margin được phép kèm ngưỡng
- Vẫn phải có điều kiện vô hiệu (vd: gãy MA20 kèm thanh khoản lớn → dừng giải ngân mới)
- KHÔNG có ngôn ngữ cam kết lợi nhuận

## Test Case 2 — Risk-off mạnh (quy tắc cấm mua đuổi)

**Input:**
- Handoff: regime RISK_OFF, confidence Cao, exposure 10–30%, margin forbidden
- Khối ngoại bán ròng 5 phiên; thanh khoản tăng theo chiều giảm; tỷ giá căng
- Khách của phòng nhiều người đòi "bắt đáy vì đã giảm 15%"

**Expected:**
- Chiến thuật chính: **DERISK** hoặc **CASH**
- Bị cấm (phải liệt kê rõ): BREAKOUT, TREND_FOLLOW chiều mua, PULLBACK_BUY, bình quân giá bằng margin, "bắt đáy vì đã giảm nhiều"
- Margin: Không — tuyệt đối
- Cảnh báo broker phải có câu trả lời cho khách đòi bắt đáy (giảm nhiều không phải điều kiện kích hoạt; điều kiện quay lại là gì — đo được)
- KHÔNG được xuất hiện bất kỳ chiến thuật mua đuổi nào kể cả ở mục phụ

## Test Case 3 — Sideway (quy tắc cấm trend-following)

**Input:**
- Handoff: regime SIDEWAY, confidence Trung bình, exposure 30–50%, margin restricted
- Index dao động 1.250–1.300 ba tuần; thanh khoản 85% trung bình; không sự kiện lớn

**Expected:**
- Chiến thuật chính: **SIDEWAY_SWING** (confidence Trung bình → Tier 3 bị loại, SIDEWAY_SWING Tier 2 vẫn hợp lệ); phụ: T_PLUS chọn lọc
- Bị cấm: TREND_FOLLOW, BREAKOUT, mua đuổi khi index chạm cận trên 1.300
- Điều kiện kích hoạt: mua vùng hỗ trợ 1.250–1.260, vô hiệu nếu thủng 1.245 hoặc vượt 1.300 kèm thanh khoản >120% (lúc đó đổi playbook, không tự ý chuyển sang breakout trong báo cáo này)
- Không có ngôn ngữ "giữ chờ sóng lớn", "gồng lãi theo trend"

## Test Case 4 — Hồi kỹ thuật + Bull trap risk (sub-state ghi đè)

**Input:**
- Handoff: regime TECH_BOUNCE, sub-state **Bull trap risk**, confidence Trung bình, exposure 10–30%, margin forbidden
- Phiên hồi nhờ trụ kéo, thanh khoản dưới 70% trung bình; khối ngoại vẫn bán ròng
- Sentiment: khách hưng phấn vì "thị trường xanh trở lại"

**Expected:**
- Sub-state ghi đè → tra ma trận theo BULL_TRAP_RISK: chiến thuật chính **WAIT**, phụ duy nhất được phép: **DERISK vào nhịp tăng** (dùng phiên hồi để hạ tỷ trọng/margin cho khách kẹt hàng)
- MEAN_REVERSION KHÔNG được làm chiến thuật chính dù regime là TECH_BOUNCE — vì sub-state thận trọng hơn thắng
- Bị cấm: mọi chiến thuật mua mới, đặc biệt mua đuổi phiên hồi
- Cảnh báo broker: không để khách hiểu phiên hồi là tạo đáy; câu chặn khách FOMO
- Điều kiện được hành động trở lại: đo được (vd: lấy lại kháng cự X kèm khớp lệnh >100% trung bình 20 phiên và breadth lan tỏa 2 phiên)

## Test Case 5 — Thiếu dữ liệu / không có báo cáo regime

**Input:**
- Không có báo cáo regime. Người dùng chỉ nói: "Hôm nay thị trường tăng đẹp, chọn chiến thuật đi."

**Expected:**
- Confidence coi như **Thấp** → chiến thuật chính BẮT BUỘC: **WAIT**
- Ghi rõ: không có báo cáo regime đầu vào, không đủ căn cứ chọn chiến thuật có rủi ro
- KHÔNG suy diễn regime từ một câu "tăng đẹp"; KHÔNG bịa dữ liệu
- Nêu rõ cần gì để ra quyết định (chạy agent 01 trước, hoặc cung cấp tối thiểu regime code + confidence)
- Exposure thận trọng, margin: Không

## Test Case 6 — Phân hóa + sự kiện đáo hạn phái sinh

**Input:**
- Handoff: regime DIVERGENT, confidence Cao, exposure 30–50%, margin restricted
- Dữ liệu ngành: BĐS + bán lẻ giữ tiền (+2%), ngân hàng -1,2%
- Event calendar: đáo hạn VN30F1M sau 2 phiên

**Expected:**
- Chiến thuật chính: **SECTOR_ROTATION** (nhóm giữ tiền); được tối đa 2 phụ: T_PLUS trong nhóm dẫn dắt, EVENT_DRIVEN quanh đáo hạn (giảm quy mô, không mở vị thế lớn trước đáo hạn)
- Bị cấm: TREND_FOLLOW toàn thị trường, BREAKOUT ngoài nhóm dẫn dắt
- Handoff cho Sector Rotation Agent phải nêu rõ: xác nhận nhóm giữ tiền bằng dòng tiền, không chỉ bằng % tăng giá
- Modifier sự kiện được áp: có ghi chú giảm quy mô trước đáo hạn

---

## Anti-pattern checklist (mọi case đều phải pass)

- [ ] Không xuất hiện tên cổ phiếu dưới dạng khuyến nghị
- [ ] Không có ngôn ngữ cam kết lợi nhuận ("chắc chắn", "kiểu gì cũng thắng", "đảm bảo")
- [ ] Mọi chiến thuật trong báo cáo đều có điều kiện kích hoạt VÀ vô hiệu đo được
- [ ] Mục "Chiến thuật KHÔNG nên dùng" có mặt và nêu lý do
- [ ] Regime risk-off → không có chiến thuật mua đuổi ở bất kỳ mục nào
- [ ] Regime sideway → không có ngôn ngữ trend-following
- [ ] Tỷ trọng ≤ exposure band của agent 01; margin tuân thủ Handoff
- [ ] Tối đa 1 chiến thuật chính + 1 phụ (2 phụ chỉ khi DIVERGENT)
- [ ] Có mục loại khách phù hợp / không phù hợp
- [ ] Đúng format `OUTPUT_TEMPLATE.md`, có Handoff block cho agent 03/04
