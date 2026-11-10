from copy import deepcopy
import json

import pytest

from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from tools._shared import ROOT
from tools.resolve_account import tool as accounts
from tools.deduplicate_news.tool import canonical_url, deduplicate_news
from tools.cross_check_claim import tool as claims


def test_resolve_account_alias_keeps_provenance() -> None:
    result = accounts.resolve_account(" @sama ")
    assert result["status"] == "found"
    assert result["candidates"][0]["screenname"] == "sama"
    assert result["candidates"][0]["source_url"] == "https://blog.samaltman.com/"
    assert result["live_verified"] is False


def test_resolve_account_does_not_guess_unknown_names() -> None:
    result = accounts.resolve_account("Unknown Example Researcher")
    assert result["status"] == "not_found"
    assert result["candidates"] == []


def test_resolve_account_keeps_all_ambiguous_candidates(monkeypatch, tmp_path) -> None:
    path = tmp_path / "accounts.json"
    path.write_text(json.dumps({"accounts": [
        {"name": "Alex Example", "screenname": "alex_one", "source_url": "https://example.com/one"},
        {"name": "Alex Example", "screenname": "alex_two", "source_url": "https://example.com/two"},
    ]}), encoding="utf-8")
    monkeypatch.setattr(accounts, "ACCOUNT_FILE", path)
    result = accounts.resolve_account("Alex Example")
    assert result["status"] == "ambiguous"
    assert {item["screenname"] for item in result["candidates"]} == {"alex_one", "alex_two"}


@pytest.mark.parametrize("name", ["", "   ", "@", None, [], 42])
def test_resolve_account_rejects_bad_input(name) -> None:
    assert accounts.resolve_account(name)["error"] == "invalid_argument"


