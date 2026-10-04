import pandas as pd
reviews = pd.read_csv("../data/cleaned/reviews_clean.csv")

reviews = reviews.drop_duplicates(subset=["review_id"], keep="first")

print("Total rows:", len(reviews))
print("Unique review_id:", reviews["review_id"].nunique())

duplicates = reviews[reviews.duplicated(subset=["review_id"], keep=False)]

print("\nDuplicate review IDs:", len(duplicates))

print(duplicates[["review_id","order_id"]].head(20))