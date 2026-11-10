from __future__ import annotations

from typing import Any
import requests

from tools._shared import TIMEOUT, err


def get_weather(city: str = "Hanoi") -> dict[str, Any]:
    """Tra cứu thông tin thời tiết hiện tại theo thành phố."""
    try:
        clean_city = (city or "").strip()
        if not clean_city:
            return {"tool": "weather", "error": "ValueError", "message": "City cannot be empty"}

        url = f"https://wttr.in/{clean_city}?format=j1"
        headers = {"User-Agent": "AI20k-Research-Agent/1.0"}
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        current = (data.get("current_condition") or [{}])[0]
        temp_c = current.get("temp_C", "N/A")
        desc = (current.get("weatherDesc") or [{}])[0].get("value", "Clear")
        humidity = current.get("humidity", "N/A")
        wind = current.get("windspeedKmph", "N/A")

        return {
            "tool": "weather",
            "city": clean_city,
            "temperature_c": temp_c,
            "condition": desc,
            "humidity": f"{humidity}%",
            "wind_kmph": f"{wind} km/h",
            "status": "success",
        }
    except Exception as exc:
        return err("weather", exc)
