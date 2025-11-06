import requests, json

class EventBus:
    def __init__(self, query_service_url: str):
        self.query_service_url = query_service_url

    def publish(self, event_type: str, payload: dict):
        event = {"type": event_type, "payload": payload}
        try:
            requests.post(f"{self.query_service_url}/events", json=event, timeout=2)
        except requests.exceptions.RequestException:
            print("Failed to deliver event, will retry later.")
