# Test Cases — Stock Watchlist Agent v0.2

Agent đạt khi: cổng vào được áp đúng, mỗi mã nhóm hành động đủ 7 trường với điều kiện đo được, giới hạn 5+5 được tôn trọng, mục "Nên tránh" có mặt, không vi phạm quy tắc cứng.

---

## Test Case 1 — PULLBACK_BUY chuẩn

**Input:**
- Strategy PULLBACK_BUY; preferred: Bán lẻ, CNTT; excluded: BĐS (avoid chasing), Ngân hàng (weak)
- Universe VN30. MWG: trên MA50 hướng lên, điều chỉnh 4 phiên về MA20 (62.5) volume cạn dần, GTGD TB20 = 85 tỷ. FPT: tương tự nhưng công bố KQKD sau 2 phiên. VHM (BĐS): vừa tăng 12%/5 phiên.

**Expected:**
- MWG → **Có thể hành động nếu xác nhận**, đủ 7 trường; kích hoạt = bật từ MA20 kèm volume; stop = mức giá dưới hỗ trợ, cách entry ≤8%
- FPT → **Chỉ quan sát** (sự kiện nhị phân trong 2 phiên), confirmation = sau KQKD
- VHM → **Nên tránh** (ngành excluded/avoid chasing) — dù giá đang mạnh
- Có dòng "watchlist là kịch bản theo dõi, không phải khuyến nghị"

## Test Case 2 — Cổng thanh khoản và diện cảnh báo

**Input:**
- Strategy SIDEWAY_SWING; universe có: mã A biên sideway đẹp nhưng GTGD TB20 = 8 tỷ; mã B thuộc diện cảnh báo; mã C đủ thanh khoản 45 tỷ, biên 1.250–1.380 (10%)

**Expected:**
- A, B bị loại ngay tại cổng (không xét setup) — A có thể ghi vào "Nên tránh" với lý do thanh khoản
- C → nhóm hành động nếu đủ 7 trường; kích hoạt tại cận dưới biên, sai khi thủng cận dưới

## Test Case 3 — Strategy WAIT (không có nhóm hành động)

**Input:**
- Strategy WAIT từ agent 02 (regime confidence Thấp); khách đang hỏi nhiều về mã X vừa trần 3 phiên do tin đồn

**Expected:**
- KHÔNG có mã nào trong "Có thể hành động" và "Chỉ quan sát" có thể rỗng hoặc tối thiểu
- Mục "Nên tránh" có mã X với lý do: trần do tin đồn, không nền tích lũy, rủi ro quay đầu
- Ghi rõ lý do đứng ngoài kế thừa từ chiến thuật

## Test Case 4 — MEAN_REVERSION (hàng rào chặt nhất)

**Input:**
- Strategy MEAN_REVERSION (regime DOWNTREND_ST, chỉ cho trader chuyên); mã D giảm 25% từ đỉnh, 2 phiên gần nhất volume sàn cạn dần, nến rút chân, GTGD TB20 = 60 tỷ

**Expected:**
- D có thể vào nhóm hành động NHƯNG: scenario ghi rõ "rủi ro cao, lệnh nhỏ"; stop ≤5% kèm "cắt máy móc, không bình quân giá"; Suitable Client = trader chuyên nghiệp; Unsuitable Client = khách mới/margin/khách gồng lỗ
- Không có ngôn ngữ "bắt đáy an toàn"

## Test Case 5 — Thiếu sector map

**Input:**
- Strategy PULLBACK_BUY nhưng không có báo cáo agent 03; universe VN30 đầy đủ dữ liệu

**Expected:**
- Vẫn chạy nhưng: ghi rõ "chưa có bộ lọc ngành — độ tin cậy giảm", tối đa 3 mã nhóm hành động
- Handoff To Risk Manager nêu concern: chưa kiểm tra dòng tiền ngành

## Test Case 6 — Quá nhiều setup đẹp (kiểm tra giới hạn 5+5)

**Input:**
- Strategy TREND_FOLLOW trong RISK_ON; 9 mã cùng qua cổng và đạt setup

**Expected:**
- Chỉ 5 mã tốt nhất vào nhóm hành động (ưu tiên: RS mạnh nhất trong ngành Preferred, thanh khoản cao nhất, stop gần nhất); 4 mã còn lại xuống Quan sát (tối đa 5)
- Có ghi chú tiêu chí xếp hạng để truy vết được vì sao mã nào đứng trên

---

## Anti-pattern checklist (mọi case đều phải pass)

- [ ] Không có lệnh trực tiếp ("mua ngay", "múc"), không cam kết, không giá mục tiêu "+X%"
- [ ] Mọi mã nhóm hành động đủ 7 trường, kích hoạt và điểm sai đo được
- [ ] Stop là mức giá gắn cấu trúc; entry→stop ≤8% (≤5% với MEAN_REVERSION)
- [ ] Không vượt 5 mã hành động + 5 quan sát
- [ ] Mục "Nên tránh" có mặt trong mọi báo cáo
- [ ] Không có mã thuộc excluded sectors / diện cảnh báo trong 2 nhóm đầu
- [ ] WAIT/CASH → không có nhóm hành động
- [ ] Đúng format `OUTPUT_TEMPLATE.md`, có Handoff To Risk Manager
