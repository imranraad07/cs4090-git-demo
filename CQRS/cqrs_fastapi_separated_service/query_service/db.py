from typing import Dict, List, Optional
from .models import Order

class ReadDB:
    def __init__(self):
        self.orders: Dict[str, Order] = {}

    def update(self, order: Order):
        self.orders[order.id] = order

    def get_all(self) -> List[Order]:
        return list(self.orders.values())

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)
