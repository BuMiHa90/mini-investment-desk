# Test Cases — Sector Rotation Agent v0.2

Agent đạt khi: xếp loại đúng theo ma trận RS × Flow, nhóm Avoid Chasing đầy đủ và có lý do định lượng, hành vi đúng theo strategy code, không vi phạm quy tắc cứng.

---

## Test Case 1 — Phân hóa, chiến thuật SECTOR_ROTATION

**Input:**
- Handoff 02: strategy SECTOR_ROTATION, directive "tìm nhóm giữ tiền, xác nhận bằng dòng tiền", exposure ceiling 50%, margin restricted
- BĐS: +3,2%/5p (Index +0,4%), +5,1%/20p (Index -1,0%); GTGD 150% TB20; 9/15 mã tăng — NHƯNG VIC chiếm 80% mức tăng ngành
- Bán lẻ: +2,1%/5p, +3,0%/20p; GTGD 125% TB20; 7/9 mã tăng; ngoại mua ròng nhẹ
- Chứng khoán: +1,8%/5p nhưng -2,0%/20p; GTGD 130% TB20; 18/25 mã tăng
- Ngân hàng: -1,2%/5p, -2,5%/20p; GTGD 70% TB20; ngoại bán ròng MBB, VPB

**Expected:**
- Bán lẻ → **Strong** (RS+ cả 2 khung, Flow+ thật, độ rộng tốt)
- BĐS → **Avoid Chasing** (mức tăng dồn vào 1 trụ — dù RS+ Flow+ vẫn phải gắn nhãn)
- Chứng khoán → **Improving** (RS trái chiều 2 khung, Flow+) kèm điều kiện xác nhận đo được để lên Strong
- Ngân hàng → **Weak / bị rút tiền** (RS- + Flow- + ngoại bán)
- Nhắc VIC/MBB chỉ làm bằng chứng dòng tiền, có ghi chú không phải khuyến nghị

## Test Case 2 — Risk-off, chiến thuật DERISK

**Input:**
- Handoff 02: strategy DERISK, exposure ceiling 30%, margin forbidden
- Đa số ngành RS- Flow-; thép beta cao giảm mạnh nhất, thanh khoản cạn; điện/dược giữ giá tốt nhất

**Expected:**
- Chế độ map: **Đảo chiều — xếp hạng nhóm nên GIẢM TRƯỚC** (thép và nhóm beta cao, thanh khoản kém đứng đầu danh sách giảm)
- Nhóm giữ giá (điện, dược) ghi nhận là nơi "đỡ" danh mục, KHÔNG khuyến nghị mua mới
- Không có nhóm Strong khuyến nghị mua trong báo cáo
- Handoff cho 04: excluded = gần như toàn bộ; preferred = rỗng hoặc chỉ quan sát

## Test Case 3 — Chiến thuật WAIT

**Input:**
- Handoff 02: strategy WAIT (confidence regime Thấp), directive "không cần chạy watchlist hôm nay"

**Expected:**
- Chỉ xuất **map quan sát**: nhóm giữ giá tốt nhất để theo dõi, ghi rõ KHÔNG hành động
- Không có khuyến nghị mua/giảm nào
- Handoff cho 04 ghi rõ: không chạy watchlist, chờ chiến thuật mới

## Test Case 4 — Tăng giá không có dòng tiền (bẫy xếp loại)

**Input:**
- Handoff 02: strategy PULLBACK_BUY
- Dầu khí: +4%/5p vượt index NHƯNG GTGD chỉ 60% TB20, 3/10 mã tăng, mức tăng dồn vào GAS

**Expected:**
- Dầu khí → **Avoid Chasing** (tăng rỗng ruột: RS+ nhưng Flow-), KHÔNG được vào Strong
- Lý do định lượng đầy đủ: GTGD 60% TB20, độ rộng 3/10, 1 trụ kéo

## Test Case 5 — Thiếu dữ liệu Flow

**Input:**
- Handoff 02: strategy SECTOR_ROTATION
- Chỉ có hiệu suất ngành 5/20 phiên; không có GTGD ngành, không độ rộng, không dòng ngoại

**Expected:**
- Chỉ dùng trục RS; KHÔNG có nhóm Strong nào (tối đa Improving)
- Data gaps ghi rõ: thiếu toàn bộ trục Flow → map độ tin cậy thấp
- Handoff cho 04: yêu cầu xác nhận thanh khoản ở cấp cổ phiếu trước khi đưa vào nhóm hành động

---

## Anti-pattern checklist (mọi case đều phải pass)

- [ ] Không có tên cổ phiếu dưới dạng khuyến nghị (chỉ làm bằng chứng dòng tiền, có ghi chú)
- [ ] Không kết luận Strong khi thiếu Flow hoặc chỉ có 1 phiên dữ liệu
- [ ] Mục Avoid Chasing có mặt trong mọi báo cáo có khuyến nghị
- [ ] Mỗi xếp loại có số liệu RS + Flow tra ngược được
- [ ] Hành vi đúng theo strategy code (WAIT→quan sát, DERISK→đảo chiều)
- [ ] Đúng format `OUTPUT_TEMPLATE.md`, có Handoff To Stock Watchlist
