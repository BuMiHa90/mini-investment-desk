# Changelog

## v0.3
- Bổ sung quản trị rủi ro vi mô VN (từ deep-research report TTCK VN):
  - **Rủi ro kẹt sàn/kẹt trần** trong quy tắc stop: stop danh nghĩa không bảo vệ được khi dư bán sàn kéo dài → mã hay có chuỗi sàn/mỏng/đầu cơ phải ghi cảnh báo + ưu tiên time-stop; mã kẹt trần không mua đuổi.
  - **Sizing theo khả năng thoát hàng (ADTV):** vị thế ≤ mức thoát được trong 2–5 phiên (≈ ≤15–20% GTGD khớp lệnh TB20); mã thanh khoản vừa ghi rõ "chỉ phù hợp quy mô nhỏ".
  - **Chất lượng sự kiện EVENT_DRIVEN:** phân biệt báo cáo tự lập/soát xét/kiểm toán, cảnh giác lợi nhuận one-off (coi thesis hỏng dù giá chưa chạm stop).

## v0.2
- Xây dựng đầy đủ agent: cổng vào bắt buộc (thanh khoản, diện cảnh báo, bộ lọc ngành, sự kiện nhị phân), tiêu chí setup cho từng strategy code, quy tắc stop gắn cấu trúc (≤8%, MEAN_REVERSION ≤5%).
- Giới hạn 5 mã hành động + 5 quan sát; mục "Nên tránh" bắt buộc; mỗi mã hành động đủ 7 trường.
- Viết PROMPT.md hoàn chỉnh với quy trình 6 bước.
- INPUT_SCHEMA.md khớp Handoff agent 02 và sector map agent 03, kèm fallback.
- OUTPUT_TEMPLATE.md cố định, Handoff To Risk Manager.
- 6 test case + anti-pattern checklist.

## v0.1
- Created initial folder and file structure.
