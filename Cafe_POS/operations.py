class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        item = MenuItem(name, price)
        self.items.append(item)

    def get_item_price(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item.price
        return 0


class Sale:
    def __init__(self):
        self.total_sales = 0

    def add_sale(self, amount):
        self.total_sales += amount

    def get_total_sales(self):
        return self.total_sales

    def clear_total_sales(self):
        self.total_sales = 0


class Table:
    def __init__(self, number):
        self.number = number
        self.waiter = None
        self.customers = 0
        self.orders = []

    def add_customers(self, count):
        self.customers = count

    def add_order(self, item, quantity):
        self.orders.append((item, quantity))

    def prepare_bill(self, menu):
        if len(self.orders) == 0:
            return ''
        bill = f"The bill for table {self.number}\n"
        bill += "\n{:25s}{:20s}{:10s}".format("Item", "Quantity", "Price")
        total_amount = 0
        for item, quantity in self.orders:
            price = menu.get_item_price(item)
            amount = price * quantity
            bill += "\n{:25s}{:20d}R{:>10.2f}".format(item, quantity, amount)
            total_amount += amount
        bill += f"\n\nThe total of your order was R {total_amount}\n"
        bill += f"\nYou were helped by {self.waiter}\n"
        return bill


class PointOfSaleSystem:
    def __init__(self):
        self.waiters = []
        self.tables = {}
        self.sales = Sale()
        self.menu = Menu()

    def load_waiters(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(',')
                waiter = User(username, password)
                self.waiters.append(waiter)

    def load_menu(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name, price = line.strip().split(',')
                self.menu.add_item(name, float(price))

    def login(self, username, password):
        for waiter in self.waiters:
            if waiter.username == username and waiter.password == password:
                return waiter
        print("Invalid username or password.")
        return None

    def assign_table(self, waiter):
        print("Please select one of the available tables or press 0 to exit")
        for number, table in self.tables.items():
            if table.waiter is None:
                print(f"{number}. Table {number}")
        table_number = int(input())
        if table_number == 0:
            return
        if table_number not in self.tables:
            table = Table(table_number)
            self.tables[table_number] = table
        else:
            table = self.tables[table_number]
        if table.waiter is not None:
            print("This table is already assigned to a waiter.")
        else:
            table.waiter = waiter
            add_customers = input("Do you want to add customers to the table? (y/n): ")
            if add_customers.lower() == 'y':
                self.change_customers(waiter)

    def change_customers(self, waiter):
        print("Select table to assign customers or 0 to exit")
        for number, table in self.tables.items():
            if table.waiter == waiter:
                print(f"{number}. Table {number}")
        table_number = int(input())
        if table_number == 0:
            return
        table = self.tables.get(table_number)
        if table is None:
            print("Invalid table number.")
        elif table.waiter != waiter:
            print("This table is not assigned to you.")
        else:
            customer_count = int(input(f"How many customers are seated at Table {table_number}? "))
            table.add_customers(customer_count)

    def add_to_order(self, waiter):
        print("Select a table to add orders to:")
        for number, table in self.tables.items():
            if table.waiter == waiter:
                print(f"{number}. Table {number}")
        table_number = int(input("Please select a table or 0 to exit: "))
        if table_number == 0:
            return
        table = self.tables.get(table_number)
        if table is None:
            print("Invalid table number.")
        elif table.waiter != waiter:
            print("This table is not assigned to you.")
        else:
            while True:
                print("\nSelect an item from the list to add to the order\n")
                self.menu.display_menu_items()
                choice = int(input("Choose an item to add: "))
                if choice < 1 or choice > len(self.menu.items):
                    print("Invalid choice. Please try again.\n")
                    continue
                item_name = self.menu.items[choice - 1]
                quantity = int(input("How many items do you want to add? "))
                table.add_order(item_name, quantity)
                add_more = input("Add another item? (y/n): ")
                if add_more.lower() != 'y':
                    break

    def prepare_bill(self, waiter):
        print("Select a table:")
        for number, table in self.tables.items():
            if table.waiter == waiter:
                print(f"{number}. Table {number}")
        table_number = int(input("Select table or type 0 to exit: "))
        if table_number == 0:
            return
        table = self.tables.get(table_number)
        if table is None:
            print("Invalid table number.")
        elif table.waiter != waiter:
            print("This table is not assigned to you.")
        else:
            bill = table.prepare_bill(self.menu)
            if bill:
                print("-" * 76)
                print(bill)
                print("-" * 76)

    def complete_sale(self, waiter):
        print("Please Select table:")
        for number, table in self.tables.items():
            if table.waiter == waiter:
                print(f"{number}. Table {number}")
        table_number = int(input("Select table or press 0 to cancel: "))
        if table_number == 0:
            return
        table = self.tables.get(table_number)
        if table is None:
            print("Invalid table number.")
        elif table.waiter != waiter:
            print("This table is not assigned to you.")
        else:
            if len(table.orders) == 0:
                print("Please prepare bill before completing sale")
            else:
                filename = input("Enter a filename: ")
                with open(filename, 'w') as file:
                    file.write(table.prepare_bill(self.menu))
                total_amount = 0
                for item, quantity in table.orders:
                    price = self.menu.get_item_price(item)
                    total_amount += price * quantity
                self.sales.add_sale(total_amount)
                table.orders = []
                table.waiter = None
                table.customers = 0
                print("Sale completed successfully.")

    def display_total_sales(self):
        total_sales = self.sales.get_total_sales()
        print(f"The total sales is R {total_sales}")

    def clear_total_sales(self):
        self.sales.clear_total_sales()
        print("Total sales cleared.")