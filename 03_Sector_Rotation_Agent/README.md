# 03 Sector Rotation Agent

Bước 3 của Mini Investment Desk: đọc **dòng tiền theo nhóm ngành** trong khuôn khổ chiến thuật đã chọn ở bước 2. Agent này trả lời duy nhất câu hỏi *"Tiền đang ở đâu, đang đi đâu, và nhóm nào không được mua đuổi?"* — không chọn cổ phiếu.

## Mô hình tham chiếu

Thiết kế mô phỏng vai trò **Sector Strategy / Flow Desk** tại quỹ lớn:

- **Ma trận RS × Flow**: sức mạnh giá tương đối (so VN-Index, 5/20 phiên) × dòng tiền (thanh khoản, độ rộng nội ngành, khối ngoại) → 4 nhóm Strong / Improving / Weak / Avoid Chasing.
- **Giá tăng không có dòng tiền không phải ngành mạnh** — Flow là điều kiện bắt buộc của nhãn Strong.
- **Một phiên không phải xu hướng** — tối thiểu 5 phiên mới được kết luận.
- **Avoid Chasing là mục bắt buộc** — phần broker dùng để chặn khách FOMO vào ngành đã tăng nóng.

## Cấu trúc thư mục

| File | Vai trò |
|---|---|
| `AGENT_SPEC.md` | Ma trận RS × Flow, định nghĩa tăng nóng, hành vi theo strategy code |
| `PROMPT.md` | System prompt hoàn chỉnh, dán vào model là chạy |
| `INPUT_SCHEMA.md` | Trường đầu vào (Handoff từ agent 02 + dữ liệu ngành), nguồn miễn phí, fallback |
| `OUTPUT_TEMPLATE.md` | Format SECTOR ROTATION REPORT cố định để agent 04 parse |
| `TEST_CASES.md` | 5 ca kiểm thử + anti-pattern checklist |
| `CHANGELOG.md` | Lịch sử phiên bản |

## Cách chạy

1. Chạy agent 01 → 02 trước để có `STRATEGY SELECTION REPORT`.
2. Dán nội dung `PROMPT.md` làm system prompt.
3. Dán Handoff của agent 02 + dữ liệu ngành theo `INPUT_SCHEMA.md` làm message.
4. Output là `SECTOR ROTATION REPORT` — khối `Handoff To Stock Watchlist` là input của agent 04.

## Nguyên tắc bất biến

Đọc dòng tiền theo bối cảnh chiến thuật. Tăng giá rỗng ruột không phải ngành mạnh. Một phiên không phải xu hướng. Luôn chỉ rõ nhóm cấm mua đuổi. Không phím mã. Báo cáo đọc dưới 3 phút.
