import csv
import re
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Product, Session


def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        price_float = float(split_price[1])
        return int(price_float * 100)
    except (IndexError, ValueError):
        raise ValueError("Invalid price format. Please enter price in format $X.XX.")


def clean_date(date_str):
    try:
        split_date = date_str.split("/")
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return date(year, month, day)
    except (IndexError, ValueError):
        raise ValueError("Invalid date format. Please enter date in format MM/DD/YYYY.")


def load_csv():
    products = []
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)
        for row in data:
            product_name, product_price, product_quantity, date_updated = row
            product_price = clean_price(product_price)
            product_quantity = int(product_quantity)
            date_updated = clean_date(date_updated)
            new_product = Product(
                product_name=product_name.strip(),
                product_price=product_price,
                product_quantity=product_quantity,
                date_updated=date_updated
            )
            products.append(new_product)
    return products


def add_a_new_product():
    with Session() as session_instance:
        while True:
            product_name = input('Product Name: ').strip()
            product_price = None
            while product_price is None:
                try:
                    price_input = input("Product Price (Ex: $5.06): ")
                    product_price = clean_price(price_input)
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid price.")

            product_quantity = None
            while product_quantity is None:
                try:
                    quantity_input = int(input("Product Quantity: "))
                    if quantity_input < 0:
                        raise ValueError("Quantity cannot be negative.")
                    product_quantity = quantity_input
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid quantity.")

            date_updated = None
            while date_updated is None:
                try:
                    date_input = input("Date Updated (Ex: MM/DD/YYYY): ")
                    date_updated = clean_date(date_input)
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid date.")

            new_product = Product(
                product_name=product_name,
                product_price=product_price,
                product_quantity=product_quantity,
                date_updated=date_updated
            )
            session_instance.add(new_product)
            session_instance.commit()
            print("New product added successfully.")
            break


def view_all_products(products=None):
    if products is None:
        products = load_csv()
    for index, product in enumerate(products, start=1):
        print(f"Product ID: {index}")
        print(f"Product Name: {product.product_name}")
        print(f"Product Price: ${product.product_price / 100:.2f}")
        print(f"Product Quantity: {product.product_quantity}")
        print(f"Date Updated: {product.date_updated.strftime('%m/%d/%Y') if product.date_updated else 'N/A'}")
        print('-' * 20)


def display_product_by_id(product_id):
    try:
        product_id = int(product_id)
        with Session() as session_instance:
            product = session_instance.query(Product).filter_by(product_id=product_id).first()
            if product:
                product_price_str = f"{product.product_price:.2f}" if isinstance(product.product_price, float) else f"{product.product_price}"
                date_updated_str = product.date_updated.strftime('%m/%d/%Y') if product.date_updated else "N/A"
                print(f"Product ID: {product.product_id}")
                print(f"Product Name: {product.product_name}")
                print(f"Product Price: {product_price_str}")
                print(f"Product Quantity: {product.product_quantity}")
                print(f"Date Updated: {date_updated_str}")
            else:
                print("Product not found.")
    except ValueError:
        print("Invalid product ID.")


def update_product(product_id):
    with Session() as session_instance:
        try:
            product_id = int(product_id)
            product = session_instance.query(Product).filter_by(product_id=product_id).first()
            if product:
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
                        if re.match(r'^\$\d+\.\d{2}$', updated_price):
                            product.product_price = clean_price(updated_price)
                            break
                        else:
                            print("Invalid price format. Please try again by entering price in format $X.XX.")
                elif user_update_option == "B":
                    while True:
                        updated_quantity = int(input("Enter the updated quantity: "))
                        if updated_quantity < 0:
                            raise ValueError("Quantity cannot be negative.")
                        product.product_quantity = updated_quantity
                        break
                elif user_update_option == "C":
                    while True:
                        updated_date = input("Enter the updated date (Ex: MM/DD/YYYY): ")
                        if re.match(r'^\d{2}/\d{2}/\d{4}$', updated_date):
                            updated_date = clean_date(updated_date)
                            if updated_date is not None:
                                product.date_updated = updated_date
                                break
                        print("Invalid date format. Please enter date in format MM/DD/YYYY.")

                session_instance.commit()
                print("Product updated successfully.")
            else:
                print("Product not found.")
        except ValueError as e:
            print(f"Error: {e}")


def delete_product(product_id):
    with Session() as session_instance:
        try:
            product_id = int(product_id)
            product = session_instance.query(Product).filter_by(product_id=product_id).first()
            if product:
                print(f"Product ID: {product.product_id}")
                print(f"Product Name: {product.product_name}")
                print(f"Product Price: {product.product_price}")
                print(f"Product Quantity: {product.product_quantity}")
                print(f"Date Updated: {product.date_updated}")
                while True:
                    confirm_delete = input("Do you want to delete this product? (Y/N or 'Q' to quit): ").strip().lower()
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
