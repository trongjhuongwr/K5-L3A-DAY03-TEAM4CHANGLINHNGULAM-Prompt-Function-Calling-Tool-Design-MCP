# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần:
> - **Phần A (mục 2)** — giới thiệu agent ngắn gọn, phục vụ Team Showdown (A1, A2, A3). Kèm poster tại [report/team/poster.html](poster.html).
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng thực nghiệm, dựa trên log thật trong `runs/`, `transcripts/`, và lịch sử git commit.
>
> Mọi bảng đều trỏ tới file thật trong repo: run JSON, transcript, commit. Đánh giá theo chuẩn [RUBRIC.md](../../RUBRIC.md).

---

## 1. Thông tin nhóm

- **Tên nhóm:** Team 4 (4 Chàng Lính Ngự Lâm)
- **Lớp:** L3A
- **Repo:** `K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`
- **Thành viên và phân công:** xem chi tiết tại [TEAM.md](../../TEAM.md)
  1. Nguyễn Trọng Hưởng (MSSV: 2A202603607) — Trưởng nhóm / Core Architect ([2A202603607_NguyenTrongHuong.md](2A202603607_NguyenTrongHuong.md))
  2. Đàm Tuấn Linh (MSSV: 2A202603624) — Research & Evidence Specialist ([2A202603624_DamTuanLinh.md](2A202603624_DamTuanLinh.md))
  3. Lê Thành Đạt (MSSV: 2A202603579) — UI & Testing Specialist ([2A202603579_LeThanhDat.md](2A202603579_LeThanhDat.md))
  4. Phạm Ngọc Trung Quân (MSSV: 2A202603626) — Content Analysis Specialist ([2A202603626_PhamNgocTrungQuan.md](2A202603626_PhamNgocTrungQuan.md))
- **Provider / model dùng cho v0–v3:** OpenRouter / `openai/gpt-4o-mini` (và kiểm chứng chéo với OpenAI provider).

---

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent là trợ lý nghiên cứu đa năng thông minh:
- **Thu thập & Tổng hợp:** Tìm kiếm bài đăng mạng xã hội X theo tài khoản/từ khóa, lọc tin theo khoảng thời gian thực, đọc và trích xuất nội dung URL, tra cứu văn bản chính sách nội bộ và bài báo nghiên cứu arXiv.
- **Tiện ích thực tế:** Tích hợp bộ công cụ mở rộng phong phú gồm tính toán biểu thức an toàn, tra cứu giá crypto thời gian thực, tìm kiếm repo GitHub, và xem thời tiết địa phương.
- **Kiểm chứng & Phân tích chuyên sâu:** Tra cứu định danh tài khoản (`resolve_account`), gom URL trùng lặp (`deduplicate_news`), thu thập bằng chứng kiểm chứng chéo phát biểu (`cross_check_claim`), so sánh đa góc nhìn (`compare`) và phân tích cảm xúc (`sentiment`).
- **Ranh giới an toàn (Guardrail):** Luôn hỏi lại người dùng khi thiếu dữ liệu bắt buộc (`clarify`) và **chỉ gửi thông tin lên Telegram khi có xác nhận rõ ràng** (`send(confirmed=true)`).

**Cách chạy UI:**
```powershell
cd starter_v0
streamlit run app.py
```
*(Dependencies đã được cấu hình trong `starter_v0/requirements.txt`: `streamlit`, `yaml`, `requests`, `openai`)*.

**Poster giới thiệu:** Xem poster trực quan tại [report/team/poster.html](poster.html).

### A2. Tool agent có

