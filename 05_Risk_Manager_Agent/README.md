# 05 Risk Manager Agent

Bước 5 (cuối) của Mini Investment Desk: **chốt phủ quyết rủi ro** trước khi broker dùng thông tin tư vấn khách. Rà từng ý tưởng từ watchlist (bước 4) qua 6 cổng kiểm tra và quyết định **Pass / Conditional Pass / Reject**. Agent này không tìm cơ hội mới — chỉ tìm lý do để chặn.

## Mô hình tham chiếu

Thiết kế mô phỏng vai trò **Risk Committee / Compliance Gate** tại quỹ lớn:

- **Quyền phủ quyết tuyệt đối**: Reject là chung cuộc trong ngày; muốn xét lại phải có dữ liệu mới.
- **6 cổng theo thứ tự**: nhất quán pipeline → chất lượng kịch bản → thanh khoản/chất lượng hàng → sự kiện → suitability → rủi ro cấp danh mục.
- **Suitability (KYC)**: ý tưởng rủi ro cao không bao giờ Pass cho khách không phù hợp.
- **Thiếu dữ liệu = rủi ro**: dữ liệu mỏng thì không có Pass sạch, tối đa Conditional.
- **Nghiêng về chặn**: tỷ lệ Reject/Conditional cao là pipeline hoạt động đúng.

## Cấu trúc thư mục

| File | Vai trò |
|---|---|
| `AGENT_SPEC.md` | 6 cổng kiểm tra, thang quyết định, quy tắc danh mục |
| `PROMPT.md` | System prompt hoàn chỉnh, dán vào model là chạy |
| `INPUT_SCHEMA.md` | Trường đầu vào (watchlist 04 + bối cảnh pipeline + hồ sơ khách), fallback |
| `OUTPUT_TEMPLATE.md` | Format RISK REVIEW REPORT — báo cáo cuối broker đọc |
| `TEST_CASES.md` | 6 ca kiểm thử + anti-pattern checklist |
| `CHANGELOG.md` | Lịch sử phiên bản |

## Cách chạy

1. Chạy agent 01 → 02 → 03 → 04 trước.
2. Dán nội dung `PROMPT.md` làm system prompt.
3. Dán `STOCK WATCHLIST REPORT` + regime/strategy context + hồ sơ khách (nếu có) làm message.
4. Output là `RISK REVIEW REPORT` — sản phẩm cuối cùng của desk, broker dùng trực tiếp để tư vấn.

## Nguyên tắc bất biến

Mặc định hoài nghi. Mọi quyết định tra ngược được về cổng. Conditional không đo được là Reject. Không tìm cơ hội mới. Bảo vệ vốn của khách và uy tín phòng hơn mọi cơ hội.
