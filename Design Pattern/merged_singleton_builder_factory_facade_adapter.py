import streamlit as st

############################################################
# Singleton for logging and configuration
############################################################

class LogConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
            cls._instance.currency = "USD"
        return cls._instance

    def log(self, text):
        self.logs.append(text)

############################################################
# Builder Pattern
############################################################

class Product:
    def __init__(self, name=None, color=None, size=None):
        self.name = name
        self.color = color
        self.size = size

    def info(self):
        return f"{self.name} (Color: {self.color}, Size: {self.size})"

class ProductBuilder:
    def __init__(self):
        self.product = Product()

    def set_name(self, name):
        self.product.name = name
        return self

    def set_color(self, color):
        self.product.color = color
        return self

    def set_size(self, size):
        self.product.size = size
        return self

    def build(self):
        return self.product

############################################################
# Payment Interface
############################################################

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Must implement pay")

############################################################
# Concrete Processors
############################################################

class CreditCardProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Credit card processed {amount}"

class PayPalProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"PayPal processed {amount}"

############################################################
# Legacy API and Adapter
############################################################

class LegacyBankAPI:
    def send_payment(self, value):
        return f"Legacy Bank transferred {value}"

class LegacyBankAdapter(PaymentProcessor):
    def __init__(self, legacy_api):
        self.legacy_api = legacy_api

    def pay(self, amount):
        return self.legacy_api.send_payment(amount)

############################################################
# Factory Pattern including adapter option
############################################################

class PaymentFactory:
    @staticmethod
    def create(method):
        if method == "Credit Card":
            return CreditCardProcessor()
        if method == "PayPal":
            return PayPalProcessor()
        if method == "Legacy Bank (Adapter)":
            return LegacyBankAdapter(LegacyBankAPI())
        raise ValueError("Unknown method")

############################################################
# Facade Pattern
############################################################

class InventoryService:
    def check(self, product):
        return f"Stock confirmed for {product.info()}"

class PaymentService:
    def handle(self, message):
        return message

class ShippingService:
    def ship(self, product):
        return f"Shipment created for {product.info()}"

class OrderFacade:
    def __init__(self, logger):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
        self.logger = logger

    def place(self, product, processor, amount):
        results = []

        step = self.inventory.check(product)
        self.logger.log(step)
        results.append(step)

        payment_result = self.payment.handle(processor.pay(amount))
        self.logger.log(payment_result)
        results.append(payment_result)

        final_step = self.shipping.ship(product)
        self.logger.log(final_step)
        results.append(final_step)

        return results

############################################################
# Streamlit UI
############################################################

st.title("Unified Patterns (Signleton, Builder, Factory, Adapter, Facade) Demo")

logger = LogConfig()

############################################################
# Singleton
############################################################

st.subheader("Configuration")
st.write(f"Currency: {logger.currency}")

############################################################
# Builder
############################################################

st.subheader("Build Product")
builder = ProductBuilder()

name = st.text_input("Product name", "Lamp")
color = st.selectbox("Color", ["Red", "Blue", "White"])
size = st.selectbox("Size", ["Small", "Medium", "Large"])

product = builder.set_name(name).set_color(color).set_size(size).build()
st.write(f"Product: {product.info()}")

############################################################
# Factory with Adapter
############################################################

st.subheader("Select Payment Method")
method = st.selectbox("Method", ["Credit Card", "PayPal", "Legacy Bank (Adapter)"])
amount = st.number_input("Amount", min_value=1, value=85)

processor = PaymentFactory.create(method)

############################################################
# Facade
############################################################

st.subheader("Place Order")

if st.button("Place Order"):
    facade = OrderFacade(logger)
    steps = facade.place(product, processor, amount)
    # for s in steps:
    #     st.success(s)

############################################################
# Logs
############################################################

st.subheader("Logs")
for line in logger.logs:
    st.write(line)

############################################################
# Summary
############################################################

st.subheader("Summary of Patterns")

st.markdown(
    """
**Singleton**
* Stores logs and global configuration.

**Builder**
* Assembles product attributes incrementally.

**Factory**
* Creates payment processors, including the adapter.

**Adapter**
* Wraps a legacy API to match the expected payment interface.

**Facade**
* Coordinates inventory, payment, and shipping into one call.
"""
)
