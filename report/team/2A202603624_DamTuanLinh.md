# Báo cáo cá nhân — Đàm Tuấn Linh — 2A202603624

## 1. Thông tin thành viên

- **Họ tên:** Đàm Tuấn Linh
- **MSSV:** 2A202603624
- **Email cá nhân:** damlinh820@gmail.com
- **Email trường:** 26ai.linhdt3@vinuni.edu.vn
- **Nhóm:** Team 4 Chàng Lính Ngự Lâm
- **Ngày báo cáo:** 10/11/2026

## 2. Phần việc phụ trách

Tôi phụ trách đề xuất chức năng, phối hợp triển khai và thử nghiệm ba tool bổ sung cho Research Agent. Tôi sử dụng Codex hỗ trợ viết mã, khai báo tool, tạo test và phân tích kết quả; phạm vi chức năng được điều chỉnh theo khả năng thực tế của code.

| Tool | Chức năng đã triển khai | Tác dụng |
|---|---|---|
| `resolve_account` | Tra tên, alias hoặc handle trong danh mục tài khoản local có nguồn tham chiếu. Trả tên, handle, URL và trạng thái `found`, `ambiguous` hoặc `not_found`. | Giảm lỗi tự ghép họ tên thành username; cung cấp ứng viên để hỏi lại khi có nhiều kết quả. |
| `deduplicate_news` | Chuẩn hóa URL, bỏ tham số tracking và fragment, gộp các URL tương đương nhưng giữ nguồn và item gốc. Các tiêu đề giống nhau ở URL khác chỉ được đánh dấu để xem lại. | Giảm tin bị lặp trong digest và giữ bằng chứng nguồn khi tổng hợp nhiều kết quả. |
| `cross_check_claim` | Nhận một phát biểu và giới hạn số nguồn, dùng tìm kiếm web và đọc trang để thu thập đoạn nội dung kèm URL, thời điểm truy xuất và lỗi nếu có. | Hỗ trợ đối chiếu phát biểu dựa trên bằng chứng có thể kiểm tra lại. |

Ở phiên bản hiện tại, `resolve_account` chưa tra được mọi tài khoản X theo thời gian thực; danh mục ban đầu còn nhỏ. `deduplicate_news` chưa tự nhận diện mọi bài cùng nói về một sự kiện. `cross_check_claim` trả `needs_review` hoặc `insufficient_evidence`, chưa tự phân loại “được hỗ trợ” hay “mâu thuẫn” và chưa xác minh tính độc lập của nguồn.

## 3. Đóng góp cụ thể

### 3.1. Bổ sung công cụ và hướng dẫn agent sử dụng

Tôi xác định đầu vào, đầu ra và trường hợp sử dụng cho ba tool; yêu cầu agent xử lý các tình huống thiếu dữ liệu, trùng kết quả và chưa đủ bằng chứng. Phần triển khai có mã Python, tài liệu `TOOL.md`, đăng ký trong `TOOL_FUNCTIONS`, khai báo trong `tools.yaml` và hướng dẫn routing trong system prompt.

Các tình huống kiểm tra được bổ sung gồm tên tài khoản không có trong danh mục, tên có nhiều ứng viên, URL khác nhau bởi tham số tracking, dữ liệu sai kiểu và lỗi tìm kiếm/đọc trang. Luồng phụ thuộc cũng được kiểm tra: tra tài khoản trước rồi truyền handle thực tế trả về sang `timeline`.

### 3.2. Đặt câu hỏi thử agent và phát hiện lỗi ngày hiện tại

Tôi cùng nhóm đặt câu hỏi kiểm tra agent của nhóm mình và các nhóm khác. Một câu hỏi đơn giản nhưng phát hiện được lỗi là: **“Hôm nay là ngày mấy?”** Trong các lượt thử tôi tham gia, có agent trả lời **10/11/2023**, trong khi ngày thực hành là **10/11/2026**. Đây là quan sát từ các lượt thử, chưa phải thống kê đầy đủ tất cả agent.

Khi kiểm tra code của nhóm mình, nguyên nhân được xác định là ứng dụng truyền prompt tĩnh nhưng chưa cung cấp ngày giờ hiện tại cho model. Model không có đồng hồ hệ thống riêng trong lời gọi API nên có thể đoán sai ngày hoặc tiếp tục dựa vào câu trả lời sai trong lịch sử chat. Với agent của nhóm khác, cần kiểm tra code từng nhóm trước khi kết luận nguyên nhân tương tự.

Giải pháp của nhóm là bổ sung `runtime_context.py`: lấy ngày giờ từ máy chạy ứng dụng theo múi giờ `Asia/Bangkok` (UTC+7), rồi truyền vào mỗi lượt gọi model của UI, chat CLI và agent. Ngày được tính động, không ghi cứng năm 2026 vào prompt. Test kiểm tra chuyển ngày theo múi giờ cũng được bổ sung.

### 3.3. Đối chiếu lời trả lời với log thực thi

