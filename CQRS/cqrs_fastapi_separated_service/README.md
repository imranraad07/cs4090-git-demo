## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run Services

### Terminal 1: Start Query Service
```
uvicorn query_service.main:app --port 8001
```

### Terminal 2: Start Command Service
```
uvicorn command_service.main:app --port 8000
```

## Test the System

### Create an Order
```
curl -X POST http://127.0.0.1:8000/orders      -H "Content-Type: application/json"      -d '{"customer": "Alice", "items": ["pen", "notebook"]}'
```

### List All Orders
```
curl http://127.0.0.1:8001/orders
```

### Get a Specific Order
```
curl http://127.0.0.1:8001/orders/<order_id>
```

## Description

- **Command Service** handles write operations and publishes events.
- **Query Service** handles read operations and subscribes to events.
- Communication occurs through HTTP POST requests on `/events`.
