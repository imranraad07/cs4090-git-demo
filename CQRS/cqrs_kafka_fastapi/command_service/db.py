from typing import Dict, Optional
from models import Order

class WriteDB:
    def __init__(self):
        self.orders: Dict[str, Order] = {}

    def save(self, order: Order):
        self.orders[order.id] = order

    def get(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)
