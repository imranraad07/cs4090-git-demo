import streamlit as st
import time

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
# Strategy Pattern (Discount)
############################################################

class DiscountStrategy:
    def apply(self, amount):
        raise NotImplementedError()


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
        return max(amount - self.deduction, 0)


class BuyOneGetOneStrategy(DiscountStrategy):
    def apply(self, amount):
        return amount / 2


############################################################
# Payment Interface
############################################################

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError()


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
        return self.processor.pay(amount + amount * self.rate)


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
        raise ValueError("Unknown method")


############################################################
# Observer Pattern
############################################################

class Observer:
    def update(self, message):
        raise NotImplementedError()


class EmailObserver(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(f"Email: {message}")


class SmsObserver(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(f"SMS: {message}")


class LogObserver(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(f"Log: {message}")


class OrderStatus:
    def __init__(self):
        self.status = "Pending"
        self.observers = []

    def attach(self, obs):
        self.observers.append(obs)

    def set_status(self, new):
        self.status = new
        self.notify(new)

    def notify(self, message):
        for obs in self.observers:
            obs.update(message)


############################################################
# PubSub Pattern
############################################################

class MessageBroker:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, sub):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(sub)

    def publish(self, topic, data):
        if topic in self.subscribers:
            for s in self.subscribers[topic]:
                s.notify(topic, data)


class PubSubSubscriber(Observer):
    def __init__(self):
        self.messages = []

    def notify(self, topic, data):
        self.messages.append(f"{topic}: {data}")


############################################################
# Facade Pattern (Timed Events)
############################################################

class InventoryService:
    def check(self, p):
        return f"Stock confirmed for {p.info()}"


class PaymentService:
    def handle(self, msg):
        return msg


class ShippingService:
    def ship(self, p):
        return f"Shipment created for {p.info()}"


class OrderFacade:
    def __init__(self, logger, broker):
        self.logger = logger
        self.broker = broker
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()

    def place(self, product, processor, amount, status_tracker, display):
        results = []

        # Event 1: Inventory check
        msg1 = self.inventory.check(product)
        results.append(msg1)
        self.logger.log(msg1)
        status_tracker.set_status("Inventory checked")
        self.broker.publish("order.events", "Inventory checked")
        display.write(msg1)
        time.sleep(0.5)

        # Event 2: Payment
        msg2 = processor.pay(amount)
        results.append(msg2)
        self.logger.log(msg2)
        status_tracker.set_status("Payment processed")
        self.broker.publish("order.events", "Payment processed")
        display.write(msg2)
        time.sleep(1.0)

        # Event 3: Shipping
        msg3 = self.shipping.ship(product)
        results.append(msg3)
        self.logger.log(msg3)
        status_tracker.set_status("Shipped")
        self.broker.publish("order.events", "Shipped")
        display.write(msg3)
        time.sleep(1.5)

        return results


############################################################
# Streamlit UI
############################################################

st.title("Unified Patterns Demo With Timed Events")

logger = LogConfig()
logger.clear()
broker = MessageBroker()

############################################################
# Builder
############################################################

st.subheader("Build Product")
builder = ProductBuilder()

name = st.text_input("Product Name", "Monitor")
color = st.selectbox("Color", ["Black", "White", "Gray"])
size = st.selectbox("Size", ["Small", "Medium", "Large"])

product = builder.set_name(name).set_color(color).set_size(size).build()

############################################################
# Strategy
############################################################

st.subheader("Discount Strategy")
choice = st.selectbox("Strategy", ["No Discount", "Percentage", "Fixed", "Buy One Get One"])

if choice == "No Discount":
    strategy = NoDiscount()
elif choice == "Percentage":
    percent = st.slider("Percent", 1, 50, 20)
    strategy = PercentageDiscount(percent / 100)
elif choice == "Fixed":
    deduction = st.number_input("Deduction", 1, 100, 10)
    strategy = FixedAmountDiscount(deduction)
else:
    strategy = BuyOneGetOneStrategy()

############################################################
# Payment Setup
############################################################

method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Legacy Bank (Adapter)"])
base_amount = st.number_input("Base Amount", 1, 500, 200)
discounted_amount = strategy.apply(base_amount)

processor = PaymentFactory.create(method)

############################################################
# Decorators
############################################################

use_log = st.checkbox("Logging Decorator")
use_tax = st.checkbox("Tax Decorator")
use_sec = st.checkbox("Security Decorator")

if use_log:
    processor = LoggingDecorator(processor, logger)

if use_tax:
    processor = TaxDecorator(processor, logger.tax_rate)

if use_sec:
    processor = SecurityDecorator(processor)

############################################################
# Observer
############################################################

st.subheader("Observers")

status = OrderStatus()

email_o = EmailObserver()
sms_o = SmsObserver()
log_o = LogObserver()

if st.checkbox("Email Observer"):
    status.attach(email_o)

if st.checkbox("SMS Observer"):
    status.attach(sms_o)

# if st.checkbox("Log Observer"):
#     status.attach(log_o)

############################################################
# PubSub
############################################################

st.subheader("PubSub")

pub_o = PubSubSubscriber()

if st.checkbox("Enable PubSub Subscriber"):
    broker.subscribe("order.events", pub_o)

############################################################
# Execution
############################################################

if st.button("Place Order"):
    placeholder = st.empty()

    facade = OrderFacade(logger, broker)
    output = facade.place(product, processor, discounted_amount, status, placeholder)

    # st.subheader("Final Output")
    # for line in output:
    #     st.success(line)

    st.subheader("Logs")
    if use_log:
        for l in logger.logs:
            st.write(l)
    else:
        st.write("Logging disabled")

    st.subheader("Observer Outputs")
    for m in email_o.messages:
        st.write(m)
    for m in sms_o.messages:
        st.write(m)
    for m in log_o.messages:
        st.write(m)

    st.subheader("PubSub Outputs")
    for m in pub_o.messages:
        st.write(m)
