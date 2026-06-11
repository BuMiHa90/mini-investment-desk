# Changelog

## v0.2
- Xây dựng đầy đủ agent: 6 cổng kiểm tra theo thứ tự (nhất quán pipeline, chất lượng kịch bản, thanh khoản/làm giá, sự kiện, suitability, rủi ro cấp danh mục).
- Thang quyết định Pass / Conditional Pass / Reject với yêu cầu tra ngược về cổng; Conditional bắt buộc có điều kiện đo được.
- Quy tắc danh mục: tập trung ngành, tổng exposure vs ceiling, tương quan kịch bản.
- Viết PROMPT.md hoàn chỉnh; INPUT_SCHEMA.md khớp output agent 04 + bối cảnh pipeline, kèm fallback.
- OUTPUT_TEMPLATE.md bổ sung Correlation risk và yêu cầu Final Broker Note dùng được nguyên văn.
- 6 test case + anti-pattern checklist.

## v0.1
- Created initial folder and file structure.
