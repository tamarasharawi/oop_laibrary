import uuid
from datetime import datetime
from itertools import count

class Category:
    def __init__(self, name):
        self.name = name

class Library () : 
    def __init__(self , title , author , price , quantity , category) :
        self.title=title
        self.price=price
        self.author=author
        self.quantity=quantity
        self.category = category

    def add_Books(self, quantity):
        self.quantity += quantity
    
    def remove_Books(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
        else:
            raise ValueError("Insufficient stock")


class Book(Library):
    def __init__(self, title, author, price, quantity, category):
        super().__init__(title, author, price, quantity, category)

class Inventory:
    def __init__(self):
        self.books = []

    def add (self, Book):
        self.books.append(Book)

    def view(self):
        print("Inventory:")
        categories = {}
        for Book in self.books:
            category_name = Book.category.name
            if category_name not in categories:
                categories[category_name] = []
            categories[category_name].append(Book)
        for category_name, books in categories.items():
            print(f"\n{category_name}:")
            for Book in books:
                print(f"{Book} - Stock: {Book.quantity}")
                print(f"Book: {Book['book'].title}, Quantity: {Book['quantity']}")


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, book, quantity):
        self.items.append({"book": book, "quantity": quantity})

    def view_cart(self):
        if not self.items:
            print("Your shopping cart is empty add books pleas ")
        else:
            print("Shopping Cart:")
            for item in self.items:
                print(f"Book: {item['book'].title}, Quantity: {item['quantity']}")

class Order:
    order_counter = count(1)

    def __init__(self, items):
        self.order_id = next(Order.order_counter)
        self.items = items
        self.date_of_purchase = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def __str__(self):
        order_details = f"Order ID: {self.order_id}\nDate of Purchase: {self.date_of_purchase}\nItems Purchased:\n"
        for item in self.items:
            order_details += f"{item['product']} - Quantity: {item['quantity']}\n"
        return order_details

class checkOrder:
    def check(self, cart):
        order = Order(cart.items)
        print("Order successfully ")
        print(order)
        return order


class Report:
    def sales_report(self, orders):
        total_sales = 0
        print("Sales Report:")
        for order in orders:
            for item in order.items:
                total_sales += item['product'].price * item['quantity']
        print(f"Total Sales: ${total_sales}")

    def sales_report(self):
        self.reports.sales_report(self.check_order.orders)


class UI:
    def __init__(self):
        self.inventory = Inventory()
        self.shopping_cart = ShoppingCart()
        self.check_oreder = checkOrder()
        self.reports = Report()

    def menu (self):
        print("\n1. View Inventory")
        print("2. Add Product to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Generate Sales Report")
        print("6. Exit")


    def run(self):
        while True:
            self.menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.inventory.view()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.shopping_cart.view_cart()
            elif choice == "4":
                self.checkout()
            elif choice == "5":
                self.generate_sales_report()    
            elif choice == "6":
                print("Thank you for using the system.")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_to_cart(self):
        title = input("Enter the title of the product: ")
        quantity = int(input("Enter the quantity: "))

        for Book in self.inventory.books:
            if Book.title == title:
                self.shopping_cart.add_to_cart(Book, quantity)
                print("Product added to cart.")
                return
        print("Product not found.")

    def checkout(self):
        if not self.shopping_cart.items:
            print("Your cart is empty.")
            return
        self.check_oreder.checkout(self.shopping_cart)
        self.shopping_cart.items = []    



ui = UI()

fiction_category = Category("Fiction")
non_fiction_category = Category("Non-Fiction")

book1 = Book("Harry", "J.K. Rowling", 25.99, 50, fiction_category)
book2 = Book("Potter", "J.K. Rowling", 25.99, 50, fiction_category)
book3 = Book("Harry Potter", "J.K. Rowling", 25.99, 50, fiction_category)
book4 = Book("Programming", "John Doe", 39.99, 30, non_fiction_category)
book5 = Book("Python Programming", "John Doe", 39.99, 30, non_fiction_category)
ui.inventory.add(book1)
ui.inventory.add(book2)
ui.inventory.add(book3)
ui.inventory.add(book4)
ui.inventory.add(book5)


ui.run()