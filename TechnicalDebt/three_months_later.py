# payment_handler.py - Version 2.0 (Interest Payments Start)
# INTEREST: Patching problems from the quick implementation

class PaymentProcessor:
   def __init__(self):
       # INTEREST: Now we need to track more state
       self.failed_attempts = {}  # Track failed attempts per card
       self.refund_queue = []     # Manual refund tracking
  
   def process_payment(self, amount, card_number, expiry, cvv, user_email, billing_address):
       """
       INTEREST: Added parameters and complexity because original was too simple
       """
       # INTEREST 1: Fraud detection added as afterthought
       if self.is_suspicious_transaction(amount, card_number, user_email):
           return {"status": "fraud_rejected", "message": "Transaction flagged"}
      
       # INTEREST 2: Rate limiting because we had no security initially
       if self.failed_attempts.get(card_number, 0) > 3:
           return {"status": "error", "message": "Too many failed attempts"}
      
       # INTEREST 3: CVV validation added after security audit
       if not self.validate_cvv(card_number, cvv):
           self.failed_attempts[card_number] = self.failed_attempts.get(card_number, 0) + 1
           return {"status": "error", "message": "Invalid CVV"}
      
       # INTEREST 4: Expiry validation added after customer complaints
       if not self.validate_expiry(expiry):
           return {"status": "error", "message": "Card expired"}
      
       # INTEREST 5: Address verification added for fraud prevention
       if not self.verify_address(billing_address):
           return {"status": "error", "message": "Address verification failed"}

       # The original simple logic, now buried under patches
       if card_number == "4111111111111111":
           return {"status": "success", "transaction_id": "test_123"}
      
       transaction_id = f"tx_{int(time.time())}"

       # INTEREST 6: More complex logging for compliance
       with open("transactions.txt", "a") as f:
           f.write(f"{transaction_id},{amount},{card_number},{user_email},{billing_address}\n")
      
       # INTEREST 7: Email confirmation added after customer requests
       self.send_confirmation_email(user_email, amount, transaction_id)
      
       return {"status": "success", "transaction_id": transaction_id}
  
   # INTEREST: All these methods were added as patches
   def is_suspicious_transaction(self, amount, card_number, email):
       # Quick fraud detection added after actual fraud occurred
       return amount > 1000 or "@temp-mail.org" in email
  
   def validate_cvv(self, card_number, cvv):
       return len(cvv) == 3 and cvv.isdigit()
  
   def validate_expiry(self, expiry):
       return len(expiry) == 5 and "/" in expiry
  
   def verify_address(self, address):
       return len(address) > 10  # Very basic check
  
   def send_confirmation_email(self, email, amount, transaction_id):
       # Quick email integration added after customer complaints
       print(f"Email sent to {email}: Payment of ${amount} confirmed - {transaction_id}")
       # The original simple logic, now buried under patches
       if card_number == "4111111111111111":
           return {"status": "success", "transaction_id": "test_123"}
      
       transaction_id = f"tx_{int(time.time())}"

       # INTEREST 6: More complex logging for compliance
       with open("transactions.txt", "a") as f:
           f.write(f"{transaction_id},{amount},{card_number},{user_email},{billing_address}\n")
      
       # INTEREST 7: Email confirmation added after customer requests
       self.send_confirmation_email(user_email, amount, transaction_id)
      
       return {"status": "success", "transaction_id": transaction_id}
  
   # INTEREST: All these methods were added as patches
   def is_suspicious_transaction(self, amount, card_number, email):
       # Quick fraud detection added after actual fraud occurred
       return amount > 1000 or "@temp-mail.org" in email
  
   def validate_cvv(self, card_number, cvv):
       return len(cvv) == 3 and cvv.isdigit()
  
   def validate_expiry(self, expiry):
       return len(expiry) == 5 and "/" in expiry
  
   def verify_address(self, address):
       return len(address) > 10  # Very basic check
  
   def send_confirmation_email(self, email, amount, transaction_id):
       # Quick email integration added after customer complaints
       print(f"Email sent to {email}: Payment of ${amount} confirmed - {transaction_id}")
