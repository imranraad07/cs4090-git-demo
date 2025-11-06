import json
import asyncio
from aiokafka import AIOKafkaConsumer
from handlers import EventHandler
from events import DomainEvent

class KafkaEventConsumer:
    def __init__(self, topic: str, handler: EventHandler, bootstrap_servers: str = "localhost:9092"):
        self.topic = topic
        self.handler = handler
        self.bootstrap_servers = bootstrap_servers
        self.consumer: AIOKafkaConsumer | None = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )
        await self.consumer.start()
        asyncio.create_task(self.consume_loop())

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume_loop(self):
        assert self.consumer
        async for msg in self.consumer:
            event = DomainEvent(**msg.value)
            self.handler.handle(event)
