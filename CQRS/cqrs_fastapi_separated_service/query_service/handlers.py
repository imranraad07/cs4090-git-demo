from .db import ReadDB
from .models import Order
from .events import DomainEvent

ORDER_CREATED = "ORDER_CREATED"

class EventHandler:
    def __init__(self, db: ReadDB):
        self.db = db

    def handle(self, event: DomainEvent):
        if event.type == ORDER_CREATED:
            order = Order(**event.payload)
            self.db.update(order)
