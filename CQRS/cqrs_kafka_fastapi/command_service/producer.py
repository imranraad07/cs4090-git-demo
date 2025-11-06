import json
from aiokafka import AIOKafkaProducer

class KafkaEventProducer:
    def __init__(self, topic: str, bootstrap_servers: str = "localhost:9092"):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def publish(self, event_type: str, payload: dict):
        if not self.producer:
            raise RuntimeError("Producer not started")
        event = {"type": event_type, "payload": payload}
        await self.producer.send_and_wait(self.topic, event)
