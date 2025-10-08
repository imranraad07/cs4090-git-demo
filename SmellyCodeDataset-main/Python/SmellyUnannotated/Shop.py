"""
Copyright (c) 2025 Ahmed R. Sadik, Honda Research Institute Europe GmbH 

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree. This dataset contains smelly code for research and refactoring purposes.
"""


from Cashier import Cashier
from Chef import Chef
from Pizza import Pizza, CheesePizza, VeggiePizza, TunaPizza, PepperoniPizza

class Shop:
    def __init__(self):
        self.chef = Chef()
        self.casher = Cashier(self.chef)
        self.pizza = None
        self.frequent_customer_discount = False
        self.first_name = None
        self.last_name = None
        self.address = None
        self.phone_number = None
        self.email = None
        self.temp_discount_code = None
        self.temp_order_note = None

    def create_pizza(self, pizza_type: str) -> Pizza:
        if pizza_type == "Cheese":
            return CheesePizza()
        elif pizza_type == "Veggie":
            return VeggiePizza()
        elif pizza_type == "Tuna":
            return TunaPizza()
        elif pizza_type == "Pepperoni":
            return PepperoniPizza()
        else:
            raise ValueError("Unknown pizza type")

    def receive_order(self, pizza_type: str):
        print(f"Pizza Shop received order for {pizza_type} pizza.")
        self.pizza = self.create_pizza(pizza_type)
        self.casher.take_order(pizza_type)

    def update_contact_info(self, first_name, last_name, address, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def update_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def update_address(self, address):
        self.address = address

    def update_phone_number(self, phone_number):
        self.phone_number = phone_number

    def update_email(self, email):
        self.email = email

    def notify_for_promotion(self):
        print("Notifying customer for promotion")

    def notify_for_discount(self):
        print("Notifying customer for discount")

    def notify_for_new_arrivals(self):
        print("Notifying customer for new arrivals")

    def apply_discount(self):
        print("Applying discount for customer")

    def apply_loyalty_points(self):
        print("Applying loyalty points for customer")

    def handle_complaint(self, complaint):
        if complaint == "cold pizza":
            self.casher.calm_customer_down()
        elif complaint == "late delivery":
            self.casher.calm_customer_down()
        elif complaint == "wrong order":
            self.casher.calm_customer_down()
        else:
            self.casher.calm_customer_down()

    def ask_for_receipt(self):
        print("Customer is asking for a receipt.")

    def another_unused_method(self):
        pass

    def yet_another_unused_method(self):
        pass

    def chain_of_methods(self):
        print("Shop is initiating a message chain")
        self.casher.chef.clean_kitchen()

    def middleman_method(self):
        print("Shop is calling a middleman method")
        self.middle_method()

    def middle_method(self):
        print("Middleman method delegating to another method")
        self.real_method()

    def real_method(self):
        print("Real method doing the actual work")

    def access_internal_details(self):
        print(f"Accessing internal details: {self.casher.chef.busy}")

    def long_method(self):
        print("Shop is handling many tasks in a single method")
        self.update_contact_info("John", "Doe", "123 Street", "555-5555", "john.doe@example.com")
        self.update_name("John", "Doe")
        self.update_address("123 Street")
        self.update_phone_number("555-5555")
        self.update_email("john.doe@example.com")
        self.notify_for_promotion()
        self.notify_for_discount()
        self.notify_for_new_arrivals()
        self.apply_discount()
        self.apply_loyalty_points()
        self.handle_complaint("cold pizza")
        self.ask_for_receipt()
        self.chain_of_methods()
        self.middleman_method()
        self.access_internal_details()

    def order_with_unnecessary_details(self):
        print("Shop is placing a detailed order")
        self.receive_order("Veggie")
        self.update_contact_info("John", "Doe", "123 Street", "555-5555", "john.doe@example.com")
        self.apply_discount()
        self.apply_loyalty_points()
