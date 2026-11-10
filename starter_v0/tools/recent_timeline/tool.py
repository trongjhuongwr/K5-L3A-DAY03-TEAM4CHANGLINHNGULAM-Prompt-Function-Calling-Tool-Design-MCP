from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from tools.timeline.tool import get_user_tweets


def _parse_posted_at(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(raw)
        except (TypeError, ValueError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def recent_timeline(
    screenname: str = "",
    days: int = 7,
    limit: int = 5,
    timezone: str = "Asia/Bangkok",
) -> dict[str, Any]:
    """Return the newest posts within a relative day window, using their timestamps."""
    tool_name = "recent_timeline"
    if not isinstance(screenname, str) or not screenname.strip():
        return {"tool": tool_name, "error": "invalid_argument", "message": "screenname is required"}
    if isinstance(days, bool) or not isinstance(days, int) or days < 1:
        return {"tool": tool_name, "error": "invalid_argument", "message": "days must be a positive integer"}
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        return {"tool": tool_name, "error": "invalid_argument", "message": "limit must be a positive integer"}
    try:
        zone = ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, TypeError):
        return {"tool": tool_name, "error": "invalid_argument", "message": "timezone must be a valid IANA timezone"}

    try:
        # Ask the existing timeline tool for a larger sample, then filter locally.
        normalized_screenname = screenname.strip().lstrip("@")
        source = get_user_tweets(screenname=normalized_screenname, limit=200)
        if source.get("error"):
            return {
                "tool": tool_name,
                "error": source["error"],
                "message": source.get("message", "Timeline provider failed"),
            }

        now = datetime.now(zone)
        cutoff = now - timedelta(days=days)
        dated: list[tuple[datetime, dict[str, Any]]] = []
        undated_count = 0
        for item in source.get("items") or []:
            if not isinstance(item, dict):
                undated_count += 1
                continue
            posted_at = _parse_posted_at(item.get("date"))
            if posted_at is None:
                undated_count += 1
                continue
            local_time = posted_at.astimezone(zone)
            if cutoff <= local_time <= now:
                dated.append((local_time, item))

        dated.sort(key=lambda pair: pair[0], reverse=True)
        source_items = source.get("items") or []
        parsed_source_dates = [
            _parse_posted_at(item.get("date"))
            for item in source_items
            if isinstance(item, dict)
        ]
        valid_source_dates = [value.astimezone(zone) for value in parsed_source_dates if value is not None]
        coverage_complete = bool(valid_source_dates and min(valid_source_dates) <= cutoff)

        return {
            "tool": tool_name,
            "screenname": normalized_screenname,
            "days": days,
            "timezone": timezone,
            "window_start": cutoff.isoformat(timespec="seconds"),
            "window_end": now.isoformat(timespec="seconds"),
            "items": [item for _, item in dated[:limit]],
            "item_count": min(len(dated), limit),
            "source_item_count": len(source_items),
            "undated_item_count": undated_count,
            "coverage_complete": coverage_complete,
        }
    except Exception as exc:
        return {"tool": tool_name, "error": type(exc).__name__, "message": str(exc)}
