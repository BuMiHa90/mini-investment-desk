# Changelog

## v0.3
- Bổ sung quản trị rủi ro vi mô VN (từ deep-research report TTCK VN):
  - **Cổng 3** thêm **rủi ro kẹt sàn** (stop danh nghĩa không bảo vệ được khi dư bán sàn → Conditional + time-stop) và **sizing theo khả năng thoát hàng** (≤15–20% GTGD khớp lệnh TB20, vượt → trần khối lượng).
  - **Cổng 6** thêm **tập trung theo theme vĩ mô** (không chỉ theo ngành): các mã cùng phụ thuộc một câu chuyện vĩ mô (hệ Vingroup, tín dụng/BĐS, thuế quan/lãi suất/tỷ giá) → "đa dạng 5 mã" chưa chắc là đa dạng.

## v0.2
- Xây dựng đầy đủ agent: 6 cổng kiểm tra theo thứ tự (nhất quán pipeline, chất lượng kịch bản, thanh khoản/làm giá, sự kiện, suitability, rủi ro cấp danh mục).
- Thang quyết định Pass / Conditional Pass / Reject với yêu cầu tra ngược về cổng; Conditional bắt buộc có điều kiện đo được.
- Quy tắc danh mục: tập trung ngành, tổng exposure vs ceiling, tương quan kịch bản.
- Viết PROMPT.md hoàn chỉnh; INPUT_SCHEMA.md khớp output agent 04 + bối cảnh pipeline, kèm fallback.
- OUTPUT_TEMPLATE.md bổ sung Correlation risk và yêu cầu Final Broker Note dùng được nguyên văn.
- 6 test case + anti-pattern checklist.

## v0.1
- Created initial folder and file structure.
