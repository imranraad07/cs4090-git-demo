// File: PaymentSystem.java

// 1. Abstraction: Abstract class defines what "payment" means
abstract class PaymentMethod {
    public abstract void processPayment(double amount);
}

// 2. Inheritance: Concrete classes extend the abstract class
class CreditCardPayment extends PaymentMethod {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processed $" + amount + " using Credit Card.");
    }
}

class PayPalPayment extends PaymentMethod {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processed $" + amount + " using PayPal.");
    }
}

// 3. Encapsulation: Wallet hides its balance using private access
class Wallet {
    private double balance;  // This field is encapsulated

    public Wallet(double initialBalance) {
        this.balance = initialBalance;
    }

    public double getBalance() {
        return balance;
    }

    public boolean deduct(double amount) {
        if (amount > balance) {
            System.out.println("Insufficient funds.");
            return false;
        }
        balance -= amount;
        return true;
    }
}

// 4. Polymorphism: Accepts any payment method (CreditCard or PayPal)
class PaymentProcessor {
    public void makePayment(PaymentMethod method, double amount) {
        method.processPayment(amount);  // Polymorphic call
    }
}

// Application entry point
public class PaymentSystem {
    public static void main(String[] args) {
        // Set up
        Wallet userWallet = new Wallet(500.0);
        PaymentProcessor processor = new PaymentProcessor();

        // Example 1: Use Credit Card
        if (userWallet.deduct(100.0)) {
            processor.makePayment(new CreditCardPayment(), 100.0);
        }

        // Example 2: Use PayPal
        if (userWallet.deduct(200.0)) {
            processor.makePayment(new PayPalPayment(), 200.0);
        }

        // Final Wallet Balance (uses encapsulation to read safely)
        System.out.println("Remaining Wallet Balance: $" + userWallet.getBalance());
    }
}
