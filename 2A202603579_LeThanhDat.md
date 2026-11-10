# Báo cáo cá nhân — Lê Thành Đạt - 2A202603579

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Lê Thành Đạt
- MSSV: 2A202603579
- Email: 26ai.datlt7@vinuni.edu.vn

## 2. Phần việc phụ trách

...

## 3. Đóng góp cụ thể

...

## 4. Bằng chứng

- File/commit/PR:
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:

## 5. Tự đánh giá

Trong quá trình thực hiện, tôi đã hiểu rõ hơn cách đánh giá một research agent bằng bằng chứng thay vì chỉ dựa vào câu trả lời nhìn có vẻ hợp lý. Tôi xây dựng bộ 6 eval case gồm 3 single-turn và 3 multi-turn cho `calculator`, `sentiment` và `compare`; đồng thời viết 9 unit test để kiểm tra đường chạy thành công, dữ liệu thiếu hoặc không hợp lệ và xử lý lỗi của ba tool.

Khi chạy eval, tôi phát hiện bộ chấm so sánh cứng các object lồng nhau nên báo lỗi với những metadata bổ sung hợp lệ. Tôi đã điều chỉnh cách so sánh để kiểm tra các trường được kỳ vọng, làm rõ các case còn mơ hồ và cập nhật hướng dẫn routing cho `compare`. Sau đó, cả 6 case đều đạt trong lần chạy kiểm tra cuối.

Qua bài lab, tôi rút ra rằng chất lượng eval phụ thuộc nhiều vào việc viết kỳ vọng rõ ràng và phân biệt lỗi của model, tool với lỗi của chính bộ chấm. Tôi muốn cải thiện thêm bằng cách mở rộng eval cho các cách diễn đạt khác nhau, bổ sung kiểm thử hồi quy cho bộ chấm và hoàn thiện bằng chứng đóng góp trong báo cáo. Kết quả 6/6 hiện tại chỉ phản ánh bộ case và lần chạy đã thực hiện, chưa đủ để khẳng định agent hoạt động chính xác với mọi yêu cầu thực tế.
