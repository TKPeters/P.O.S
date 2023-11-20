from operations import PointOfSaleSystem

def main():
    pos = PointOfSaleSystem()
    pos.load_waiters("Login.txt")
    pos.load_menu("Stock.txt")
    while True:
        print("\n1. Login\n2. Assign Table\n3. Add Customers\n4. Add to Order\n5. Prepare Bill\n6. Complete Sale\n7. Display Total Sales\n8. Clear Total Sales\n9. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            username = input("Enter username: ")
            password = input("Enter password: ")
            waiter = pos.login(username, password)
            if waiter:
                print(f"Welcome, {waiter.username}!")
            else:
                print("Login failed. Please try again.")
        elif choice == 2:
            pos.assign_table(waiter)
        elif choice == 3:
            pos.change_customers(waiter)
        elif choice == 4:
            pos.add_to_order(waiter)
        elif choice == 5:
            pos.prepare_bill(waiter)
        elif choice == 6:
            pos.complete_sale(waiter)
        elif choice == 7:
            pos.display_total_sales()
        elif choice == 8:
            pos.clear_total_sales()
        elif choice == 9:
            print("Thank you for using the Point of Sale System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()