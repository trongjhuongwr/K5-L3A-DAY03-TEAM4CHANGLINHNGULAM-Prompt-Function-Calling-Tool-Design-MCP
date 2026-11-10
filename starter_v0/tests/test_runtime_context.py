from datetime import datetime, timezone

from runtime_context import current_date_context


def test_runtime_date_uses_bangkok_day_after_utc_midnight_boundary() -> None:
    context = current_date_context(datetime(2026, 11, 9, 18, 30, tzinfo=timezone.utc))
    assert "Current date: 2026-11-10" in context
    assert "2026-11-10T01:30:00+07:00" in context


def test_runtime_date_changes_when_new_day_is_supplied() -> None:
    before = current_date_context(datetime(2026, 11, 10, 16, 59, tzinfo=timezone.utc))
    after = current_date_context(datetime(2026, 11, 10, 17, 1, tzinfo=timezone.utc))
    assert "Current date: 2026-11-10" in before
    assert "Current date: 2026-11-11" in after
