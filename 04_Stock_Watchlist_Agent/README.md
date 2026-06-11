# 04 Stock Watchlist Agent

Bước 4 của Mini Investment Desk: chuyển chiến thuật (bước 2) + bản đồ ngành (bước 3) thành **watchlist cổ phiếu theo kịch bản**. Đây là agent duy nhất trong pipeline được nêu tên mã — nên có hàng rào chặt nhất: không có điều kiện kích hoạt thì không có mã nào trong nhóm hành động.

## Mô hình tham chiếu

Thiết kế mô phỏng vai trò **Analyst Pod / Idea Generation Desk** tại quỹ lớn:

- **Idea = thesis + trigger + invalidation + stop + client fit**: mỗi mã đủ 7 trường mới được vào nhóm hành động.
- **Cổng vào trước, setup sau**: thanh khoản tối thiểu, không diện cảnh báo, đúng ngành ưu tiên, không sự kiện nhị phân cận kề.
- **Watchlist ngắn**: tối đa 5 mã hành động + 5 mã quan sát — desk thật không theo dõi nổi hơn.
- **"Điều gì khiến mình sai?" hỏi trước "lên được bao nhiêu?"**: điểm sai bắt buộc, giá mục tiêu không có chỗ trong báo cáo.

## Cấu trúc thư mục

| File | Vai trò |
|---|---|
| `AGENT_SPEC.md` | Cổng vào, tiêu chí setup theo strategy code, quy tắc stop, cấu trúc 3 nhóm |
| `PROMPT.md` | System prompt hoàn chỉnh, dán vào model là chạy |
| `INPUT_SCHEMA.md` | Trường đầu vào (Handoff 02 + sector map 03 + dữ liệu cổ phiếu), fallback |
| `OUTPUT_TEMPLATE.md` | Format STOCK WATCHLIST REPORT cố định để agent 05 parse |
| `TEST_CASES.md` | 6 ca kiểm thử + anti-pattern checklist |
| `CHANGELOG.md` | Lịch sử phiên bản |

## Cách chạy

1. Chạy agent 01 → 02 → 03 trước.
2. Dán nội dung `PROMPT.md` làm system prompt.
3. Dán Handoff agent 02 + `SECTOR ROTATION REPORT` + universe và dữ liệu giá/volume làm message.
4. Output là `STOCK WATCHLIST REPORT` — khối `Handoff To Risk Manager` là input của agent 05.

## Nguyên tắc bất biến

Watchlist là kịch bản theo dõi có điều kiện, không phải khuyến nghị mua bán. Không có kích hoạt thì không hành động. Stop gắn cấu trúc, không tùy hứng. Mục "Nên tránh" luôn có mặt. Phân vân thì xếp xuống Quan sát.
