"""Offline unit tests for the three team-added local analysis tools.

Each tool has a happy-path case, a missing/bad-input case, and an invalid-input
failure case. These tests exercise tool behavior directly without provider or
network access.
"""
from __future__ import annotations

from tools import TOOL_FUNCTIONS


calculator = TOOL_FUNCTIONS["calculator"]
sentiment = TOOL_FUNCTIONS["sentiment"]
compare = TOOL_FUNCTIONS["compare"]


# ---------------- calculator ----------------

def test_calculator_evaluates_supported_expression() -> None:
    result = calculator(expression="sqrt(144) + 2 * 3")

    assert result["status"] == "success"
    assert result["result"] == 18
    assert result["expression"] == "sqrt(144) + 2 * 3"


def test_calculator_empty_expression_returns_error() -> None:
    result = calculator(expression="  ")

    assert result["error"] == "ValueError"
    assert result["message"] == "Expression cannot be empty"


def test_calculator_rejects_unsupported_syntax_without_raising() -> None:
    result = calculator(expression="__import__('os').system('echo unsafe')")

    assert result["tool"] == "calculator"
    assert result["error"] == "ValueError"


# ---------------- sentiment ----------------

def test_sentiment_classifies_multiple_items_and_detailed_summary() -> None:
    result = sentiment(
        items=[{"text": "Dịch vụ rất tốt"}, {"text": "Chất lượng tệ"}],
        summary_style="detailed",
    )

    assert result["item_count"] == 2
    assert [item["label"] for item in result["results"]] == ["positive", "negative"]
    assert result["counts"] == {"positive": 1, "neutral": 0, "negative": 1}
    assert "Đã phân tích 2 văn bản" in result["summary"]


def test_sentiment_empty_items_returns_error() -> None:
    result = sentiment(items=[])

    assert "error" in result
    assert result["tool"] == "sentiment"


def test_sentiment_invalid_item_returns_error_without_raising() -> None:
    result = sentiment(items=[{"text": "Tốt"}, {"text": "   "}])

    assert result["error"] == "Item thứ 2 thiếu text hợp lệ."


# ---------------- compare ----------------

def test_compare_finds_shared_and_unique_terms() -> None:
    result = compare(sources=[
        {"title": "A", "content": "AI giúp cá nhân hóa việc học"},
        {"title": "B", "content": "AI hỗ trợ cá nhân hóa việc học"},
    ], dimensions=["nội dung"])

    assert result["source_count"] == 2
    assert result["dimensions"] == ["nội dung"]
    assert set(result["common_terms"]) == {"ai", "cá", "nhân", "hóa", "việc", "học"}
    assert result["method"] == "keyword_overlap"


def test_compare_rejects_fewer_than_two_sources() -> None:
    result = compare(sources=[{"title": "A", "content": "Một nguồn"}])

    assert result["error"] == "Cần cung cấp từ 2 đến 3 nguồn."


def test_compare_invalid_source_content_returns_error_without_raising() -> None:
    result = compare(sources=[
        {"title": "A", "content": "Nội dung hợp lệ"},
        {"title": "B", "content": "  "},
    ])

    assert result["error"] == "Source thứ 2 thiếu content."
