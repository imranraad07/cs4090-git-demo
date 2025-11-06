from db.read_db import ReadDB
from query.queries import GetOrderByIdQuery, GetAllOrdersQuery

class OrderQueryHandler:
    def __init__(self, db: ReadDB):
        self.db = db

    def handle_get_all(self, _: GetAllOrdersQuery):
        return self.db.get_all()

    def handle_get_by_id(self, query: GetOrderByIdQuery):
        return self.db.get_by_id(query.id)
