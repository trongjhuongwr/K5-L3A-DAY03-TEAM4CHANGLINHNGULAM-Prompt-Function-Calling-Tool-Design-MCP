"""Offline unit tests for built-in tools and the team-added recent_timeline tool."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = TOOL_FUNCTIONS["clarify"](
        question="Chọn tài khoản nào?",
        response_type="choice",
        options=["A", "B"],
    )
    assert result["options"] == ["A", "B"]
    assert result["awaiting_user"] is True


def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "a1", "section": "A"},
        {"title": "b1", "section": "B"},
        {"title": "a2", "section": "A"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="sections")
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    result = TOOL_FUNCTIONS["format"](
        items=[{"title": "one"}, {"title": "two"}], template="thread"
    )
    assert result["markdown"].splitlines()[0].startswith("1/")
    assert "\n\n2/" in result["markdown"]


def test_format_empty_items_does_not_crash() -> None:
    for items in (None, []):
        result = TOOL_FUNCTIONS["format"](items=items, template="sections")
        assert result["item_count"] == 0


def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Approved update", confirmed=True)
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "test-token" in calls[0]["url"]
    assert calls[0]["json"] == {
        "chat_id": "test-chat", "text": "Approved update", "parse_mode": "Markdown"
    }
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Approved update", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert calls == []


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)
    assert "time_range" not in calls[0]["json"]
    assert result["items"] == []


def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {
        "markdown": "Article summary",
        "metadata": {"title": "T", "sourceURL": "https://example.com/a"},
    }}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/a")
    assert result["items"][0] == {
        "title": "T", "url": "https://example.com/a",
        "source": "example.com", "summary": "Article summary",
    }


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000, "metadata": {}}}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/a")
    assert len(result["items"][0]["summary"]) == 4000


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    timeline = [{"screen_name": "sample", "text": "no id"}]
    timeline += [
        {"screen_name": "sample", "tweet_id": str(i), "text": f"post {i}"}
        for i in range(6)
    ]
    calls = fake_http(FakeResponse({"timeline": timeline}))
    result = TOOL_FUNCTIONS["timeline"]("sample", limit=3)
    assert calls[0]["params"]["screenname"] == "sample"
    assert len(result["items"]) == 3
    assert all(item["url"].startswith("https://x.com/sample/status/") for item in result["items"])


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"tweets": []}))
    result = TOOL_FUNCTIONS["social_search"]("OpenAI", search_type="Top")
    assert calls[0]["params"] == {"query": "OpenAI", "search_type": "Top"}
    assert result["search_type"] == "Top"


def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="   ")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="confidential customer", policy_area="data_privacy")
    assert result["results"]
    assert all(item["policy_area"] == "data_privacy" for item in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](query="citation verified fact", policy_area="source_citation", top_k=20)
    matching = [item for item in result["results"] if item["section"] == "Injection probe"]
    assert matching
    assert any("ignore the citation policy" in line.lower() for line in matching[0]["untrusted_text"])
    assert "ignore the citation policy" not in matching[0]["facts"].lower()


def test_recent_timeline_filters_by_timestamp(monkeypatch) -> None:
    from tools.recent_timeline import tool as recent_tool

    now = datetime.now(timezone.utc)
    monkeypatch.setattr(recent_tool, "get_user_tweets", lambda **kwargs: {
        "items": [
            {"title": "new", "date": (now - timedelta(days=1)).isoformat()},
            {"title": "old", "date": (now - timedelta(days=12)).isoformat()},
        ]
    })
    result = recent_tool.recent_timeline("@sample", days=7, limit=5, timezone="UTC")
    assert result["screenname"] == "sample"
    assert result["item_count"] == 1
    assert result["items"][0]["title"] == "new"
    assert result["coverage_complete"] is True


def test_recent_timeline_rejects_invalid_days() -> None:
    result = TOOL_FUNCTIONS["recent_timeline"]("sample", days="seven")
    assert result["error"] == "invalid_argument"
    assert "positive integer" in result["message"]


def test_recent_timeline_returns_provider_error_dict(monkeypatch) -> None:
    from tools.recent_timeline import tool as recent_tool

    monkeypatch.setattr(
        recent_tool,
        "get_user_tweets",
        lambda **kwargs: {"tool": "get_user_tweets", "error": "RuntimeError", "message": "offline"},
    )
    result = recent_tool.recent_timeline("sample", days=7, timezone="UTC")
    assert result == {"tool": "recent_timeline", "error": "RuntimeError", "message": "offline"}
