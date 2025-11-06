# CQRS with FastAPI and Kafka

A minimal working example of **CQRS (Command Query Responsibility Segregation)** using **FastAPI** and **Apache Kafka**, with two independent microservices:
- **Command Service** – handles writes and publishes events to Kafka  
- **Query Service** – consumes Kafka events and maintains a read model

---

## Requirements

- Ubuntu (or any Linux)
- Python 3.10 or higher
- Java 11 or higher (required for Kafka)

Install Python dependencies:
```
pip install -r requirements.txt
```


## ⚙️ Install and Start Kafka (Ubuntu)

### 1. Install Java

```bash
sudo apt update
sudo apt install openjdk-11-jdk -y
```

### 2. Download and Extract Kafka 3.7.2

```bash
wget https://downloads.apache.org/kafka/3.7.2/kafka_2.12-3.7.2.tgz
tar -xzf kafka_2.12-3.7.2.tgz
cd kafka_2.12-3.7.2
```

### 3. Start Zookeeper and Kafka

Use **two terminals**:

**Terminal 1:**

```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

**Terminal 2:**

```
bin/kafka-server-start.sh config/server.properties
```

### 4. Create Kafka Topic

```
bin/kafka-topics.sh --create --topic order_events --bootstrap-server localhost:9092
```

### Investigate Topic:

List All Topics:

```
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Describe a Specific Topic:
```
bin/kafka-topics.sh --describe --topic order_events --bootstrap-server localhost:9092
```
What it shows:
- PartitionCount: How many partitions the topic has.
- ReplicationFactor: How many copies of each partition exist (for fault tolerance).
- Leader: Which broker handles writes for that partition.
- ISR (In-Sync Replicas): Brokers currently in sync with the leader.

Read Messages from a Topic (Consumer CLI):
```
bin/kafka-console-producer.sh --topic order_events --bootstrap-server localhost:9092
```

Read Messages from a Topic (Producer CLI):
```
bin/kafka-console-consumer.sh --topic order_events --bootstrap-server localhost:9092
```


Delete a Topic (DONT DO IT UNLESS YOU ACTUALLY WANT IT)
```
bin/kafka-topics.sh --delete --topic order_events --bootstrap-server localhost:9092
```

| Purpose          | Command                           |
| ---------------- | --------------------------------- |
| List topics      | `--list`                          |
| Describe topic   | `--describe --topic order_events` |
| Produce messages | `kafka-console-producer.sh`       |
| Consume messages | `kafka-console-consumer.sh`       |
| Delete topic     | `--delete --topic order_events`   |


## Run the Services

Use separate terminals for each service.

### **Terminal 1: Query Service**

```
cd query_service
uvicorn main:app --port 8001
```

### **Terminal 2: Command Service**

```
cd command_service
uvicorn main:app --port 8000
```

---

## Test the API

### Create an Order

```
curl -X POST http://127.0.0.1:8000/orders \
     -H "Content-Type: application/json" \
     -d '{"customer": "Alice", "items": ["pen", "notebook"]}'
```

Response:

```json
{"id": "some-uuid", "status": "CREATED"}
```

### List All Orders

```
curl http://127.0.0.1:8001/orders
```

Expected:

```
[
  {
    "id": "some-uuid",
    "customer": "Alice",
    "items": ["pen", "notebook"],
    "status": "CREATED"
  }
]
```

## Project Structure

```
cqrs_kafka_fastapi/
├── README.md
├── requirements.txt
├── command_service/
│   ├── main.py
│   ├── db.py
│   ├── handlers.py
│   ├── commands.py
│   ├── models.py
│   └── producer.py
└── query_service/
    ├── main.py
    ├── db.py
    ├── handlers.py
    ├── consumer.py
    ├── models.py
    └── events.py
```


## Notes

* **run each service from inside its own folder** (`cd command_service` or `cd query_service`)
* Both services communicate asynchronously through Kafka.
* Each service can be scaled independently.
