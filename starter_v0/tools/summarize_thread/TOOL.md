---
name: summarize_thread
track: core
kind: local_formatter
provider: none
requires_env: []
inputs: [thread_url, max_items, depth]
outputs: [summary, key_points, participants]
side_effect: false
---

# summarize_thread

Tóm tắt một thread conversation (Twitter thread, Hacker News, Reddit) thành các điểm chính.

## Mục đích

- **Khi dùng:** "Tóm tắt Twitter thread này", "Những điểm chính trong cuộc thảo luận?", "Chiết xuất phần kết luận"
- **Không dùng:** Khi chỉ cần 1 bài đơn lẻ

## Args

- `thread_url` (string): URL của thread
- `max_items` (int): default 20, tối đa 50
- `depth` (enum): `shallow` (title + conclusion) | `deep` (all points)

## Output

```json
{
  "original_url": "https://twitter.com/.../status/...",
  "title": "Tác động của AI trên việc làm",
  "key_points": [
    "AI sẽ thay thế 30% công việc",
    "Nhưng sẽ tạo công việc mới"
  ],
  "participants": ["@userA", "@userB"],
  "sentiment": "mixed",
  "items_processed": 15
}
```
