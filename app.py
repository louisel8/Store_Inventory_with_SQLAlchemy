from models import engine, Base
import app_func
from sqlalchemy.orm import sessionmaker, Session
from models import Product


def menu():
    while True:
        print('''
            \nPRODUCT INVENTORY
            \n- A - Adding a new product
            \r- B - Backup the database
            \r- C - View all products
            \r- D - Update a product
            \r- V - Displaying a product by its ID
            \r- E - Delete a product by its ID
            \r- Q - Exit''')
        user_option = input("\nPlease enter an option to continue: ")
        if user_option.upper() in ['A', 'B', 'C', 'D', 'V', 'E', 'Q']:
            return user_option
        else:
            input("Please enter a valid option from above: ")


def app():
    app_running = True
    while app_running:
        user_option = menu()
        if user_option.upper() == 'A':
            app_func.add_a_new_product()

        elif user_option.upper() == 'B':
            app_func.backup_database()
            print("Database backed up to 'backup.csv'")

        elif user_option.upper() == 'C':
            app_func.view_all_products()

        elif user_option.upper() == 'D':
            product_id = input("Please enter the product ID: ")
            if product_id.isdigit():
                app_func.update_product(int(product_id))
            else:
                print("Invalid product ID. Please enter a numeric value.")

        elif user_option.upper() == 'V':
            product_id = input("Please enter the product ID: ")
            if product_id.isdigit():
                app_func.display_product_by_id(int(product_id))
            else:
                print("Invalid product ID. Please enter a numeric value.")

        elif user_option.upper() == 'E':
            product_id = input("Please enter the product ID: ")
            if product_id.isdigit():
                app_func.delete_product(product_id)
            else:
                print("Invalid product ID. Please enter a numeric value.")

        elif user_option.upper() == 'Q':
            print("Exiting the Product Inventory...")
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
