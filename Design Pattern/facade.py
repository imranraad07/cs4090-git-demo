import streamlit as st

# Subsystems
class InventoryService:
    def check_stock(self, item):
        return f"Stock for {item} is available"

class PaymentService:
    def process_payment(self, amount):
        return f"Payment of {amount} completed"

class ShippingService:
    def create_shipment(self, item):
        return f"Shipment created for {item}"

# Facade
class OrderFacade:
    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()

    def place_order(self, item, amount):
        steps = []
        steps.append(self.inventory.check_stock(item))
        steps.append(self.payment.process_payment(amount))
        steps.append(self.shipping.create_shipment(item))
        return steps

# Streamlit UI
st.title("Facade Pattern Demo")

item = st.text_input("Item name", "Laptop")
amount = st.number_input("Amount", value=500, min_value=1)

if st.button("Place Order"):
    facade = OrderFacade()
    results = facade.place_order(item, amount)
    for r in results:
        st.success(r)
