# Output Template — MARKET REGIME REPORT

Format cố định. `02_Strategy_Selector_Agent` parse theo đúng các heading dưới đây — không đổi tên trường, không thêm bớt mục.

---

# MARKET REGIME REPORT — [dd/mm/yyyy]

## Scorecard

| Trụ cột | Trọng số | Điểm (-2..+2) | Căn cứ chính (1 dòng) |
|---|---|---|---|
| Trend | 25% | | |
| Breadth | 20% | | |
| Liquidity | 20% | | |
| Flows | 15% | | |
| Volatility/Phái sinh | 10% | | |
| Macro/Sentiment | 10% | | |
| **Composite** | | **[-2..+2]** | |

## Kết luận

- **Trạng thái thị trường chính:** [regime theo bảng mapping]
- **Trạng thái phụ (nếu có):** [Phân hóa / Hồi kỹ thuật / Bull trap risk / Panic selling — kèm lý do 1 dòng]
- **Mức độ tự tin:** [Thấp / Trung bình / Cao — kèm lý do theo quy tắc confidence]
- **So với phiên trước:** [Giữ nguyên / Nâng / Hạ — nếu nâng phải nêu xác nhận 2 phiên hoặc phiên bùng nổ]

## Dữ liệu ủng hộ

- [3–5 gạch đầu dòng, có số liệu cụ thể]

## Dữ liệu chưa xác nhận / còn thiếu

- [Trường nào thiếu, ảnh hưởng gì đến kết luận]

## Rủi ro chính trong ngày

- [1–2 rủi ro lớn nhất, kèm kịch bản cụ thể nếu xảy ra]

## Khuyến nghị khung (không phím mã)

- **Tỷ trọng cổ phiếu tham khảo:** [band theo mapping, ghi rõ có/không margin]
- **Chiến thuật phù hợp:** [2–3 gạch đầu dòng]
- **Chiến thuật nên tránh:** [2–3 gạch đầu dòng]

## Điều kiện chuyển trạng thái

- **Nâng regime khi:** [điều kiện đo được: mốc điểm + ngưỡng thanh khoản + breadth]
- **Hạ regime khi:** [điều kiện đo được]

## Cảnh báo cho broker

- [Điều khách hàng dễ hiểu sai nhất trong regime hiện tại — 1–3 câu]

## Handoff cho Strategy Selector

- **Regime code:** [RISK_ON / UPTREND_CAUTIOUS / NEUTRAL / SIDEWAY / DIVERGENT / TECH_BOUNCE / BULL_TRAP_RISK / RISK_OFF / DOWNTREND_ST / PANIC]
- **Exposure band:** [vd 30–50%]
- **Margin:** [allowed / restricted / forbidden]
- **Ràng buộc chiến lược:** [vd: chỉ chiến lược phòng thủ, không breakout]
