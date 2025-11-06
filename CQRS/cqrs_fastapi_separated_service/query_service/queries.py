from pydantic import BaseModel

class GetOrderByIdQuery(BaseModel):
    id: str

class GetAllOrdersQuery(BaseModel):
    pass
