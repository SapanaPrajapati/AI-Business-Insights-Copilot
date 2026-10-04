import pandas as pd


customers = pd.read_csv("../data/cleaned/customers_clean.csv")
orders = pd.read_csv("../data/cleaned/orders_dataset_clean.csv")
order_items = pd.read_csv("../data/cleaned/order_items_clean.csv")
payments = pd.read_csv("../data/cleaned/order_payments_clean.csv")
reviews = pd.read_csv("../data/cleaned/reviews_clean.csv")
products = pd.read_csv("../data/cleaned/products_clean.csv")
sellers = pd.read_csv("../data/cleaned/sellers_clean.csv")
geolocation = pd.read_csv("../data/cleaned/geolocation_clean.csv")

# translation = pd.read_csv("../data/cleaned/translation_clean.csv")

print("All datasets loaded successfully!")


#importing data 

customers.to_sql(
    "customers",
    con=engine,
    if_exists="replace",
    index=False
)

orders.to_sql(
    "orders",
    con=engine,
    if_exists="replace",
    index=False
)

order_items.to_sql(
    "order_items",
    con=engine,
    if_exists="replace",
    index=False
)

payments.to_sql(
    "payments",
    con=engine,
    if_exists="replace",
    index=False
)

products.to_sql(
    "products",
    con=engine,
    if_exists="replace",
    index=False
)

reviews.to_sql(
    "reviews",
    con=engine,
    if_exists="replace",
    index=False
)

sellers.to_sql(
    "sellers",
    con=engine,
    if_exists="replace",
    index=False
)

geolocation.to_sql(
    "geolocation",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ All tables imported successfully!")

