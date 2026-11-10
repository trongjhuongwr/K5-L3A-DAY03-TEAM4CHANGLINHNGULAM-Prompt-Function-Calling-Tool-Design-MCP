
from __future__ import annotations

import re
from typing import Any


_STOPWORDS = {
    "the", "a", "an", "and", "or", "is", "are",
    "of", "to", "in", "for", "on", "with",
    "là", "và", "của", "các", "những", "được",
    "trong", "với", "cho", "một", "có", "về",
    "này", "đó", "theo", "từ",
}


def _extract_terms(text: str) -> set[str]:
    """Trích xuất tập từ khóa đơn giản từ văn bản."""

    words = re.findall(
        r"[^\W\d_]+",
        text.lower(),
        flags=re.UNICODE,
    )

    return {
        word for word in words
        if len(word) > 1 and word not in _STOPWORDS
    }


def compare_sources(
    sources: list[dict[str, Any]] | None = None,
    dimensions: list[str] | None = None,
) -> dict[str, Any]:
    """
    So sánh 2-3 nguồn văn bản dựa trên từ khóa.

    Không tự xác minh tính đúng sai của nội dung nguồn.
    """

    if not isinstance(sources, list) or not 2 <= len(sources) <= 3:
        return {
            "tool": "compare",
            "error": "Cần cung cấp từ 2 đến 3 nguồn.",
        }

    if dimensions is None:
        dimensions = []

    if not isinstance(dimensions, list) or not all(
        isinstance(item, str) for item in dimensions
    ):
        return {
            "tool": "compare",
            "error": "dimensions phải là danh sách chuỗi.",
        }

    source_terms = []

    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            return {
                "tool": "compare",
                "error": f"Source thứ {index + 1} không hợp lệ.",
            }

        title = source.get("title", f"Source {index + 1}")
        content = source.get("content", "")

        if not isinstance(content, str) or not content.strip():
            return {
                "tool": "compare",
                "error": f"Source thứ {index + 1} thiếu content.",
            }

        if not isinstance(title, str):
            return {
                "tool": "compare",
                "error": f"Title của source thứ {index + 1} không hợp lệ.",
            }

        terms = _extract_terms(content)

        source_terms.append({
            "title": title,
            "source_url": source.get("source_url", ""),
            "terms": terms,
        })

    common_terms = set.intersection(
        *(source["terms"] for source in source_terms)
    )

    results = []

    for source in source_terms:
        unique_terms = source["terms"] - common_terms

        results.append({
            "title": source["title"],
            "source_url": source["source_url"],
            "common_terms": sorted(common_terms),
            "unique_terms": sorted(unique_terms),
            "term_count": len(source["terms"]),
        })

    return {
        "tool": "compare",
        "source_count": len(sources),
        "dimensions": dimensions,
        "common_terms": sorted(common_terms),
        "results": results,
        "method": "keyword_overlap",
    }
