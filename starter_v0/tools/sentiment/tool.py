"""
tools/sentiment/tool.py

Phân tích sentiment của danh sách text (keyword-based, không cần ML library).
"""

from __future__ import annotations

import re
from typing import Any

from tools._shared import err


# Positive/Negative keywords (simple heuristic)
POSITIVE_WORDS = {
    "amazing", "awesome", "great", "excellent", "good", "love", "fantastic",
    "wonderful", "brilliant", "perfect", "incredible", "revolutionary",
    "best", "beautiful", "happy", "joy", "success", "win", "thank", "kudos",
    "recommend", "useful", "helpful", "nice", "smart", "clever", "impressive"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "hate", "horrible", "worst", "ugly", "poor",
    "fail", "failure", "problem", "issue", "bug", "crash", "broken", "useless",
    "waste", "annoying", "frustrated", "sad", "angry", "concern", "risk",
    "danger", "threat", "mistake", "error", "wrong", "disappointing", "sucks"
}


def _calculate_sentiment_score(text: str) -> float:
    """
    Tính sentiment score (0-1) dựa vào keyword matching.
    0 = very negative, 0.5 = neutral, 1 = very positive
    """
    if not text or not isinstance(text, str):
        return 0.5

    text_lower = text.lower()
    words = re.findall(r"\b\w+\b", text_lower)

    if not words:
        return 0.5

    positive_count = sum(1 for w in words if w in POSITIVE_WORDS)
    negative_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    total_sentiment_words = positive_count + negative_count

    if total_sentiment_words == 0:
        return 0.5  # neutral if no sentiment words

    # Normalize: 0 = all negative, 1 = all positive
    score = positive_count / total_sentiment_words
    return score


def analyze_sentiment(
    items: list[dict[str, str]] | None = None,
    summary_style: str = "brief"
) -> dict[str, Any]:
    """
    Phân tích tâm trạng (sentiment) của danh sách text.

    Args:
        items: Danh sách items {"text": "...", "source": "..."}
        summary_style: "brief" hoặc "detailed"

    Returns:
        {
            "overall_sentiment": "positive" | "neutral" | "negative",
            "score": float (0-1),
            "breakdown": {"positive": int, "neutral": int, "negative": int},
            "summary": str
        }
    """
    try:
        if not items:
            items = []

        if not isinstance(items, list):
            raise ValueError("items phải là array")

        if len(items) == 0:
            return {
                "tool": "sentiment",
                "status": "success",
                "overall_sentiment": "neutral",
                "score": 0.5,
                "breakdown": {"positive": 0, "neutral": 0, "negative": 0},
                "summary": "Không có item để phân tích",
                "total_items": 0,
            }

        # Phân tích mỗi item
        sentiments = []
        scores = []

        for item in items:
            if not isinstance(item, dict):
                continue

            text = item.get("text", "")
            if not text or not isinstance(text, str):
                continue

            # Tính sentiment score (0-1)
            score = _calculate_sentiment_score(text)
            scores.append(score)

            # Classify
            if score > 0.6:
                sentiment = "positive"
            elif score < 0.4:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            sentiments.append(sentiment)

        # Tính toán breakdown
        breakdown = {
            "positive": sentiments.count("positive"),
            "neutral": sentiments.count("neutral"),
            "negative": sentiments.count("negative"),
        }

        # Tính average score
        avg_score = sum(scores) / len(scores) if scores else 0.5

        # Determine overall sentiment
        if avg_score > 0.6:
            overall = "positive"
        elif avg_score < 0.4:
            overall = "negative"
        else:
            overall = "neutral"

        # Generate summary
        if summary_style == "detailed":
            summary = (
                f"Phân tích {len(items)} item: {breakdown['positive']} tích cực, "
                f"{breakdown['neutral']} trung lập, {breakdown['negative']} tiêu cực. "
                f"Điểm trung bình: {avg_score:.2f}/1.0. "
                f"Kết luận: Nhìn chung {overall}."
            )
        else:  # brief
            pct = int(avg_score * 100)
            summary = f"Chủ yếu {overall} ({pct}% điểm tích cực)"

        return {
            "tool": "sentiment",
            "status": "success",
            "overall_sentiment": overall,
            "score": round(avg_score, 2),
            "breakdown": breakdown,
            "summary": summary,
            "total_items": len(items),
        }

    except Exception as exc:
        return err("sentiment", exc)
