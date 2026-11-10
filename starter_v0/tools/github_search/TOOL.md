---
name: github_search
track: bonus
kind: live_api
provider: GitHub
requires_env: []
inputs: [query, limit, sort]
outputs: [tool, query, total_count, items]
side_effect: false
---
# github_search

Tìm kiếm các kho lưu trữ mã nguồn mở (repositories) trên GitHub theo từ khóa và độ phổ biến (stars).
