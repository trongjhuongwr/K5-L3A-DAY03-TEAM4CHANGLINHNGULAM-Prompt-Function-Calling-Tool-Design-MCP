from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from tools._shared import ROOT, err


ACCOUNT_FILE = ROOT / "data" / "accounts.json"


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.strip().lstrip("@").casefold())
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).split())


def _load_accounts(path: Path) -> list[dict[str, Any]]:
    records = json.loads(path.read_text(encoding="utf-8"))["accounts"]
    if not isinstance(records, list):
        raise ValueError("accounts must be a list")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each account must be an object")
        if not isinstance(record.get("name"), str) or not record["name"].strip():
            raise ValueError("Account name is required")
        if not isinstance(record.get("screenname"), str) or not re.fullmatch(r"[A-Za-z0-9_]{1,15}", record["screenname"]):
            raise ValueError("Invalid screenname in account directory")
        aliases = record.get("aliases", [])
        if not isinstance(aliases, list) or any(not isinstance(alias, str) for alias in aliases):
            raise ValueError("Account aliases must be a list of strings")
        if not isinstance(record.get("source_url"), str) or not record["source_url"].startswith("https://"):
            raise ValueError("Account source_url is required")
    return records


def resolve_account(name: str = "") -> dict[str, Any]:
    """Find candidate handles in the local, explicitly sourced account directory."""
    if not isinstance(name, str) or not _normalize(name):
        return {"tool": "resolve_account", "error": "invalid_argument", "message": "name must be a non-empty string"}
    try:
        query = _normalize(name)
        records = _load_accounts(ACCOUNT_FILE)
        exact, partial = [], []
        for record in records:
            names = [_normalize(value) for value in [record["name"], record["screenname"], *record.get("aliases", [])]]
            if query in names:
                exact.append(record)
            elif len(query) >= 3 and any(set(query.split()).issubset(set(value.split())) for value in names):
                partial.append(record)
        candidates = []
        seen = set()
        for record in exact or partial:
            handle = record["screenname"].casefold()
            if handle in seen:
                continue
            seen.add(handle)
            candidates.append({
                "name": record["name"],
                "screenname": record["screenname"],
                "url": f"https://x.com/{record['screenname']}",
                "source_url": record["source_url"],
                "verification": record.get("verification", "not_recorded"),
                "checked_on": record.get("checked_on"),
            })
        return {
            "tool": "resolve_account",
            "query": name,
            "status": "found" if len(candidates) == 1 else "ambiguous" if candidates else "not_found",
            "candidates": candidates,
            "lookup_source": "local_directory",
            "live_verified": False,
            "note": "Directory match only. Check source_url and verification; this call does not recheck current account ownership.",
        }
    except Exception as exc:
        return err("resolve_account", exc)
