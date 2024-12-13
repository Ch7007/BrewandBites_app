from dal import DataAccessLayer
from datetime import datetime
import hashlib

class BusinessLogic:
    def __init__(self):
        self.dal = DataAccessLayer()

    # User Management
    def register_user(self, username, password, email, role):
        if not username or not password or not email:
            print("Error: All fields are required.")
            return
        if role not in ['admin', 'user']:
            print("Error: Role must be 'admin' or 'user'.")
            return
        self.dal.add_user(username, password, email, role)

    def update_user_info(self, user_id, updates):
        if not updates:
            print("Error: No updates provided.")
            return
        self.dal.update_user(user_id, updates)

    def view_all_users(self):
        """Retrieve all registered users with their ID, username, email, and role."""
        return self.dal.get_all_users()

    def delete_user(self, user_id):
        self.dal.delete_user(user_id)

    def authenticate_user(self, username, password):
        user = self.dal.get_user_by_username(username)
        if not user:
            print("Error: User not found.")
            return None
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.password == hashed_password:
            print("Authentication successful.")
            return user
        else:
            print("Error: Incorrect password.")
            return None

    # Expense Management
    def record_expense(self, date, amount, category, description=None):
        if not date or not amount or not category:
            print("Error: Date, amount, and category are required.")
            return
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return
        if amount <= 0:
            print("Error: Amount must be greater than zero.")
            return
        self.dal.add_expense(parsed_date, amount, category, description)

    def view_expense_history(self):
        expenses = self.dal.get_expense_history()
        return [{"date": e.date, "amount": e.amount, "category": e.category, "description": e.description} for e in expenses]

    # Inventory Management
    def add_inventory_item(self, item_name, quantity, cost):
        if not item_name or quantity is None or cost is None:
            print("Error: Item name, quantity, and cost are required.")
            return
        if quantity < 0 or cost < 0:
            print("Error: Quantity and cost must be non-negative.")
            return
        self.dal.add_inventory_item(item_name, quantity, cost)

    def update_inventory_item(self, item_id, updates):
        if not updates:
            print("Error: No updates provided.")
            return
        self.dal.update_inventory_item(item_id, updates)

    def delete_inventory_item(self, item_id):
        self.dal.delete_inventory_item(item_id)

    def view_inventory(self):
        inventory = self.dal.get_inventory()
        return [{"id": inv.id, "item_name": inv.item_name, "quantity": inv.quantity, "cost": inv.cost} for inv in inventory]

    def purchase_item(self, item_id, quantity):
        """Handle purchasing an inventory item."""
        item = self.dal.get_inventory_item(item_id)
        if not item:
            print("Error: Item not found.")
            return

        if quantity > item.quantity:
            print("Error: Not enough stock available.")
            return

        total_amount = item.cost * quantity
        print(f"Total amount to pay: {total_amount:.2f}")
        payment_done = input("Is payment done? (yes/no): ").strip().lower()

        if payment_done == "yes":
            new_quantity = item.quantity - quantity
            self.dal.update_inventory_quantity(item_id, new_quantity)
            today = datetime.now().strftime("%Y-%m-%d")
            items_sold = f"{item.item_name} x {quantity}"
            self.record_sale(today, total_amount, items_sold)
            print("Purchase complete.")
        else:
            print("Purchase not done.")

    # Sales Management
    def record_sale(self, date, amount, items_sold):
        if not date or not amount or not items_sold:
            print("Error: Date, amount, and items sold are required.")
            return
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return
        if amount <= 0:
            print("Error: Amount must be greater than zero.")
            return
        self.dal.add_sale(parsed_date, amount, items_sold)

    def view_sales_history(self):
        sales = self.dal.get_sales_history()
        return [{"date": s.date, "amount": s.amount, "items_sold": s.items_sold} for s in sales]

    # Reporting
    def generate_reports(self):
        """Generate and return structured reports."""
        return {
            "Expenses": self.dal.generate_expense_report(),
            "Inventory": self.dal.generate_inventory_report(),
            "Sales": self.dal.generate_sales_report(),
        }

