# Day 03 Lab v2 Report — Research Agent

## Team

- Team: Team 4 (from repository name)
- Members: Chưa được cung cấp
- Provider/model đã đo: OpenRouter / `openai/gpt-4o-mini`
- Ngày ghi nhận: 2026-11-10

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent tìm bài đăng theo tài khoản hoặc chủ đề, lọc bài theo khoảng ngày, tra cứu web/tin tức, đọc URL và tổng hợp kết quả thành digest. Agent có thể tra cứu chính sách nội bộ và paper arXiv; chỉ gửi Telegram sau khi nội dung được duyệt và xác nhận.

**Link dùng thử:** Chưa deploy. Giao diện Streamlit đã được thêm tại `app.py`; cần môi trường Python và API keys hợp lệ để chạy.

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi thông tin còn thiếu hoặc xác nhận hành động | Không |
| timeline | Lấy bài mới nhất của một tài khoản X | Không |
| recent_timeline | Lấy timeline rồi lọc timestamp theo số ngày gần nhất | Có |
| social_search | Tìm bài X theo từ khóa, Latest hoặc Top | Không |
| lookup | Tra cứu web và tin tức theo thời gian | Không |
| fetch | Đọc nội dung URL | Không |
| format | Định dạng kết quả thành digest | Không |
| send | Gửi Telegram sau khi xác nhận | Không |
| policy | Tìm trong chính sách nội bộ | Không |
| papers | Tìm paper trên arXiv | Không |
| paper_text | Trích văn bản từ paper arXiv cụ thể | Không |
| resolve_account | Tra tên/alias sang handle trong danh mục có nguồn tham chiếu | Có |
| deduplicate_news | Gộp URL trùng, giữ item gốc và nguồn; đánh dấu tiêu đề giống nhau để xem lại | Có |
| cross_check_claim | Tìm và đọc bằng chứng web cho một phát biểu, trả trạng thái cần xem xét | Có |

## A3. Câu hỏi mẫu để thử

1. Lấy 5 tweet mới nhất của Elon Musk.
2. Tóm tắt 5 tweet của Elon Musk trong 7 ngày qua.
3. Tra handle X của Andrej Karpathy và cho tôi nguồn đối chiếu.
4. Gộp URL trùng trong danh sách kết quả tôi cung cấp, giữ nguồn gốc.
5. Đối chiếu phát biểu “Mọi bài trên arXiv đều đã được bình duyệt” với tối đa 2 nguồn web.

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---|---|---|
| v0 | baseline | Đo chất lượng ban đầu | N/A | case 0.65; routing 0.75; args 0.65; multi-turn 1.00 | `v0_B_base_openrouter_20261110T104223427707.json` |
| v1 | system_prompt.md + tools.yaml | Mô tả routing và arguments rõ hơn sẽ tăng độ chính xác | case 0.65; routing 0.75; args 0.65; multi-turn 1.00 | case 0.80; routing 1.00; args 0.80; multi-turn 0.8333 | `v1_B_base_openrouter_20261110T170341521305.json` |
| v2 | system_prompt.md | Handle chuẩn và ưu tiên correction mới nhất sẽ cải thiện arguments nhiều lượt | case 0.80; routing 1.00; args 0.80; multi-turn 0.8333 | case 0.75; routing 1.00; args 0.75; multi-turn 1.00 | `v2_B_base_openrouter_20261110T171803334319.json` |
| v3 | Chưa chạy | Dự kiến: bắt buộc response_type rõ ràng cho clarify | Chờ v2 | Chưa đo | Chưa có |
| tools-v1 | Ba tool mới, registry, tools.yaml và routing prompt | Khai báo chức năng rõ giúp model route đúng yêu cầu cho ba tool mới | N/A — suite mới, không so với base | 3/3 case; routing 1.00; args 1.00 | `tools-v1_B_group_openrouter_20261110T200552940598.json` |

v2 đã sửa case handle nhiều lượt `M03`, nâng multi-turn lên 100%, nhưng tổng case giảm một điểm do query tin tức bị viết lại ở `R03` và `R13`. Một lần chạy chưa đủ để kết luận nguyên nhân do prompt hay độ biến thiên model.

## B2. Failure Analysis

| Case ID | Failure Type | Actual Tool Calls (v2) | What Failed | Fix dự kiến |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool / wrong_arg_value | `lookup(query="tin tức AI", topic="news", timeframe="day")` | Query phải là chủ đề cốt lõi `AI` theo eval | Quy định rõ bỏ từ dẫn “tin tức”, “hôm nay”, “có gì” khỏi query và chuyển thành topic/timeframe |
| R10_missing_handle | missing_info | `clarify(question=...)` | Không truyền `response_type="text"` | Bắt buộc truyền response_type trong schema và prompt |
| R11_missing_url | missing_info | `clarify(question=...)` | Không truyền `response_type="text"` | Như trên |
| R12_confirm_before_send | wrong_boundary | `clarify(question=...)` | Không truyền `response_type="yes_no"`; hỏi xin nội dung thay vì xác nhận | Nêu rõ yes_no cho xác nhận trước hành động gửi; không gọi send khi chưa có xác nhận |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | `lookup(query="tin AI", ...)` + `social_search(query="AI", ...)` | Query web phải giữ chủ đề cốt lõi `AI` | Quy định chuẩn hóa query web bằng ví dụ; giữ song song tool social_search đúng |

