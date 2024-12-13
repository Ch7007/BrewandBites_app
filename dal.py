from models import User, Expense, Inventory, Sale, init_db, get_session
from sqlalchemy.exc import IntegrityError

# Data Access Layer
class DataAccessLayer:
    engine = init_db('sqlite:///cafe_management.db')
    def __init__(self):
        self.session = get_session(self.engine)

    # User Management
    def add_user(self, username, password, email, role):
        try:
            new_user = User(username=username, password=password, email=email, role=role)
            self.session.add(new_user)
            self.session.commit()
            print(f"User '{username}' added successfully.")
        except IntegrityError:
            self.session.rollback()
            print(f"Error: Username or email already exists.")

    def update_user(self, user_id, updates):
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.session.commit()
        print(f"User ID {user_id} updated successfully.")

    def get_all_users(self):
        """Fetch all users with their ID, username, email, and role."""
        users = self.session.query(User).all()
        return [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]

    def delete_user(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        self.session.delete(user)
        self.session.commit()
        print(f"User ID {user_id} deleted successfully.")

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    # Expense Management
    def add_expense(self, date, amount, category, description):
        expense = Expense(date=date, amount=amount, category=category, description=description)
        self.session.add(expense)
        self.session.commit()
        print("Expense added successfully.")

    def get_expense_history(self):
        return self.session.query(Expense).all()

    # Inventory Management
    def add_inventory_item(self, item_name, quantity, cost):
        try:
            inventory_item = Inventory(item_name=item_name, quantity=quantity, cost=cost)
            self.session.add(inventory_item)
            self.session.commit()
            print(f"Inventory item '{item_name}' added successfully.")
        except IntegrityError:
            self.session.rollback()
            print(f"Error: Inventory item '{item_name}' already exists.")

    def update_inventory_item(self, item_id, updates):
        item = self.session.query(Inventory).filter_by(id=item_id).first()
        if not item:
            print(f"Inventory item with ID {item_id} not found.")
            return
        for key, value in updates.items():
            if hasattr(item, key):
                setattr(item, key, value)
        self.session.commit()
        print(f"Inventory item ID {item_id} updated successfully.")

    def delete_inventory_item(self, item_id):
        item = self.session.query(Inventory).filter_by(id=item_id).first()
        if not item:
            print(f"Inventory item with ID {item_id} not found.")
            return
        self.session.delete(item)
        self.session.commit()
        print(f"Inventory item ID {item_id} deleted successfully.")

    def get_inventory(self):
        return self.session.query(Inventory).all()

    def get_inventory_item(self, item_id):
        """Fetch item details from the inventory by ID."""
        item = self.session.query(Inventory).filter_by(id=item_id).first()
        return item

    def update_inventory_quantity(self, item_id, new_quantity):
        """Update the quantity of an inventory item."""
        item = self.session.query(Inventory).filter_by(id=item_id).first()
        if item:
            item.quantity = new_quantity
            self.session.commit()
            print("Inventory updated successfully.")
        else:
            print("Error: Item not found.")

    # Sales Management
    def add_sale(self, date, amount, items_sold):
        sale = Sale(date=date, amount=amount, items_sold=items_sold)
        self.session.add(sale)
        self.session.commit()
        print("Sale recorded successfully.")

    def get_sales_history(self):
        return self.session.query(Sale).all()

    # Reporting
    def generate_expense_report(self):
        """Fetch and structure expense data."""
        expenses = self.session.query(Expense).all()
        return [
            {
                "Date": exp.date.strftime("%Y-%m-%d"),
                "Amount": f"{exp.amount:.2f}",
                "Category": exp.category,
                "Description": exp.description,
            }
            for exp in expenses
        ]

    def generate_inventory_report(self):
        """Fetch and structure inventory data."""
        inventory = self.session.query(Inventory).all()
        return [
            {
                "Item Name": inv.item_name,
                "Quantity": inv.quantity,
                "Cost": f"{inv.cost:.2f}",
            }
            for inv in inventory
        ]

    def generate_sales_report(self):
        """Fetch and structure sales data."""
        sales = self.session.query(Sale).all()
        return [
            {
                "Date": sale.date.strftime("%Y-%m-%d"),
                "Amount": f"{sale.amount:.2f}",
                "Items Sold": sale.items_sold,
            }
            for sale in sales
        ]

