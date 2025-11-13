import streamlit as st

############################################################
# Singleton for configuration and logging
############################################################

class LogConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
            cls._instance.currency = "USD"
            cls._instance.tax_rate = 0.07
        return cls._instance

    def log(self, message):
        self.logs.append(message)

    def clear(self):
        self.logs = []


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
# Payment Base Interface
############################################################

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Must implement pay")


############################################################
# Concrete Payments
############################################################

class CreditCardProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Credit card processed {amount}"


class PayPalProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"PayPal processed {amount}"


############################################################
# Adapter Pattern
############################################################

class LegacyBankAPI:
    def send_payment(self, value):
        return f"Legacy Bank transferred {value}"


class LegacyBankAdapter(PaymentProcessor):
    def __init__(self, api):
        self.api = api

    def pay(self, amount):
        return self.api.send_payment(amount)


############################################################
# Decorator Pattern
############################################################

class PaymentDecorator(PaymentProcessor):
    def __init__(self, processor):
        self.processor = processor

    def pay(self, amount):
        return self.processor.pay(amount)


class LoggingDecorator(PaymentDecorator):
    def __init__(self, processor, logger):
        super().__init__(processor)
        self.logger = logger

    def pay(self, amount):
        result = self.processor.pay(amount)
        self.logger.log(f"LOG: Payment of {amount}")
        return result + " (logged)"


class TaxDecorator(PaymentDecorator):
    def __init__(self, processor, rate):
        super().__init__(processor)
        self.rate = rate

    def pay(self, amount):
        total = amount + (amount * self.rate)
        return self.processor.pay(total)


class SecurityDecorator(PaymentDecorator):
    def pay(self, amount):
        return "Security check ok. " + self.processor.pay(amount)


############################################################
# Factory Pattern
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
        raise ValueError("Unknown payment method")


############################################################
# Facade Pattern
############################################################

class InventoryService:
    def check(self, product):
        return f"Stock confirmed for {product.info()}"


class PaymentService:
    def handle(self, msg):
        return msg


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

        step1 = self.inventory.check(product)
        results.append(step1)
        self.logger.log(step1)

        step2 = processor.pay(amount)
        results.append(step2)
        self.logger.log(step2)

        step3 = self.shipping.ship(product)
        results.append(step3)
        self.logger.log(step3)

        return results


############################################################
# Streamlit UI
############################################################

st.title("Unified Patterns (Signleton, Builder, Factory, Adapter, Facade, Decorator) Demo")

logger = LogConfig()
logger.clear()

############################################################
# Builder
############################################################

st.subheader("Build Product")
builder = ProductBuilder()

name = st.text_input("Product Name", "Monitor")
color = st.selectbox("Color", ["Black", "White", "Gray"])
size = st.selectbox("Size", ["Small", "Medium", "Large"])

product = builder.set_name(name).set_color(color).set_size(size).build()
st.write("Product:", product.info())


############################################################
# Factory + Adapter
############################################################

st.subheader("Payment Method")
method = st.selectbox("Choose", ["Credit Card", "PayPal", "Legacy Bank (Adapter)"])
amount = st.number_input("Amount", min_value=1, value=200)

processor = PaymentFactory.create(method)


############################################################
# Decorators (Applied Conditionally)
############################################################

st.subheader("Enhance Payment Processor")

use_logging = st.checkbox("Enable Logging Decorator")
use_tax = st.checkbox("Enable Tax Decorator")
use_security = st.checkbox("Enable Security Decorator")

logging_enabled = use_logging

if use_logging:
    processor = LoggingDecorator(processor, logger)

if use_tax:
    processor = TaxDecorator(processor, logger.tax_rate)

if use_security:
    processor = SecurityDecorator(processor)


############################################################
# Facade
############################################################

if st.button("Place Order"):
    facade = OrderFacade(logger)
    output = facade.place(product, processor, amount)

    st.subheader("Order Output")
    # for line in output:
    #     st.success(line)

    st.subheader("Logs")
    if logging_enabled:
        for entry in logger.logs:
            st.write(entry)
    else:
        st.write("Logging disabled.")


############################################################
# Summary
############################################################

st.subheader("Summary")
st.write("Singleton for config and logs")
st.write("Builder constructs product")
st.write("Factory selects processor")
st.write("Adapter supports legacy API")
st.write("Decorator adds optional features")
st.write("Facade coordinates workflow")
