Bổ sung cách lấy missing data:

## Số mã tăng trần, giảm sàn của sàn HOSE
GET request tới: https://cafef.vn/du-lieu/Ajax/PriceHistory/PriceHistory.ashx?centerid=1
Data schema trả về: {"Data":{"TotalStockUp":128,"TotalStockDown":180,"TotalStockNochange":49,"TotalKichtran":5,"TotalKichsan":3,"Volume":517581557,"TotalValue":14597.09633554},"Message":null,"Success":true}

Lấy TotalKichtran là số lượng mã tăng trần, TotalKichsan là số lượng mã giảm sàn
**Note:** cách này có thể dùng làm backup để lấy số lượng mã tăng/giảm của toàn bộ HOSE.

## Tổng khối lượng và giá trị giao dịch thỏa thuận VNINDEX
GET request tới: https://api-finance-t19.24hmoney.vn/v1/web/indices/agreements-trading-history?device_id=web1782126832vtsa2om3p04je0swryh0ketx9nqw8568282&device_name=INVALID&device_model=Windows+10&network_carrier=INVALID&connection_type=INVALID&os=Chrome&os_version=149.0.0.0&access_token=INVALID&push_token=INVALID&locale=vi&browser_id=web1782126832vtsa2om3p04je0swryh0ketx9nqw8568282&code=10

Data schema trả về: {"message":"success","status":200,"data":[{"total_transactions":350,"total_vol":74496109,"total_val":2338509438160,"total_symbol":62,"update_time":1782117006},...],"execute_time_ms":1}

Lấy giá trị data[0].total_vol là tổng khối lượng giao dịch thỏa thuận, total_val là tổng giá trị giao dịch thỏa thuận
**Note:** Lấy khối lượng và giá trị tổng của VNINDEX trừ đi khối lượng và giá trị thỏa thuận sẽ ra khối lượng và giá trị khớp lệnh


## global_overnight, fx_rates, domestic_policy, sentiment_note
các thông tin này tổng hợp từ một repo khác (cùng Github account)