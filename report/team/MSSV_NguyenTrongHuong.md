# Báo cáo cá nhân — Nguyễn Trọng Hướng — [Điền MSSV]

## 1. Thông tin thành viên

- **Họ tên:** Nguyễn Trọng Hướng
- **MSSV:** [Điền MSSV của bạn vào đây]
- **Email:** nguyentronghuong05@gmail.com
- **Nhóm:** Team 4 (4 Chàng Lính Ngự Lâm)
- **Repo:** `K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`

## 2. Phần việc phụ trách

- Trưởng nhóm / Kiến trúc hệ thống cốt lõi (Core Pipeline & Tooling).
- Thực hiện chu trình lặp tối ưu hóa Prompt và Tool Declaration từ v0 đến v3 (nâng độ chính xác từ 65% lên 100%).
- Thiết kế, triển khai và viết unit test cho 4 công cụ mới: `calculator`, `crypto_price`, `github_search`, `weather`.
- Xây dựng bộ dữ liệu đánh giá nhóm gồm đúng 10 test case (5 single-turn, 5 multi-turn) tại `data/eval_group.json`.
- Thiết kế và lập trình giao diện Web Chat Streamlit hoàn chỉnh tại `starter_v0/app.py`.
- Chịu trách nhiệm hoàn thiện Phần B của Báo cáo nhóm: Bảng B1 (Version Evidence), Bảng B3 (Team Eval Cases), Bảng B5a & B5 (Tools & Test Challenge Evidence).

## 3. Đóng góp cụ thể

### 3.1. Tối ưu hóa Prompt & Tool Declaration (v0 → v3)
- Phân tích 7 case thất bại ở bản baseline v0 (độ chính xác 65%): phát hiện model đoán mò khi thiếu thông tin, bị nhầm lẫn giữa tìm kiếm mạng xã hội và web search, không biết hỏi lại khi thiếu arguments.
- **v1:** Bổ sung quy tắc routing nghiêm ngặt, chặn đoán mò, bắt buộc gọi `clarify` khi thiếu tham số bắt buộc. Độ chính xác tăng lên 85%.
- **v2:** Chống hiện tượng over-clarify (hỏi lại thừa khi người dùng đã cung cấp URL hoặc handle rõ ràng), xử lý map tên sang handle chuẩn. Độ chính xác đạt 95%.
- **v3:** Hỗ trợ đa lượt (multi-turn), xử lý ngữ cảnh sửa đổi và chuyển đổi công cụ linh hoạt (giải quyết triệt để case M06). Độ chính xác đạt tuyệt đối **100% (20/20 cases passed)**.

### 3.2. Phát triển 4 công cụ mới và kiểm thử đơn vị
- `calculator`: Đánh giá biểu thức toán học an toàn bằng `ast` (hỗ trợ `sqrt`, `abs`, các phép tính lũy thừa).
- `crypto_price`: Tra cứu giá tiền mã hóa theo thời gian thực (hỗ trợ cặp giao dịch USDT, BTC qua Binance/CoinGecko API).
- `github_search`: Tìm kiếm kho lưu trữ GitHub theo từ khóa, trả về tên repo, mô tả, sao (stars) và đường dẫn.
- `weather`: Tra cứu thông tin thời tiết địa phương theo thời gian thực qua `wttr.in`.
- Viết trọn vẹn bộ unit test trong `tests/test_tools_todo.py` bao gồm: happy path, input xấu từ model, xử lý ngoại lệ trả về dictionary lỗi (đạt tiêu chuẩn 0 failed, 0 skipped).

### 3.3. Xây dựng giao diện Streamlit UI
- Lập trình ứng dụng chat tại `starter_v0/app.py` với giao diện trực quan: hỗ trợ chọn provider/model, hiển thị danh mục tool trực quan theo icon, inspect tool calls chi tiết từng lượt và xuất transcript tự động.

## 4. Bằng chứng

- **Commits & PR:**
  - `78d2e48`: Baseline v0 phase
  - `f871015`: Baseline v0 + UI phase done
  - `8240ebc`: Tối ưu v1 + viết tool
  - `a21930f`: Update UI and test
  - `9976bfb`: Hoàn thành v3 phase
- **Files:**
  - UI: [starter_v0/app.py](file:///starter_v0/app.py)
  - Tools: [calculator](file:///starter_v0/tools/calculator/), [crypto_price](file:///starter_v0/tools/crypto_price/), [github_search](file:///starter_v0/tools/github_search/), [weather](file:///starter_v0/tools/weather/)
  - Unit tests: [starter_v0/tests/test_tools_todo.py](file:///starter_v0/tests/test_tools_todo.py)
  - Run logs: `runs/v0_B_base_openrouter_*.json` đến `runs/v3_B_base_openrouter_*.json`, `runs/v3_B_group_openrouter_*.json`
- **Kết quả kiểm thử:** Toàn bộ test suite đạt **150 passed, 0 failed, 0 skipped**.

## 5. Tự đánh giá

- Đã hoàn thành vượt mức các yêu cầu của bài lab Day 03: pipeline tối ưu đạt 100%, 4 công cụ mới có test đầy đủ, giao diện người dùng hoàn thiện và bộ case đánh giá đạt chuẩn.
- Đã phối hợp tốt cùng các thành viên trong nhóm để tổng hợp và tích hợp mã nguồn mượt mà lên nhánh chính.