Tôi đặt câu hỏi lấy tweet mới nhất của Elon Musk và hỏi thời tiết hôm nay. Khi chatbot trả lời chung chung rằng có “lỗi kỹ thuật”, việc kiểm tra transcript cho thấy `timeline` thiếu `RAPIDAPI_KEY` và `lookup` thiếu `TAVILY_API_KEY` ở các lượt chạy đó. Điều này giúp phân biệt lỗi cấu hình API với lỗi model chọn tool hoặc điền arguments.

Tôi cũng lưu ý câu hỏi thời tiết cần có địa điểm, còn yêu cầu lấy bài trong một khoảng ngày cần có mốc thời gian đáng tin cậy. Các quan sát này được dùng để góp ý về việc hỏi lại và cách diễn giải kết quả của agent.

## 4. Bằng chứng

### 4.1. File và commit

- Ba implementation: [resolve_account](starter_v0/tools/resolve_account/tool.py), [deduplicate_news](starter_v0/tools/deduplicate_news/tool.py), [cross_check_claim](starter_v0/tools/cross_check_claim/tool.py).
- Danh mục tài khoản và nguồn tham chiếu: [accounts.json](starter_v0/data/accounts.json).
- Khai báo và đăng ký tool: [tools.yaml](starter_v0/artifacts/tools.yaml), [tools/__init__.py](starter_v0/tools/__init__.py).
- Test cho các tool và luồng phụ thuộc: [test_research_extensions.py](starter_v0/tests/test_research_extensions.py).
- Sửa lỗi ngày hiện tại: [runtime_context.py](starter_v0/runtime_context.py), [test_runtime_context.py](starter_v0/tests/test_runtime_context.py).
- Tài liệu chức năng, giới hạn và cách thử: [TOOLS_EXTENSION.md](starter_v0/artifacts/TOOLS_EXTENSION.md).
- Commit tích hợp code và bằng chứng trong repo: [948a032 — Add research tools, chatbot fixes, and evaluation evidence](https://github.com/trongjhuongwr/K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP/commit/948a032).

### 4.2. Kết quả kiểm tra

- **Unit/integration test:** toàn bộ suite đạt **132 passed, 0 failed, 0 skipped**. Kết quả lưu trong [research_tools_pytest.txt](starter_v0/analysis/research_tools_pytest.txt). Đây là tổng số test của repo, gồm các test có sẵn và test bổ sung.
- **Eval bằng model thật:** G11, G12 và G13 đều PASS với OpenRouter / `openai/gpt-4o-mini`. Log: [tools-v1_B_group_openrouter_20261110T200552940598.json](starter_v0/runs/tools-v1_B_group_openrouter_20261110T200552940598.json).
- Trong lần chạy này, tool tài khoản trả `found`; tool gộp tin gộp hai URL thành một; tool đối chiếu phát biểu lấy được hai đoạn nội dung trang và trả `needs_review`.
- **Giới hạn phép đo:** kết quả 3/3 đánh giá routing và các arguments được khai báo trong eval. Nó chưa chứng minh khả năng kiểm chứng mọi phát biểu, chất lượng tất cả nguồn hay chất lượng agent trên mọi yêu cầu.

### 4.3. AI/công cụ đã dùng và cách tự kiểm tra

Tôi sử dụng **Codex** để hỗ trợ đọc README và code, đề xuất schema, viết implementation/test, đọc JSON log và hoàn thiện tài liệu. Dự án dùng **OpenRouter** để chạy model, **Tavily** để tìm kiếm và **Firecrawl** để đọc trang cho tool thu thập bằng chứng.

Cách kiểm tra là đối chiếu yêu cầu với code và log: xem tool nào được gọi, arguments thực tế, kết quả trả về và lỗi bên trong `tool_results`. Unit test dùng mock để kiểm tra nhánh lỗi mà không cần API thật; eval dùng model thật để đo việc chọn tool. Tôi không coi câu trả lời nghe hợp lý hoặc một case PASS là đủ để khẳng định tool đã lấy được dữ liệu đúng.

Các lệnh tái hiện, chạy từ `starter_v0/`:

```powershell
python -m pytest -q
python scripts/eval_research_tools.py --provider openrouter --version tools-v1
```

## 5. Tự đánh giá

Tôi đã đóng góp vào việc mở rộng chức năng agent và phát hiện những vấn đề có thể gặp khi sử dụng thực tế: sai handle, kết quả lặp, thiếu bằng chứng, đoán ngày hiện tại và che khuất lỗi cấu hình bằng thông báo quá chung chung. Qua bài lab, tôi hiểu rõ hơn sự khác nhau giữa lỗi routing, lỗi arguments, lỗi code của tool và lỗi môi trường/API.

Điểm cần cải thiện là khả năng tự đọc và kiểm tra mã do AI hỗ trợ tạo ra, thiết kế thêm tình huống kiểm thử ngoài các ví dụ đã biết và đánh giá chất lượng nguồn sâu hơn. Hướng tiếp theo là mở rộng danh mục tài khoản có đối chiếu nguồn, kiểm tra việc gộp tin cùng sự kiện và bổ sung đánh giá ngữ nghĩa cho phát biểu, đồng thời giữ rõ trạng thái chưa đủ bằng chứng.
