class PaymentProcessor:
   def process_payment(self, amount, card_number, expiry, cvv):
       """
       Quick and dirty payment processing
       KNOWN DEBT: No validation, no error handling, hardcoded logic
       BUSINESS REASON: Investor demo in 2 weeks
       """
       # Debt Item 1: Hardcoded test credentials
       if card_number == "4111111111111111":  # Test card
           return {"status": "success", "transaction_id": "test_123"}
      
       # Debt Item 2: Simple length validation only
       if len(card_number) != 16:
           return {"status": "error", "message": "Invalid card"}
      
       # Debt Item 3: No actual payment gateway integration
       # Using a mock for demo purposes
       transaction_id = f"tx_{int(time.time())}"
      
       # Debt Item 4: Writing to a simple file instead of database
       with open("transactions.txt", "a") as f:
           f.write(f"{transaction_id},{amount},{card_number}\n")
      
       return {"status": "success", "transaction_id": transaction_id}
