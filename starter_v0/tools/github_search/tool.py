from __future__ import annotations

from typing import Any
import requests

from tools._shared import TIMEOUT, err


def search_github(query: str = "", limit: int = 5, sort: str = "stars") -> dict[str, Any]:
    """Tìm kiếm repository trên GitHub."""
    try:
        clean_query = (query or "").strip()
        if not clean_query:
            return {"tool": "github_search", "error": "ValueError", "message": "Query cannot be empty"}

        safe_limit = max(1, min(int(limit or 5), 20))
        url = "https://api.github.com/search/repositories"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI20k-Research-Agent/1.0",
        }
        params = {
            "q": clean_query,
            "sort": sort or "stars",
            "order": "desc",
            "per_page": safe_limit,
        }

        resp = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        items = []
        for repo in data.get("items", []):
            items.append({
                "name": repo.get("full_name"),
                "url": repo.get("html_url"),
                "description": repo.get("description") or "",
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language") or "Unknown",
                "forks": repo.get("forks_count", 0),
            })

        return {
            "tool": "github_search",
            "query": clean_query,
            "total_count": data.get("total_count", 0),
            "items": items,
        }
    except Exception as exc:
        return err("github_search", exc)
