"""Weather data access layer supporting OpenWeather and Weatherbit providers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Final, Literal, Optional

import requests

ProviderName = Literal["openweather"]


class WeatherProviderError(RuntimeError):
    """Raised when a provider fails to supply weather data."""


@dataclass(frozen=True)
class WeatherSnapshot:
    """Normalized weather observation returned by a provider."""

    location: str
    temperature_c: float
    humidity_pct: float
    rainfall_mm: float
    provider: ProviderName
    observed_at: datetime


_CACHE_TTL: Final = timedelta(minutes=30)
_cache: dict[str, tuple[datetime, WeatherSnapshot]] = {}

_OPENWEATHER_KEY: Final[Optional[str]] = os.getenv("OPENWEATHER_API_KEY")


def _cache_key(location: str, provider: ProviderName) -> str:
    return f"{provider}:{location.strip().lower()}"


def _cache_get(location: str, provider: ProviderName) -> WeatherSnapshot | None:
    key = _cache_key(location, provider)
    entry = _cache.get(key)
    if not entry:
        return None
    created, snapshot = entry
    if datetime.now(timezone.utc) - created > _CACHE_TTL:
        _cache.pop(key, None)
        return None
    return snapshot


def _cache_set(location: str, snapshot: WeatherSnapshot) -> None:
    key = _cache_key(location, snapshot.provider)
    _cache[key] = (datetime.now(timezone.utc), snapshot)


def _fetch_openweather(location: str) -> WeatherSnapshot:
    if not _OPENWEATHER_KEY:
        raise WeatherProviderError("OPENWEATHER_API_KEY is not configured")

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": location, "appid": _OPENWEATHER_KEY, "units": "metric"},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise WeatherProviderError(f"OpenWeather request failed: {exc}") from exc

    try:
        main = payload["main"]
        rain = payload.get("rain", {})
        rainfall = rain.get("1h") or rain.get("3h", 0.0)
        if rainfall is None:
            rainfall = 0.0
        timestamp = datetime.fromtimestamp(payload.get("dt", 0), tz=timezone.utc)
    except (KeyError, TypeError) as exc:
        raise WeatherProviderError(
            f"OpenWeather response missing fields: {exc}"
        ) from exc

    return WeatherSnapshot(
        location=location,
        temperature_c=float(main.get("temp", 0.0)),
        humidity_pct=float(main.get("humidity", 0.0)),
        rainfall_mm=float(rainfall),
        provider="openweather",
        observed_at=timestamp,
    )


def get_weather_snapshot(
    location: str,
    *,
    use_cache: bool = True,
) -> WeatherSnapshot:
    """Fetch a normalized weather snapshot for the given location using OpenWeather only."""
    location = location.strip()
    if not location:
        raise WeatherProviderError("Location must be provided for weather lookup")
    if not _OPENWEATHER_KEY:
        raise WeatherProviderError("OPENWEATHER_API_KEY is not configured")
    if use_cache:
        cached = _cache_get(location, "openweather")
        if cached:
            return cached
    snapshot = _fetch_openweather(location)
    _cache_set(location, snapshot)
    return snapshot


def clear_weather_cache() -> None:
    """Reset cached weather responses (useful for testing)."""

    _cache.clear()
