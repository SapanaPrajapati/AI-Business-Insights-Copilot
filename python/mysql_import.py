import pandas as pd
from sqlalchemy import create_engine

# ==========================
# MySQL Connection
# ==========================

username = "root"
password = "12345678"          # Your MySQL password
host = "localhost"
port = "3306"
database = "ai_business_insights"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# ==========================
# Read Cleaned CSV Files
# ==========================

customers = pd.read_csv("../data/cleaned/customers_clean.csv")
orders = pd.read_csv("../data/cleaned/orders_dataset_clean.csv")
order_items = pd.read_csv("../data/cleaned/order_items_clean.csv")
payments = pd.read_csv("../data/cleaned/order_payments_clean.csv")
products = pd.read_csv("../data/cleaned/products_clean.csv")
reviews = pd.read_csv("../data/cleaned/reviews_clean.csv")
sellers = pd.read_csv("../data/cleaned/sellers_clean.csv")
geolocation = pd.read_csv("../data/cleaned/geolocation_clean.csv")

# ==========================
# Remove Duplicate Reviews
# ==========================

print(f"\nReviews before removing duplicates: {len(reviews)}")

reviews = reviews.drop_duplicates(
    subset=["review_id"],
    keep="first"
)

print(f"Reviews after removing duplicates: {len(reviews)}")

# ==========================
# Rename Incorrect Columns
# ==========================

products.rename(columns={
    "product_name_lenght": "product_name_length",
    "product_description_lenght": "product_description_length"
}, inplace=True)

# ==========================
# Convert Date Columns
# ==========================

order_date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in order_date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

reviews["review_creation_date"] = pd.to_datetime(
    reviews["review_creation_date"],
    errors="coerce"
)

reviews["review_answer_timestamp"] = pd.to_datetime(
    reviews["review_answer_timestamp"],
    errors="coerce"
)

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

# ==========================
# Import Function
# ==========================

def import_table(df, table_name):
    try:
        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi"
        )
        print(f"✅ {table_name} imported successfully.")

    except Exception as e:
        print(f"\n❌ Error importing '{table_name}'")
        print(e)
        print("-" * 60)

# ==========================
# Import Tables
# ==========================

print("\nStarting Data Import...\n")

import_table(customers, "customers")
import_table(products, "products")
import_table(sellers, "sellers")
import_table(orders, "orders")
import_table(order_items, "order_items")
import_table(payments, "payments")
import_table(reviews, "reviews")
import_table(geolocation, "geolocation")

print("\nOrders Columns:")
print(orders.columns.tolist())

print("\nProducts Columns:")
print(products.columns.tolist())

print("\n🎉 Data import process completed!")