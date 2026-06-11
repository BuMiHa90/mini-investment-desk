# Changelog

## v0.2 — 2026-06-11
- Xây dựng phương pháp luận đầy đủ theo mô hình Risk Regime Desk của quỹ lớn: scorecard 6 trụ cột có trọng số (Trend 25%, Breadth 20%, Liquidity 20%, Flows 15%, Volatility 10%, Macro/Sentiment 10%) thay cho phân loại cảm tính.
- Thêm mapping Composite Score → regime → exposure band + trạng thái margin.
- Thêm quy tắc hysteresis "hạ nhanh, nâng chậm" chống nhiễu và quy tắc định lượng cho Bull trap risk / Panic selling.
- Viết PROMPT.md hoàn chỉnh (trước đó là TODO), chuẩn hóa OUTPUT_TEMPLATE.md có Handoff block cho Strategy Selector.
- Mở rộng INPUT_SCHEMA.md theo 6 trụ cột, thêm nguồn dữ liệu miễn phí và quy tắc fallback khi thiếu dữ liệu.
- Điền 5 test cases (gồm 1 case dùng dữ liệu thật phiên 10–11/06/2026) + anti-pattern checklist.

## v0.1
- Created initial folder and file structure.
