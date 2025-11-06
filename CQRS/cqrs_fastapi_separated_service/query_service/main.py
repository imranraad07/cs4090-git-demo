from fastapi import FastAPI, HTTPException
from .db import ReadDB
from .handlers import EventHandler
from .events import DomainEvent
from .queries import GetOrderByIdQuery, GetAllOrdersQuery

app = FastAPI(title="Query Service")

db = ReadDB()
event_handler = EventHandler(db)

@app.post("/events")
def receive_event(event: DomainEvent):
    event_handler.handle(event)
    return {"received": event.type}

@app.get("/orders")
def list_orders():
    return db.get_all()

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = db.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
