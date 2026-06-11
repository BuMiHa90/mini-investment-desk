# Output Template — STRATEGY SELECTION REPORT

Format cố định. `03_Sector_Rotation_Agent` và `04_Stock_Watchlist_Agent` parse theo đúng các heading dưới đây — không đổi tên trường, không thêm bớt mục.

---

# STRATEGY SELECTION REPORT — [dd/mm/yyyy]

## Market regime đầu vào

- **Regime code:** [từ Handoff agent 01]
- **Trạng thái phụ:** [nếu có]
- **Confidence:** [Thấp / Trung bình / Cao]
- **Exposure band / Margin:** [vd 10–30% / forbidden]

## Chiến thuật chính hôm nay

- **[Mã chiến thuật] — [Tên chiến thuật]** (Risk Tier [0–3])

## Vì sao chọn chiến thuật này

- [2–4 gạch đầu dòng, tra ngược được về ma trận: regime X + confidence Y + modifier Z → chiến thuật này]

## Chiến thuật phụ (nếu có)

- **[Mã] — [Tên]:** [1 dòng phạm vi áp dụng — cho ai, quy mô nào]

## Chiến thuật KHÔNG nên dùng (bị cấm hôm nay)

- **[Mã] — [Tên]:** [vì sao bị cấm trong bối cảnh hiện tại — 1 dòng]
- [liệt kê đủ các chiến thuật nguy hiểm nhất với regime hiện tại, tối thiểu 2]

## Điều kiện được hành động (kích hoạt)

- [Điều kiện đo được: mốc index, % thanh khoản so trung bình 20 phiên, ngưỡng breadth — tối thiểu 2]

## Điều kiện phải đứng ngoài / vô hiệu

- [Điều kiện đo được khiến chiến thuật chính bị hủy — tối thiểu 2]

## Thời gian nắm giữ phù hợp

- [Theo thư viện chiến thuật, điều chỉnh theo bối cảnh]

## Tỷ trọng tham khảo

- [Không vượt Exposure band của agent 01; ghi rõ cho vị thế mới vs danh mục hiện có]

## Có nên dùng margin không

- [Không / Hạn chế (điều kiện cụ thể) / Được phép (kèm ngưỡng) — tuân thủ margin_status từ Handoff]

## Loại khách phù hợp

- [Chân dung cụ thể: tần suất theo dõi, kỷ luật cắt lỗ, khẩu vị rủi ro]

## Loại khách KHÔNG phù hợp

- [Chân dung cụ thể — broker dùng mục này để chặn khách]

## Cảnh báo cho broker

- [1–3 câu: điều khách dễ hiểu sai nhất hôm nay, câu nói nên dùng khi khách đòi làm điều bị cấm]

## Handoff

- **Strategy code:** [WAIT / CASH / DERISK / T_PLUS / SIDEWAY_SWING / PULLBACK_BUY / BREAKOUT / TREND_FOLLOW / SECTOR_ROTATION / MEAN_REVERSION / EVENT_DRIVEN]
- **Secondary code:** [mã hoặc NONE]
- **Cho Sector Rotation Agent:** [cần tìm nhóm ngành kiểu gì — vd: nhóm giữ tiền trong phân hóa / nhóm phòng thủ / không cần chạy hôm nay]
- **Cho Stock Watchlist Agent:** [tiêu chí lọc theo chiến thuật — vd: cổ phiếu còn uptrend chờ pullback về MA20 / KHÔNG chạy watchlist hôm nay]
- **Exposure ceiling:** [%, ≤ exposure band của agent 01]
- **Margin:** [allowed / restricted / forbidden]
