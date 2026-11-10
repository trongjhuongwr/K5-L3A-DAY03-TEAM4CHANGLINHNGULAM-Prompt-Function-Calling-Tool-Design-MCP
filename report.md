### Failure Analysis — Baseline v0

**Run ID:** `v0_B_base_openrouter_20261110T104223427707`

**Kết quả:** 20 test cases, trong đó 13 PASS (65%) và 7 FAIL (35%).

Qua phân tích 7 case FAIL, nhóm xác định bốn loại lỗi thực tế:

- `wrong_arg_value` (2 case R03 + R13): Agent lựa chọn đúng công cụ nhưng truyền sai hoặc thiếu giá trị tham số.
- `missing_info` (2 case R10 + R11): Agent không yêu cầu làm rõ thông tin còn thiếu trước khi gọi công cụ.
- `out_of_scope` (2 case R08 + R14): Agent thực hiện lời gọi công cụ không phù hợp với phạm vi yêu cầu.
- `wrong_boundary` (1 case R12): Agent thực hiện hành động gửi trước khi có bước xác nhận cần thiết.

**Nhận định:** Baseline v0 đạt độ chính xác 65%, cho thấy Agent đã xử lý tốt phần lớn trường hợp định tuyến công cụ cơ bản. Tuy nhiên, Agent còn hạn chế trong việc tuân thủ tham số chính xác, xác định thông tin bắt buộc và kiểm soát điều kiện trước khi thực hiện hành động.

**Định hướng cải tiến v1:** Điều chỉnh system prompt để quy định rõ điều kiện gọi công cụ, bắt buộc hỏi lại khi thiếu tham số, bảo toàn giá trị tham số từ yêu cầu người dùng và không thực hiện hành động gửi khi chưa được xác nhận.

### Failure Analysis — Baseline v1
Kết quả v1 tốt hơn baseline về routing và arguments: đạt 16/20 (80%), so với v0 là 13/20 (65%). Routing tăng từ 75% lên 100%; argument accuracy từ 65% lên 80%. Tuy nhiên, multi-turn giảm từ 100% xuống 83,3%.

Bốn case còn lỗi:
- R10_missing_handle và R11_missing_url: chọn đúng clarify, nhưng thiếu response_type="text".
- R12_confirm_before_send: cũng chọn clarify, nhưng eval đòi response_type="yes_no" để xin xác nhận gửi. Câu hỏi thực tế lại xin người dùng cung cấp nội dung.
- M03_correction_handle: giữ limit=3 nhưng dùng andrejkarpathy, trong khi eval mong handle karpathy.
Các case R03 và R13 đã qua, gồm routing tin tức và truyền topic=news, timeframe=day. Hai case ngoài phạm vi cũng qua.