## Directory structure:
cqrs_fastapi/
├── main.py
├── command/
│   ├── commands.py
│   ├── handlers.py
├── query/
│   ├── queries.py
│   ├── handlers.py
├── db/
│   ├── write_db.py
│   ├── read_db.py
├── events/
│   ├── bus.py
│   ├── events.py
└── models/
    └── order.py



## install:
pip install fastapi uvicorn pydantic

## run:
uvicorn main:app --reload

CQRS service will start on http://127.0.0.1:8000

## verify:
http://127.0.0.1:8000/docs
This is the Swagger UI that FastAPI generates automatically. You will see all available endpoints there.

## Example:
Create an order:
curl -X POST http://127.0.0.1:8000/orders \
     -H "Content-Type: application/json" \
     -d '{"customer": "Alice", "items": ["book", "pen"]}'


Response Json:
{"id": "550e8400-e29b-41d4-a716-446655440000"}

Get all orders:
curl http://127.0.0.1:8000/orders

Get order by ID:
curl http://127.0.0.1:8000/orders/550e8400-e29b-41d4-a716-446655440000
