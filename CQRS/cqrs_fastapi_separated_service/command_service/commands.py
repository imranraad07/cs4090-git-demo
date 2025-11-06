from pydantic import BaseModel
from typing import List

class CreateOrderCommand(BaseModel):
    id: str
    customer: str
    items: List[str]
