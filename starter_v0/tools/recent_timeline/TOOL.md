---
name: recent_timeline
track: core
kind: live_api
provider: RapidAPI Twitter API45 plus local timestamp filtering
requires_env: [RAPIDAPI_KEY]
inputs: [screenname, days, limit, timezone]
outputs: [items, item_count, window_start, window_end, coverage_complete]
side_effect: false
---
# recent_timeline

Fetches a larger recent timeline sample for one X account and filters posts by
their returned `date` timestamps against the current time in the requested IANA
timezone. The API response may not contain enough history to cover the entire
requested window; `coverage_complete` is false unless the oldest dated returned
post reaches the requested start boundary. Undated posts are excluded.
