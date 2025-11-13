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
# Product Builder Pattern
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
# Strategy Pattern for discounts
############################################################

class DiscountStrategy:
    def apply(self, amount):
        raise NotImplementedError("Must implement apply")


class NoDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent

    def apply(self, amount):
        return amount - (amount * self.percent)


class FixedAmountDiscount(DiscountStrategy):
    def __init__(self, deduction):
        self.deduction = deduction

    def apply(self, amount):
        result = amount - self.deduction
        return max(result, 0)


class BuyOneGetOneStrategy(DiscountStrategy):
    def apply(self, amount):
        return amount / 2


############################################################
# Base Payment interface
############################################################

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Must implement pay")


############################################################
# Concrete Payment Implementations
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
        self.logger.log(step1)
        results.append(step1)

        step2 = processor.pay(amount)
        self.logger.log(step2)
        results.append(step2)

        step3 = self.shipping.ship(product)
        self.logger.log(step3)
        results.append(step3)

        return results


############################################################
# Streamlit UI
############################################################

st.title("Unified Patterns (Signleton, Builder, Factory, Adapter, Facade, Decorator, Strategy) Demo")

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
# Strategy Selection
############################################################

st.subheader("Discount Strategy")
strategy_name = st.selectbox(
    "Choose discount strategy",
    [
        "No Discount",
        "Percentage Discount",
        "Fixed Discount",
        "Buy One Get One"
    ]
)

if strategy_name == "No Discount":
    strategy = NoDiscount()

elif strategy_name == "Percentage Discount":
    percent = st.slider("Percent", 1, 50, 20)
    strategy = PercentageDiscount(percent / 100)

elif strategy_name == "Fixed Discount":
    deduction = st.number_input("Deduction amount", min_value=1, value=10)
    strategy = FixedAmountDiscount(deduction)

elif strategy_name == "Buy One Get One":
    strategy = BuyOneGetOneStrategy()


############################################################
# Factory + Adapter
############################################################

st.subheader("Payment Method")
method = st.selectbox("Choose", ["Credit Card", "PayPal", "Legacy Bank (Adapter)"])
base_amount = st.number_input("Base Amount", min_value=1, value=200)


############################################################
# Apply strategy to amount
############################################################

discounted_amount = strategy.apply(base_amount)
st.write(f"Discounted amount: {discounted_amount}")

processor = PaymentFactory.create(method)


############################################################
# Decorators
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
    output = facade.place(product, processor, discounted_amount)

    # st.subheader("Order Result")
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
st.write("Strategy selects discount behavior")
st.write("Singleton stores config and logs")
st.write("Builder constructs product")
st.write("Factory selects processor")
st.write("Adapter supports legacy API")
st.write("Decorator adds optional features")
st.write("Facade coordinates workflow")
