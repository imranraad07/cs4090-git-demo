from pydantic import BaseModel

class DomainEvent(BaseModel):
    type: str
    payload: dict
