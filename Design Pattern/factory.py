import streamlit as st

# Product interface
class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement pay")

# Concrete products
class CreditCardProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Credit card payment processed for {amount}"

class PayPalProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"PayPal payment processed for {amount}"

class CryptoProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Crypto payment processed for {amount}"

# Factory
class PaymentFactory:
    @staticmethod
    def create_processor(method):
        processors = {
            "Credit Card": CreditCardProcessor,
            "PayPal": PayPalProcessor,
            "Crypto": CryptoProcessor
        }
        return processors[method]()

# Streamlit UI
st.title("Factory Pattern Demo")

method = st.selectbox(
    "Select payment method",
    ["Credit Card", "PayPal", "Crypto"]
)

amount = st.number_input("Amount", min_value=1, value=50)

if st.button("Process Payment"):
    processor = PaymentFactory.create_processor(method)
    result = processor.pay(amount)
    st.success(result)
