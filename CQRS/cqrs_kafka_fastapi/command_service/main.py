from fastapi import FastAPI
from uuid import uuid4
from db import WriteDB
from handlers import CommandHandler
from commands import CreateOrderCommand
from producer import KafkaEventProducer

app = FastAPI(title="Command Service (Kafka)")

db = WriteDB()
producer = KafkaEventProducer(topic="order_events")
handler = CommandHandler(db, producer)

@app.on_event("startup")
async def startup_event():
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

@app.post("/orders")
async def create_order(payload: dict):
    order_id = str(uuid4())
    command = CreateOrderCommand(id=order_id, **payload)
    await handler.handle_create_order(command)
    return {"id": order_id, "status": "CREATED"}
