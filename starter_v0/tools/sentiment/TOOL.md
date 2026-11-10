---
name: sentiment
track: bonus
kind: local_formatter
provider: none (TextBlob)
requires_env: []
inputs: [items, summary_style]
outputs: [sentiment_scores, summary]
side_effect: false
---

# sentiment

Phân tích tâm trạng/sentiment của một danh sách tweet hoặc bài viết (positive/neutral/negative).

## Mục đích

- **Khi dùng:** "Mọi người nói gì về OpenAI — tích cực hay tiêu cực?", "Phân tích cảm xúc từ 10 tweet này", "OpenAI được đánh giá như thế nào?"
- **Không dùng:** Khi chỉ cần lấy dữ liệu (không phân tích)

## Args

- `items` (array): `[{text: "...", source: "..."}, ...]` — danh sách text cần phân tích
- `summary_style` (enum): `brief` (1-2 câu) | `detailed` (paragraph)

## Output

```json
{
  "overall_sentiment": "positive",
  "score": 0.72,
  "breakdown": {
    "positive": 7,
    "neutral": 2,
    "negative": 1
  },
  "summary": "Chủ yếu tích cực, 72% bài viết khen ngợi..."
}
```
