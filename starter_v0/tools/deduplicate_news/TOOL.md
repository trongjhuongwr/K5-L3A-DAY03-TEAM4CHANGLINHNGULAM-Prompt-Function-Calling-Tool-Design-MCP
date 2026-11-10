---
name: deduplicate_news
track: core
kind: local_formatter
provider: Local URL normalization
requires_env: []
inputs: [items]
outputs: [items, input_count, output_count, duplicate_groups, possible_duplicate_groups]
side_effect: false
---
# deduplicate_news

Removes fragments and common tracking parameters, normalizes host casing and
default ports, then merges identical canonical URLs. All merged originals and
source URLs remain in duplicate_groups. Missing/invalid URLs are kept separately.
Different URLs with the same title are only flagged for review; semantic event
deduplication is not implemented. Meaningful query parameters and paths are kept.
