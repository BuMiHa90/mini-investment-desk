# 01 Market Regime Agent

Bước 1 của Mini Investment Desk: xác định **trạng thái thị trường** trước khi chọn chiến thuật. Agent này trả lời duy nhất câu hỏi *"Hôm nay thị trường đang chơi theo luật nào?"* — không chọn cổ phiếu, không đưa khuyến nghị giao dịch.

## Mô hình tham chiếu

Thiết kế mô phỏng vai trò **Risk Regime Desk / CIO Office** tại quỹ lớn:

- **Regime trước, vị thế sau** (Bridgewater): output của agent này là ràng buộc đầu vào cho mọi quyết định phía sau.
- **Composite score thay vì cảm tính** (Goldman Risk Appetite Indicator): 6 trụ cột có trọng số — Trend 25%, Breadth 20%, Liquidity 20%, Flows 15%, Volatility/Phái sinh 10%, Macro/Sentiment 10%.
- **Giá là trọng tài cuối** (AQR/trend-following): trụ Trend trọng số lớn nhất.
- **Hạ nhanh, nâng chậm** (risk desk asymmetry): hạ regime ngay trong ngày; nâng regime cần xác nhận 2 phiên hoặc phiên bùng nổ thanh khoản.

## Cấu trúc thư mục

| File | Vai trò |
|---|---|
| `AGENT_SPEC.md` | Phương pháp luận đầy đủ: thang điểm 6 trụ cột, mapping regime, quy tắc hysteresis và confidence |
| `PROMPT.md` | System prompt hoàn chỉnh, dán vào model là chạy |
| `INPUT_SCHEMA.md` | Trường dữ liệu đầu vào, bắt buộc/tùy chọn, nguồn miễn phí, quy tắc fallback |
| `OUTPUT_TEMPLATE.md` | Format báo cáo cố định để `02_Strategy_Selector_Agent` parse |
| `TEST_CASES.md` | 5 ca kiểm thử + anti-pattern checklist |
| `CHANGELOG.md` | Lịch sử phiên bản |

## Cách chạy

1. Dán nội dung `PROMPT.md` làm system prompt.
2. Dán khối dữ liệu theo `INPUT_SCHEMA.md` làm message (sau 15h30 lấy từ bài tổng kết phiên sẽ đủ trường nhất).
3. Nếu không có dữ liệu: agent tự thu thập từ nguồn công khai (cần web access) và ghi rõ nguồn + độ trễ.
4. Output là `MARKET REGIME REPORT` — phần `Handoff` cuối báo cáo (regime code, exposure band, trạng thái margin) là input của agent 02.

## Nguyên tắc bất biến

Ưu tiên bảo vệ vốn khi không rõ xu hướng. Thiếu dữ liệu phải nói thiếu. Thị trường nhiễu phải nói nhiễu. Không phím mã, không cam kết hướng thị trường. Báo cáo đọc dưới 3 phút.
