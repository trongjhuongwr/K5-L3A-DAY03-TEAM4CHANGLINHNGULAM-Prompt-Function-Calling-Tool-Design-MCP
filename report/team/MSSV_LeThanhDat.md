# Báo cáo cá nhân — Lê Thành Đạt — [Điền MSSV]

## 1. Thông tin thành viên

- **Họ tên:** Lê Thành Đạt
- **MSSV:** [Điền MSSV của bạn vào đây]
- **Email cá nhân:** dat.ltforwork@gmail.com
- **Nhóm:** Team 4 (4 Chàng Lính Ngự Lâm)
- **Repo:** `K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP`

## 2. Phần việc phụ trách

- Thử nghiệm độc lập và đánh giá độ chính xác của agent với OpenAI provider trên môi trường local.
- Phụ trách **Phần A của Báo cáo nhóm (`group_report.md`)**:
  - Mục A1: Giới thiệu 1–2 câu về chức năng agent và hướng dẫn chi tiết lệnh chạy giao diện người dùng UI.
  - Mục A2: Bảng tổng hợp toàn diện các tool mà nhóm đã phát triển và tích hợp.
  - Mục A3: Xây dựng 3–5 câu prompt mẫu để người khác kiểm thử agent trong phiên Showdown.
- Mục 3 (Giải pháp): Tóm tắt các thay đổi cấu trúc trong `system_prompt.md` và `tools.yaml`.

## 3. Đóng góp cụ thể

### 3.1. Thử nghiệm đánh giá với OpenAI Provider
- Tiến hành chạy thử nghiệm đánh giá độc lập v0 đến v3 trên môi trường máy cá nhân sử dụng trực tiếp OpenAI API (`openai/gpt-4o-mini`).
- Ghi nhận và theo dõi các chỉ số đánh giá trước/sau: đo lường sự khác biệt về khả năng bám sát schema giữa OpenAI native và OpenRouter. Kết quả cho thấy qua các phiên bản điều chỉnh prompt và tools, mô hình đạt độ chính xác routing 1.0 và argument 1.0.

### 3.2. Soạn thảo Phần A cho Báo cáo nhóm (Showdown Ready)
- Tổng hợp danh mục toàn bộ 10 công cụ mới của nhóm thành bảng A2 phân loại rõ ràng:
  - Nhóm tiện ích mở rộng: `calculator`, `crypto_price`, `github_search`, `weather`.
  - Nhóm nghiên cứu & kiểm chứng: `resolve_account`, `deduplicate_news`, `cross_check_claim`.
  - Nhóm phân tích nội dung: `compare`, `sentiment`, `summarize_thread`.
- Thiết lập kịch bản 5 câu hỏi mẫu tiêu biểu (A3) từ đơn giản đến phức tạp (tính toán, tra cứu thời tiết/crypto, kiểm tra tin tức và tổng hợp thread).

## 4. Bằng chứng

- **Commits:**
  - `0dedaae`: commit lần 1 (ghi nhận kết quả thử nghiệm model OpenAI và điều chỉnh prompt/tools).
- **Files:**
  - Phần A trong [report/team/group_report.md](file:///report/team/group_report.md)
  - [starter_v0/artifacts/version_log.csv](file:///starter_v0/artifacts/version_log.csv)
- **Công cụ đã dùng:**
  - OpenAI API, Python 3.13, PowerShell.

## 5. Tự đánh giá

- Đã chủ động thử nghiệm chéo mô hình với provider khác để kiểm chứng tính ổn định của prompt.
- Đã hoàn thành tốt phần giới thiệu agent và tài liệu kiểm thử cho nhóm.
