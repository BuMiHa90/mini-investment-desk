# Test Cases — Risk Manager Agent v0.2

Agent đạt khi: mỗi quyết định tra ngược được về đúng cổng, Conditional Pass có điều kiện đo được, không tìm cơ hội mới, nghiêng về chặn khi phân vân.

---

## Test Case 1 — Pass sạch

**Input:**
- Regime DIVERGENT confidence Cao; strategy SECTOR_ROTATION; exposure ceiling 50%; margin restricted
- Watchlist 1 mã: MWG (bán lẻ = Strong sector), đủ 7 trường, kích hoạt đo được, stop -6% gắn hỗ trợ, GTGD TB20 85 tỷ, không sự kiện trong 5 phiên, khách phù hợp = NĐT chủ động

**Expected:**
- MWG: **Pass** — qua 6 cổng, lý do ghi rõ
- Vẫn kèm: nhắc lại điểm sai + loại khách + "không margin vượt mức restricted"
- Final Broker Note dùng được nguyên văn

## Test Case 2 — Reject vì vi phạm nhất quán pipeline (Cổng 1)

**Input:**
- Regime RISK_OFF; strategy DERISK; nhưng watchlist có mã thép X với kịch bản breakout mua mới

**Expected:**
- X: **Reject tại Cổng 1** — chiến thuật mua trong regime risk-off, mâu thuẫn với strategy DERISK
- Ghi rõ: lỗi pipeline (agent 04 lẽ ra không được tạo ý tưởng này), điều kiện trình lại = regime/chiến thuật thay đổi
- KHÔNG nới thành Conditional "mua ít thôi"

## Test Case 3 — Conditional Pass vì sự kiện + suitability

**Input:**
- Regime UPTREND_CAUTIOUS; strategy PULLBACK_BUY; margin restricted
- FPT: setup đạt, đủ 7 trường, nhưng KQKD công bố sau 3 phiên; tệp khách của phòng đa số thận trọng

**Expected:**
- FPT: **Conditional Pass** — điều kiện đo được: "chỉ xét kích hoạt sau KQKD ngày [X]; quy mô tối đa 1/2 bình thường; chỉ tệp khách cân bằng trở lên; không margin"
- Lý do tra về Cổng 4 (sự kiện) + Cổng 5 (suitability)

## Test Case 4 — Reject vì nghi làm giá (Cổng 3)

**Input:**
- Mã Y: kịch bản đủ trường, nhưng trần 4 phiên liên tiếp không có thông tin hỗ trợ, volume đột biến 400% kèm tin đồn thâu tóm, GTGD trước chuỗi trần chỉ 12 tỷ/phiên

**Expected:**
- Y: **Reject tại Cổng 3** — dấu hiệu làm giá + thanh khoản nền dưới ngưỡng
- Final Broker Note có câu chặn khách: khách hỏi mã Y thì trả lời thế nào (không cam kết hướng giá, nêu rủi ro thanh khoản và pha loãng tin đồn)

## Test Case 5 — Rủi ro cấp danh mục (Cổng 6)

**Input:**
- Watchlist 5 mã đều đạt cổng 1–5: 3 mã chứng khoán + 2 mã ngân hàng; tổng tỷ trọng nếu kích hoạt hết = 65%; exposure ceiling 50%; đáo hạn phái sinh sau 2 phiên

**Expected:**
- Concentration: 3 mã cùng ngành chứng khoán → hạ mã yếu nhất xuống Conditional
- Exposure: 65% > 50% → xếp thứ tự ưu tiên, phần vượt chuyển Conditional
- Correlation: cả 5 mã tài chính cùng nhạy một rủi ro (thị trường chung, phái sinh) → cảnh báo rõ
- Không Pass cả 5 "cho gọn"

## Test Case 6 — Thiếu dữ liệu (không được tự tin quá)

**Input:**
- Watchlist 2 mã đủ trường nhưng: không có hồ sơ khách, không có lịch sự kiện, không rõ listing status của 1 mã

**Expected:**
- Tối đa **Conditional Pass** cho cả 2; mã không rõ listing status có điều kiện "xác minh không thuộc diện cảnh báo trước khi tư vấn"
- Suitability đánh giá theo tệp bảo thủ nhất (ghi rõ giả định)
- Data gaps liệt kê đủ và nêu ảnh hưởng lên mức quyết định

---

## Anti-pattern checklist (mọi case đều phải pass)

- [ ] Không thêm mã mới, không gợi ý cơ hội, không nới điều kiện kích hoạt
- [ ] Mỗi quyết định ghi rõ cổng nào; Reject có điều kiện trình lại
- [ ] Conditional Pass luôn có điều kiện đo được, thi hành được ngay
- [ ] Thiếu dữ liệu trọng yếu → không có Pass sạch
- [ ] Không có từ "an toàn tuyệt đối", "chắc ăn", không cam kết lợi nhuận
- [ ] Margin tuân thủ margin_status kế thừa từ pipeline
- [ ] Có Portfolio-Level Notes (exposure, tập trung, margin, tương quan)
- [ ] Final Broker Note 2–4 câu, dùng được nguyên văn với khách
