from db.write_db import WriteDB
from events.bus import EventBus
from events.events import DomainEvent, ORDER_CREATED
from command.commands import CreateOrderCommand
from models.order import Order

class OrderCommandHandler:
    def __init__(self, db: WriteDB, bus: EventBus):
        self.db = db
        self.bus = bus

    def handle_create_order(self, command: CreateOrderCommand):
        order = Order(id=command.id, customer=command.customer, items=command.items)
        self.db.save(order)
        event = DomainEvent(type=ORDER_CREATED, payload=order.dict())
        self.bus.publish(event)
