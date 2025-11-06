from fastapi import FastAPI, HTTPException
from uuid import uuid4

from db.write_db import WriteDB
from db.read_db import ReadDB
from events.bus import EventBus
from events.events import ORDER_CREATED, DomainEvent
from command.handlers import OrderCommandHandler
from command.commands import CreateOrderCommand
from query.handlers import OrderQueryHandler
from query.queries import GetOrderByIdQuery, GetAllOrdersQuery

app = FastAPI(title="CQRS Example")

write_db = WriteDB()
read_db = ReadDB()
bus = EventBus()

command_handler = OrderCommandHandler(write_db, bus)
query_handler = OrderQueryHandler(read_db)

def update_read_model(event: DomainEvent):
    from models.order import Order
    order = Order(**event.payload)
    read_db.update(order)

bus.subscribe(ORDER_CREATED, update_read_model)

@app.post("/orders")
def create_order(payload: dict):
    order_id = str(uuid4())
    command = CreateOrderCommand(id=order_id, **payload)
    command_handler.handle_create_order(command)
    return {"id": order_id}

@app.get("/orders")
def list_orders():
    return query_handler.handle_get_all(GetAllOrdersQuery())

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = query_handler.handle_get_by_id(GetOrderByIdQuery(id=order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
