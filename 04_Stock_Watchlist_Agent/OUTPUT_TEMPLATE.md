# Output Template — STOCK WATCHLIST REPORT

Format cố định. `05_Risk_Manager_Agent` parse theo đúng các heading dưới đây — không đổi tên trường, không thêm bớt mục.

---

# STOCK WATCHLIST REPORT — [dd/mm/yyyy]

## Watchlist Summary

- **Strategy context:** [strategy code + 1 dòng]
- **Sector context:** [preferred / excluded từ agent 03]
- **Data gaps:** [thiếu gì, ảnh hưởng gì]
- *Watchlist là kịch bản theo dõi có điều kiện, không phải khuyến nghị mua bán.*

## Có thể hành động nếu xác nhận

(Tối đa 5 mã. Mã thiếu bất kỳ cột nào không được nằm ở đây.)

| Ticker | Scenario | Activation Condition | Invalid Level | Reference Stop-loss | Main Risks | Suitable Client | Unsuitable Client |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Chỉ quan sát

(Tối đa 5 mã. Confirmation Needed phải đo được.)

| Ticker | Reason To Watch | Confirmation Needed | Main Risks |
|---|---|---|---|
|  |  |  |  |

## Nên tránh

(Bắt buộc có — các mã khách hay hỏi nhưng đang nguy hiểm.)

| Ticker | Reason To Avoid | Risk Note |
|---|---|---|
|  |  |  |

## Handoff To Risk Manager

- **Items requiring risk review:** [mã nào cần soi kỹ nhất, theo thứ tự]
- **Key concerns:** [thanh khoản / sự kiện sắp tới / beta cao / mức độ đầu cơ / khoảng cách stop]
- **Exposure & margin context:** [exposure ceiling + margin status kế thừa từ agent 02]
