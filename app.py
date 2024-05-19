from models import engine, Base
import app_func


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
        user_option = input("\nPlease enter an option to continue: ").strip().upper()
        if user_option in ['A', 'B', 'C', 'D', 'V', 'E', 'Q']:
            return user_option
        else:
            print("Please enter a valid option from above.")


def app():
    app_running = True
    while app_running:
        user_option = menu()

        if user_option == 'A':
            app_func.add_a_new_product()

        elif user_option == 'B':
            app_func.backup_database()
            print("Database backed up to 'backup.csv'")

        elif user_option == 'C':
            app_func.view_all_products()

        elif user_option == 'D':
            app_func.update_product()

        elif user_option == 'V':
            product_id_input = input("Please enter the product ID: ").strip()
            app_func.display_product_by_id(product_id_input)

        elif user_option == 'E':
            app_func.delete_product()

        elif user_option == 'Q':
            print("Exiting the Product Inventory...")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app_func.load_csv_and_clean_duplicates()
    app()
