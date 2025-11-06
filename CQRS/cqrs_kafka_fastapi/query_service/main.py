from fastapi import FastAPI, HTTPException
from db import ReadDB
from handlers import EventHandler
from consumer import KafkaEventConsumer

app = FastAPI(title="Query Service (Kafka)")

db = ReadDB()
handler = EventHandler(db)
consumer = KafkaEventConsumer("order_events", handler)

@app.on_event("startup")
async def startup_event():
    await consumer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()

@app.get("/orders")
def list_orders():
    return db.get_all()

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = db.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
