# Output Template — RISK REVIEW REPORT

Format cố định. Đây là báo cáo CUỐI CÙNG broker đọc trước khi tư vấn khách — không đổi tên trường, không thêm bớt mục.

---

# RISK REVIEW REPORT — [dd/mm/yyyy]

## Risk Review Summary

- **Market context:** [regime + strategy code, 1 dòng]
- **Review scope:** [số mã được rà / nguồn watchlist]
- **Data gaps:** [thiếu gì → ảnh hưởng mức quyết định tối đa thế nào]

## Decisions

| Ticker | Decision | Reason (cổng nào) | Required Conditions | Main Risks | Suitable Client | Unsuitable Client |
|---|---|---|---|---|---|---|
|  | Pass / Conditional Pass / Reject |  |  |  |  |  |

(Reject phải ghi thêm: điều gì thay đổi thì được trình lại.)

## Portfolio-Level Notes

- **Exposure risk:** [tổng tỷ trọng nếu kích hoạt hết vs exposure ceiling]
- **Concentration risk:** [số mã cùng ngành trong nhóm Pass]
- **Margin risk:** [đối chiếu margin_status; tình trạng margin tệp khách]
- **Correlation risk:** [các ý tưởng có cùng chết vì một rủi ro không — tỷ giá, lãi suất, sự kiện]

## Final Broker Note

- [2–4 câu broker nói được nguyên văn với khách: hôm nay được làm gì trong điều kiện nào, tuyệt đối không làm gì, và câu trả lời khi khách đòi làm điều đã bị Reject]
