from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_PARAMS = {"fbclid", "gclid", "dclid", "msclkid", "mc_cid", "mc_eid"}


def canonical_url(url: Any) -> str | None:
    """Remove common tracking fields; preserve meaningful paths/query values."""
    if not isinstance(url, str) or not url.strip():
        return None
    try:
        parts = urlsplit(url.strip())
        scheme = parts.scheme.lower()
        if scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
            return None
        host = parts.hostname.lower()
        if ":" in host:
            host = f"[{host}]"
        if parts.port and (scheme, parts.port) not in {("http", 80), ("https", 443)}:
            host += f":{parts.port}"
        query = [
            (key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if not key.casefold().startswith("utm_") and key.casefold() not in TRACKING_PARAMS
        ]
        # Preserve parameter ordering: some services interpret repeated keys in order.
        return urlunsplit((scheme, host, parts.path or "/", urlencode(query), ""))
    except (ValueError, UnicodeError):
        return None


def deduplicate_news(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Merge only identical canonical URLs; retain originals and title-only hints."""
    if items is None:
        items = []
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        return {"tool": "deduplicate_news", "error": "invalid_argument", "message": "items must be a list of objects"}
    if any(item.get("url") is not None and not isinstance(item["url"], str) for item in items):
        return {"tool": "deduplicate_news", "error": "invalid_argument", "message": "item url must be a string or null"}

    groups: list[dict[str, Any]] = []
    by_url: dict[str, int] = {}
    for index, item in enumerate(items):
        url = canonical_url(item.get("url"))
        if url is not None and url in by_url:
            group = groups[by_url[url]]
            group["indexes"].append(index)
            group["original_items"].append(deepcopy(item))
        else:
            if url is not None:
                by_url[url] = len(groups)
            groups.append({"canonical_url": url, "indexes": [index], "original_items": [deepcopy(item)]})

    output = []
    titles: dict[str, list[int]] = defaultdict(list)
    for group_index, group in enumerate(groups):
        original_items = group["original_items"]
        representative = deepcopy(original_items[0])
        representative["duplicate_count"] = len(original_items)
        representative["source_urls"] = list(dict.fromkeys(item["url"] for item in original_items if item.get("url")))
        representative["sources"] = list(dict.fromkeys(item["source"] for item in original_items if isinstance(item.get("source"), str) and item["source"]))
        output.append(representative)
        for item in original_items:
            title = item.get("title")
            if isinstance(title, str) and title.strip():
                title_key = " ".join(title.casefold().split())
                if group_index not in titles[title_key]:
                    titles[title_key].append(group_index)

    return {
        "tool": "deduplicate_news",
        "input_count": len(items),
        "output_count": len(output),
        "removed_count": len(items) - len(output),
        "items": output,
        "duplicate_groups": [group for group in groups if len(group["indexes"]) > 1],
        "possible_duplicate_groups": [
            {"title": title, "output_indexes": indexes, "needs_review": True}
            for title, indexes in titles.items() if len(indexes) > 1
        ],
    }
