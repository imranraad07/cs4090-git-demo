from pydantic import BaseModel
from typing import List, Literal

class Order(BaseModel):
    id: str
    customer: str
    items: List[str]
    status: Literal["CREATED", "CONFIRMED", "CANCELLED"] = "CREATED"
