"""Market Price Service - Fetches real-time mandi prices from government sources.

Uses data.gov.in API for agricultural commodity prices.
Falls back to cached/static data when API is unavailable.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# API Configuration
DATA_GOV_API_BASE = "https://api.data.gov.in/resource"
# Daily Price of Various Commodities from data.gov.in
COMMODITY_PRICE_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"  # Public demo key

# Cache settings
CACHE_DURATION_HOURS = 6
_price_cache: dict = {}
_cache_timestamp: Optional[datetime] = None

# Crop name mapping (our names -> API commodity names)
CROP_TO_COMMODITY = {
    "rice": "Rice",
    "wheat": "Wheat",
    "maize": "Maize",
    "cotton": "Cotton",
    "groundnut": "Groundnut",
    "sugarcane": "Sugarcane",
    "banana": "Banana",
    "apple": "Apple",
    "mango": "Mango",
    "grapes": "Grapes",
    "coffee": "Coffee",
    "jute": "Jute",
    "coconut": "Coconut",
    "papaya": "Papaya",
    "orange": "Orange",
    "chickpea": "Bengal Gram(Gram)",
    "kidneybeans": "Rajma",
    "pigeonpeas": "Arhar (Tur/Red Gram)",
    "mothbeans": "Moth",
    "mungbean": "Green Gram (Moong)",
    "blackgram": "Black Gram (Urd Beans)",
    "lentil": "Masur Dal",
    "pomegranate": "Pomegranate",
    "watermelon": "Watermelon",
    "muskmelon": "Muskmelon",
}

# Fallback static prices (MSP/Average market prices in ₹/quintal)
FALLBACK_PRICES = {
    "rice": {
        "price": 2183,
        "trend": "Stable",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "wheat": {
        "price": 2275,
        "trend": "Stable",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "maize": {
        "price": 2090,
        "trend": "Rising",
        "demand": "Moderate",
        "source": "MSP 2024-25",
    },
    "cotton": {
        "price": 7020,
        "trend": "Rising",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "groundnut": {
        "price": 6377,
        "trend": "Rising",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "sugarcane": {
        "price": 315,
        "trend": "Stable",
        "demand": "High",
        "source": "FRP 2024-25",
    },
    "banana": {
        "price": 1800,
        "trend": "Rising",
        "demand": "High",
        "source": "Market Avg",
    },
    "apple": {
        "price": 8500,
        "trend": "Seasonal",
        "demand": "Moderate",
        "source": "Market Avg",
    },
    "mango": {
        "price": 4500,
        "trend": "Seasonal",
        "demand": "High",
        "source": "Market Avg",
    },
    "grapes": {
        "price": 4200,
        "trend": "Rising",
        "demand": "Moderate",
        "source": "Market Avg",
    },
    "coffee": {
        "price": 9500,
        "trend": "Rising",
        "demand": "High",
        "source": "Market Avg",
    },
    "jute": {
        "price": 5050,
        "trend": "Stable",
        "demand": "Moderate",
        "source": "MSP 2024-25",
    },
    "coconut": {
        "price": 2800,
        "trend": "Stable",
        "demand": "High",
        "source": "Market Avg",
    },
    "papaya": {
        "price": 2000,
        "trend": "Rising",
        "demand": "Moderate",
        "source": "Market Avg",
    },
    "orange": {
        "price": 3500,
        "trend": "Stable",
        "demand": "High",
        "source": "Market Avg",
    },
    "chickpea": {
        "price": 5440,
        "trend": "Rising",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "kidneybeans": {
        "price": 6800,
        "trend": "Stable",
        "demand": "Moderate",
        "source": "Market Avg",
    },
    "pigeonpeas": {
        "price": 7000,
        "trend": "Rising",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "mothbeans": {
        "price": 5650,
        "trend": "Stable",
        "demand": "Moderate",
        "source": "Market Avg",
    },
    "mungbean": {
        "price": 8558,
        "trend": "Rising",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "blackgram": {
        "price": 6950,
        "trend": "Rising",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "lentil": {
        "price": 6425,
        "trend": "Stable",
        "demand": "High",
        "source": "MSP 2024-25",
    },
    "pomegranate": {
        "price": 8500,
        "trend": "Rising",
        "demand": "Moderate",
        "source": "Market Avg",
    },
    "watermelon": {
        "price": 1500,
        "trend": "Seasonal",
        "demand": "High",
        "source": "Market Avg",
    },
    "muskmelon": {
        "price": 2200,
        "trend": "Seasonal",
        "demand": "Moderate",
        "source": "Market Avg",
    },
}


@dataclass
class MarketPrice:
    """Market price data for a commodity."""

    crop: str
    price: float
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    modal_price: Optional[float] = None
    trend: str = "Stable"
    demand: str = "Moderate"
    market: str = "All India"
    state: str = ""
    last_updated: str = ""
    source: str = "data.gov.in"
    is_live: bool = False


def _determine_trend(current_price: float, historical_avg: float) -> str:
    """Determine price trend based on comparison with historical average."""
    if current_price > historical_avg * 1.05:
        return "Rising"
    elif current_price < historical_avg * 0.95:
        return "Falling"
    return "Stable"


def _determine_demand(modal_price: float, min_price: float, max_price: float) -> str:
    """Estimate demand based on price spread."""
    if max_price > 0 and min_price > 0:
        spread_ratio = (max_price - min_price) / modal_price if modal_price > 0 else 0
        if spread_ratio < 0.15:
            return "High"  # Tight spread = high demand
        elif spread_ratio > 0.30:
            return "Low"  # Wide spread = volatile/low demand
    return "Moderate"


def fetch_live_prices(commodity: str, state: str = "") -> Optional[MarketPrice]:
    """Fetch live prices from data.gov.in API.

    Args:
        commodity: Name of the commodity to fetch prices for
        state: Optional state filter

    Returns:
        MarketPrice object if successful, None otherwise
    """
    try:
        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": 10,
            "filters[commodity]": commodity,
        }

        if state:
            params["filters[state]"] = state

        response = requests.get(
            f"{DATA_GOV_API_BASE}/{COMMODITY_PRICE_RESOURCE_ID}",
            params=params,
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])

            if records:
                # Calculate average from multiple market records
                prices = []
                min_prices = []
                max_prices = []
                markets = []
                states = []

                for record in records:
                    try:
                        modal = float(record.get("modal_price", 0))
                        min_p = float(record.get("min_price", 0))
                        max_p = float(record.get("max_price", 0))

                        if modal > 0:
                            prices.append(modal)
                        if min_p > 0:
                            min_prices.append(min_p)
                        if max_p > 0:
                            max_prices.append(max_p)

                        markets.append(record.get("market", ""))
                        states.append(record.get("state", ""))
                    except (ValueError, TypeError):
                        continue

                if prices:
                    avg_price = sum(prices) / len(prices)
                    avg_min = sum(min_prices) / len(min_prices) if min_prices else None
                    avg_max = sum(max_prices) / len(max_prices) if max_prices else None

                    # Get fallback data for trend comparison
                    crop_key = next(
                        (k for k, v in CROP_TO_COMMODITY.items() if v == commodity),
                        commodity.lower(),
                    )
                    fallback = FALLBACK_PRICES.get(crop_key, {})
                    historical_avg = fallback.get("price", avg_price)

                    trend = _determine_trend(avg_price, historical_avg)
                    demand = _determine_demand(
                        avg_price,
                        avg_min or avg_price * 0.9,
                        avg_max or avg_price * 1.1,
                    )

                    return MarketPrice(
                        crop=crop_key,
                        price=round(avg_price, 2),
                        min_price=round(avg_min, 2) if avg_min else None,
                        max_price=round(avg_max, 2) if avg_max else None,
                        modal_price=round(avg_price, 2),
                        trend=trend,
                        demand=demand,
                        market=", ".join(set(m for m in markets[:3] if m)),
                        state=", ".join(set(s for s in states[:2] if s)),
                        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
                        source="data.gov.in (Live)",
                        is_live=True,
                    )

    except requests.RequestException as e:
        logger.warning(f"Failed to fetch live prices for {commodity}: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to parse API response for {commodity}: {e}")

    return None


def get_market_price(crop_name: str, state: str = "") -> dict:
    """Get market price for a crop with live data fallback.

    Args:
        crop_name: Name of the crop
        state: Optional state filter for regional prices

    Returns:
        Dictionary with price, trend, demand, and metadata
    """
    global _price_cache, _cache_timestamp

    crop_key = crop_name.lower().strip()
    cache_key = f"{crop_key}:{state}"

    # Check cache validity
    if _cache_timestamp and (datetime.now() - _cache_timestamp) < timedelta(
        hours=CACHE_DURATION_HOURS
    ):
        if cache_key in _price_cache:
            return _price_cache[cache_key]

    # Try to fetch live data
    commodity_name = CROP_TO_COMMODITY.get(crop_key)
    if commodity_name:
        live_price = fetch_live_prices(commodity_name, state)
        if live_price:
            result = {
                "price": live_price.price,
                "min_price": live_price.min_price,
                "max_price": live_price.max_price,
                "trend": live_price.trend,
                "demand": live_price.demand,
                "market": live_price.market,
                "state": live_price.state,
                "last_updated": live_price.last_updated,
                "source": live_price.source,
                "is_live": True,
            }

            # Update cache
            _price_cache[cache_key] = result
            _cache_timestamp = datetime.now()

            return result

    # Fallback to static data
    fallback = FALLBACK_PRICES.get(
        crop_key,
        {"price": 3000, "trend": "Stable", "demand": "Moderate", "source": "Estimated"},
    )

    return {
        "price": fallback["price"],
        "trend": fallback["trend"],
        "demand": fallback["demand"],
        "source": fallback.get("source", "Fallback Data"),
        "is_live": False,
        "last_updated": "Static MSP/Market Rates",
    }


def get_all_crop_prices() -> dict[str, dict]:
    """Get prices for all supported crops.

    Returns:
        Dictionary mapping crop names to their price data
    """
    return {crop: get_market_price(crop) for crop in FALLBACK_PRICES.keys()}


def refresh_price_cache() -> None:
    """Force refresh of the price cache."""
    global _price_cache, _cache_timestamp
    _price_cache = {}
    _cache_timestamp = None

    # Pre-fetch all prices
    for crop in FALLBACK_PRICES.keys():
        get_market_price(crop)


__all__ = [
    "MarketPrice",
    "get_market_price",
    "get_all_crop_prices",
    "refresh_price_cache",
    "FALLBACK_PRICES",
]