| Tên tool | Làm được gì | Phân loại | Tác giả phụ trách |
|---|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin bắt buộc hoặc yêu cầu xác nhận | Có sẵn | Starter |
| `timeline` | Lấy các bài đăng mới nhất từ tài khoản X theo handle | Có sẵn | Starter |
| `social_search` | Tìm kiếm bài đăng X theo từ khóa, lọc theo `Latest` hoặc `Top` | Có sẵn | Starter |
| `lookup` | Tra cứu tin tức và thông tin web có giới hạn thời gian | Có sẵn | Starter |
| `fetch` | Đọc và trích xuất tóm tắt nội dung bài viết từ URL (Firecrawl API) | Có sẵn | Starter |
| `format` | Định dạng danh sách tin thành bản tin tổng hợp Markdown | Có sẵn | Starter |
| `send` | Gửi bản tin lên Telegram sau khi người dùng xác nhận (`confirmed=true`) | Có sẵn (Guardrail) | Starter |
| `policy` | Tra cứu quy định nội bộ công ty (bảo mật dữ liệu, trích dẫn nguồn) | Có sẵn | Starter |
| `papers` | Tìm kiếm các bài báo khoa học trên arXiv | Có sẵn | Starter |
| `paper_text` | Trích xuất toàn văn hoặc đoạn trích từ bài báo arXiv | Có sẵn | Starter |
| `calculator` | Đánh giá biểu thức số học an toàn bằng cú pháp AST | Mới (CP3) | Nguyễn Trọng Hướng |
| `crypto_price` | Tra cứu giá tiền mã hóa thời gian thực (USDT/BTC qua CoinGecko/Binance) | Mới (CP3) | Nguyễn Trọng Hướng |
| `github_search` | Tìm kiếm kho lưu trữ GitHub theo từ khóa, lấy repo, sao, link | Mới (CP3) | Nguyễn Trọng Hướng |
| `weather` | Tra cứu thông tin thời tiết địa phương real-time qua `wttr.in` | Mới (CP3) | Nguyễn Trọng Hướng |
| `resolve_account` | Tra cứu handle chuẩn từ danh mục `accounts.json` có nguồn đối chiếu | Mới (Research) | Đàm Tuấn Linh |
| `deduplicate_news` | Chuẩn hóa URL, loại bỏ tracking parameter (`utm_*`), gộp tin trùng lặp | Mới (Research) | Đàm Tuấn Linh |
| `cross_check_claim` | Thu thập bằng chứng đa nguồn từ web để đối chiếu một phát biểu | Mới (Research) | Đàm Tuấn Linh |
| `compare` | So sánh độ tin cậy, sắc thái (`tone`) và tìm điểm đồng thuận giữa các nguồn | Mới (Analysis) | Trung Quân |
| `sentiment` | Phân tích cảm xúc văn bản (tích cực, tiêu cực, trung lập) không phụ thuộc ML nặng | Mới (Analysis) | Trung Quân |
| `summarize_thread` | Bóc tách và tóm tắt luồng thảo luận trên Twitter, Reddit, HackerNews | Mới (Analysis) | Trung Quân |

### A3. Câu hỏi mẫu để thử

1. **Tra cứu & Tính toán:** *"Giá Bitcoin hôm nay là bao nhiêu USDT? Nếu tôi có 0.35 BTC thì trị giá bao nhiêu USD?"*
2. **Kiểm tra thời tiết & Tin tức:** *"Thời tiết Hà Nội hôm nay thế nào? Tìm cho tôi 3 tin mới nhất về trí tuệ nhân tạo."*
3. **Mã nguồn GitHub:** *"Tìm các repo GitHub nổi bật nhất về 'Agent Evaluation benchmark'."*
4. **Kiểm chứng phát biểu:** *"Đối chiếu phát biểu sau với 2 nguồn web: 'Mọi bài trên arXiv đều đã qua bình duyệt peer-review'."*
5. **Ranh giới gửi tin:** *"Gửi bản tin tóm tắt về Nvidia sang Telegram ngay cho tôi."* (Agent sẽ kích hoạt hỏi xác nhận thay vì tự ý gửi).

---

## 3. Giải pháp

