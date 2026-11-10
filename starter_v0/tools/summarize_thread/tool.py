"""
tools/summarize_thread/tool.py

Tóm tắt thread conversation.
"""

from __future__ import annotations

from typing import Any
import re

from tools._shared import err


def summarize_thread(
    thread_url: str = "",
    max_items: int = 20,
    depth: str = "deep"
) -> dict[str, Any]:
    """
    Tóm tắt một thread conversation.

    Args:
        thread_url: URL của thread
        max_items: Max items to process (default 20, max 50)
        depth: "shallow" (title+conclusion) hoặc "deep" (all points)

    Returns:
        {
            "original_url": str,
            "title": str,
            "key_points": [str],
            "participants": [str],
            "sentiment": "positive" | "neutral" | "negative" | "mixed",
            "items_processed": int
        }
    """
    try:
        if not thread_url or not isinstance(thread_url, str):
            raise ValueError("thread_url is required")

        if not thread_url.startswith("http"):
            raise ValueError("thread_url must start with http:// or https://")

        # Validate max_items
        if max_items < 1:
            max_items = 20
        if max_items > 50:
            max_items = 50

        # Parse URL to detect platform
        platform = "unknown"
        if "twitter.com" in thread_url or "x.com" in thread_url:
            platform = "twitter"
        elif "reddit.com" in thread_url:
            platform = "reddit"
        elif "news.ycombinator.com" in thread_url:
            platform = "hackernews"

        # Mock thread data (in production, would use fetch tool first)
        # For now, return placeholder based on platform
        key_points = [
            "First point from thread",
            "Second insight mentioned",
            "Conclusion or consensus"
        ]

        participants = ["@user1", "@user2", "@user3"]

        # Sentiment heuristics
        sentiment = "neutral"

        # Title extraction (mock)
        title = f"Thread from {platform.title()}"

        return {
            "tool": "summarize_thread",
            "status": "success",
            "original_url": thread_url,
            "platform": platform,
            "title": title,
            "key_points": key_points[:3] if depth == "shallow" else key_points,
            "participants": participants,
            "sentiment": sentiment,
            "items_processed": len(key_points),
            "depth": depth,
            "max_items_allowed": max_items,
            "note": "Production version would use fetch tool to get actual thread content"
        }

    except Exception as exc:
        return err("summarize_thread", exc)
