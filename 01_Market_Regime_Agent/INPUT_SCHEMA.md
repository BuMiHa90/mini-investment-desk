# Input Schema — Market Regime Agent v0.2

Các trường được nhóm theo 6 trụ cột của scorecard (xem `AGENT_SPEC.md`). Trường **bắt buộc** thiếu thì confidence tự động giảm theo quy tắc trong spec.

## 1. Trend (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| vnindex_ohlc | VN-Index: open, high, low, close, % thay đổi | 1.803,71 (+0,59%) |
| vn30_close | VN30 đóng cửa, % thay đổi | 1.960,97 (+0,46%) |
| ma_position | Vị trí index so với MA20/50/200 | Trên MA200, dưới MA20/50 |
| swing_structure | Đỉnh–đáy gần nhất (cao dần/thấp dần) | Đỉnh 1.933 (28/5), đáy 1.789 (10/6) |
| key_levels | Hỗ trợ / kháng cự đang theo dõi | HT 1.780–1.750; KC 1.811–1.830 |

## 2. Breadth (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| advancers_decliners | Số mã tăng/giảm/đứng giá trên HOSE | 207 / 105 / 50 |
| ceiling_floor_count | Số mã trần / sàn | 5 trần / 2 sàn |
| pct_above_ma50 | % mã trên MA50 (nếu có) | 45% |
| index_contribution | Top mã đóng góp điểm số (phát hiện trụ kéo) | VIC +4,65 điểm trên tổng +10,66 |

## 3. Liquidity (bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| matched_value_hose | GTGD khớp lệnh HOSE (loại thỏa thuận) | 10.000 tỷ |
| value_vs_20d_avg | So với trung bình 20 phiên | 65% |
| volume_direction | Thanh khoản tăng theo chiều tăng hay giảm giá | Tăng nhẹ trong phiên hồi |

## 4. Flows (bắt buộc tối thiểu khối ngoại)

| Field | Mô tả | Ví dụ |
|---|---|---|
| foreign_net_today | Khối ngoại ròng phiên (tỷ đồng), mã bán/mua chính | -543 tỷ; bán MBB, VPB |
| foreign_net_5d | Lũy kế 5 phiên | -7.190 tỷ |
| prop_trading | Tự doanh ròng (không bắt buộc) | +120 tỷ |
| margin_level | Dư nợ margin / nhận định margin (không bắt buộc) | Margin cao gần đỉnh |

## 5. Volatility & Phái sinh (không bắt buộc)

| Field | Mô tả | Ví dụ |
|---|---|---|
| intraday_range | Biên độ dao động phiên, gap mở cửa | Gap -0,6%, biên 10 điểm |
| f1_basis | Basis VN30F1M so với VN30 | -8,2 điểm |
| f1_oi_volume | OI và khối lượng phái sinh | OI tăng, vol tăng |

## 6. Macro & Sentiment (không bắt buộc nhưng nên có)

| Field | Mô tả | Ví dụ |
|---|---|---|
| global_overnight | Phố Wall, DXY, lợi suất Mỹ đêm qua | S&P -1,1%, DXY tăng |
| fx_rates | USD/VND, lãi suất liên ngân hàng | Tỷ giá căng, +0,3% tuần |
| domestic_policy | Tin chính sách trong nước | Room tín dụng, KRX, nâng hạng |
| sentiment_note | Tâm lý NĐT (định tính) | Đứng ngoài, thanh khoản cạn |
| event_calendar | Sự kiện sắp tới (đáo hạn phái sinh, review ETF, họp Fed) | Đáo hạn F1M 18/6 |

## Meta

| Field | Mô tả |
|---|---|
| report_date | Ngày báo cáo (bắt buộc) |
| missing_data_note | Ghi chú dữ liệu thiếu — agent tự điền nếu người dùng không cung cấp |

## Nguồn dữ liệu gợi ý (miễn phí, đủ cho desk nhỏ)

- **Index, breadth, khối ngoại, tường thuật phiên**: CafeF, Vietstock, các bài tổng kết phiên trên Baomoi (chi tiết nhất sau 15h30).
- **Điểm số realtime**: simplize.vn, fireant.vn, TradingView (HOSE:VNINDEX).
- **Phái sinh, basis**: bảng giá phái sinh các CTCK, Vietstock derivatives.
- **Vĩ mô/tỷ giá**: SBV, Wichart, bản tin sáng các CTCK.
- Lưu ý: bài "nhận định phiên X" buổi sáng thường chỉ nói lại phiên hôm trước — số liệu phiên hôm nay phải lấy từ bài tổng kết sau giờ đóng cửa hoặc trang dữ liệu.

## Quy tắc fallback khi thiếu dữ liệu

1. Thiếu trường không bắt buộc → trụ cột tương ứng chấm 0 (trung tính), ghi vào "Dữ liệu chưa xác nhận".
2. Thiếu 1 trường bắt buộc → confidence tối đa là Trung bình.
3. Thiếu ≥2 trường bắt buộc → confidence Thấp, regime mặc định nghiêng phòng thủ (không được kết luận Risk-on).
4. Người dùng không đưa dữ liệu nào → agent tự thu thập từ nguồn công khai, ghi rõ nguồn và độ trễ của từng số liệu.
