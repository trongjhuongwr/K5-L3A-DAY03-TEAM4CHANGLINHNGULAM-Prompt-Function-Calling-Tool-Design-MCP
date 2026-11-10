# Team

## Thông tin nhóm

- Tên nhóm: Team 4 (4 Chàng Lính Ngự Lâm)
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`
- URL repo: `https://github.com/trongjhuongwr/K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`
- Nhánh nộp: `main`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Trọng Hướng | [Điền MSSV] | nguyentronghuong05@gmail.com | [trongjhuongwr](https://github.com/trongjhuongwr) | Trưởng nhóm / Core Architect |
|   2 | Đàm Tuấn Linh | 2A202603624 | damlinh820@gmail.com | [damlinh820](https://github.com/damlinh820) | Research & Evidence Specialist |
|   3 | Lê Thành Đạt | [Điền MSSV] | dat.ltforwork@gmail.com | [datlt203357](https://github.com/datlt203357) | UI & Testing Specialist |
|   4 | Trung Quân | [Điền MSSV] | trungquana123@gmail.com | [Jaden](https://github.com/trungquana123) | Content Analysis Specialist |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng `report/team/MSSV_HoTen.md`.

---

## 1. NguyenTrongHuong-[MSSV]
- **File báo cáo:** [report/team/MSSV_NguyenTrongHuong.md](report/team/MSSV_NguyenTrongHuong.md)

### Phần việc phụ trách
- Kiến trúc hệ thống cốt lõi (Core Pipeline & Tooling).
- Chu trình tối ưu hóa prompt & tools từ v0 đến v3 (đạt 100% accuracy).
- Phát triển 4 tools: `calculator`, `crypto_price`, `github_search`, `weather` + full unit test suite.
- Lập trình giao diện Web Chat Streamlit tại `starter_v0/app.py`.
- Thiết kế 10 case kiểm thử nhóm (`starter_v0/data/eval_group.json`).

### Đóng góp cụ thể
- Cải thiện độ chính xác: v0 (65%) -> v1 (85%) -> v2 (95%) -> v3 (100%).
- Viết 4 công cụ mới, hoàn thành tất cả TODO tests đạt tiêu chuẩn 0 skipped.
- Viết các bảng B1, B3, B5a và B5 trong `group_report.md`.

### Bằng chứng
- Commits: `78d2e48`, `f871015`, `8240ebc`, `a21930f`, `9976bfb`.
- Files: `starter_v0/app.py`, `starter_v0/tools/calculator`, `crypto_price`, `github_search`, `weather`, `test_tools_todo.py`.

---

## 2. DamTuanLinh-2A202603624
- **File báo cáo:** [report/team/2A202603624_DamTuanLinh.md](report/team/2A202603624_DamTuanLinh.md)

### Phần việc phụ trách
- Đề xuất và phát triển 3 công cụ nghiên cứu chuyên sâu: `resolve_account`, `deduplicate_news`, `cross_check_claim`.
- Xây dựng module đồng hồ hệ thống động `runtime_context.py` sửa lỗi nhận diện sai năm (2023 vs 2026).
- Phân tích lỗi phiên bản v0 và lập bảng Failure Analysis (B2).

### Đóng góp cụ thể
- Cung cấp giải pháp timezone `Asia/Bangkok` (UTC+7) giúp agent trả lời đúng ngày giờ thực tế.
- Viết bộ 3 công cụ nghiên cứu kèm danh mục tài khoản `accounts.json` và bộ test `test_research_extensions.py`.
- Viết bảng B2 và Mục 5 (Khó khăn & cách xử lý) trong `group_report.md`.

### Bằng chứng
- Commits: `948a032`, `228f554`.
- Files: `starter_v0/runtime_context.py`, `starter_v0/tools/resolve_account`, `deduplicate_news`, `cross_check_claim`, `starter_v0/tests/test_research_extensions.py`.

---

## 3. LeThanhDat-[MSSV]
- **File báo cáo:** [report/team/MSSV_LeThanhDat.md](report/team/MSSV_LeThanhDat.md)

### Phần việc phụ trách
- Đánh giá chéo hành vi của model với OpenAI provider trên máy cá nhân.
- Soạn thảo Phần A cho Báo cáo nhóm (`group_report.md`): Mục A1, A2, A3 và Mục 3 (Giải pháp).
- Chuẩn bị tài liệu hướng dẫn chạy UI và câu hỏi mẫu kiểm thử cho Showdown.

### Đóng góp cụ thể
- Thử nghiệm độc lập và ghi nhận log với OpenAI model đạt 100% accuracy.
- Lập bảng tổng hợp toàn bộ các tool của cả nhóm (A2) và bộ 5 câu hỏi mẫu đa dạng (A3).

### Bằng chứng
- Commits: `0dedaae`.
- Files: Mục A1–A3, Mục 3 trong `report/team/group_report.md`.

---

## 4. TrungQuan-[MSSV]
- **File báo cáo:** [report/team/MSSV_TrungQuan.md](report/team/MSSV_TrungQuan.md)

### Phần việc phụ trách
- Phát triển 3 công cụ phân tích nội dung: `compare`, `sentiment`, `summarize_thread`.
- Tổng hợp và phân tích Live Chat Transcripts (Bảng B4).
- Viết nội dung Reflection & Thảo luận (Mục 7 / B6) và hoàn thiện `TEAM.md`.

### Đóng góp cụ thể
- Xây dựng 3 công cụ phân tích nội dung không phụ thuộc thư viện ML cồng kềnh.
- Phát hiện và xử lý lỗi tách từ dính dấu câu trong bộ phân tích cảm xúc.
- Lập bảng phân tích từ 7 file transcripts thực tế và trả lời câu hỏi phản tư.

### Bằng chứng
- Commits: `15239dd`.
- Files: `starter_v0/tools/compare`, `sentiment`, `summarize_thread`, `starter_v0/tests/test_content_analysis_tools.py`, Bảng B4 trong `report/team/group_report.md`.
