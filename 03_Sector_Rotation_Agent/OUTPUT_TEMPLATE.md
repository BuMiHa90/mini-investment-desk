# Output Template — SECTOR ROTATION REPORT

Format cố định. `04_Stock_Watchlist_Agent` parse theo đúng các heading dưới đây — không đổi tên trường, không thêm bớt mục.

---

# SECTOR ROTATION REPORT — [dd/mm/yyyy]

## Strategy Context

- **Strategy code đầu vào:** [từ Handoff agent 02]
- **Chế độ map:** [Đầy đủ / Quan sát (WAIT-CASH) / Đảo chiều-giảm trước (DERISK)]

## Sector Map

### Strong Sectors

| Ngành | RS (5p / 20p vs Index) | Flow (GTGD vs TB20, độ rộng nội ngành) | Ghi chú 1 dòng |
|---|---|---|---|
|  |  |  |  |

### Improving Sectors

| Ngành | RS | Flow | Điều kiện xác nhận để lên Strong (đo được) |
|---|---|---|---|
|  |  |  |  |

### Weak Sectors

| Ngành | RS | Flow | Dấu hiệu rút tiền |
|---|---|---|---|
|  |  |  |  |

### Avoid Chasing

| Ngành | Lý do định lượng (tăng %/số phiên, trụ kéo, trần) | Rủi ro nếu mua đuổi |
|---|---|---|
|  |  |  |

## Evidence

- [3–5 gạch đầu dòng số liệu then chốt; nếu nhắc tên mã chỉ làm bằng chứng dòng tiền, ghi rõ "không phải khuyến nghị"]

## Risks

- [1–3 rủi ro của chính bản đồ này — vd: dữ liệu mới 3 phiên, phân hóa có thể đảo nhanh quanh sự kiện X]

## Handoff To Stock Watchlist

- **Preferred sector filters:** [ngành ưu tiên lọc, theo thứ tự]
- **Excluded sector filters:** [ngành loại hẳn + nhóm Avoid Chasing]
- **Liquidity note:** [ngưỡng thanh khoản tối thiểu / nhóm thanh khoản cạn cần né]
- **Missing data:** [trục/trường nào thiếu, ảnh hưởng gì đến độ tin cậy của map]
