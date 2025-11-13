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

    def log(self, message):
        self.logs.append(message)

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
# Factory Pattern
############################################################

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Must implement pay")

class CreditCardProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Credit card payment processed for {amount}"

class PayPalProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"PayPal payment processed for {amount}"

class CryptoProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Crypto payment processed for {amount}"

class PaymentFactory:
    @staticmethod
    def create_processor(method):
        options = {
            "Credit Card": CreditCardProcessor,
            "PayPal": PayPalProcessor,
            "Crypto": CryptoProcessor
        }
        return options[method]()

############################################################
# Facade Pattern
############################################################

class InventoryService:
    def check_stock(self, product):
        return f"Stock available for {product.info()}"

class PaymentService:
    def process(self, text):
        return text

class ShippingService:
    def ship(self, product):
        return f"Shipment created for {product.info()}"

class OrderFacade:
    def __init__(self, logger):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
        self.logger = logger

    def place_order(self, product, processor, amount):
        results = []

        step = self.inventory.check_stock(product)
        self.logger.log(step)
        results.append(step)

        payment_result = self.payment.process(processor.pay(amount))
        self.logger.log(payment_result)
        results.append(payment_result)

        shipped = self.shipping.ship(product)
        self.logger.log(shipped)
        results.append(shipped)

        return results

############################################################
# Streamlit UI
############################################################

st.title("Unified Patterns (Signleton, Builder, Factory, Facade) Demo")

logger = LogConfig()

############################################################
# Singleton display
############################################################

st.subheader("Configuration Singleton")
st.write(f"Currency: {logger.currency}")

############################################################
# Builder example
############################################################

st.subheader("Build Product")
builder = ProductBuilder()

name = st.text_input("Product name", "Chair")
color = st.selectbox("Color", ["Red", "Green", "Blue"])
size = st.selectbox("Size", ["Small", "Medium", "Large"])

product = builder.set_name(name).set_color(color).set_size(size).build()
st.write(f"Built Product: {product.info()}")

############################################################
# Factory example
############################################################

st.subheader("Select Payment Method")
method = st.selectbox("Method", ["Credit Card", "PayPal", "Crypto"])
amount = st.number_input("Amount", min_value=1, value=120)
processor = PaymentFactory.create_processor(method)

############################################################
# Facade example
############################################################

st.subheader("Place Order")

if st.button("Place Order"):
    facade = OrderFacade(logger)
    output = facade.place_order(product, processor, amount)
    for entry in output:
        st.success(entry)

############################################################
# Log output
############################################################

st.subheader("Logger Output")
for entry in logger.logs:
    st.write(entry)

############################################################
# Summary
############################################################

st.subheader("Pattern Summary")

st.markdown(
    """
**Singleton**
* Holds configuration and logs for the entire application.

**Builder**
* Constructs products step by step.

**Factory**
* Creates payment processors based on the selected method.

**Facade**
* Coordinates checking stock, processing payment, and shipping.
"""
)
