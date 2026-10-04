import os
import pandas as pd

from dotenv import load_dotenv
from database import load_data
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ==============================
# LOAD BUSINESS DATA
# ==============================

category_query = """
SELECT
    p.product_category_name_english AS Category,
    ROUND(SUM(oi.price), 2) AS Revenue,
    COUNT(DISTINCT oi.order_id) AS Orders
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.product_category_name_english
ORDER BY Revenue DESC
LIMIT 10;
"""


category_df = load_data(category_query)


# ==============================
# CONVERT DATA TO TEXT
# ==============================

category_data = category_df.to_string(index=False)


print("\n==============================")
print("TOP 10 CATEGORY DATA")
print("==============================\n")

print(category_data)


# ==============================
# ASK GEMINI
# ==============================

question = """
Which product category should the business focus on?
Analyze the provided category revenue and order data.
"""


prompt = f"""
You are an AI Business Analyst working with the Brazilian Olist
E-Commerce dataset.

IMPORTANT:
You must use ONLY the business data provided below.
Do not invent numbers.
Do not say that data is unavailable.

BUSINESS DATA:

Top 10 Product Categories:

{category_data}


BUSINESS QUESTION:

{question}


Provide the answer in this format:

### 📊 Business Insight

Identify the strongest category and explain why.

### 🔍 Analysis

Compare the important categories using the provided
revenue and order data.

### 💡 Recommendation

Give a practical business recommendation.

### ✅ Conclusion

Give a short final conclusion.

Use the actual category names and numbers from the data.
"""


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


print("\n==============================")
print("GEMINI BUSINESS INSIGHT")
print("==============================\n")

print(response.text)