"""
tools/compare/tool.py

So sánh nhiều sources/perspectives trên cùng một topic.
"""

from __future__ import annotations

from typing import Any

from tools._shared import err


def compare_sources(
    sources: list[dict[str, str]] | None = None,
    dimensions: list[str] | None = None
) -> dict[str, Any]:
    """
    So sánh 2-3 sources trên cùng topic.

    Args:
        sources: [{"title": "...", "content": "...", "source_url": "..."}, ...]
        dimensions: Optional [accuracy, tone, timeliness, clarity]

    Returns:
        {
            "topic": str,
            "comparison": {source_name: {claim, confidence, tone}},
            "consensus": str,
            "conflicts": [str],
            "recommendation": str
        }
    """
    try:
        if not sources:
            sources = []

        if not isinstance(sources, list):
            raise ValueError("sources phải là array")

        if len(sources) < 2:
            return {
                "tool": "compare",
                "status": "error",
                "error": "Cần ít nhất 2 sources để so sánh",
            }

        if len(sources) > 5:
            sources = sources[:5]  # Cap at 5

        # Extract key info từ mỗi source
        comparison = {}

        for idx, source in enumerate(sources):
            if not isinstance(source, dict):
                continue

            title = source.get("title", f"Source {idx + 1}")
            content = source.get("content", "")
            url = source.get("source_url", "")

            # Simple heuristics để extract claim + confidence
            content_lower = content.lower() if isinstance(content, str) else ""

            # Confidence indicators
            confidence = "medium"
            if any(w in content_lower for w in ["definitely", "confirmed", "released", "announced"]):
                confidence = "high"
            elif any(w in content_lower for w in ["might", "could", "maybe", "possibly"]):
                confidence = "low"

            # Tone indicators
            tone = "neutral"
            if any(w in content_lower for w in ["amazing", "revolutionary", "incredible", "great"]):
                tone = "positive"
            elif any(w in content_lower for w in ["concern", "risk", "problem", "bad"]):
                tone = "negative"

            # Extract potential claim (first 100 chars of content)
            claim = content[:100] + "..." if content and len(content) > 100 else content

            comparison[title] = {
                "claim": claim or "(no content)",
                "confidence": confidence,
                "tone": tone,
                "source_url": url,
            }

        # Find consensus (most common confidence level)
        confidences = [v.get("confidence") for v in comparison.values()]
        most_common_confidence = max(set(confidences), key=confidences.count) if confidences else "neutral"

        # Detect conflicts (different tones or confidences)
        conflicts = []
        tones = [v.get("tone") for v in comparison.values()]
        if len(set(tones)) > 1:
            conflicts.append(f"Different tones: {', '.join(set(tones))}")

        confidences_set = set(confidences)
        if len(confidences_set) > 1:
            conflicts.append(f"Different confidence levels: {', '.join(confidences_set)}")

        # Generate consensus
        consensus = f"Based on {len(sources)} sources, confidence level is {most_common_confidence}"

        # Recommendation
        if most_common_confidence == "high" and not conflicts:
            recommendation = "Strong consensus - information appears reliable"
        elif conflicts:
            recommendation = "Mixed signals - recommend reading multiple sources"
        else:
            recommendation = "Moderate confidence - additional verification recommended"

        return {
            "tool": "compare",
            "status": "success",
            "total_sources": len(sources),
            "comparison": comparison,
            "consensus": consensus,
            "conflicts": conflicts,
            "recommendation": recommendation,
            "dimensions_checked": dimensions or ["confidence", "tone"],
        }

    except Exception as exc:
        return err("compare", exc)
