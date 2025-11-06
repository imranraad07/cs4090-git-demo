from typing import Dict, List, Optional
from models.order import Order

class ReadDB:
    def __init__(self):
        self.orders_view: Dict[str, Order] = {}

    def update(self, order: Order):
        self.orders_view[order.id] = order

    def get_all(self) -> List[Order]:
        return list(self.orders_view.values())

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self.orders_view.get(order_id)
