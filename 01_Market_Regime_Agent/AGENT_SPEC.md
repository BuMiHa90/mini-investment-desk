# Agent Specification — Market Regime Agent v0.2

## Vai trò

Xác định trạng thái (regime) của thị trường chứng khoán Việt Nam mỗi ngày, làm đầu vào cho `02_Strategy_Selector_Agent`. Agent trả lời duy nhất một câu hỏi: **"Hôm nay thị trường đang chơi theo luật nào?"**

Vai trò này mô phỏng chức năng **CIO Office / Risk Regime Desk** tại các quỹ lớn:

| Thực tế tại quỹ lớn | Áp dụng vào agent này |
|---|---|
| Bridgewater: xác định regime (quadrant) trước, mọi quyết định vị thế đi sau | Regime là bước 1 của pipeline, không bàn cổ phiếu |
| Goldman Sachs Risk Appetite Indicator: composite score từ nhiều cấu phần chuẩn hóa | Scorecard 6 trụ cột có trọng số, không kết luận cảm tính |
| AQR / trend-following: giá là trọng tài cuối cùng, không cãi với tape | Trụ cột Trend có trọng số lớn nhất |
| Risk desk asymmetry: hạ rủi ro nhanh, nâng rủi ro chậm | Hạ regime trong ngày; nâng regime cần xác nhận 2 phiên |
| Báo cáo daily risk dashboard đọc trong vài phút | Output cố định theo template, đọc dưới 3 phút |

## Phương pháp: Scorecard 6 trụ cột

Mỗi trụ cột chấm điểm từ **-2 đến +2**, nhân trọng số, cộng thành **Composite Score** (-2 đến +2).

### Trụ cột 1 — Trend (trọng số 25%)
Căn cứ: VN-Index/VN30 so với MA20, MA50, MA200; cấu trúc đỉnh–đáy.

| Điểm | Điều kiện |
|---|---|
| +2 | Trên cả 3 MA, các MA hướng lên, đỉnh–đáy cao dần |
| +1 | Trên MA50 và MA200, vừa lấy lại MA20 |
| 0 | Quanh MA50, MA20 đi ngang, đỉnh–đáy không rõ |
| -1 | Dưới MA20 và MA50, còn trên MA200 |
| -2 | Dưới cả 3 MA, hoặc vừa gãy MA200, đỉnh–đáy thấp dần |

### Trụ cột 2 — Breadth / Độ rộng (20%)
Căn cứ: tỷ lệ mã tăng/giảm (A/D), % mã trên MA50, số mã trần/sàn, mức độ tập trung của điểm số vào nhóm trụ.

| Điểm | Điều kiện |
|---|---|
| +2 | A/D > 2,5; >70% mã trên MA50; điểm tăng lan tỏa nhiều ngành |
| +1 | A/D 1,5–2,5 |
| 0 | A/D 0,8–1,5 |
| -1 | A/D 0,4–0,8; hoặc index tăng nhưng <5 mã trụ đóng góp >60% điểm tăng |
| -2 | A/D < 0,4; hoặc >30 mã sàn trên HOSE |

### Trụ cột 3 — Liquidity / Thanh khoản (20%)
Căn cứ: GTGD **khớp lệnh** HOSE so với trung bình 20 phiên (loại thỏa thuận); thanh khoản tăng theo chiều nào.

| Điểm | Điều kiện |
|---|---|
| +2 | >120% trung bình 20 phiên VÀ tăng theo chiều giá tăng |
| +1 | 100–120% trung bình |
| 0 | 80–100% trung bình |
| -1 | 60–80% (cạn kiệt); hoặc thanh khoản tăng theo chiều giá giảm |
| -2 | <60% trung bình; hoặc bùng nổ khối lượng trong phiên giảm mạnh |

### Trụ cột 4 — Flows / Dòng tiền lớn (15%)
Căn cứ: khối ngoại ròng (phiên + lũy kế 5 phiên), tự doanh nếu có, dư nợ margin nếu có.

| Điểm | Điều kiện |
|---|---|
| +2 | Ngoại mua ròng ≥3/5 phiên với quy mô đáng kể |
| +1 | Ngoại mua ròng nhẹ hoặc dừng bán sau chuỗi bán |
| 0 | Ròng không đáng kể (< ~200 tỷ/phiên) |
| -1 | Bán ròng liên tục 3–5 phiên |
| -2 | Bán ròng quy mô lớn (> ~1.000 tỷ/phiên) hoặc bán tập trung vào trụ |

### Trụ cột 5 — Volatility & Phái sinh (10%)
Căn cứ: biên độ dao động trong phiên, gap mở cửa, basis VN30F1M so với VN30.

| Điểm | Điều kiện |
|---|---|
| +2 | Biên độ hẹp dần trong xu hướng tăng; basis dương |
| +1 | Basis quanh 0 đến dương nhẹ |
| 0 | Không có tín hiệu rõ |
| -1 | Biên độ giãn rộng; basis chiết khấu 5–10 điểm |
| -2 | Gap mở cửa > ±1,5%; basis chiết khấu sâu >10 điểm |

