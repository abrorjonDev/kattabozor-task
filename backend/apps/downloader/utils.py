from typing import Dict, Any

from downloader.models import Product, Attribute


def add_attributes(product: Product, attrs: Dict[str, Any]):
    """Adds attributes, but doesn't save to db."""
    try:
        return Attribute(**attrs, product=product)
    except Exception:
        return None