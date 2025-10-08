# payment_service.py - Refactored Version (Debt Repayment)
# After months of pain, we finally refactor properly

from abc import ABC, abstractmethod
import datetime

# Proper abstraction and separation of concerns
class PaymentGateway(ABC):
   @abstractmethod
   def process_payment(self, payment_request): pass

class ValidationService:
   def validate_payment(self, payment_request):
       # Single responsibility: validation only
       pass

class FraudDetectionService:
   def check_for_fraud(self, payment_request):
       # Single responsibility: fraud detection
       pass

class TaxCalculationService:
   def calculate_tax(self, payment_request):
       # Single responsibility: tax calculations
       pass

class AnalyticsService:
   def track_payment(self, payment_request, result):
       # Single responsibility: analytics
       pass

# Clean, focused payment processor
class CleanPaymentProcessor:
   def __init__(self):
       self.validation = ValidationService()
       self.fraud_detection = FraudDetectionService()
       self.tax_calculator = TaxCalculationService()
       self.analytics = AnalyticsService()
       self.gateway = StripeGateway()  # Proper dependency injection

   def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
       """
       Clean, readable, maintainable code
       Each concern is separated into its own service
       """
       # Validate input
       validation_result = self.validation.validate_payment(payment_request)
       if not validation_result.is_valid:
           return PaymentResult.error(validation_result.errors)
      
       # Check for fraud
       fraud_result = self.fraud_detection.check_for_fraud(payment_request)
       if fraud_result.is_fraud:
           return PaymentResult.fraud_detected(fraud_result.reason)
       # Calculate tax
       tax_info = self.tax_calculator.calculate_tax(payment_request)
       # Process payment
       gateway_result = self.gateway.process_payment(payment_request, tax_info)
       # Track analytics
       self.analytics.track_payment(payment_request, gateway_result)
      
       return gateway_result

# Data transfer objects for clear contracts
@dataclass
class PaymentRequest:
   amount: Decimal
   currency: str
   card_token: str  # Never store raw card numbers!
   customer_email: str
   billing_address: Address
   product_type: str
   vat_number: Optional[str]
@dataclass
class PaymentResult:
   status: str
   transaction_id: str
   error_message: Optional[str]
   tax_amount: Decimal
