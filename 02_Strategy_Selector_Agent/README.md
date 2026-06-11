# 02 Strategy Selector Agent

Bước 2 của Mini Investment Desk: chọn **chiến thuật giao dịch/phân bổ** phù hợp với regime đã được xác định ở bước 1. Agent này trả lời duy nhất câu hỏi *"Hôm nay nên đánh theo kiểu gì — hay nên đứng ngoài?"* — không chọn cổ phiếu, không đưa lệnh, không cam kết lợi nhuận.

## Mô hình tham chiếu

Thiết kế mô phỏng vai trò **Playbook Desk / Head of Trading Strategy** tại quỹ lớn:

- **Playbook theo regime** (pod shop): mỗi trạng thái thị trường chỉ cho phép một tập chiến thuật — ma trận Regime → Cho phép / Bị cấm, không thương lượng.
- **"Đứng ngoài cũng là một vị thế"** (Druckenmiller): WAIT và CASH là chiến thuật hạng nhất.
- **Risk budgeting**: mỗi chiến thuật có Risk Tier 0–3, không được vượt Risk Budget của regime; confidence thấp thì hạ bậc.
- **Không có invalidation thì không có vị thế**: chiến thuật không có điều kiện kích hoạt + vô hiệu đo được sẽ không được xuất hiện trong báo cáo.

## Cấu trúc thư mục

| File | Vai trò |
|---|---|
| `AGENT_SPEC.md` | Thư viện 11 chiến thuật, ma trận Regime → Chiến thuật, bộ modifier, quy tắc cứng |
| `PROMPT.md` | System prompt hoàn chỉnh, dán vào model là chạy |
| `INPUT_SCHEMA.md` | Trường đầu vào (Handoff từ agent 01 + sentiment/tin tức/ngành), quy tắc fallback |
| `OUTPUT_TEMPLATE.md` | Format STRATEGY SELECTION REPORT cố định để agent 03/04 parse |
| `TEST_CASES.md` | 6 ca kiểm thử + anti-pattern checklist |
| `CHANGELOG.md` | Lịch sử phiên bản |

## Cách chạy

1. Chạy `01_Market_Regime_Agent` trước để có `MARKET REGIME REPORT`.
2. Dán nội dung `PROMPT.md` làm system prompt.
3. Dán báo cáo regime (tối thiểu khối Handoff) + ngữ cảnh theo `INPUT_SCHEMA.md` làm message.
4. Output là `STRATEGY SELECTION REPORT` — khối `Handoff` cuối báo cáo (strategy code, tiêu chí cho agent 03/04, exposure ceiling, margin) là input của bước 3 và 4.

## Nguyên tắc bất biến

Risk-off thì cấm mua đuổi. Sideway thì cấm tư duy trend-following. Chưa xác nhận thì chờ. Không có điều kiện kích hoạt thì không có chiến thuật. Không cam kết lợi nhuận. Phải chỉ rõ chiến thuật bị cấm hôm nay. Báo cáo đọc dưới 3 phút.
