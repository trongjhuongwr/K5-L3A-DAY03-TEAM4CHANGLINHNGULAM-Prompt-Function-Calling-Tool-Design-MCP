# Báo cáo cá nhân — Phạm Ngọc Trung Quân — 2A202603626

## 1. Thông tin thành viên

- **Họ tên:** Phạm Ngọc Trung Quân
- **MSSV:** 2A202603626
- **Email:** trungquana123@gmail.com
- **Nhóm:** Team 4 (4 Chàng Lính Ngự Lâm)
- **Repo:** `K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`

## 2. Phần việc phụ trách

- Thiết kế và phát triển 3 công cụ phân tích nội dung chuyên sâu: `compare`, `sentiment`, `summarize_thread`.
- Khai báo tool vào `system_prompt.md`, `tools.yaml`, và `tools/__init__.py`.
- Phụ trách **Phần B của Báo cáo nhóm (`group_report.md`)**:
  - Bảng B4 (Live Chat Evidence): Trích xuất và lập bảng phân tích từ các file transcripts có trong thư mục `transcripts/`.
  - Mục 7 / B6 (Reflection & Thảo luận): Trả lời các câu hỏi phản tư về tối ưu hóa agent, ranh giới system prompt vs tools, và các lỗi cần review thủ công.
- Cập nhật và hoàn thiện thông tin thành viên trong file [`TEAM.md`](file:///TEAM.md).

## 3. Đóng góp cụ thể

### 3.1. Phát triển 3 công cụ phân tích nội dung
- `compare`: So sánh từ 2 đến 5 nguồn tin trên cùng một chủ đề; phân tích độ tin cậy (`confidence`), sắc thái (`tone`), tìm điểm đồng thuận (`consensus`) và mâu thuẫn (`conflicts`).
- `sentiment`: Phân tích tâm trạng/cảm xúc văn bản (tích cực, tiêu cực, trung lập) dựa trên lexicon từ khóa có chọn lọc, nhẹ nhàng và không phụ thuộc thư viện ML cồng kềnh.
  - *Đóng góp phát hiện bug:* Phát hiện và sửa lỗi bóc tách từ dính dấu câu trong tokenizer đơn giản (sử dụng regex `\b\w+\b` thay vì `split()` thuần) giúp nhận diện chính xác các từ cảm xúc có dấu câu đi kèm.
- `summarize_thread`: Nhận diện nền tảng (Twitter/X, Reddit, HackerNews) từ URL và trích xuất tóm tắt cấu trúc phân tầng các điểm luận chính trong thảo luận.

### 3.2. Bằng chứng Live Chat & Phản tư (Reflection)
- Phân tích 7 file transcripts thực tế của nhóm: đối chiếu giữa yêu cầu của người dùng, công cụ được model gọi, việc tuân thủ quy tắc xác nhận khi gửi tin (`send(confirmed=true)`), và phản hồi thân thiện bằng tiếng Việt.
- Soạn thảo nội dung Reflection cho báo cáo nhóm, làm rõ sự khác biệt giữa việc ép hành vi bằng system prompt và việc hướng dẫn model bằng mô tả parameters trong `tools.yaml`.

## 4. Bằng chứng

- **Commits:**
  - `15239dd`: update 3 new tools (`compare`, `sentiment`, `summarize_thread`)
- **Files:**
  - Tools: [compare](file:///starter_v0/tools/compare/), [sentiment](file:///starter_v0/tools/sentiment/), [summarize_thread](file:///starter_v0/tools/summarize_thread/)
  - Unit tests: [test_content_analysis_tools.py](file:///starter_v0/tests/test_content_analysis_tools.py)
  - Bảng B4 & Mục B6 trong [report/team/group_report.md](file:///report/team/group_report.md)
  - [TEAM.md](file:///TEAM.md)

## 5. Tự đánh giá

- Đã chủ động đóng góp 3 tool phân tích nội dung hữu ích, mở rộng khả năng tổng hợp của agent.
- Hiểu sâu về cách phối hợp giữa function calling của LLM và các thuật toán xử lý dữ liệu truyền thống.
