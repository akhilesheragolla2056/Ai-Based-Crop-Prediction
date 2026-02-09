# Average NPK values (kg/ha) for selected Indian states/districts
# Source: Government of India Soil Health Card data (example values, not exhaustive)
# Format: {"region_key": {"N": value, "P": value, "K": value}}


# Expanded NPK_LOOKUP with all Indian states, UTs, and major districts/cities (including Mumbai, Pune, Nagpur, Hyderabad, Chennai, Bengaluru, Kolkata, Delhi, etc.)
NPK_LOOKUP = {
    # States
    "andhra pradesh": {"N": 70.0, "P": 28.0, "K": 36.0},
    "arunachal pradesh": {"N": 65.0, "P": 25.0, "K": 30.0},
    "assam": {"N": 68.0, "P": 27.0, "K": 32.0},
    "bihar": {"N": 88.0, "P": 37.0, "K": 43.0},
    "chhattisgarh": {"N": 72.0, "P": 29.0, "K": 35.0},
    "goa": {"N": 60.0, "P": 22.0, "K": 28.0},
    "gujarat": {"N": 83.0, "P": 34.0, "K": 41.0},
    "haryana": {"N": 92.0, "P": 41.0, "K": 46.0},
    "himachal pradesh": {"N": 67.0, "P": 26.0, "K": 31.0},
    "jharkhand": {"N": 74.0, "P": 30.0, "K": 37.0},
    "karnataka": {"N": 85.0, "P": 32.0, "K": 42.0},
    "kerala": {"N": 69.0, "P": 27.0, "K": 33.0},
    "madhya pradesh": {"N": 86.0, "P": 36.0, "K": 44.0},
    "maharashtra": {"N": 80.0, "P": 35.0, "K": 40.0},
    "manipur": {"N": 62.0, "P": 23.0, "K": 29.0},
    "meghalaya": {"N": 63.0, "P": 24.0, "K": 30.0},
    "mizoram": {"N": 61.0, "P": 22.0, "K": 28.0},
    "nagaland": {"N": 64.0, "P": 25.0, "K": 31.0},
    "odisha": {"N": 77.0, "P": 31.0, "K": 38.0},
    "punjab": {"N": 95.0, "P": 42.0, "K": 48.0},
    "rajasthan": {"N": 84.0, "P": 35.0, "K": 41.0},
    "sikkim": {"N": 66.0, "P": 25.0, "K": 30.0},
    "tamil nadu": {"N": 82.0, "P": 34.0, "K": 41.0},
    "telangana": {"N": 75.0, "P": 30.0, "K": 38.0},
    "tripura": {"N": 60.0, "P": 22.0, "K": 28.0},
    "uttar pradesh": {"N": 90.0, "P": 40.0, "K": 45.0},
    "uttarakhand": {"N": 68.0, "P": 27.0, "K": 32.0},
    "west bengal": {"N": 78.0, "P": 33.0, "K": 39.0},
    # Union Territories
    "andaman and nicobar islands": {"N": 55.0, "P": 20.0, "K": 25.0},
    "chandigarh": {"N": 58.0, "P": 21.0, "K": 27.0},
    "dadra and nagar haveli and daman and diu": {"N": 59.0, "P": 22.0, "K": 28.0},
    "jammu and kashmir": {"N": 70.0, "P": 28.0, "K": 36.0},
    "ladakh": {"N": 56.0, "P": 20.0, "K": 25.0},
    "lakshadweep": {"N": 54.0, "P": 19.0, "K": 24.0},
    "puducherry": {"N": 73.0, "P": 29.0, "K": 36.0},
    # Major cities/districts (examples, add more as needed)
    "mumbai": {"N": 81.0, "P": 36.0, "K": 41.0},
    "pune": {"N": 80.0, "P": 35.0, "K": 40.0},
    "nagpur": {"N": 80.0, "P": 35.0, "K": 40.0},
    "hyderabad": {"N": 75.0, "P": 30.0, "K": 38.0},
    "chennai": {"N": 82.0, "P": 34.0, "K": 41.0},
    "bengaluru": {"N": 85.0, "P": 32.0, "K": 42.0},
    "kolkata": {"N": 78.0, "P": 33.0, "K": 39.0},
    "delhi": {"N": 87.0, "P": 36.0, "K": 44.0},
    # Add more districts/cities as needed
}


def get_npk_for_region(region: str) -> dict[str, float] | None:
    key = region.strip().lower()
    return NPK_LOOKUP.get(key)
