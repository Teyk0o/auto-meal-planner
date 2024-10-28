import re
from typing import Optional


def clean_price(price: str) -> Optional[float]:
    """
    Clean and convert price string to float values.
    Handles both unit prices and kilogram prices.

    Args:
        price (str): Price string to be cleaned and converted.
                    Examples:
                    - Unit price: "2                     €                    ,89"
                    - Kg price: "55,58 € / kg"

    Returns:
        Optional[float]: Price value as float or None if price string is invalid.

    Examples:
        >>> clean_price("2                     €                    ,89")
        2.89
        >>> clean_price("9                     €                    ,39")
        9.39
        >>> clean_price("55,58 € / kg")
        55.58
    """
    if not price or not isinstance(price, str):
        return None

    try:
        # Clean all spaces and special characters
        cleaned = re.sub(r'\s+', '', price)

        # If it's a price per kilogram, remove the '/kg' part
        if '/kg' in cleaned.lower():
            cleaned = cleaned.split('€')[0]
        else:
            cleaned = cleaned.replace('€', '')

        # Format wanted: "2,89" or "55,58"
        parts = cleaned.split(',')
        if len(parts) == 2:
            euros = parts[0]
            cents = parts[1]
            if euros.isdigit() and cents.isdigit():
                return float(f"{euros}.{cents}")

        # If the price is already in float format
        if '.' in cleaned:
            try:
                return float(cleaned)
            except ValueError:
                pass

        # If the price is an integer
        if cleaned.isdigit():
            return float(cleaned)

        return None

    except Exception as e:
        return None