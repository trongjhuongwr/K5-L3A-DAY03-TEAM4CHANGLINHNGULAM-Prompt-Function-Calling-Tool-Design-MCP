from __future__ import annotations

from datetime import datetime, timedelta, timezone


LOCAL_TIMEZONE = timezone(timedelta(hours=7), name="Asia/Bangkok")


def current_date_context(now: datetime | None = None) -> str:
    """Build fresh clock context outside the cached prompt/model runtime."""
    current = datetime.now(LOCAL_TIMEZONE) if now is None else now.astimezone(LOCAL_TIMEZONE)
    return (
        "Runtime clock supplied by the application:\n"
        f"Current date: {current.date().isoformat()}\n"
        f"Current timestamp: {current.isoformat(timespec='seconds')}\n"
        "Timezone: Asia/Bangkok (UTC+07:00).\n"
        "Use this clock for today, now, yesterday, and relative date ranges. "
        "Do not guess the current date from training data or earlier assistant replies. "
        "A historical date in the user's request is a requested date, not a replacement for this clock."
    )
