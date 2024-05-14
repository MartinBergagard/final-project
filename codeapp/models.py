from __future__ import annotations

# python built-in imports
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class our_class:
    country: str
    item_type: str
    sales_channel: str
    order_priority: str
    order_date: datetime
    order_id: int
    ship_date: datetime
    units_sold: int
    total_profit: float