## B3. Team Eval Cases

Đã viết 13 case: 8 single-turn và 5 multi-turn. Đã chạy riêng G11–G13 bằng OpenRouter, cả ba PASS. Chưa chạy lại toàn bộ group; không dùng số liệu ba case mới để thay thế kết quả base v0–v3.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_recent_window_routes_to_recent_timeline | Lọc khoảng 7 ngày của một tài khoản | recent_timeline, elonmusk, 7 ngày, limit 5 | Chưa chạy |
| G02_top_social_search | Từ “nổi bật nhất” chọn Top | social_search, query OpenAI, Top | Chưa chạy |
| G03_news_today_uses_day_window | Tin hôm nay chọn news/day và query AI | lookup | Chưa chạy |
| G04_missing_article_url_asks | Thiếu URL thì hỏi lại | clarify/text | Chưa chạy |
| G05_out_of_scope_no_tool | Yêu cầu ngoài research | Không gọi tool | Chưa chạy |
| G06_multiturn_clarify_then_timeline | Giữ limit sau khi được bổ sung handle | timeline, elonmusk, limit 5 | Chưa chạy |
| G07_multiturn_topic_correction_preserves_news_window | Đổi chủ đề, giữ news/day | lookup, robotics | Chưa chạy |
| G08_multiturn_url_then_fetch | Giữ URL qua nhiều lượt | fetch URL được cung cấp | Chưa chạy |
| G09_multiturn_send_requires_confirmation | Chỉ gửi đúng draft sau xác nhận | send, confirmed=true | Chưa chạy |
| G10_multiturn_corrected_account_handle | Ưu tiên tài khoản đã correction | timeline, karpathy, limit 3 | Chưa chạy |
| G11_resolve_account_directory | Xác định handle từ danh mục có nguồn tham chiếu | resolve_account | PASS, trả found |
| G12_deduplicate_existing_items | Gộp các URL có tracking trong items đã có | deduplicate_news | PASS routing; thực thi gộp 2 thành 1 |
| G13_collect_claim_evidence | Thu thập nguồn đối chiếu phát biểu | cross_check_claim, max_sources=2 | PASS; trả 2 page_excerpt, needs_review, không có lỗi fetch |

## B4. Live Chat Evidence

Chưa có transcript live trong `transcripts/`. Cần chạy ít nhất 3 lượt chat và cập nhật bảng này từ transcript thật.

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | `tools/send/tool.py` | Code từ starter kiểm tra confirmation | Chưa có transcript live chứng minh; không bật gửi khi chưa duyệt nội dung |
| arXiv/company policy | `tools/papers/`, `tools/paper_text/`, `tools/policy/` | Có implementation sẵn từ starter | Cần key/provider và kiểm tra kết quả khi chạy live |
| UI | `app.py` | Streamlit AppTest đã khởi tạo thành công và có ô chat; prompt/schema đọc mới theo lượt, hash ghi theo lượt | Chưa có public link; AppTest chưa chứng minh chất lượng trả lời qua UI với model thật |
| Tool unit tests | `tests/`, `analysis/research_tools_pytest.txt` | Toàn bộ suite đạt 132 passed, 0 failed, 0 skipped | Chạy offline bằng Python trong `.venv` ngoài sandbox |

Tool mới `recent_timeline` đọc timestamp trả về, lọc theo khoảng N ngày và báo `coverage_complete=false` nếu dữ liệu API chưa lùi đến đầu khoảng cần tìm. Nó không thể bảo đảm bao phủ đầy đủ nếu API chỉ trả về một cửa sổ timeline ngắn.

Ba tool bổ sung được mô tả trong `artifacts/TOOLS_EXTENSION.md`. `resolve_account` dùng danh mục local nhỏ, giữ nguồn và trạng thái xác minh từng bản ghi; không tự tra tài khoản mới ngoài danh mục. `deduplicate_news` chỉ tự gộp URL tương đương, không khẳng định cùng tiêu đề là cùng sự kiện. `cross_check_claim` đã tìm/đọc được hai trang trong run mới, nhưng không đánh giá nguồn gốc độc lập hay tự đưa ra verdict đúng/sai. Các kiểm tra bằng mock còn xác nhận được lỗi search/fetch, fallback snippet có nhãn, và chuỗi resolve_account -> timeline -> answer.

## B6. Reflection

- Quy tắc chọn tool, hỏi lại và giữ context thuộc `system_prompt.md`.
- Ranh giới từng tool, enum, convention arguments và required fields thuộc `tools.yaml`.
- `R12` cần xem thủ công: eval muốn `yes_no`, nhưng nội dung “bản tin này” chưa hiện rõ trong câu hỏi. Trong ứng dụng thật, chỉ xác nhận gửi sau khi người dùng thấy đúng nội dung cuối cùng.
- Đã sửa lỗi model đoán ngày hiện tại: `runtime_context.py` lấy thời gian thật từ máy theo UTC+07:00 và truyền vào mỗi lượt UI/chat/agent, không cache ngày trong prompt tĩnh. Hai test kiểm tra đổi ngày theo múi giờ đã qua. Các log trước thay đổi này chưa có runtime clock context.
- Bước tiếp theo: chạy v3 để đo clarify; tiếp theo kiểm tra query normalization và chạy eval group/provider thật khi API keys sẵn sàng.

## B7. Small Local Model Challenge

Chưa thực hiện.
