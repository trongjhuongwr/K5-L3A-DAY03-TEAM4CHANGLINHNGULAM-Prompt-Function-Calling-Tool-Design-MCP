
from __future__ import annotations

import re
from typing import Any


_POSITIVE_WORDS = {
    "good", "great", "excellent", "love", "amazing",
    "happy", "useful", "helpful", "success", "awesome",
    "tốt", "tuyệt", "tuyệt vời", "hài lòng", "yêu thích",
    "hữu ích", "tích cực", "thành công", "đẹp",
}

_NEGATIVE_WORDS = {
    "bad", "terrible", "hate", "awful", "poor",
    "sad", "useless", "fail", "broken", "disappointing",
    "tệ", "kém", "thất vọng", "vô ích", "tiêu cực",
    "lỗi", "chậm", "khó chịu", "không tốt",
}


def _tokenize(text: str) -> list[str]:
    """Tách văn bản thành các từ để phân tích."""
    return re.findall(r"[^\W\d_]+", text.lower(), flags=re.UNICODE)


def _classify(text: str) -> dict[str, Any]:
    """Phân loại cảm xúc của một văn bản."""

    words = _tokenize(text)

    positive_count = sum(
        1 for word in words if word in _POSITIVE_WORDS
    )
    negative_count = sum(
        1 for word in words if word in _NEGATIVE_WORDS
    )

    if positive_count > negative_count:
        label = "positive"
    elif negative_count > positive_count:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "positive_count": positive_count,
        "negative_count": negative_count,
    }


def analyze_sentiment(
    items: list[dict[str, Any]] | None = None,
    summary_style: str = "brief",
) -> dict[str, Any]:
    """
    Phân tích cảm xúc của danh sách văn bản.

    Trả về kết quả phân loại từng item và thống kê tổng hợp.
    """

    if not isinstance(items, list) or not items:
        return {
            "tool": "sentiment",
            "error": "Danh sách items không được để trống.",
        }

    if summary_style not in {"brief", "detailed"}:
        return {
            "tool": "sentiment",
            "error": "summary_style phải là brief hoặc detailed.",
        }

    results = []

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            return {
                "tool": "sentiment",
                "error": f"Item thứ {index + 1} không hợp lệ.",
            }

        text = item.get("text")

        if not isinstance(text, str) or not text.strip():
            return {
                "tool": "sentiment",
                "error": f"Item thứ {index + 1} thiếu text hợp lệ.",
            }

        result = _classify(text)

        results.append({
            "text": text,
            "source": item.get("source", ""),
            **result,
        })

    counts = {
        "positive": 0,
        "neutral": 0,
        "negative": 0,
    }

    for item in results:
        counts[item["label"]] += 1

    if summary_style == "brief":
        summary = (
            f"Positive: {counts['positive']}, "
            f"Neutral: {counts['neutral']}, "
            f"Negative: {counts['negative']}."
        )
    else:
        summary = (
            f"Đã phân tích {len(results)} văn bản. "
            f"Có {counts['positive']} tích cực, "
            f"{counts['neutral']} trung lập và "
            f"{counts['negative']} tiêu cực."
        )

    return {
        "tool": "sentiment",
        "summary": summary,
        "counts": counts,
        "results": results,
        "item_count": len(results),
    }
