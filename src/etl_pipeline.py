from dotenv import load_dotenv
import os

load_dotenv()
import os
import numpy as np
import pandas as pd
import mysql.connector
from pathlib import Path

# STEP 1: Project paths

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


# STEP 2: Extract data

def extract_data():

    customers = pd.read_csv(RAW / "customers.csv")
    products = pd.read_csv(RAW / "products.csv")
    orders = pd.read_csv(
        RAW / "orders.csv",
        parse_dates=["order_date"]
    )

    print("Data extracted successfully!")

    return customers, products, orders


# STEP 3: Transform and clean data

def transform_data(customers, products, orders):

    # Remove duplicate records

    customers = customers.drop_duplicates(
        subset=["customer_id"]
    ).copy()

    products = products.drop_duplicates(
        subset=["product_id"]
    ).copy()

    orders = orders.drop_duplicates(
        subset=["order_id"]
    ).copy()

    # Handle missing values

    customers["city"] = customers["city"].fillna("Unknown")

    orders = orders.dropna(
        subset=[
            "order_date",
            "quantity",
            "customer_id",
            "product_id"
        ]
    ).copy()

    # Convert quantity to integer

    orders["quantity"] = orders["quantity"].astype(int)

    # Remove invalid quantities

    orders = orders[orders["quantity"] > 0]

    # NumPy numerical validation

    products["unit_price"] = np.where(
        products["unit_price"] > 0,
        products["unit_price"],
        np.nan
    )

    products = products.dropna(
        subset=["unit_price"]
    )

    # Join orders with customers and products

    sales = orders.merge(
        customers,
        on="customer_id",
        how="inner"
    )

    sales = sales.merge(
        products,
        on="product_id",
        how="inner"
    )

    # Calculate revenue

    sales["revenue"] = np.round(
        sales["quantity"] * sales["unit_price"],
        2
    )

    print("Data transformation completed!")

    return customers, products, orders, sales


# STEP 4: Save cleaned CSV files

def save_processed_data(customers, products, orders, sales):

    PROCESSED.mkdir(parents=True, exist_ok=True)

    customers.to_csv(
        PROCESSED / "customers_clean.csv",
        index=False
    )

    products.to_csv(
        PROCESSED / "products_clean.csv",
        index=False
    )

    orders.to_csv(
        PROCESSED / "orders_clean.csv",
        index=False
    )

    sales.to_csv(
        PROCESSED / "sales_enriched.csv",
        index=False
    )

    print("Processed CSV files saved!")


# STEP 5: Connect to MySQL

def get_connection():

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "retail_sales")
    )


# STEP 6: Load data into MySQL

def load_to_mysql(customers, products, orders, sales):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY,
                customer_name VARCHAR(100),
                city VARCHAR(100),
                signup_date DATE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT PRIMARY KEY,
                product_name VARCHAR(100),
                category VARCHAR(100),
                unit_price DECIMAL(12,2)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT PRIMARY KEY,
                customer_id INT,
                product_id INT,
                order_date DATE,
                quantity INT,
                order_status VARCHAR(30),
                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id),
                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                order_id INT PRIMARY KEY,
                customer_id INT,
                product_id INT,
                order_date DATE,
                quantity INT,
                order_status VARCHAR(30),
                customer_name VARCHAR(100),
                city VARCHAR(100),
                signup_date DATE,
                product_name VARCHAR(100),
                category VARCHAR(100),
                unit_price DECIMAL(12,2),
                revenue DECIMAL(14,2)
            )
        """)

        # Delete previous batch data in child-first order

        for table in ["sales", "orders", "products", "customers"]:
            cursor.execute(f"DELETE FROM {table}")

        # Prepare customer records

        customer_rows = [
            (
                int(r.customer_id),
                str(r.customer_name),
                str(r.city),
                pd.Timestamp(r.signup_date).date()
            )
            for r in customers.itertuples(index=False)
        ]

        # Prepare product records

        product_rows = [
            (
                int(r.product_id),
                str(r.product_name),
                str(r.category),
                float(r.unit_price)
            )
            for r in products.itertuples(index=False)
        ]

        # Prepare order records

        order_rows = [
            (
                int(r.order_id),
                int(r.customer_id),
                int(r.product_id),
                pd.Timestamp(r.order_date).date(),
                int(r.quantity),
                str(r.order_status)
            )
            for r in orders.itertuples(index=False)
        ]

        # Prepare enriched sales records

        sales_rows = [
            (
                int(r.order_id),
                int(r.customer_id),
                int(r.product_id),
                pd.Timestamp(r.order_date).date(),
                int(r.quantity),
                str(r.order_status),
                str(r.customer_name),
                str(r.city),
                pd.Timestamp(r.signup_date).date(),
                str(r.product_name),
                str(r.category),
                float(r.unit_price),
                float(r.revenue)
            )
            for r in sales.itertuples(index=False)
        ]

        # Insert records into MySQL

        cursor.executemany(
            "INSERT INTO customers VALUES (%s,%s,%s,%s)",
            customer_rows
        )

        cursor.executemany(
            "INSERT INTO products VALUES (%s,%s,%s,%s)",
            product_rows
        )

        cursor.executemany(
            "INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s)",
            order_rows
        )

        cursor.executemany(
            """INSERT INTO sales VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )""",
            sales_rows
        )

        connection.commit()

        print("Data loaded into MySQL successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# STEP 7: Main ETL execution

def main():

    customers, products, orders = extract_data()

    customers, products, orders, sales = transform_data(
        customers,
        products,
        orders
    )

    save_processed_data(
        customers,
        products,
        orders,
        sales
    )

    load_to_mysql(
        customers,
        products,
        orders,
        sales
    )

    print("\nETL PIPELINE COMPLETED!")
    print("Customers:", len(customers))
    print("Products:", len(products))
    print("Orders:", len(orders))
    print("Sales:", len(sales))


if __name__ == "__main__":
    main()
