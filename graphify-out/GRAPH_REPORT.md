# Graph Report - Mini_Investment_Desk_Agent_System_v1  (2026-06-22)

## Corpus Check
- 91 files · ~122,032 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 745 nodes · 700 edges · 72 communities (70 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e6885e5d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]

## God Nodes (most connected - your core abstractions)
1. `STRATEGY SELECTION REPORT — 16/06/2026` - 15 edges
2. `STRATEGY SELECTION REPORT — [dd/mm/yyyy]` - 15 edges
3. `SECTOR ROTATION MAP — 2026-06-19` - 12 edges
4. `BÁO CÁO TRẠNG THÁI THỊ TRƯỜNG — RISK REGIME DESK` - 10 edges
5. `BÁO CÁO MARKET REGIME — 2026-06-19` - 10 edges
6. `BÁO CÁO TRẠNG THÁI THỊ TRƯỜNG` - 10 edges
7. `BÁO CÁO TRẠNG THÁI THỊ TRƯỜNG — LPBS Risk Regime Desk` - 10 edges
8. `MARKET REGIME REPORT — 16/06/2026` - 10 edges
9. `Input Schema — Market Regime Agent v0.2` - 10 edges
10. `MARKET REGIME REPORT — [dd/mm/yyyy]` - 10 edges

## Surprising Connections (you probably didn't know these)
- `run_pipeline_agents()` --calls--> `load_system_prompt()`  [EXTRACTED]
  pipeline/run_agents_cli.py → pipeline/run_agents.py

## Import Cycles
- None detected.

## Communities (72 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (11): Dữ liệu thu thập bổ sung qua web search, Dữ liệu được cung cấp (input — vnstock/VCI), I. KIỂM KÊ DỮ LIỆU, II. SCORECARD, III. XÁC ĐỊNH REGIME, IV. TRẠNG THÁI PHỤ, 📋 MARKET REGIME REPORT — 2026-06-12, Trường vẫn thiếu & ảnh hưởng (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (15): Bộ điều chỉnh áp dụng (theo thứ tự), 🔑 CHIẾN THUẬT CHÍNH — `CASH` (Giữ tiền / Capital Preservation), 🔧 CHIẾN THUẬT PHỤ — `DERISK` (Giảm tỷ trọng / Hạ margin), ⚠️ Cảnh báo Bull Trap — Theo dõi ngay phiên thứ Hai 16/6, I. HANDOFF NHẬN ĐƯỢC (TỪ MARKET REGIME AGENT), II. QUY TRÌNH RA QUYẾT ĐỊNH, III. CHIẾN THUẬT ĐƯỢC CHỌN, IV. CHIẾN THUẬT KHÔNG NÊN DÙNG — BỊ CẤM TRONG BỐI CẢNH HIỆN TẠI (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (22): I. HANDOFF NHẬN & CHẾ ĐỘ BÁO CÁO, II. NGUỒN DỮ LIỆU & GIỚI HẠN, III. PHÂN TÍCH RS & FLOW — 10 NGÀNH THANH KHOẢN LỚN NHẤT, IV. SECTOR MAP 4 NHÓM, Logistics / Cảng-Kho vận (GMD, HAH, ACV), 🔴 NHÓM 1 — WEAK / BỊ RÚT TIỀN (Giảm tỷ trọng ưu tiên trong DERISK), 🟡 NHÓM 2 — IMPROVING (Quan sát — không giải ngân trong CASH), 🔵 NHÓM 3 — QUAN SÁT (Không đủ dữ liệu để phân loại) (+14 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (10): Cảnh báo cho broker, Dữ liệu chưa xác nhận / còn thiếu, Dữ liệu ủng hộ, Handoff cho Strategy Selector, Khuyến nghị khung (không phím mã), Kết luận, MARKET REGIME REPORT — 16/06/2026, Rủi ro chính trong ngày (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (18): build_market_snapshot(), fetch(), fetch_breadth(), fetch_extra_fields(), fetch_f1_basis(), fetch_foreign_net(), fetch_index_contribution(), _history() (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (15): Chiến thuật chính hôm nay, Chiến thuật KHÔNG nên dùng (bị cấm hôm nay), Chiến thuật phụ (nếu có), Có nên dùng margin không, Cảnh báo cho broker, Handoff, Loại khách KHÔNG phù hợp, Loại khách phù hợp (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (6): 0. Ghi chú bắt buộc về chế độ báo cáo, 1. Sector Map (bản đồ quan sát — không phải khuyến nghị hành động), 2. Evidence (số liệu trích dẫn — chỉ để minh chứng dòng tiền, KHÔNG phải khuyến nghị mua bán), 3. Risks, 4. Handoff To Stock Watchlist Agent, SECTOR ROTATION REPORT — 16/06/2026

