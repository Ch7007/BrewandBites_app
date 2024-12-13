import hashlib
from bll import BusinessLogic

class PresentationLayer:
    def __init__(self):
        self.bll = BusinessLogic()
        self.current_user = None

    def login(self):
        print("\n--- Login ---")
        username = input("Username: ")
        password = input("Password: ")
        user = self.bll.authenticate_user(username, password)
        if user:
            self.current_user = user
            print(f"Welcome, {self.current_user.username}!")
        else:
            print("Login failed.")

    def admin_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. Manage Users")
            print("2. Generate Reports")
            print("3. Manage Expenses")
            print("4. Manage Inventory")
            print("5. Record Sales (Manual)")
            print("6. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.manage_users()
            elif choice == "2":
                self.generate_reports()
            elif choice == "3":
                self.manage_expenses()
            elif choice == "4":
                self.manage_inventory()
            elif choice == "5":
                self.record_sales()
            elif choice == "6":
                self.current_user = None
                break
            else:
                print("Invalid choice. Try again.")

    def user_menu(self):
        while True:
            print("\n--- User Menu ---")
            print("1. View Available items")
            print("2. Purchase Items")
            print("3. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                inventory = self.bll.view_inventory()
                if not inventory:
                    print("\n--- Available Items ---\n")
                    print("No items available at the moment.")
                else:
                    print("\n\n--- Available Items ---\n")

                    # Define column headers
                    headers = ["ID", "Item Name", "Available Quantity", "Cost"]

                    # Calculate column widths dynamically
                    column_widths = {
                        "ID": max(len("ID"), max(len(str(item['id'])) for item in inventory)),
                        "Item Name": max(len("Item Name"), max(len(item['item_name']) for item in inventory)),
                        "Available Quantity": max(len("Available Quantity"),
                                                  max(len(str(item['quantity'])) for item in inventory)),
                        "Cost": max(len("Cost"), max(len(f"{item['cost']:.2f}") for item in inventory))
                    }

                    # Create a formatted header row
                    header_row = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
                    separator = "-+-".join("-" * column_widths[header] for header in headers)

                    # Print the header and separator
                    print(header_row)
                    print(separator)

                    # Print each inventory item
                    for item in inventory:
                        row = f"{item['id']:<{column_widths['ID']}} | " \
                              f"{item['item_name']:<{column_widths['Item Name']}} | " \
                              f"{item['quantity']:<{column_widths['Available Quantity']}} | " \
                              f"{item['cost']:<{column_widths['Cost']}.2f}"
                        print(row)
            elif choice == "2":
                self.purchase_item()
            elif choice == "3":
                self.current_user = None
                break
            else:
                print("Invalid choice. Try again.")

    def manage_users(self):
        while True:
            print("\n--- Manage Users ---")
            print("1. Register User")
            print("2. View All Registered Users")
            print("3. Update User Info")
            print("4. Delete User")
            print("5. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                username = input("Username: ")
                password = hashlib.sha256(input("Password: ").encode()).hexdigest()
                email = self.input_email()
                role = input("Role (admin/user): ")
                self.bll.register_user(username, password, email, role)
            elif choice == "2":
                users = self.bll.view_all_users()
                print("\n--- Registered Users ---")
                for user in users:
                    print(f"ID: {user['id']} | Username: {user['username']} | Email: {user['email']} | Role: {user['role']}")
            elif choice == "3":
                user_id = int(input("User ID: "))
                updates = {}
                username = input("New Username (leave blank to skip): ")
                if username:
                    updates["username"] = username
                email = self.input_email()
                if email:
                    updates["email"] = email
                password = hashlib.sha256(input("\nNote: Must provide new password otherwise it will be a null value (Just press enter while logging in)\n\nNew Password: ").encode()).hexdigest()
                if password:
                    updates["password"] = password
                self.bll.update_user_info(user_id, updates)
            elif choice == "4":
                user_id = int(input("User ID: "))
                self.bll.delete_user(user_id)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")

    def manage_expenses(self):
        while True:
            print("\n--- Manage Expenses ---")
            print("1. Record Expense")
            print("2. View Expense History")
            print("3. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                date = input("Date (YYYY-MM-DD): ")
                amount = float(input("Amount: "))
                category = input("Category: ")
                description = input("Description (optional): ")
                self.bll.record_expense(date, amount, category, description)
            elif choice == "2":
                expenses = self.bll.view_expense_history()
                print("\n--- Expense History ---")
                for expense in expenses:
                    print(f"Date: {expense['date']} | Amount: {expense['amount']} | Category: {expense['category']} | Description: {expense['description']}")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Try again.")

    def manage_inventory(self):
        while True:
            print("\n--- Manage Inventory ---")
            print("1. Add Inventory Item")
            print("2. Update Inventory Item")
            print("3. Delete Inventory Item")
            print("4. View Inventory")
            print("5. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                item_name = input("Item Name: ")
                quantity = int(input("Quantity: "))
                cost = float(input("Cost: "))
                self.bll.add_inventory_item(item_name, quantity, cost)
            elif choice == "2":
                item_id = int(input("Item ID: "))
                updates = {}
                item_name = input("New Item Name (leave blank to skip): ")
                if item_name:
                    updates["item_name"] = item_name
                quantity = input("New Quantity (leave blank to skip): ")
                if quantity:
                    updates["quantity"] = int(quantity)
                cost = input("New Cost (leave blank to skip): ")
                if cost:
                    updates["cost"] = float(cost)
                self.bll.update_inventory_item(item_id, updates)
            elif choice == "3":
                item_id = int(input("Item ID: "))
                self.bll.delete_inventory_item(item_id)
            elif choice == "4":
                inventory = self.bll.view_inventory()
                print("\n--- Inventory ---")
                for item in inventory:
                    print(f"ID: {item['id']} | Item Name: {item['item_name']} | Available Quantity: {item['quantity']} | Cost: {item['cost']}")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")

    def purchase_item(self):
        """Handle the purchase process for the user."""
        print("\n--- Purchase Item ---")
        item_id = int(input("Enter the ID of the item to purchase (Check ID from Available Items): "))
        quantity = int(input("Enter the quantity to purchase: "))
        self.bll.purchase_item(item_id, quantity)

    @staticmethod
    def input_email():
        while True:
            email = input("Email: ")

            # Basic email format validation
            if (
                    email.count("@") == 1 and
                    email.count(".") >= 1 and
                    len(email.split("@")[0]) > 0 and  # Part before @ must not be empty
                    len(email.split("@")[1]) > 0 and  # Part after @ must not be empty
                    "." in email.split("@")[1] and  # Domain part must contain '.'
                    not email.endswith(".") and  # Email must not end with '.'
                    not email.startswith("@")  # Email must not start with '@'
            ):
                return email
            else:
                print("❌ Invalid email format. Please enter a valid email (e.g., user@example.com).")

    def record_sales(self):
        print("\n--- Record Sales ---")
        date = input("Date (YYYY-MM-DD): ")
        amount = float(input("Amount: "))
        items_sold = input("Items Sold: ")
        self.bll.record_sale(date, amount, items_sold)

    def generate_reports(self):
        """Display structured reports in a readable format."""
        print("\n=== Reports ===")
        reports = self.bll.generate_reports()

        for report_type, data in reports.items():
            print(f"\n--- {report_type} Report ---")
            if not data:
                print("No data available.")
                continue

            # Extract headers from the first record
            headers = data[0].keys()
            column_widths = {header: max(len(header), max(len(str(row[header])) for row in data)) for header in headers}

            # Print the header row
            header_row = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
            separator = "-+-".join("-" * column_widths[header] for header in headers)
            print(header_row)
            print(separator)

            # Print each row of the report
            for row in data:
                row_data = " | ".join(f"{str(value):<{column_widths[key]}}" for key, value in row.items())
                print(row_data)

    def start(self):
        print("\nWelcome to Brew and Bite Café Management System!")
        while True:
            self.login()
            if self.current_user:
                if self.current_user.role == 'admin':
                    self.admin_menu()
                else:
                    self.user_menu()
            else:
                print("Goodbye!")
                break


if __name__ == "__main__":

    app = PresentationLayer()
    app.start()
