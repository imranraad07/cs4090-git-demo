from .models import Order
from .db import WriteDB
from .bus import EventBus
from .commands import CreateOrderCommand

ORDER_CREATED = "ORDER_CREATED"

class CommandHandler:
    def __init__(self, db: WriteDB, bus: EventBus):
        self.db = db
        self.bus = bus

    def handle_create_order(self, command: CreateOrderCommand):
        order = Order(**command.dict())
        self.db.save(order)
        self.bus.publish(ORDER_CREATED, order.dict())
