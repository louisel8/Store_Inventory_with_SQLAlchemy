import csv
from datetime import datetime, date
from models import Product, session, Session
from sqlalchemy import func
import re


def clean_name(name_str):
    cleaned_name = str(name_str.strip())
    return cleaned_name


def clean_price(price_str):
    try:
        if not re.match(r'^\$\d+\.\d{2}$', price_str):
            raise ValueError("Invalid price format.")
        split_price = price_str.split('$')
        price_float = float(split_price[1])
        return int(price_float * 100)
    except (IndexError, ValueError) as e:
        raise ValueError(f"{e}")


def clean_qty(qty_str):
    try:
        cleaned_qty = int(qty_str)
        return cleaned_qty
    except ValueError as e:
        raise ValueError(f"{e}")


def clean_date(date_str):
    try:
        split_date = date_str.split("/")
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return date(year, month, day)
    except ValueError:
        print('''
            \n****** Date Error ******
            \rThe date format should include a valid month, day, and year.
            \rEx: 11/1/2018; Please re-enter''')
        return None


def load_csv_and_clean_duplicates():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = clean_name(row[0])
                product_price = clean_price(row[1])
                product_quantity = clean_qty(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(
                    product_name=product_name,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    date_updated=date_updated
                )
                session.add(new_product)
        session.commit()


def add_a_new_product():
    while True:
        try:
            product_name = input("Product Name: ").strip()
            if not product_name:
                print("Product name cannot be empty. Please try again.")
                continue

            while True:
                product_price_input = input("Product Price (Ex: $8.05): ")
                if product_price_input.lower() == 'q':
                    return
                try:
                    product_price = clean_price(product_price_input)
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid price format (Ex: $X.XX), or enter 'Q' to return to the main menu.")

            while True:
                product_quantity_input = input("Product Quantity: ")
                if product_quantity_input.lower() == 'q':
                    return
                try:
                    product_quantity = clean_qty(product_quantity_input)
                    if product_quantity >= 0:
                        break
                    else:
                        print("Invalid input, please enter a non-negative integer, or enter 'Q' to return to the main menu.")
                except ValueError as e:
                    print(f"Invalid input, please enter an integer, or enter 'Q' to return to the main menu.")

            while True:
                date_updated_input = input("Date Updated (Ex: 11/1/2018): ")
                if date_updated_input.lower() == 'q':
                    return
                date_updated = clean_date(date_updated_input)
                if date_updated:
                    break

            existing_product = session.query(Product).filter(
                func.lower(Product.product_name) == product_name.lower()).first()
            if existing_product:
                existing_product.product_price = product_price
                existing_product.product_quantity = product_quantity
                existing_product.date_updated = date_updated
                session.commit()
                print(f"The product '{product_name}' already exists in the database.")
                print("The product's stats have been updated to the new information you just added.")
            else:
                new_product = Product(
                    product_name=product_name,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    date_updated=date_updated
                )
                session.add(new_product)
                session.commit()
                print("New product added successfully.")
            break
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data, or enter 'Q' to return to the main menu.")


def view_all_products():
    with Session() as session_instance:
        products = session_instance.query(Product).all()
        for product in products:
            print(f"Product ID: {product.product_id}")
            print(f"Product Name: {product.product_name}")
            print(f"Product Price: ${product.product_price / 100:.2f}")
            print(f"Product Quantity: {product.product_quantity}")
            print(f"Date Updated: {product.date_updated.strftime('%m/%d/%Y') if product.date_updated else 'N/A'}")
            print('-' * 20)


def display_product_by_id(product_id):
    try:
        with Session() as session_instance:
            product = session_instance.query(Product).filter_by(product_id=product_id).first()
            if product:
                print(f"Product ID: {product.product_id}")
                print(f"Product Name: {product.product_name}")
                print(f"Product Price: ${product.product_price / 100:.2f}")
                print(f"Product Quantity: {product.product_quantity}")
                print(f"Date Updated: {product.date_updated.strftime('%m/%d/%Y') if product.date_updated else 'N/A'}")
                print('-' * 20)
            else:
                print("Product not found.")
    except ValueError:
        print("Invalid product ID. Please enter a numeric value.")


def update_product():
    while True:
        try:
            product_id_input = input("Please enter the product ID (or 'Q' to go back to the main menu): ").strip()
            if product_id_input.lower() == 'q':
                return
            product_id = int(product_id_input)
            with Session() as session_instance:
                product = session_instance.query(Product).filter_by(product_id=product_id).first()
                if product:
                    display_product_by_id(product_id)
                    print("- A - Update price\n- B - Update Quantity\n- C - Update the date updated\n")
                    while True:
                        user_update_option = input("Please enter an option to update (or 'Q' to quit): ").strip().upper()
                        if user_update_option in ['A', 'B', 'C']:
                            break
                        elif user_update_option == 'Q':
                            return
                        else:
                            print("Invalid option. Please enter 'A', 'B', 'C', or 'Q'.")

                    if user_update_option == "A":
                        while True:
                            updated_price = input("Enter the updated price: ")
                            if updated_price.lower() == 'q':
                                return
                            try:
                                if re.match(r'^\$\d+\.\d{2}$', updated_price):
                                    product.product_price = clean_price(updated_price)
                                    break
                                else:
                                    print("Invalid price format. Please try again by entering price in format $X.XX.")
                            except ValueError as e:
                                print(f"Error: {e}")
                    elif user_update_option == "B":
                        while True:
                            updated_quantity = input("Enter the updated quantity: ")
                            if updated_quantity.lower() == 'q':
                                return
                            try:
                                updated_quantity = int(updated_quantity)
                                if updated_quantity < 0:
                                    raise ValueError("Quantity cannot be negative.")
                                product.product_quantity = updated_quantity
                                break
                            except ValueError as e:
                                print(f"Error: {e}. Please enter a valid quantity.")
                    elif user_update_option == "C":
                        while True:
                            updated_date = input("Enter the updated date (Ex: MM/DD/YYYY): ")
                            if updated_date.lower() == 'q':
                                return
                            try:
                                if re.match(r'^\d{2}/\d{2}/\d{4}$', updated_date):
                                    updated_date = clean_date(updated_date)
                                    if updated_date is not None:
                                        product.date_updated = updated_date
                                        break
                                else:
                                    print("Invalid date format. Please enter date in format MM/DD/YYYY.")
                            except ValueError as e:
                                print(f"Error: {e}")

                    session_instance.commit()
                    print("Product updated successfully.")
                else:
                    print("Product not found.")
        except ValueError as e:
            print(f"Error: {e}")


def delete_product():
    while True:
        try:
            product_id_input = input("Please enter the product ID (or 'Q' to go back to the main menu): ").strip()
            if product_id_input.lower() == 'q':
                return
            product_id = int(product_id_input)
            with Session() as session_instance:
                product = session_instance.query(Product).filter_by(product_id=product_id).first()
                if product:
                    print(f"Product ID: {product.product_id}")
                    print(f"Product Name: {product.product_name}")
                    print(f"Product Price: {product.product_price}")
                    print(f"Product Quantity: {product.product_quantity}")
                    print(f"Date Updated: {product.date_updated}")

                    while True:
                        confirm_delete = input(
                            "Do you want to delete this product? (Y/N or 'Q' to quit): ").strip().lower()
                        if confirm_delete in ['y', 'n']:
                            break
                        elif confirm_delete == 'q':
                            return
                        else:
                            print("Invalid option. Please enter 'Y', 'N', or 'Q'.")

                    if confirm_delete == 'y':
                        session_instance.delete(product)
                        session_instance.commit()
                        print("Product deleted successfully.")
                    else:
                        print("Product not deleted.")
                    break
                else:
                    print("Product not found.")
        except ValueError:
            print("Invalid product ID.")


def backup_database():
    with open('backup.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Product Price', 'Product Quantity', 'Date Updated'])
        with Session() as session_instance:
            products = session_instance.query(Product).all()
            for product in products:
                writer.writerow([product.product_name, product.product_price / 100, product.product_quantity,
                                 product.date_updated.strftime('%m/%d/%Y') if product.date_updated else ""])