def test_resolve_account_broken_directory_returns_error(monkeypatch, tmp_path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("not json", encoding="utf-8")
    monkeypatch.setattr(accounts, "ACCOUNT_FILE", path)
    result = accounts.resolve_account("Sam Altman")
    assert result["error"] == "JSONDecodeError"


def test_deduplicate_news_removes_tracking_keeps_originals_without_mutation() -> None:
    items = [
        {"title": "A", "url": "https://EXAMPLE.com:443/a?id=1&utm_source=x#top", "source": "feed1", "summary": "one"},
        {"title": "B", "url": "https://example.com/a?id=1&fbclid=abc", "source": "feed2", "summary": "two"},
    ]
    original = deepcopy(items)
    result = deduplicate_news(items)
    assert result["input_count"] == 2
    assert result["output_count"] == 1
    assert result["removed_count"] == 1
    assert result["items"][0]["sources"] == ["feed1", "feed2"]
    assert result["duplicate_groups"][0]["original_items"] == original
    assert items == original


def test_deduplicate_news_preserves_meaningful_url_differences() -> None:
    result = deduplicate_news([
        {"url": "https://example.com/a?id=1"},
        {"url": "https://example.com/a?id=2"},
        {"url": "https://example.com/A?id=1"},
    ])
    assert result["output_count"] == 3


def test_deduplicate_news_equal_titles_are_only_review_candidates() -> None:
    result = deduplicate_news([
        {"title": "Same news", "url": "https://one.example/story"},
        {"title": "same   NEWS", "url": "https://two.example/story"},
    ])
    assert result["output_count"] == 2
    assert result["possible_duplicate_groups"][0]["needs_review"] is True


def test_deduplicate_news_keeps_items_without_urls() -> None:
    assert deduplicate_news([{"title": "A"}, {"title": "A"}])["output_count"] == 2
    assert deduplicate_news(None)["output_count"] == 0


@pytest.mark.parametrize("items", ["bad", [None], [{"url": 123}]])
def test_deduplicate_news_rejects_invalid_input(items) -> None:
    assert deduplicate_news(items)["error"] == "invalid_argument"


def test_canonical_url_preserves_repeated_parameter_order() -> None:
    assert canonical_url("https://example.com/?tag=b&tag=a&utm_campaign=x") == "https://example.com/?tag=b&tag=a"
    assert canonical_url("not a url") is None
    assert canonical_url("https://example.com:bad/a") is None


def test_cross_check_claim_collects_page_evidence_with_no_truth_verdict(monkeypatch) -> None:
    calls = []
    def search(**kwargs):
        calls.append(kwargs)
        return {"items": [{"title": "Result", "url": "https://example.com/a", "summary": "snippet"}]}
    monkeypatch.setattr(claims, "web_search", search)
    monkeypatch.setattr(claims, "read_url", lambda **kwargs: {
        "items": [{"url": kwargs["url"], "title": "Article", "summary": "Full excerpt"}]
    })
    result = claims.cross_check_claim("A specific claim", max_sources=2)
    assert calls[0]["timeframe"] is None
    assert calls[0]["query"] == "A specific claim"
    assert result["status"] == "needs_review"
    assert result["assessment"] == "not_assessed"
    assert result["independence_assessed"] is False
    assert result["evidence"][0]["content_source"] == "page_excerpt"
    assert result["evidence"][0]["excerpt"] == "Full excerpt"
    assert result["evidence"][0]["retrieved_at"]


def test_cross_check_claim_labels_snippet_fallback_and_fetch_error(monkeypatch) -> None:
    monkeypatch.setattr(claims, "web_search", lambda **kwargs: {
        "items": [{"url": "https://example.com/a", "summary": "Search snippet only"}]
    })
    monkeypatch.setattr(claims, "read_url", lambda **kwargs: {"error": "HTTPError", "message": "HTTP 429"})
    result = claims.cross_check_claim("A specific claim")
    assert result["evidence"][0]["content_source"] == "search_snippet"
    assert result["errors"][0]["stage"] == "fetch"
    assert result["status"] == "needs_review"


def test_cross_check_claim_search_failure_does_not_fetch(monkeypatch) -> None:
    monkeypatch.setattr(claims, "web_search", lambda **kwargs: {"error": "RuntimeError", "message": "Missing key"})
    def unexpected_fetch(**kwargs):
        pytest.fail("No page fetch should occur after search failure")
    monkeypatch.setattr(claims, "read_url", unexpected_fetch)
    result = claims.cross_check_claim("A claim")
    assert result["status"] == "insufficient_evidence"
    assert result["error"] == "search_failed"


def test_cross_check_claim_deduplicates_urls_and_limits_requests(monkeypatch) -> None:
    monkeypatch.setattr(claims, "web_search", lambda **kwargs: {"items": [
        {"url": "https://example.com/a?utm_source=x"},
        {"url": "https://example.com/a"},
        {"url": "https://example.com/b"},
    ]})
    calls = []
    def fetch(url):
        calls.append(url)
        return {"items": [{"url": url, "summary": "excerpt"}]}
    monkeypatch.setattr(claims, "read_url", fetch)
    result = claims.cross_check_claim("A claim", max_sources=1)
    assert len(calls) == 1
    assert result["source_count"] == 1


def test_cross_check_claim_no_sources_is_insufficient(monkeypatch) -> None:
    monkeypatch.setattr(claims, "web_search", lambda **kwargs: {"items": []})
    result = claims.cross_check_claim("A claim")
    assert result["status"] == "insufficient_evidence"
    assert result["evidence"] == []


@pytest.mark.parametrize("claim,max_sources", [("", 3), (None, 3), ("claim", 0), ("claim", True), ("claim", 6), ("claim", "3")])
def test_cross_check_claim_rejects_invalid_arguments(claim, max_sources) -> None:
    assert claims.cross_check_claim(claim, max_sources)["error"] == "invalid_argument"


def test_chat_resolves_handle_before_dependent_timeline_call(monkeypatch) -> None:
    from chat import run_model_tool_loop
    from providers.base import ModelResponse, ToolCall

    class ScriptedProvider:
        def __init__(self):
            self.round = 0

        def complete(self, messages, tools, **kwargs):
            self.round += 1
            if self.round == 1:
                return ModelResponse(text=None, tool_calls=[ToolCall("resolve_account", {"name": "Andrej Karpathy"})])
            if self.round == 2:
                events = json.loads(messages[-1]["content"].split("TOOL_RESULTS_JSON:\n", 1)[1].split("\n\nUse collected", 1)[0])
                handle = events[0]["result"]["candidates"][0]["screenname"]
                return ModelResponse(text=None, tool_calls=[ToolCall("timeline", {"screenname": handle, "limit": 1})])
            return ModelResponse(text="One result", tool_calls=[])

    seen = []
    def timeline(screenname, limit):
        seen.append((screenname, limit))
        return {"items": [{"title": "A post", "url": "https://x.com/karpathy/status/1"}]}
    monkeypatch.setitem(TOOL_FUNCTIONS, "timeline", timeline)
    result = run_model_tool_loop(
        provider=ScriptedProvider(),
        messages=[{"role": "system", "content": "test"}, {"role": "user", "content": "Find the account, then posts"}],
        tools=to_openai_tools(load_tool_declarations(ROOT / "artifacts" / "tools.yaml")),
        model=None, max_tool_rounds=6,
    )
    assert result["status"] == "answered"
    assert seen == [("karpathy", 1)]
    assert [event["tool"] for event in result["tool_events"]] == ["resolve_account", "timeline"]


def test_research_eval_subset_only_contains_the_new_read_only_tools() -> None:
    from scripts.eval_research_tools import NEW_CASES

    eval_file = ROOT / "analysis" / "eval_research_tools.json"
    dataset = json.loads(eval_file.read_text(encoding="utf-8"))
    selected = [case for case in dataset["cases"] if case["id"] in NEW_CASES]
    assert {case["id"] for case in selected} == NEW_CASES
    names = {call["name"] for case in selected for call in case["expect"]["tool_calls"]}
    assert names == {"resolve_account", "deduplicate_news", "cross_check_claim"}
