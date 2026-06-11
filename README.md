# Mini Investment Desk Agent System v1

Hệ thống 5 agent mô phỏng quy trình của một desk đầu tư chuyên nghiệp, áp dụng cho phòng môi giới chứng khoán nhỏ tại LPBS. Mục tiêu: tư vấn khách hàng thực tế, có kỷ luật, có truy vết — **không phím hàng bừa, không cam kết lợi nhuận**.

## Pipeline

```
01 Market Regime ──► 02 Strategy Selector ──► 03 Sector Rotation ──► 04 Stock Watchlist ──► 05 Risk Manager
   "Thị trường        "Đánh kiểu gì            "Tiền đang ở          "Theo dõi mã nào,      "Cái nào được phép
    đang chơi          hay đứng ngoài?"          ngành nào?"            kịch bản gì?"          nói với khách?"
    luật nào?"
```

Mỗi agent chỉ trả lời MỘT câu hỏi và truyền kết quả xuống bước sau qua khối **Handoff** có format cố định:

| Bước | Agent | Output | Handoff xuống bước sau |
|---|---|---|---|
| 1 | Market Regime | MARKET REGIME REPORT | Regime code, exposure band, margin status, ràng buộc chiến lược |
| 2 | Strategy Selector | STRATEGY SELECTION REPORT | Strategy code, tiêu chí cho agent 03/04, exposure ceiling |
| 3 | Sector Rotation | SECTOR ROTATION REPORT | Preferred/excluded sectors, lưu ý thanh khoản |
| 4 | Stock Watchlist | STOCK WATCHLIST REPORT | Mã cần soi kỹ + mối lo chính |
| 5 | Risk Manager | RISK REVIEW REPORT | Pass / Conditional Pass / Reject — sản phẩm cuối cho broker |

## Nguyên tắc thiết kế xuyên suốt

1. **Bảo vệ vốn trước, cơ hội sau** — phân vân thì chọn phương án thận trọng hơn; đứng ngoài là một vị thế hợp lệ.
2. **Mọi kết luận tra ngược được** — scorecard, ma trận, cổng kiểm tra; không có "cảm giác thị trường".
3. **Không có invalidation thì không có khuyến nghị** — mọi chiến thuật/mã đều phải có điều kiện kích hoạt VÀ điểm sai đo được.
4. **Hạ nhanh, nâng chậm** — hạ rủi ro trong ngày, nâng rủi ro cần xác nhận.
5. **Thiếu dữ liệu = rủi ro** — phải nói thiếu, hạ độ tin cậy, không bịa số.
6. **Mỗi khuyến nghị gắn loại khách** — ý tưởng rủi ro cao không bao giờ đến tay khách không phù hợp.
7. **Báo cáo đọc dưới 3–5 phút** — format cố định để agent sau parse và broker đọc nhanh.

## Cấu trúc mỗi agent

Mỗi thư mục agent có 7 file chuẩn: `README.md` (tổng quan), `AGENT_SPEC.md` (phương pháp luận), `PROMPT.md` (system prompt dán vào model là chạy), `INPUT_SCHEMA.md` (trường đầu vào + fallback), `OUTPUT_TEMPLATE.md` (format báo cáo cố định), `TEST_CASES.md` (ca kiểm thử + anti-pattern checklist), `CHANGELOG.md`.

## Cách chạy một phiên đầy đủ

1. **Sau 15h30** (đủ dữ liệu tổng kết phiên): chạy agent 01 với dữ liệu theo `01_Market_Regime_Agent/INPUT_SCHEMA.md`.
2. Lấy khối Handoff của báo cáo 01 → chạy agent 02.
3. Nếu agent 02 trả về WAIT/CASH → có thể dừng pipeline tại đây (agent 03 chỉ chạy chế độ quan sát nếu cần).
4. Ngược lại: chạy tiếp 03 (kèm dữ liệu ngành) → 04 (kèm universe + dữ liệu giá/volume) → 05 (kèm hồ sơ khách nếu có).
5. Broker chỉ tư vấn dựa trên `RISK REVIEW REPORT` của agent 05 — các mã Reject tuyệt đối không đưa cho khách.

## Vận hành tự động (báo cáo đầu ngày)

Pipeline `01 → 02 → 03` chạy tự động mỗi sáng 6h30 (thứ 2–6) qua **GitHub Actions**, xuất HTML lên **GitHub Pages** cho nhân viên xem. Agent 04/05 (watchlist + risk review) chạy thủ công khi trưởng phòng yêu cầu — giữ con người trong vòng kiểm soát trước khi tên mã đến tay broker.

```
GitHub Actions (cron 6h30 VN, T2–T6)
  └─ pipeline/fetch_data.py    : vnstock lấy VN-Index/VN30, tính MA, thanh khoản, swing
  └─ pipeline/run_agents.py    : Claude API — agent 01 (web search) → 02 → 03 (web search)
  └─ pipeline/render_html.py   : dashboard docs/index.html + lưu trữ docs/archive/
  └─ commit → GitHub Pages
```

### Cài đặt lần đầu (làm 1 lần)

1. Tạo repo **public** trên GitHub, push code lên (`git push`).
2. Repo → **Settings → Secrets and variables → Actions → New repository secret**: thêm `ANTHROPIC_API_KEY`.
3. Repo → **Settings → Pages → Source**: chọn `Deploy from a branch`, branch `main`, thư mục `/docs`.
4. Chạy thử: tab **Actions → daily-desk-report → Run workflow**. Sau ~5 phút, báo cáo xuất hiện tại `https://<user>.github.io/<repo>/`.
5. (Tùy chọn) Repo → Settings → Variables: đặt `CLAUDE_MODEL` để đổi model (mặc định `claude-sonnet-4-6`).

### Chạy tay trên máy local

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python -m pipeline.run_pipeline          # chạy thật
python -m pipeline.run_pipeline --mock   # test render không tốn API
```

### Lưu ý vận hành

- Repo public → báo cáo công khai trên internet (đã chấp nhận; báo cáo 01→03 không nêu tên mã).
- vnstock là API không chính thức — nếu đứt, pipeline KHÔNG chết: agent 01 tự web-search bù, hạ confidence và ghi rõ thiếu gì.
- Ngày nghỉ lễ thị trường: báo cáo vẫn chạy với dữ liệu phiên gần nhất (agent tự ghi chú độ trễ).

## Kiểm thử

Mỗi agent có bộ test case riêng trong `TEST_CASES.md`. Trước khi đưa vào sử dụng, chạy đủ các case và đối chiếu anti-pattern checklist — đặc biệt các case "thiếu dữ liệu" và "risk-off" (hai tình huống agent dễ vi phạm kỷ luật nhất).

## Giới hạn

- Đây là công cụ hỗ trợ ra quyết định, không phải hệ thống giao dịch tự động và không thay thế đánh giá của con người.
- Chất lượng output phụ thuộc chất lượng dữ liệu đầu vào — dữ liệu miễn phí có độ trễ.
- Không agent nào được phép cam kết lợi nhuận hay hướng thị trường; mọi báo cáo chỉ có giá trị trong ngày.