Nhóm áp dụng nguyên lý lặp kiểm chứng dựa trên bằng chứng (evidence-based iteration loop):
1. **Tinh chỉnh `artifacts/system_prompt.md`:**
   - Loại bỏ các chỉ dẫn xấu của starter (như đoán mò username, gọi tool send bừa bãi).
   - Thiết lập quy tắc routing phân cấp rõ ràng: phân biệt `lookup` (web) vs `social_search` (mạng xã hội X); nhận diện khi nào cần gọi `clarify` (thiếu username, thiếu URL).
   - Bổ sung cơ chế inject đồng hồ thời gian động qua module [`runtime_context.py`](file:///starter_v0/runtime_context.py) lấy múi giờ `Asia/Bangkok` (UTC+7) giúp agent luôn biết chính xác ngày hôm nay.
2. **Chuẩn hóa `artifacts/tools.yaml`:**
   - Mô tả chi tiết khi nào nên dùng và khi nào **không** nên dùng cho từng công cụ.
   - Định nghĩa chính xác schema các tham số bắt buộc (`required`), enum (`response_type`, `search_type`, `template`), và các ràng buộc guardrail của `send`.
3. **Phát triển 10 công cụ mới:** Đảm bảo 100% các tool đều có file `TOOL.md`, đăng ký trong `TOOL_FUNCTIONS`, khai báo trong `tools.yaml` và có bộ unit test độc lập xử lý lỗi an toàn (trả về dictionary lỗi thay vì crash exception).

---

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Dữ liệu được trích xuất trực tiếp từ [starter_v0/artifacts/version_log.csv](file:///starter_v0/artifacts/version_log.csv) và các file run JSON trong `starter_v0/runs/`. Toàn bộ các run đều thỏa mãn điều kiện hợp lệ: `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| **v0** | Baseline gốc | Đo hành vi chưa tối ưu của starter prompt và tool declaration gốc | N/A | **0.65** | [v0_B_base_openrouter_20261110T105123112923.json](file:///starter_v0/runs/v0_B_base_openrouter_20261110T105123112923.json) |
| **v1** | `system_prompt.md` | Chặn đoán mò, bổ sung quy tắc routing nghiêm ngặt và bắt buộc hỏi lại khi thiếu thông tin | 0.65 | **0.85** | [v1_B_base_openrouter_20261110T112216959209.json](file:///starter_v0/runs/v1_B_base_openrouter_20261110T112216959209.json) |
| **v2** | `system_prompt.md` | Chống over-clarify khi đã có URL rõ ràng, map tên sang canonical handle | 0.85 | **0.95** | [v2_B_base_openrouter_20261110T113251759897.json](file:///starter_v0/runs/v2_B_base_openrouter_20261110T113251759897.json) |
| **v3** | `system_prompt.md` + `tools.yaml` | Tôn trọng chuyển đổi công cụ đa lượt (multi-turn), tích hợp các tool mở rộng | 0.95 | **1.00** | [v3_B_base_openrouter_20261110T155932076825.json](file:///starter_v0/runs/v3_B_base_openrouter_20261110T155932076825.json) |
| **v3-group** | `eval_group.json` | Đánh giá 10 test case nhóm đa dạng (single + multi-turn) bao gồm cả tool mới | N/A | **1.00** (10/10) | [v3_B_group_openrouter_20261110T160007571577.json](file:///starter_v0/runs/v3_B_group_openrouter_20261110T160007571577.json) |

### B2. Failure Analysis

Phân tích chi tiết 7 case thất bại ở bản baseline v0 (trích xuất từ [v0_failure_analysis.csv](file:///v0_failure_analysis.csv) và run log v0):

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | wrong_arg_value | `lookup(query='AI news')` | Query thừa từ khóa rác `news`, mong đợi là `'AI'` | Chuẩn hóa quy tắc trích xuất thực thể cốt lõi cho query trong `system_prompt.md`. |
| `R08_out_of_scope` | unexpected_tool_call | `send(text=...)` | Yêu cầu nằm ngoài phạm vi nhưng agent tự ý gọi `send` | Bổ sung quy tắc: nếu yêu cầu không thuộc năng lực, từ chối lịch sự và KHÔNG gọi tool. |
| `R10_missing_handle` | missing_info | `timeline(screenname='...')` | Thiếu tên người dùng nhưng agent tự đoán mò username | Bắt buộc gọi `clarify` để hỏi lại handle khi người dùng chưa cung cấp. |
| `R11_missing_url` | missing_info | `fetch(url='...')` | Thiếu link bài viết nhưng agent gọi `fetch` với link giả | Yêu cầu gọi `clarify` xin URL bài báo trước khi thực hiện đọc web. |
| `R12_confirm_before_send` | wrong_boundary | `send(confirmed=False)` | Agent tự động gửi tin nhắn mà chưa có xác nhận rõ ràng | Thiết lập ranh giới an toàn: luôn gọi `clarify(response_type="yes_no")` để xin phép trước khi `send`. |
| `R13_parallel_web_and_tweets` | wrong_arg_value | `lookup(...), social_search(...)` | Query bị sai format tham số `topic` | Hướng dẫn cụ thể cách trích xuất tham số song song trong prompt. |
| `R14_out_of_scope_coding` | unexpected_tool_call | `send(...)` | Yêu cầu viết code nhưng agent gọi `send` | Nhận diện câu hỏi coding/ngoài luồng và trả lời trực tiếp không dùng tool. |

### B3. Team Eval Cases

Danh sách đúng **10 test case nhóm** (5 single-turn + 5 multi-turn) tại [starter_v0/data/eval_group.json](file:///starter_v0/data/eval_group.json):

| Case ID | Loại lượt | What It Tests | Expected Tool / Behavior | Result |
|---|---|---|---|---|
| `G01_crypto_price_routing` | Single-turn | Định tuyến câu hỏi giá crypto sang `crypto_price` | `crypto_price(symbol="BTC", currency="USDT")` | **PASS** |
| `G02_github_search_routing` | Single-turn | Tìm kiếm repo mã nguồn chuyển tới `github_search` | `github_search(query="agent evaluation", limit=3)` | **PASS** |
| `G03_weather_routing` | Single-turn | Câu hỏi thời tiết thành phố gọi `weather` | `weather(city="Hanoi")` | **PASS** |
| `G04_calculator_routing` | Single-turn | Biểu thức toán học gọi `calculator` an toàn | `calculator(expression="15 * 4 + 2 ^ 3")` | **PASS** |
| `G05_unnecessary_tool_metaphor` | Single-turn | Câu nói ẩn dụ/chào hỏi không được gọi tool | `no_tool` (trả lời trực tiếp) | **PASS** |
| `G06_crypto_clarify_then_symbol` | Multi-turn | Hỏi lại khi thiếu mã coin rồi gọi `crypto_price` ở turn 2 | Turn 1: `clarify` → Turn 2: `crypto_price(symbol="ETH")` | **PASS** |
| `G07_github_search_refinement` | Multi-turn | Cập nhật từ khóa tìm kiếm repo qua nhiều lượt | Turn 1: `github_search` → Turn 2: `github_search` mới | **PASS** |
| `G08_switch_weather_to_news` | Multi-turn | Chuyển đổi công cụ linh hoạt giữa các chủ đề | Turn 1: `weather` → Turn 2: `lookup` tin tức | **PASS** |
| `G09_calculator_multiturn` | Multi-turn | Nhớ kết quả tính toán lượt trước để tính tiếp | Turn 1: `calculator` → Turn 2: `calculator` kế thừa | **PASS** |
| `G10_confirm_before_send_action` | Multi-turn | Quy trình 2 bước: hỏi xác nhận rồi mới gửi | Turn 1: `clarify` → Turn 2: `send(confirmed=True)` | **PASS** |

### B4. Live Chat Evidence

Trích xuất từ 7 file transcripts thực tế trong thư mục [starter_v0/transcripts/](file:///starter_v0/transcripts/):

| Transcript ID | Turn | User Request | Tool Calls | Outcome & Ghi chú |
|---|---|---|---|---|
| `...121828401223` | 1 | "tôi muốn lấy thông tin các bài báo liên quan đến LLM reasoning" | `papers(query="LLM reasoning", limit=5)` | Lấy thành công 5 bài báo arXiv mới nhất kèm tóm tắt và link PDF. |
| `...121828401223` | 2 | "tóm tắt lại bài 2406.12345 và gửi telegram" | `paper_text(...)` → `clarify(question="Bạn có chắc chắn muốn gửi...?")` | **Kích hoạt Guardrail:** Agent hỏi lại xác nhận người dùng trước khi gửi. |
| `...121828401223` | 3 | "Đồng ý gửi đi" | `send(text="...", confirmed=True)` | Bản tin được gửi thành công với trạng thái `status: sent`. |
| `...121037448995` | 1 | "giá solana hiện tại thế nào" | `crypto_price(symbol="SOL", currency="USDT")` | Trả về giá SOL real-time kèm biến động 24h. |
| `...121037448995` | 2 | "thời tiết đà nẵng hôm nay mưa không" | `weather(city="Da Nang")` | Trả về nhiệt độ, độ ẩm và dự báo mưa. |
| `...120036407471` | 1 | "Hôm nay là ngày mấy?" (với `runtime_context`) | *Không gọi tool* (trả lời trực tiếp) | **Đúng thời gian thực:** Agent trả lời chính xác ngày hiện tại năm **2026** nhờ module clock UTC+7. |

### B5a. Required Evidence — Tool mới, Unit test, UI

| Hạng mục | File bằng chứng | Kết quả đạt được | Ranh giới & Guardrail |
|---|---|---|---|
| **Bộ 10 Tool mới** | `starter_v0/tools/*/` | Cả 10 tool đều có `tool.py`, `TOOL.md`, đăng ký trong `TOOL_FUNCTIONS` và `tools.yaml` | Xử lý lỗi trả về error dict, kiểm soát kiểu dữ liệu và giới hạn request. |
| **Unit tests tool mới** | `tests/test_tools_todo.py`, `tests/test_content_analysis_tools.py`, `tests/test_research_extensions.py` | Toàn bộ suite đạt **150 passed, 0 failed, 0 skipped** (vượt xa yêu cầu $\ge 3$ test/tool) | 100% test offline dùng mock/fake HTTP, không phụ thuộc kết nối mạng. |
| **Giao diện Web UI** | `starter_v0/app.py` | Streamlit app chạy mượt mà, phân loại icon theo nhóm tool, tự động lưu transcript | Hỗ trợ chọn model, hiển thị tool calls rõ ràng và không che giấu lỗi API. |

### B5. Bonus Evidence

| Bonus | Điểm | File bằng chứng | Những gì đã đạt được |
|---|---:|---|---|
| **Hơn 3 tool mới ($\ge 4$ tool)** | **3** | `starter_v0/tools/` (10 tool mới) | Nhóm đã phát triển tổng cộng **10 công cụ mới** (4 tiện ích + 3 nghiên cứu + 3 phân tích nội dung), đều có unit test đầy đủ. |
| **Test Challenge (0 skipped)** | **1** | `tests/test_tools_todo.py` | Toàn bộ test suite `pytest` đạt **150 passed, 0 skipped, 0 failed**. Đã giải quyết 100% các TODO tests của starter. |
| **Sửa lỗi Clock & Tokenizer** | — | `runtime_context.py`, `sentiment/tool.py` | 1. Sửa lỗi năm 2023 vs 2026 bằng đồng hồ UTC+7 động.<br>2. Sửa lỗi tokenizer dính dấu câu trong bộ phân tích cảm xúc `sentiment`. |

---

## 5. Khó khăn và cách xử lý

1. **Vấn đề model bị "mù" thời gian thực (Lỗi năm 2023 vs 2026):**
   - *Triệu chứng:* Khi người dùng hỏi *"Hôm nay là ngày mấy?"*, agent trả lời là *10/11/2023* (do kiến thức đóng băng của model).
   - *Giải pháp:* Đàm Tuấn Linh đã thiết kế module [`runtime_context.py`](file:///starter_v0/runtime_context.py) lấy thời gian thực từ máy chủ theo múi giờ `Asia/Bangkok` (UTC+07:00), tự động inject vào tin nhắn hệ thống ở mỗi lượt gọi. Agent nhận diện chính xác ngày hiện tại mà không cần hard-code năm 2026.
2. **Lỗi Tokenizer đơn giản trong phân tích từ khóa:**
   - *Triệu chứng:* Trong tool `sentiment`, các từ cảm xúc như `"amazing,"`, `"brilliant!"` bị trượt khỏi bộ từ điển do dính dấu phẩy và dấu chấm than khi `split()` khoảng trắng thông thường.
   - *Giải pháp:* Trung Quân đã chuyển sang trích xuất token bằng regex ranh giới từ `\b\w+\b`, giúp nhận diện chính xác 100% các từ cảm xúc trong văn bản tự nhiên.
3. **Hiện tượng Over-clarify ở phiên bản v1:**
   - *Triệu chứng:* Sau khi thêm rule bắt buộc hỏi lại khi thiếu thông tin, model có xu hướng hỏi lại cả những câu người dùng đã đưa sẵn URL hoặc tên tài khoản rõ ràng.
   - *Giải pháp:* Nguyễn Trọng Hướng đã phân tách rõ điều kiện: chỉ gọi `clarify` khi câu truy vấn hoàn toàn thiếu thực thể định danh, còn nếu đã có URL/handle thì ưu tiên gọi `fetch` hoặc `timeline`.

---

## 6. Tổng hợp đóng góp

Chi tiết đóng góp cụ thể và các file bằng chứng của từng thành viên được ghi nhận tại [TEAM.md](../../TEAM.md) và trong các báo cáo cá nhân:
- Nguyễn Trọng Hưởng: [report/team/2A202603607_NguyenTrongHuong.md](2A202603607_NguyenTrongHuong.md)
- Đàm Tuấn Linh: [report/team/2A202603624_DamTuanLinh.md](2A202603624_DamTuanLinh.md)
- Lê Thành Đạt: [report/team/2A202603579_LeThanhDat.md](2A202603579_LeThanhDat.md)
- Phạm Ngọc Trung Quân: [report/team/2A202603626_PhamNgocTrungQuan.md](2A202603626_PhamNgocTrungQuan.md)

---

## 7. Hạn chế và hướng cải thiện — B6. Reflection

1. **Ranh giới giữa `system_prompt.md` và `tools.yaml`:**
   - Các quy tắc về **hành vi ứng xử, luồng đối thoại, khi nào cần xác nhận, ưu tiên ngữ cảnh đa lượt** bắt buộc phải nằm trong `system_prompt.md`.
   - Các quy tắc về **kiểu dữ liệu, định dạng tham số (`enum`), trường bắt buộc (`required`), và mô tả công năng chi tiết từng hàm** nằm trong `tools.yaml`.
2. **Những lỗi cần review thủ công thay vì chấm tự động:**
   - Độ tự nhiên và văn phong câu hỏi của `clarify`: hệ thống eval tự động chỉ kiểm tra xem có gọi hàm `clarify` hay không, nhưng không đánh giá được câu hỏi có lịch sự, ngắn gọn và trúng ý người dùng hay không.
   - Ranh giới xác nhận ở `send`: cần người thật kiểm tra xem nội dung bản tin draft hiển thị cho người dùng có đúng là nội dung cuối cùng được gửi đi hay không.
3. **Giả thuyết cho vòng lặp tiếp theo:**
   - Nếu có thêm thời gian, nhóm sẽ tích hợp các mô hình ngôn ngữ nhỏ cục bộ (SLM / Local LLM như `qwen2.5:3b` qua Ollama) để đánh giá khả năng Function Calling của mô hình nhỏ so với các mô hình đám mây lớn.

---

## 8. Tài liệu tham khảo

- VinUni AI20k Course Material — Day 03: Prompt Engineering, Tool Calling & MCP.
- OpenAI Function Calling Guide & Structured Outputs Documentation.
- Streamlit Documentation & Firecrawl Web Scraper API.
