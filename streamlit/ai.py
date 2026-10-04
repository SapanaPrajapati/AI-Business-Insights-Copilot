import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# DETECT QUESTION TYPE
# ============================================================

def detect_question_type(question):

    question_lower = question.lower().strip()


    # ========================================================
    # CATEGORY
    # ========================================================

    if any(word in question_lower for word in [
        "category",
        "categories",
        "health beauty",
        "health & beauty",
        "product category",
        "best category",
        "top category"
    ]):

        return "category"


    # ========================================================
    # STATE / MARKET
    # ========================================================

    if any(word in question_lower for word in [
        "state",
        "states",
        "location",
        "region",
        "market",
        "best state",
        "top state"
    ]):

        return "state"


    # ========================================================
    # PRODUCT
    # ========================================================

    if any(word in question_lower for word in [
        "product",
        "products",
        "best product",
        "top product",
        "best-selling product",
        "best selling product"
    ]):

        return "product"


    # ========================================================
    # PAYMENT
    # ========================================================

    if any(word in question_lower for word in [
        "payment",
        "payments",
        "payment method",
        "payment methods",
        "credit card",
        "upi",
        "voucher",
        "boleto",
        "debit card"
    ]):

        return "payment"


    # ========================================================
    # REVENUE / SALES / MONTHLY TREND
    # ========================================================

    if any(word in question_lower for word in [
        "revenue",
        "sales",
        "month",
        "monthly",
        "growth",
        "trend",
        "increase",
        "decrease",
        "decline",
        "highest revenue",
        "lowest revenue",
        "sales trend"
    ]):

        return "revenue"


    # ========================================================
    # GENERAL
    # ========================================================

    return "general"


# ============================================================
# GET BUSINESS DATA
# ============================================================


def get_business_data(
    question,
    selected_year="All",
    selected_month="All",
    selected_state="All",
    selected_category="All"
):

    from business_queries import (
        get_monthly_revenue,
        get_category_performance,
        get_state_performance,
        get_product_performance,
        get_payment_performance
    )


    # Detect what type of business question was asked

    question_type = detect_question_type(question)


    # ========================================================
    # REVENUE ANALYSIS
    # ========================================================

    if question_type == "revenue":

        df = get_monthly_revenue()

        if df.empty:
            return "No monthly revenue data was found."

        return (
            "MONTHLY REVENUE AND ORDERS\n\n"
            + df.to_string(index=False)
        )


    # ========================================================
    # CATEGORY ANALYSIS
    # ========================================================

    elif question_type == "category":

        df = get_category_performance()

        if df.empty:
            return "No category performance data was found."

        return (
            "CATEGORY PERFORMANCE\n\n"
            + df.to_string(index=False)
        )


    # ========================================================
    # STATE ANALYSIS
    # ========================================================

    elif question_type == "state":

        df = get_state_performance()

        if df.empty:
            return "No state performance data was found."

        return (
            "STATE PERFORMANCE\n\n"
            + df.to_string(index=False)
        )


    # ========================================================
    # PRODUCT ANALYSIS
    # ========================================================

    elif question_type == "product":

        df = get_product_performance()

        if df.empty:
            return "No product performance data was found."

        return (
        "TOP PRODUCTS BY REVENUE\n\n"
        "NOTE: The Olist dataset does not contain descriptive "
        "product names. Product_ID is used to identify individual products.\n\n"
        + df.to_string(index=False)
        )


    # ========================================================
    # PAYMENT ANALYSIS
    # ========================================================

    elif question_type == "payment":

        df = get_payment_performance()

        if df.empty:
            return "No payment performance data was found."

        return (
            "PAYMENT PERFORMANCE\n\n"
            + df.to_string(index=False)
        )


    # ========================================================
    # GENERAL QUESTION
    # ========================================================

    else:

        return """
AVAILABLE BUSINESS DATA

The AI Business Copilot currently supports:

1. Revenue and monthly sales
2. Product categories
3. States and markets
4. Products
5. Payment methods

Please ask a question related to one of these areas.
"""


# ============================================================
# ASK GEMINI
# ============================================================

