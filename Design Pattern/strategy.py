import streamlit as st

############################################################
# Strategy interface
############################################################

class DiscountStrategy:
    def apply(self, amount):
        raise NotImplementedError("Must implement apply")

############################################################
# Concrete strategies
############################################################

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
# Context class using strategy
############################################################

class Checkout:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def finalize(self, amount):
        return self.strategy.apply(amount)

############################################################
# Streamlit UI
############################################################

st.title("Strategy Pattern Demo")

amount = st.number_input("Original amount", min_value=1, value=100)

strategy_name = st.selectbox(
    "Choose discount strategy",
    [
        "No Discount",
        "Percentage Discount",
        "Fixed Amount Discount",
        "Buy One Get One"
    ]
)

if strategy_name == "No Discount":
    strategy = NoDiscount()

elif strategy_name == "Percentage Discount":
    percent = st.slider("Percent", 1, 50, 20)
    strategy = PercentageDiscount(percent / 100)

elif strategy_name == "Fixed Amount Discount":
    deduction = st.number_input("Deduction amount", min_value=1, value=10)
    strategy = FixedAmountDiscount(deduction)

elif strategy_name == "Buy One Get One":
    strategy = BuyOneGetOneStrategy()

checkout = Checkout(strategy)

if st.button("Apply Strategy"):
    final_value = checkout.finalize(amount)
    st.success(f"Final amount after strategy: {final_value}")
