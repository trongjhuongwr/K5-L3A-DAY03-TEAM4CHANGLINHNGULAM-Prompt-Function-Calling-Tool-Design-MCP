"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    res = TOOL_FUNCTIONS["clarify"](question="Chọn phương án?", response_type="choice", options=["A", "B"])
    assert res["options"] == ["A", "B"]
    assert res["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "Item 1", "section": "A", "url": "https://example.com/1"},
        {"title": "Item 2", "section": "B", "url": "https://example.com/2"},
        {"title": "Item 3", "section": "A", "url": "https://example.com/3"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="sections")
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    items = [
        {"title": "Item 1", "url": "https://example.com/1"},
        {"title": "Item 2", "url": "https://example.com/2"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="thread")
    assert "1/ " in result["markdown"]
    assert "2/ " in result["markdown"]


def test_format_empty_items_does_not_crash() -> None:
    res1 = TOOL_FUNCTIONS["format"](items=None)
    assert res1["item_count"] == 0
    res2 = TOOL_FUNCTIONS["format"](items=[])
    assert res2["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Hello", confirmed=True)
    assert result["status"] == "sent"
    assert len(calls) == 1
    assert "fake-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "123456"
    assert calls[0]["json"]["text"] == "Hello"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Hello", confirmed=True)
    assert "error" in result
    assert len(calls) == 0


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({"results": []}))
    TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-fake")
    calls = fake_http(FakeResponse({
        "data": {
            "markdown": "Content body",
            "metadata": {"title": "Test Title", "sourceURL": "https://example.com/art"},
        }
    }))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/art")
    assert result["items"][0]["title"] == "Test Title"
    assert result["items"][0]["url"] == "https://example.com/art"
    assert result["items"][0]["source"] == "example.com"
    assert result["items"][0]["summary"] == "Content body"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-fake")
    fake_http(FakeResponse({"data": {"markdown": "a" * 5000, "metadata": {}}}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    fake_http(FakeResponse({
        "timeline": [
            {"text": "missing id"},
            {"tweet_id": "101", "screen_name": "sama", "text": "tweet 1"},
            {"tweet_id": "102", "screen_name": "sama", "text": "tweet 2"},
            {"tweet_id": "103", "screen_name": "sama", "text": "tweet 3"},
            {"tweet_id": "104", "screen_name": "sama", "text": "tweet 4"},
            {"tweet_id": "105", "screen_name": "sama", "text": "tweet 5"},
            {"tweet_id": "106", "screen_name": "sama", "text": "tweet 6"},
        ]
    }))
    result = TOOL_FUNCTIONS["timeline"](screenname="sama", limit=3)
    assert len(result["items"]) == 3
    for item in result["items"]:
        assert item["url"].startswith("https://x.com/sama/status/")


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"tweets": []}))
    TOOL_FUNCTIONS["social_search"](query="OpenAI", search_type="Top")
    assert calls[0]["params"]["search_type"] == "Top"
    assert calls[0]["params"]["query"] == "OpenAI"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="data", policy_area="data_privacy")
    assert len(result["results"]) > 0
    for item in result["results"]:
        assert item["policy_area"] == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](query="injection", policy_area="source_citation")
    assert len(result["results"]) > 0
    injection_hit = result["results"][0]
    assert any("ignore the citation policy" in line for line in injection_hit["untrusted_text"])
    assert "ignore the citation policy" not in injection_hit["facts"]





# ---------------- YOUR NEW TOOL(S) ----------------
# Tests for crypto_price
def test_crypto_price_happy_path(fake_http) -> None:
    calls = fake_http(FakeResponse({"symbol": "BTCUSDT", "price": "92500.50"}))
    result = TOOL_FUNCTIONS["crypto_price"](symbol="BTC", currency="USDT")
    assert result["status"] == "success"
    assert result["price"] == 92500.50
    assert "binance.com" in calls[0]["url"]


def test_crypto_price_bad_input_from_model() -> None:
    result = TOOL_FUNCTIONS["crypto_price"](symbol="")
    assert "error" in result


def test_crypto_price_failure_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse({"code": -1121, "msg": "Invalid symbol"}, status_code=400))
    result = TOOL_FUNCTIONS["crypto_price"](symbol="INVALID")
    assert "error" in result


# Tests for github_search
def test_github_search_happy_path(fake_http) -> None:
    calls = fake_http(FakeResponse({
        "total_count": 1,
        "items": [{
            "full_name": "openai/gpt-4",
            "html_url": "https://github.com/openai/gpt-4",
            "description": "Repo description",
            "stargazers_count": 12000,
            "language": "Python",
            "forks_count": 500,
        }],
    }))
    result = TOOL_FUNCTIONS["github_search"](query="agent evaluation", limit=1)
    assert result["tool"] == "github_search"
    assert len(result["items"]) == 1
    assert result["items"][0]["name"] == "openai/gpt-4"
    assert calls[0]["params"]["q"] == "agent evaluation"


def test_github_search_bad_input_from_model() -> None:
    result = TOOL_FUNCTIONS["github_search"](query="")
    assert "error" in result


def test_github_search_failure_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse({"message": "Rate limit exceeded"}, status_code=403))
    result = TOOL_FUNCTIONS["github_search"](query="test")
    assert "error" in result


# Tests for weather
def test_weather_happy_path(fake_http) -> None:
    calls = fake_http(FakeResponse({
        "current_condition": [{
            "temp_C": "26",
            "weatherDesc": [{"value": "Sunny"}],
            "humidity": "65",
            "windspeedKmph": "12",
        }],
    }))
    result = TOOL_FUNCTIONS["weather"](city="Hanoi")
    assert result["status"] == "success"
    assert result["temperature_c"] == "26"
    assert result["condition"] == "Sunny"
    assert "wttr.in/Hanoi" in calls[0]["url"]


def test_weather_bad_input_from_model() -> None:
    result = TOOL_FUNCTIONS["weather"](city="")
    assert "error" in result


def test_weather_failure_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=500))
    result = TOOL_FUNCTIONS["weather"](city="Atlantis")
    assert "error" in result


# Tests for calculator
def test_calculator_happy_path() -> None:
    result = TOOL_FUNCTIONS["calculator"](expression="15 * 4 + 2 ^ 3")
    assert result["status"] == "success"
    assert result["result"] == 68
    # Test functions
    result_sqrt = TOOL_FUNCTIONS["calculator"](expression="sqrt(144) + abs(-10)")
    assert result_sqrt["result"] == 22


def test_calculator_bad_input_from_model() -> None:
    result = TOOL_FUNCTIONS["calculator"](expression="")
    assert "error" in result


def test_calculator_unsafe_or_invalid_syntax() -> None:
    result = TOOL_FUNCTIONS["calculator"](expression="__import__('os').system('ls')")
    assert "error" in result
    result_syntax = TOOL_FUNCTIONS["calculator"](expression="5 ++-?* 2")
    assert "error" in result_syntax

