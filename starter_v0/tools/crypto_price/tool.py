from __future__ import annotations

import re
from typing import Any
import requests

from tools._shared import TIMEOUT, err


def get_crypto_price(symbol: str = "BTC", currency: str = "USDT") -> dict[str, Any]:
    """Tra cứu giá tiền điện tử theo thời gian thực."""
    try:
        clean_symbol = re.sub(r"[^A-Za-z0-9]", "", symbol or "").upper()
        clean_currency = re.sub(r"[^A-Za-z0-9]", "", currency or "USDT").upper()
        if not clean_symbol:
            return {"tool": "crypto_price", "error": "ValueError", "message": "Symbol cannot be empty"}

        trading_pair = f"{clean_symbol}{clean_currency}"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={trading_pair}"
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        price_str = data.get("price", "0")
        price_float = float(price_str)
        return {
            "tool": "crypto_price",
            "symbol": clean_symbol,
            "currency": clean_currency,
            "trading_pair": trading_pair,
            "price": price_float,
            "price_formatted": f"{price_float:,.4f} {clean_currency}",
            "status": "success",
        }
    except Exception as exc:
        return err("crypto_price", exc)
