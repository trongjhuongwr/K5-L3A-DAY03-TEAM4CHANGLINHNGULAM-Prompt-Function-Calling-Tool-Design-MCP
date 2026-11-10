from __future__ import annotations

import pytest
from tools import TOOL_FUNCTIONS


# ---------------- compare (compare_sources) ----------------

def test_compare_happy_path() -> None:
    sources = [
        {"title": "Source 1", "content": "OpenAI definitely released a revolutionary model.", "source_url": "https://example.com/1"},
        {"title": "Source 2", "content": "OpenAI confirmed the launch of new AI.", "source_url": "https://example.com/2"},
    ]
    result = TOOL_FUNCTIONS["compare"](sources=sources)
    assert result["status"] == "success"
    assert result["total_sources"] == 2
    assert "comparison" in result
    assert "consensus" in result


def test_compare_less_than_two_sources_returns_error() -> None:
    result = TOOL_FUNCTIONS["compare"](sources=[{"title": "Single", "content": "Only one source"}])
    assert result["status"] == "error"
    assert "ít nhất 2 sources" in result["error"]


def test_compare_bad_input_returns_error() -> None:
    result = TOOL_FUNCTIONS["compare"](sources="not_a_list")
    assert "error" in result


# ---------------- sentiment (analyze_sentiment) ----------------

def test_sentiment_positive_text() -> None:
    items = [{"text": "This product is amazing, brilliant, and wonderful!", "source": "review1"}]
    result = TOOL_FUNCTIONS["sentiment"](items=items)
    assert result["status"] == "success"
    assert result["overall_sentiment"] == "positive"
    assert result["score"] > 0.6


def test_sentiment_negative_text() -> None:
    items = [{"text": "Terrible service, broken app, and horrible experience.", "source": "review2"}]
    result = TOOL_FUNCTIONS["sentiment"](items=items)
    assert result["status"] == "success"
    assert result["overall_sentiment"] == "negative"
    assert result["score"] < 0.4


def test_sentiment_empty_or_bad_input() -> None:
    result_empty = TOOL_FUNCTIONS["sentiment"](items=[])
    assert result_empty["overall_sentiment"] == "neutral"
    result_bad = TOOL_FUNCTIONS["sentiment"](items="invalid_type")
    assert "error" in result_bad


# ---------------- summarize_thread ----------------

def test_summarize_thread_happy_path() -> None:
    url = "https://x.com/user/status/123456789"
    result = TOOL_FUNCTIONS["summarize_thread"](thread_url=url, depth="shallow")
    assert result["status"] == "success"
    assert result["platform"] == "twitter"
    assert len(result["key_points"]) <= 3


def test_summarize_thread_invalid_url() -> None:
    result = TOOL_FUNCTIONS["summarize_thread"](thread_url="invalid_url_not_http")
    assert "error" in result


def test_summarize_thread_empty_input() -> None:
    result = TOOL_FUNCTIONS["summarize_thread"](thread_url="")
    assert "error" in result
