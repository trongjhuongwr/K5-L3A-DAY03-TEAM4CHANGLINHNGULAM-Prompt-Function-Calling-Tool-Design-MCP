---
name: compare
track: bonus
kind: local_formatter
provider: none
requires_env: []
inputs: [sources, dimensions]
outputs: [comparison_matrix, consensus]
side_effect: false
---

# compare

So sánh 2–3 articles/sources/perspectives trên cùng một topic (pros/cons, differences, consensus).

## Mục đích

- **Khi dùng:** "So sánh 2 bài viết về GPT-5 này", "Mạng xã hội vs tin chính thức nói gì khác nhau?", "Ý kiến A và B giống/khác gì?"
- **Không dùng:** Khi chỉ cần 1 nguồn

## Args

- `sources` (array): `[{title: "...", content: "...", source_url: "..."}, ...]`
- `dimensions` (array, optional): `["accuracy", "tone", "timeliness"]`

## Output

```json
{
  "topic": "GPT-5 release date",
  "comparison": {
    "Source A": {"claim": "Q1 2026", "confidence": "medium"},
    "Source B": {"claim": "early 2026", "confidence": "low"}
  },
  "consensus": "Q1 2026 is most likely",
  "conflicts": ["Source B is less specific"]
}
```