### Community 7 - "Community 7"
Cohesion: 0.21
Nodes (9): call_agent(), call_agent(), Goi agent 01 -> 02 -> 03 qua Claude Code CLI (headless, dung goi thue bao thay, run_pipeline_agents(), load_system_prompt(), Goi lan luot agent 01 -> 02 -> 03 qua Claude API.  - System prompt cua moi age, Tra ve dict {'01': report_md, '02': ..., '03': ...}., run_pipeline_agents() (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (16): Agent Specification — Market Regime Agent v0.2, Không được làm, Mapping Composite Score → Regime, Phương pháp: Scorecard 6 trụ cột, Quy tắc bắt buộc, Quy tắc chống nhiễu (hysteresis) — "hạ nhanh, nâng chậm", Quy tắc mức độ tự tin (confidence), Quy tắc trạng thái phụ (sub-state) (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (16): Chiến thuật chính hôm nay, Chiến thuật KHÔNG nên dùng (bị cấm hôm nay), Chiến thuật phụ (nếu có), Có nên dùng margin không, Cảnh báo cho broker, Handoff, Loại khách KHÔNG phù hợp, Loại khách phù hợp (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (13): 6 cổng kiểm tra (chạy theo thứ tự cho TỪNG mã), Agent Specification — Risk Manager Agent v0.2, Cổng 1 — Nhất quán pipeline (vi phạm → Reject ngay), Cổng 2 — Chất lượng kịch bản (vi phạm → Reject), Cổng 3 — Thanh khoản & chất lượng hàng (vi phạm → Reject hoặc Conditional), Cổng 4 — Rủi ro sự kiện (→ Conditional hoặc Reject), Cổng 5 — Suitability theo khách (→ điều chỉnh phạm vi Pass), Cổng 6 — Rủi ro cấp danh mục (ghi ở Portfolio-Level Notes) (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (11): Cảnh báo cho broker, Dữ liệu chưa xác nhận / còn thiếu, Dữ liệu ủng hộ, Handoff cho Strategy Selector, Khuyến nghị khung (không phím mã), Kết luận, MARKET REGIME REPORT — [dd/mm/yyyy], Output Template — MARKET REGIME REPORT (+3 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (11): Avoid Chasing, Evidence, Handoff To Stock Watchlist, Improving Sectors, Output Template — SECTOR ROTATION REPORT, Risks, Sector Map, SECTOR ROTATION REPORT — [dd/mm/yyyy] (+3 more)

### Community 13 - "Community 13"
Cohesion: 0.17
Nodes (11): Chạy tay trên máy local, Cài đặt lần đầu (làm 1 lần), Cách chạy một phiên đầy đủ, Cấu trúc mỗi agent, Giới hạn, Kiểm thử, Lưu ý vận hành, Mini Investment Desk Agent System v1 (+3 more)

### Community 14 - "Community 14"
Cohesion: 0.18
Nodes (10): 1. Trend (bắt buộc), 2. Breadth (bắt buộc), 3. Liquidity (bắt buộc), 4. Flows (bắt buộc tối thiểu khối ngoại), 5. Volatility & Phái sinh (không bắt buộc), 6. Macro & Sentiment (không bắt buộc nhưng nên có), Input Schema — Market Regime Agent v0.2, Meta (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (10): Agent Specification — Sector Rotation Agent v0.2, Hành vi theo chiến thuật đầu vào (strategy code từ agent 02), Không được làm, Mapping vào Sector Map, Phương pháp: Ma trận RS × Flow, Quy tắc bắt buộc, Tiêu chí output tốt, Trục 1 — Relative Strength (RS) (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (10): Checklists, Example: Rename `validateUser` to `authenticateUser`, Extract Module, Refactoring with GitNexus, Rename Symbol, Risk Rules, Split Function/Service, Tools (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.20
Nodes (9): Agent Specification — Stock Watchlist Agent v0.2, Cấu trúc 3 nhóm, Cổng vào bắt buộc (gate) — xét TRƯỚC mọi setup, Không được làm, Quy tắc bắt buộc, Quy tắc stop-loss tham khảo, Tiêu chí output tốt, Tiêu chí setup theo strategy code (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.20
Nodes (9): Always Do, CLI, Daily Operations — Mini Investment Desk, Daily Workflow, Failure Handling, GitNexus — Code Intelligence, Never Do, Non-Negotiable Runtime Paths (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.20
Nodes (9): Always Do, CLI, Daily Operations — Mini Investment Desk, Daily Workflow, Failure Handling, GitNexus — Code Intelligence, Never Do, Non-Negotiable Runtime Paths (+1 more)

### Community 20 - "Community 20"
Cohesion: 0.20
Nodes (9): After Indexing, analyze — Build or refresh the index, clean — Delete the index, Commands, GitNexus CLI Commands, list — Show all indexed repos, status — Check index freshness, Troubleshooting (+1 more)

### Community 21 - "Community 21"
Cohesion: 0.26
Nodes (12): Path, _code(), _extract(), _extract_section(), _field(), _fmt_vn(), _mcard(), _md() (+4 more)

### Community 22 - "Community 22"
Cohesion: 0.22
Nodes (8): Agent Specification — Strategy Selector Agent v0.2, Bộ điều chỉnh (Modifiers) — áp SAU khi tra ma trận, Không được làm, Ma trận Regime → Chiến thuật, Quy tắc bắt buộc (hard rules), Thư viện chiến thuật (Playbook Library), Tiêu chí output tốt, Vai trò

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (8): 1. Từ Market Regime Agent (bắt buộc), 2. Tâm lý nhà đầu tư (không bắt buộc), 3. Tin tức thị trường (không bắt buộc), 4. Dữ liệu ngành (không bắt buộc), 5. Rủi ro & ràng buộc desk (không bắt buộc), Input Schema — Strategy Selector Agent v0.2, Meta, Quy tắc fallback khi thiếu dữ liệu

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (8): Anti-pattern checklist (mọi case đều phải pass), Test Case 1 — Risk-on, confidence Cao, Test Case 2 — Risk-off mạnh (quy tắc cấm mua đuổi), Test Case 3 — Sideway (quy tắc cấm trend-following), Test Case 4 — Hồi kỹ thuật + Bull trap risk (sub-state ghi đè), Test Case 5 — Thiếu dữ liệu / không có báo cáo regime, Test Case 6 — Phân hóa + sự kiện đáo hạn phái sinh, Test Cases — Strategy Selector Agent v0.2

### Community 25 - "Community 25"
Cohesion: 0.22
Nodes (8): 1. Từ Strategy Selector Agent (bắt buộc), 2. Dữ liệu ngành (bắt buộc), 3. Dòng tiền theo ngành (không bắt buộc nhưng nên có), 4. Bối cảnh (không bắt buộc), Input Schema — Sector Rotation Agent v0.2, Meta, Nguồn dữ liệu gợi ý (miễn phí), Quy tắc fallback khi thiếu dữ liệu

### Community 26 - "Community 26"
Cohesion: 0.22
Nodes (8): Anti-pattern checklist (mọi case đều phải pass), Test Case 1 — PULLBACK_BUY chuẩn, Test Case 2 — Cổng thanh khoản và diện cảnh báo, Test Case 3 — Strategy WAIT (không có nhóm hành động), Test Case 4 — MEAN_REVERSION (hàng rào chặt nhất), Test Case 5 — Thiếu sector map, Test Case 6 — Quá nhiều setup đẹp (kiểm tra giới hạn 5+5), Test Cases — Stock Watchlist Agent v0.2

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (8): Anti-pattern checklist (mọi case đều phải pass), Test Case 1 — Pass sạch, Test Case 2 — Reject vì vi phạm nhất quán pipeline (Cổng 1), Test Case 3 — Conditional Pass vì sự kiện + suitability, Test Case 4 — Reject vì nghi làm giá (Cổng 3), Test Case 5 — Rủi ro cấp danh mục (Cổng 6), Test Case 6 — Thiếu dữ liệu (không được tự tin quá), Test Cases — Risk Manager Agent v0.2

### Community 28 - "Community 28"
Cohesion: 0.22
Nodes (8): advancers_decliners (số mã tăng/giảm HOSE) → `fetch_breadth()`, Cache theo phiên (chiều fetch, tối tái dùng), CHƯA CÓ NGUỒN — vẫn skip, agent tự web search/fallback, f1_basis (basis VN30F1M vs VN30) → `fetch_f1_basis()`, foreign_net_today / foreign_net_5d (khối ngoại ròng) → `fetch_foreign_net()`, index_contribution (trừ/kéo điểm) → `fetch_index_contribution()`, Missing fields — trạng thái nguồn dữ liệu, ĐÃ XÁC THỰC — code trong `fetch_data.py`

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (8): Checklist, Example: "What breaks if I change validateUser?", Impact Analysis with GitNexus, Risk Assessment, Tools, Understanding Output, When to Use, Workflow

### Community 30 - "Community 30"
Cohesion: 0.25
Nodes (7): Anti-pattern checklist (mọi case đều phải pass), Test Case 1 — Uptrend xác nhận (Risk-on), Test Case 2 — Risk-off / Downtrend ngắn hạn, Test Case 3 — Thiếu dữ liệu, Test Case 4 — Hồi kỹ thuật + Bull trap risk (dữ liệu thật 10–11/06/2026), Test Case 5 — Panic selling, Test Cases — Market Regime Agent v0.2

### Community 31 - "Community 31"
Cohesion: 0.25
Nodes (7): Anti-pattern checklist (mọi case đều phải pass), Test Case 1 — Phân hóa, chiến thuật SECTOR_ROTATION, Test Case 2 — Risk-off, chiến thuật DERISK, Test Case 3 — Chiến thuật WAIT, Test Case 4 — Tăng giá không có dòng tiền (bẫy xếp loại), Test Case 5 — Thiếu dữ liệu Flow, Test Cases — Sector Rotation Agent v0.2

### Community 32 - "Community 32"
Cohesion: 0.25
Nodes (7): 1. Từ Strategy Selector Agent (bắt buộc), 2. Từ Sector Rotation Agent (bắt buộc), 3. Universe & dữ liệu cổ phiếu (bắt buộc), 4. Bối cảnh (không bắt buộc), Input Schema — Stock Watchlist Agent v0.2, Meta, Quy tắc fallback khi thiếu dữ liệu

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (7): Chỉ quan sát, Có thể hành động nếu xác nhận, Handoff To Risk Manager, Nên tránh, Output Template — STOCK WATCHLIST REPORT, STOCK WATCHLIST REPORT — [dd/mm/yyyy], Watchlist Summary

### Community 34 - "Community 34"
Cohesion: 0.25
Nodes (7): 1. Từ Stock Watchlist Agent (bắt buộc), 2. Bối cảnh pipeline (bắt buộc), 3. Hồ sơ khách (không bắt buộc), 4. Rủi ro sự kiện (không bắt buộc nhưng nên có), Input Schema — Risk Manager Agent v0.2, Meta, Quy tắc fallback khi thiếu dữ liệu

### Community 35 - "Community 35"
Cohesion: 0.25
Nodes (7): Appendix — CSS core (copy nguyên khối làm khung), Brand & Style, Cấu trúc trang (theo thứ tự, dùng đúng tên class), Design chuẩn cho MỌI báo cáo — nhân bản template "Bản tin TTCK", Elevation & Shape, Ngữ nghĩa màu (bắt buộc thống nhất), Quy tắc bắt buộc khi sinh báo cáo mới

### Community 36 - "Community 36"
Cohesion: 0.25
Nodes (7): Checklist, Debugging Patterns, Debugging with GitNexus, Example: "Payment endpoint returns 500 intermittently", Tools, When to Use, Workflow

### Community 37 - "Community 37"
Cohesion: 0.25
Nodes (7): Checklist, Example: "How does payment processing work?", Exploring Codebases with GitNexus, Resources, Tools, When to Use, Workflow

### Community 38 - "Community 38"
Cohesion: 0.25
Nodes (7): Always Start Here, GitNexus Guide, Graph Schema, Paginating `list_repos`, Resources Reference, Skills, Tools Reference

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): Decisions, Final Broker Note, Output Template — RISK REVIEW REPORT, Portfolio-Level Notes, RISK REVIEW REPORT — [dd/mm/yyyy], Risk Review Summary

### Community 40 - "Community 40"
Cohesion: 0.33
Nodes (5): 01 Market Regime Agent, Cách chạy, Cấu trúc thư mục, Mô hình tham chiếu, Nguyên tắc bất biến

### Community 41 - "Community 41"
Cohesion: 0.33
Nodes (5): 02 Strategy Selector Agent, Cách chạy, Cấu trúc thư mục, Mô hình tham chiếu, Nguyên tắc bất biến

### Community 42 - "Community 42"
Cohesion: 0.33
Nodes (5): 03 Sector Rotation Agent, Cách chạy, Cấu trúc thư mục, Mô hình tham chiếu, Nguyên tắc bất biến

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (5): 04 Stock Watchlist Agent, Cách chạy, Cấu trúc thư mục, Mô hình tham chiếu, Nguyên tắc bất biến

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (5): Main Prompt — Risk Manager Agent v0.2, Output, Quy trình bắt buộc: chạy 6 cổng theo thứ tự cho TỪNG mã, Quy tắc cứng (không ngoại lệ), Thang quyết định

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (5): 05 Risk Manager Agent, Cách chạy, Cấu trúc thư mục, Mô hình tham chiếu, Nguyên tắc bất biến

### Community 46 - "Community 46"
Cohesion: 0.40
Nodes (4): Main Prompt — Strategy Selector Agent v0.2, Quy trình bắt buộc (làm theo đúng thứ tự), Quy tắc cứng (nhắc lại, không ngoại lệ), Thư viện chiến thuật (chỉ được chọn trong danh sách này)

### Community 47 - "Community 47"
Cohesion: 0.50
Nodes (3): Changelog, v0.1, v0.2 — 2026-06-11

### Community 48 - "Community 48"
Cohesion: 0.50
Nodes (3): Main Prompt — Market Regime Agent v0.2, Quy trình bắt buộc (làm theo đúng thứ tự), Quy tắc cứng

### Community 49 - "Community 49"
Cohesion: 0.50
Nodes (3): Changelog, v0.1, v0.2

### Community 50 - "Community 50"
Cohesion: 0.50
Nodes (3): Changelog, v0.1, v0.2

### Community 51 - "Community 51"
Cohesion: 0.50
Nodes (3): Main Prompt — Sector Rotation Agent v0.2, Quy trình bắt buộc (làm theo đúng thứ tự), Quy tắc cứng (không ngoại lệ)

### Community 52 - "Community 52"
Cohesion: 0.50
Nodes (3): Changelog, v0.1, v0.2

### Community 53 - "Community 53"
Cohesion: 0.50
Nodes (3): Main Prompt — Stock Watchlist Agent v0.2, Quy trình bắt buộc (làm theo đúng thứ tự), Quy tắc cứng (không ngoại lệ)

### Community 54 - "Community 54"
Cohesion: 0.50
Nodes (3): Changelog, v0.1, v0.2

### Community 55 - "Community 55"
Cohesion: 0.50
Nodes (3): Handoff cho Strategy Selector, Kết luận (MOCK), MARKET REGIME REPORT — 2026-06-11

### Community 56 - "Community 56"
Cohesion: 0.50
Nodes (3): Chiến thuật chính hôm nay (MOCK), Handoff, STRATEGY SELECTION REPORT — 2026-06-11

### Community 60 - "Community 60"
Cohesion: 0.07
Nodes (26): 1. Chứng khoán (Securities), 1. Công nghệ thông tin (Technology/IT), 2. Ngân hàng (Banking), 2. Thép (Steel), 3. Bán lẻ (Retail), 3. Bất động sản (Real Estate), 4. Dầu khí (Oil & Gas), 4. Xây dựng (Construction) (+18 more)

### Community 61 - "Community 61"
Cohesion: 0.10
Nodes (20): Bước 2 — Ma trận Regime, Bước 3 — Áp bộ điều chỉnh (theo thứ tự), Bước 4 — Kiểm tra quy tắc cứng, Bước 5 — Kết quả chọn, Cơ sở, Handoff cho Agent 03 / Agent 04, Hành động thực tế, I. Handoff nhận được — Tóm tắt đầu vào (+12 more)

### Community 62 - "Community 62"
Cohesion: 0.13
Nodes (14): 1. Kiểm kê dữ liệu, 2. Bảng Scorecard, 3. Xác định Regime, 4. Trạng thái phụ, 4a. Phân hóa ngành, 4b. Hồi kỹ thuật trong ngày, 4c. Bull trap risk, 4d. Panic selling (+6 more)

### Community 63 - "Community 63"
Cohesion: 0.09
Nodes (21): 🚫 AVOID CHASING *(Cấm mua đuổi — ưu tiên THOÁT nếu đang giữ)*, Bán lẻ (MWG, DGW, FRT), Bất động sản — Vingroup Cluster (VIC, VHM, VRE), Chứng khoán (VND, VIX, SSI, HCM), Công nghệ / IT (FPT, CMG, ELC), Dầu khí (GAS, PLX, BSR, PVS), I. HANDOFF ĐÃ ĐỌC, II. ĐIỀU KIỆN THỊ TRƯỜNG TỔNG QUAN (5 PHIÊN 11–18/06/2026) (+13 more)

### Community 64 - "Community 64"
Cohesion: 0.11
Nodes (17): 1. KIỂM KÊ DỮ LIỆU, 2. SCORECARD, 3. REGIME, 4. TRẠNG THÁI PHỤ, 5. QUY TẮC "HẠ NHANH – NÂNG CHẬM", 6. CONFIDENCE, 7. CHIỀU PHẢN BIỆN, 8. ĐIỀU KIỆN CHUYỂN TRẠNG THÁI (+9 more)

### Community 65 - "Community 65"
Cohesion: 0.20
Nodes (9): 🟥 Chiến thuật chính — `WAIT`, 🟨 Chiến thuật phụ — `DERISK`, I. HANDOFF ĐÃ ĐỌC, II. QUÁ TRÌNH ÁP MA TRẬN, III. LỰA CHỌN CHIẾN THUẬT, IV. CHIẾN THUẬT BỊ CẤM HÔM NAY, STRATEGY SELECTION REPORT, V. TÓM TẮT CHO BROKER (ĐỌC < 1 PHÚT) (+1 more)

### Community 66 - "Community 66"
Cohesion: 0.09
Nodes (22): BĐS nhỏ & CK mid-small — bằng chứng Avoid Chasing, BƯỚC 1 — XÁC NHẬN HANDOFF, BƯỚC 2 — CHẤM RS VÀ FLOW: 10 NHÓM NGÀNH CHÍNH, BƯỚC 3 — MAP VÀO 4 NHÓM, BƯỚC 4 — LỌC THEO STRATEGY CODE, BƯỚC 5 — KIỂM TRA QUY TẮC CỨNG, BƯỚC 6 — EVIDENCE CÓ SỐ LIỆU, Bảng chấm điểm từng ngành (+14 more)

### Community 67 - "Community 67"
Cohesion: 0.10
Nodes (20): 1. KIỂM KÊ DỮ LIỆU ĐẦU VÀO, 2.1 Trend — Điểm: **-1** (25%), 2.2 Breadth — Điểm: **-2** (20%), 2.3 Liquidity — Điểm: **-1** (20%), 2.4 Flows — Điểm: **-2** (15%), 2.5 Volatility/Phái sinh — Điểm: **0** (10%), 2.6 Macro/Sentiment — Điểm: **0** (10%), 2. SCORECARD — CHẤM ĐIỂM TỪNG TRỤ CỘT (+12 more)

### Community 68 - "Community 68"
Cohesion: 0.15
Nodes (12): 1. HANDOFF ĐẦU VÀO — XÁC NHẬN TIẾP NHẬN, 2. QUY TRÌNH LỰA CHỌN, 3. CHIẾN THUẬT ĐÃ CHỌN, 4. CHIẾN THUẬT KHÔNG NÊN DÙNG — DANH SÁCH BỊ CẤM, 5. LƯU Ý THỰC HÀNH CHO BROKER, 6. HANDOFF → AGENT 03 (STOCK SELECTOR) / AGENT 04 (RISK MANAGER), Bước 2 — Tra ma trận Regime → Chiến thuật, Bước 3 — Áp bộ điều chỉnh (theo thứ tự) (+4 more)

### Community 69 - "Community 69"
Cohesion: 0.11
Nodes (17): 1. Handoff nhận được từ Market Regime Agent, 2. Quy trình chọn chiến thuật (vết làm việc), 3. Chiến thuật được chọn, 4. Chiến thuật bị cấm trong bối cảnh hôm nay, 5. Tóm tắt hành động theo trạng thái tài khoản, 6. Kịch bản theo dõi phiên kế tiếp, 7. HANDOFF — Stock Picker & Execution Desk (Agent 03/04), Bước 2 — Tra ma trận ban đầu theo Regime Code (+9 more)

### Community 70 - "Community 70"
Cohesion: 0.12
Nodes (15): 1. Kiểm kê dữ liệu, 2. Scorecard, 3. Xác định Regime, 4. Trạng thái phụ, 5. Quy tắc "Hạ nhanh, Nâng chậm", 6. Confidence, 7. Chiều phản biện — Rủi ro của chính kết luận này, 8. Điều kiện chuyển trạng thái (ngưỡng đo được) (+7 more)

### Community 71 - "Community 71"
Cohesion: 0.14
Nodes (13): 0. HANDOFF ĐÃ ĐỌC — Strategy Selector, 1. THU THẬP DỮ LIỆU — Nguồn & Phương pháp, 2. CHẤM ĐIỂM TỪNG NGÀNH — RS & Flow, 3. SECTOR MAP 4 NHÓM, 4. EVIDENCE CÓ SỐ LIỆU, 4A. Bất động sản — AVOID CHASING (Ưu tiên DERISK #1), 4B. CNTT — WEAK, 4C. Ngân hàng / Chứng khoán / Thép / Bán lẻ — IMPROVING (tín hiệu chưa xác nhận) (+5 more)

## Knowledge Gaps
- **510 isolated node(s):** `1. Kiểm kê dữ liệu`, `2. Scorecard`, `3. Xác định Regime`, `⚠️ BULL TRAP RISK — CẢNH BÁO BẮT BUỘC`, `📊 Phân hóa mạnh` (+505 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `1. Kiểm kê dữ liệu`, `2. Scorecard`, `3. Xác định Regime` to the rest of the system?**
  _524 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._
- **Should `Community 5` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Community 8` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Community 9` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Community 10` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._