def ask_ai(question, business_data):

    prompt = f"""
You are an expert AI Business Analyst.

You are analyzing the Brazilian Olist E-Commerce dataset.

Your job is to provide accurate, data-driven business
insights based ONLY on the business data supplied below.


============================================================
IMPORTANT RULES
============================================================

IMPORTANT RULES:

1. Use ONLY the business data provided below.
2. Do NOT invent numbers.
3. Do NOT assume missing information.
4. If the data is insufficient, clearly say so.
5. Use actual numbers from the provided data whenever possible.
6. Give practical business recommendations.
7. Keep the answer professional and concise.
8. The Olist dataset does not contain descriptive product names.
9. Use Product_ID when referring to individual products.
10. Never invent product names from Product_ID.
11. If the user asks for product names, clearly explain that
    only Product_ID is available.

============================================================
BUSINESS DATA
============================================================

{business_data}


============================================================
USER QUESTION
============================================================

{question}


============================================================
RESPONSE FORMAT
============================================================

### 📊 Business Insight

Identify the most important finding related to
the user's question.

Use actual data from the provided business data.


### 🔍 Analysis

Explain the relevant numbers, comparisons,
patterns or trends.

Use actual values wherever possible.


### 💡 Recommendation

Give 2–3 practical recommendations that the
business could take based on the analysis.


### ✅ Conclusion

Give a short executive-level conclusion.


============================================================
FINAL INSTRUCTION
============================================================

Do not invent information.

If the provided data does not contain enough
information to answer the question, say so clearly.
"""


    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response.text:

            return response.text

        else:

            return """
### ⚠️ No Response

Gemini did not return a response.
"""


    except Exception as e:

        return f"""
### ❌ Gemini Error

Unable to generate the AI response.

Error:
{str(e)}
"""

# ============================================================
# AI BUSINESS RECOMMENDATIONS
# ============================================================

def generate_business_recommendations():

    from business_queries import (
        get_category_performance,
        get_state_performance,
        get_monthly_revenue,
        get_product_performance,
        get_payment_performance
    )

    try:

        # ----------------------------------------------------
        # GET BUSINESS DATA
        # ----------------------------------------------------

        category_df = get_category_performance()
        state_df = get_state_performance()
        monthly_df = get_monthly_revenue()
        product_df = get_product_performance()
        payment_df = get_payment_performance()


        # ----------------------------------------------------
        # CONVERT DATA TO TEXT
        # ----------------------------------------------------

        category_data = category_df.head(10).to_string(
            index=False
        )

        state_data = state_df.head(10).to_string(
            index=False
        )

        monthly_data = monthly_df.to_string(
            index=False
        )

        product_data = product_df.head(10).to_string(
            index=False
        )

        payment_data = payment_df.to_string(
            index=False
        )


        # ----------------------------------------------------
        # GEMINI PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are an expert Business Intelligence Analyst.

You are analyzing the Brazilian Olist E-Commerce dataset.

Generate practical business recommendations using ONLY
the actual business data provided below.

DO NOT invent numbers.

DO NOT assume information that is not present.

============================================================
CATEGORY PERFORMANCE
============================================================

{category_data}


============================================================
STATE PERFORMANCE
============================================================

{state_data}


============================================================
MONTHLY REVENUE
============================================================

{monthly_data}


============================================================
TOP PRODUCTS
============================================================

{product_data}


============================================================
PAYMENT PERFORMANCE
============================================================

{payment_data}


============================================================
TASK
============================================================

Identify the most important business opportunities.

Provide exactly 4 recommendations.

Focus on:

1. Best product/category opportunity
2. Best geographic/state opportunity
3. Revenue/sales trend opportunity
4. Payment/customer/business improvement opportunity


============================================================
RESPONSE FORMAT
============================================================

### 💡 AI Business Recommendations

**1. 🏷 Category Opportunity**

Explain which category deserves attention and why.
Use actual revenue/order numbers.

**2. 📍 Geographic Opportunity**

Identify the strongest state/market and explain what
the business should do.

**3. 📈 Revenue Opportunity**

Analyze the revenue trend and provide a practical action.

**4. 💳 Business Improvement**

Use payment or product performance to identify another
business opportunity.

### 🎯 Overall Strategy

Give one concise overall recommendation for management.

Keep the response professional, concise and data-driven.
"""

        # ----------------------------------------------------
        # CALL GEMINI
        # ----------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text


    except Exception as e:

        return f"""
### ❌ Recommendation Error

Unable to generate AI recommendations.

Please check the database connection and Gemini API.

Error:
{str(e)}
"""