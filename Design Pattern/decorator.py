import streamlit as st

############################################################
# Base interface
############################################################

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Must implement pay")

############################################################
# Concrete component
############################################################

class BasicProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Processed payment of {amount}"

############################################################
# Decorator base class
############################################################

class PaymentDecorator(PaymentProcessor):
    def __init__(self, processor):
        self.processor = processor

    def pay(self, amount):
        return self.processor.pay(amount)

############################################################
# Concrete decorators
############################################################

class LoggingDecorator(PaymentDecorator):
    def __init__(self, processor, logger_list):
        super().__init__(processor)
        self.logger_list = logger_list

    def pay(self, amount):
        result = self.processor.pay(amount)
        self.logger_list.append(f"LOG: Payment of {amount} completed")
        return result + " (logged)"

class TaxDecorator(PaymentDecorator):
    def __init__(self, processor, rate):
        super().__init__(processor)
        self.rate = rate

    def pay(self, amount):
        total = amount + (amount * self.rate)
        return self.processor.pay(total) + f" with tax applied, total {total}"

class SecurityDecorator(PaymentDecorator):
    def pay(self, amount):
        return "Security check passed. " + self.processor.pay(amount)

############################################################
# Streamlit UI
############################################################

st.title("Decorator Pattern Demo")

amount = st.number_input("Amount", min_value=1, value=50)
apply_logging = st.checkbox("Add logging decorator")
apply_tax = st.checkbox("Add tax decorator")
apply_security = st.checkbox("Add security decorator")

log_list = []

if st.button("Process Payment"):
    processor = BasicProcessor()

    if apply_logging:
        processor = LoggingDecorator(processor, log_list)

    if apply_tax:
        processor = TaxDecorator(processor, rate=0.1)

    if apply_security:
        processor = SecurityDecorator(processor)

    output = processor.pay(amount)
    st.success(output)

if log_list:
    st.subheader("Logs")
    for line in log_list:
        st.write(line)