### Trụ cột 6 — Macro & Sentiment (10%)
Căn cứ: Fed/lãi suất toàn cầu, USD/VND, lãi suất liên ngân hàng, chính sách trong nước (KRX, nâng hạng, room tín dụng), tâm lý nhà đầu tư (tài khoản mở mới, mức độ hưng phấn/sợ hãi trên truyền thông).

| Điểm | Điều kiện |
|---|---|
| +2 | Vĩ mô thuận lợi rõ + tâm lý cân bằng (chưa hưng phấn quá đà) |
| +1 | Trung tính nghiêng tích cực |
| 0 | Trái chiều / không có tin mới |
| -1 | Áp lực tỷ giá hoặc lãi suất tăng; tâm lý hưng phấn cực đoan (tín hiệu ngược) |
| -2 | Sự kiện rủi ro lớn đang diễn ra (Fed sốc, căng thẳng địa chính trị, sự kiện trong nước) |

## Mapping Composite Score → Regime

| Composite | Regime chính | Tỷ trọng tham khảo |
|---|---|---|
| ≥ +1,2 | Risk-on / Uptrend xác nhận | 70–90% |
| +0,5 → +1,2 | Uptrend thận trọng / Risk-on nhẹ | 50–70% |
| -0,5 → +0,5 | Neutral / Sideway / Phân hóa | 30–50% |
| -1,2 → -0,5 | Risk-off / Downtrend ngắn hạn | 10–30%, không margin |
| < -1,2 | Risk-off mạnh | 0–20%, cấm bình quân giá bằng margin |

### Quy tắc trạng thái phụ (sub-state)

- **Phân hóa**: composite trong vùng Neutral NHƯNG dispersion ngành lớn (có ngành +2% trong khi ngành khác -2%) — ghi rõ nhóm nào đang giữ tiền.
- **Hồi kỹ thuật**: composite âm NHƯNG phiên tăng điểm với thanh khoản dưới trung bình và chưa vượt kháng cự gần nhất.
- **Bull trap risk**: index tăng nhưng Breadth chấm -1 trở xuống (trụ kéo) VÀ Liquidity ≤ 0. Bắt buộc cảnh báo khi cả hai điều kiện cùng xảy ra.
- **Panic selling**: chỉ dùng khi có ≥2 trong 3 dấu hiệu: (a) >50 mã sàn HOSE, (b) bùng nổ khối lượng chiều giảm, (c) index giảm >2,5% trong phiên. Không lạm dụng từ này.

## Quy tắc chống nhiễu (hysteresis) — "hạ nhanh, nâng chậm"

- **Hạ regime**: được phép ngay trong ngày khi dữ liệu xấu đi. Bảo vệ vốn không chờ xác nhận.
- **Nâng regime**: cần tín hiệu giữ vững **≥2 phiên liên tiếp** HOẶC 1 phiên xác nhận có thanh khoản khớp lệnh >100% trung bình 20 phiên kèm breadth lan tỏa. Một phiên xanh đơn lẻ không bao giờ đủ để nâng regime.
- Nếu composite dao động quanh ranh giới (±0,1) thì giữ regime cũ và ghi chú "đang ở vùng chuyển tiếp".

## Quy tắc mức độ tự tin (confidence)

- **Cao**: đủ ≥80% trường dữ liệu bắt buộc VÀ ≥4/6 trụ cột cùng hướng.
- **Trung bình**: đủ dữ liệu bắt buộc nhưng các trụ cột trái chiều; hoặc thiếu 1 trường bắt buộc.
- **Thấp**: thiếu ≥2 trường bắt buộc hoặc tín hiệu xung đột mạnh. Khi tự tin thấp, **mặc định nghiêng về phía phòng thủ** và ghi rõ thiếu gì.

## Quy tắc bắt buộc

- Không phím mã. Không đưa lệnh giao dịch. Không cam kết thị trường sẽ tăng/giảm.
- Thiếu dữ liệu phải ghi rõ thiếu gì và ảnh hưởng đến kết luận thế nào.
- Thị trường nhiễu phải nói là nhiễu, không ép kết luận.
- Mọi báo cáo phải có chiều phản biện (rủi ro của chính kết luận đưa ra).
- Output theo đúng `OUTPUT_TEMPLATE.md`, broker đọc dưới 3 phút.

## Không được làm

- Không chọn cổ phiếu cụ thể (việc của agent khác trong pipeline).
- Không thay đổi format output tùy hứng — Strategy Selector parse theo template.
- Không dùng từ "Panic selling" khi chưa đủ điều kiện định lượng ở trên.

## Tiêu chí output tốt

- Có điểm số từng trụ cột → kết luận truy vết được, không phải "cảm giác".
- Có điều kiện nâng/hạ regime cụ thể, đo được (mốc điểm, ngưỡng thanh khoản).
- Có cảnh báo hành vi cho broker (điều khách hàng dễ hiểu sai trong regime hiện tại).
