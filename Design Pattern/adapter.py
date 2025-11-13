import streamlit as st

############################################################
# Existing system interface
############################################################

class StandardPayment:
    def pay(self, amount):
        raise NotImplementedError("Must implement pay")

############################################################
# Existing implementations
############################################################

class StripePayment(StandardPayment):
    def pay(self, amount):
        return f"Stripe processed {amount}"

class SquarePayment(StandardPayment):
    def pay(self, amount):
        return f"Square processed {amount}"

############################################################
# Third party class with incompatible interface
############################################################

class LegacyBankAPI:
    def send_payment(self, value):
        return f"Legacy Bank transferred {value}"

############################################################
# Adapter
############################################################

class LegacyBankAdapter(StandardPayment):
    def __init__(self, legacy_api):
        self.legacy_api = legacy_api

    def pay(self, amount):
        return self.legacy_api.send_payment(amount)

############################################################
# Factory for convenience (optional)
############################################################

class PaymentFactory:
    @staticmethod
    def get_processor(name):
        if name == "Stripe":
            return StripePayment()
        if name == "Square":
            return SquarePayment()
        if name == "Legacy Bank Through Adapter":
            return LegacyBankAdapter(LegacyBankAPI())
        raise ValueError("Unknown processor")

############################################################
# Streamlit UI
############################################################

st.title("Adapter Pattern Demo")

st.write("This demo shows how an adapter wraps a legacy API to provide a compatible payment interface.")

processor_name = st.selectbox(
    "Select payment processor",
    ["Stripe", "Square", "Legacy Bank Through Adapter"]
)

amount = st.number_input("Amount", min_value=1, value=100)

if st.button("Process Payment"):
    processor = PaymentFactory.get_processor(processor_name)
    result = processor.pay(amount)
    st.success(result)
