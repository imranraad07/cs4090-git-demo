from fastapi import FastAPI
from uuid import uuid4
from .db import WriteDB
from .bus import EventBus
from .handlers import CommandHandler
from .commands import CreateOrderCommand

app = FastAPI(title="Command Service")

db = WriteDB()
bus = EventBus("http://localhost:8001")
handler = CommandHandler(db, bus)

@app.post("/orders")
def create_order(payload: dict):
    order_id = str(uuid4())
    command = CreateOrderCommand(id=order_id, **payload)
    handler.handle_create_order(command)
    return {"id": order_id, "status": "CREATED"}
