class PaymentProcessor:
   def __init__(self):
       self.failed_attempts = {}
       self.refund_queue = []
       # COMPOUND INTEREST: More state to manage
       self.currency_rates = self.load_currency_rates()  # Added for international
       self.tax_calculations = TaxCalculator()  # Added for compliance
       self.analytics = AnalyticsTracker()  # Added for business intelligence
   def process_payment(self, amount, card_number, expiry, cvv, user_email,
                      billing_address, currency="USD", product_type="digital",
                      customer_vat_number=None, shipping_country=None):
"""
COMPOUND INTEREST: Method now has 10 parameters and does 15 different things
Every new feature makes the code more fragile
"""
       # COMPOUND INTEREST 1: International support hacked in
       if currency != "USD":
           amount = self.convert_currency(amount, currency, "USD")
           if not amount:
               return {"status": "error", "message": "Currency conversion failed"}
       # COMPOUND INTEREST 2: Tax calculation patched in
       tax_amount = self.tax_calculations.calculate_tax(
           amount, product_type, shipping_country, customer_vat_number
       )
       total_amount = amount + tax_amount
      
       # COMPOUND INTEREST 3: Business analytics added
       self.analytics.track_payment_attempt(
           user_email, total_amount, product_type
       )
       # All the previous validations (now even more complex)
       if self.is_suspicious_transaction(total_amount, card_number, user_email, shipping_country):
           self.analytics.track_fraud_attempt(user_email, total_amount)
           return {"status": "fraud_rejected", "message": "Transaction flagged"}

       # ... 50 more lines of validation and business logic ...
       # The actual payment processing is now a small part of this method
       transaction_id = f"tx_{int(time.time())}"
       # COMPOUND INTEREST 4: Database migration started but not completed
       try:
           # New database code mixed with old file-based approach
           self.save_to_database(transaction_id, total_amount, card_number,
                               user_email, billing_address, currency, tax_amount)
       except Exception as e:
           # Fallback to old file system - debt creates more debt!
           with open("transactions.txt", "a") as f:
               f.write(f"{transaction_id},{total_amount},{card_number},ERROR:{str(e)}\n")
       # COMPOUND INTEREST 5: Multiple notification systems
       self.send_confirmation_email(user_email, total_amount, transaction_id)
       self.send_slack_notification(f"New payment: ${total_amount}")
       self.update_customer_dashboard(user_email, transaction_id)
      
       return {"status": "success", "transaction_id": transaction_id, "tax_amount": tax_amount}

# COMPOUND INTEREST: Supporting classes that grew organically
class TaxCalculator:
   """Added when we expanded to EU - complex rules hacked into simple system"""
   def calculate_tax(self, amount, product_type, country, vat_number):
       # Complex tax logic that should be in a separate service
       if country == "DE" and product_type == "physical":
           return amount * 0.19  # German VAT
       elif country == "FR" and product_type == "digital":
           return amount * 0.20  # French VAT
       # ... 10 more country rules ...
       return 0

class AnalyticsTracker:
   """Added when marketing wanted more data"""
   def track_payment_attempt(self, email, amount, product_type):
       # Mixed concerns: payment processing shouldn't handle analytics
       print(f"Analytics: {email} attempted ${amount} for {product_type}")
