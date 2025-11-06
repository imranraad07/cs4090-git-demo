from models import Order
from db import WriteDB
from producer import KafkaEventProducer
from commands import CreateOrderCommand

ORDER_CREATED = "ORDER_CREATED"

class CommandHandler:
    def __init__(self, db: WriteDB, producer: KafkaEventProducer):
        self.db = db
        self.producer = producer

    async def handle_create_order(self, command: CreateOrderCommand):
        order = Order(**command.dict())
        self.db.save(order)
        await self.producer.publish(ORDER_CREATED, order.dict())
