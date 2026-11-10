# Báo cáo cá nhân — Lê Thành Đạt — 2A202603579

## 1. Thông tin thành viên

- **Họ tên:** Lê Thành Đạt
- **MSSV:** 2A202603579
- **Email trường:** 26ai.datlt7@vinuni.edu.vn
- **Email cá nhân:** dat.ltforwork@gmail.com
- **Nhóm:** Team 4 Chàng Lính Ngự Lâm
- **Repo:** `K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`

## 2. Phần việc phụ trách

- Thử nghiệm độc lập và đánh giá độ chính xác của agent với mô hình OpenAI/OpenRouter trên môi trường local.
- Xây dựng bộ test case và unit test cho 3 công cụ: `calculator`, `sentiment`, `compare`.
- Phân tích và tinh chỉnh bộ chấm eval (`run_eval.py`) khi so sánh các object lồng nhau (nested objects) để tránh false negative.
- Đóng góp xây dựng Phần A trong Báo cáo nhóm (`group_report.md`): giới thiệu agent, chuẩn bị câu hỏi mẫu và tài liệu hướng dẫn giao diện.

## 3. Đóng góp cụ thể

### 3.1. Thử nghiệm đánh giá và tinh chỉnh bộ chấm Eval
- Xây dựng bộ 6 eval case gồm 3 single-turn và 3 multi-turn cho `calculator`, `sentiment` và `compare`.
- Khi chạy thử nghiệm, phát hiện bộ chấm so sánh cứng các object lồng nhau nên báo lỗi với những metadata bổ sung hợp lệ. Đã điều chỉnh cách so sánh trong `run_eval.py` để kiểm tra đúng các trường được kỳ vọng, làm rõ các case còn mơ hồ và cập nhật hướng dẫn routing cho `compare`.
- Đo lường và ghi nhận log với OpenAI model đạt độ chính xác cao (routing accuracy 1.0 và argument accuracy 1.0).

### 3.2. Viết Unit Tests cho các công cụ
- Viết 9 unit test độc lập kiểm tra đường chạy thành công (happy path), dữ liệu thiếu hoặc không hợp lệ, và xử lý lỗi an toàn không crash cho 3 công cụ `calculator`, `sentiment`, `compare`.
- Đảm bảo các tool luôn trả về dictionary lỗi có cấu trúc (`status: error` hoặc `error: ...`) thay vì raise unhandled exceptions.

### 3.3. Soạn thảo tài liệu và câu hỏi mẫu cho Showdown
- Đóng góp vào Phần A của Báo cáo nhóm:
  - Soạn thảo 5 câu hỏi kiểm thử mẫu (A3) bao phủ nhiều tình huống (tính toán, thời tiết, tiền mã hóa, kiểm chứng phát biểu).
  - Phối hợp tổng hợp danh mục toàn bộ các công cụ của nhóm trong bảng A2.

## 4. Bằng chứng

- **Commits:**
  - `0dedaae`: commit lần 1 (thử nghiệm OpenAI provider, cấu hình prompt & tools).
  - `db9fbf4`: commit lần 2 (tinh chỉnh `run_eval.py`, bổ sung test suite cho tools).
  - `f3e58e3`: upload cá nhân (`2A202603579_LeThanhDat.md`, `TEAM.md`).
- **Files:**
  - [starter_v0/run_eval.py](file:///starter_v0/run_eval.py)
  - [starter_v0/artifacts/version_log.csv](file:///starter_v0/artifacts/version_log.csv)
  - Phần A trong [report/team/group_report.md](file:///report/team/group_report.md)
- **Công cụ đã dùng:**
  - OpenAI API, OpenRouter, Python 3.13, Pytest.

## 5. Tự đánh giá

Trong quá trình thực hiện, tôi đã hiểu rõ hơn cách đánh giá một research agent bằng bằng chứng thay vì chỉ dựa vào câu trả lời nhìn có vẻ hợp lý. Tôi xây dựng bộ 6 eval case gồm 3 single-turn và 3 multi-turn cho `calculator`, `sentiment` và `compare`; đồng thời viết 9 unit test để kiểm tra đường chạy thành công, dữ liệu thiếu hoặc không hợp lệ và xử lý lỗi của ba tool.

Khi chạy eval, tôi phát hiện bộ chấm so sánh cứng các object lồng nhau nên báo lỗi với những metadata bổ sung hợp lệ. Tôi đã điều chỉnh cách so sánh để kiểm tra các trường được kỳ vọng, làm rõ các case còn mơ hồ và cập nhật hướng dẫn routing cho `compare`. Sau đó, cả 6 case đều đạt trong lần chạy kiểm tra cuối.

Qua bài lab, tôi rút ra rằng chất lượng eval phụ thuộc nhiều vào việc viết kỳ vọng rõ ràng và phân biệt lỗi của model, tool với lỗi của chính bộ chấm. Tôi muốn cải thiện thêm bằng cách mở rộng eval cho các cách diễn đạt khác nhau, bổ sung kiểm thử hồi quy cho bộ chấm và hoàn thiện bằng chứng đóng góp trong báo cáo. Kết quả 6/6 hiện tại chỉ phản ánh bộ case và lần chạy đã thực hiện, chưa đủ để khẳng định agent hoạt động chính xác với mọi yêu cầu thực tế.
