# ============================================================
# business_queries.py
# Brazilian Olist E-Commerce
# Business Intelligence Queries for Gemini AI
# ============================================================

from database import load_data


# ============================================================
# 1. BUILD AI FILTERS
# ============================================================

def build_ai_filters(
    selected_year="All",
    selected_month="All",
    selected_state="All",
    selected_category="All"
):
    """
    Creates a reusable SQL WHERE clause based on
    the filters selected in Streamlit.
    """

    conditions = []


    # --------------------------------------------------------
    # YEAR
    # --------------------------------------------------------

    if selected_year != "All":

        conditions.append(
            f"o.purchase_year = {int(selected_year)}"
        )


    # --------------------------------------------------------
    # MONTH
    # --------------------------------------------------------

    if selected_month != "All":

        conditions.append(
            f"o.purchase_month = '{selected_month}'"
        )


    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    if selected_state != "All":

        conditions.append(
            f"c.customer_state = '{selected_state}'"
        )


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if selected_category != "All":

        conditions.append(
            f"p.product_category_name_english = '{selected_category}'"
        )


    # --------------------------------------------------------
    # CREATE WHERE CLAUSE
    # --------------------------------------------------------

    if conditions:

        return "WHERE " + " AND ".join(conditions)

    return ""


# ============================================================
# 2. MONTHLY REVENUE
# ============================================================

def get_monthly_revenue(where_clause=""):

    query = f"""

    SELECT

        o.purchase_year AS Year,

        o.purchase_month AS Month,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        o.purchase_year,
        o.purchase_month

    ORDER BY

        o.purchase_year,
        o.purchase_month;

    """

    return load_data(query)


# ============================================================
# 3. CATEGORY PERFORMANCE
# ============================================================

def get_category_performance(where_clause=""):

    query = f"""

    SELECT

        p.product_category_name_english
            AS Category,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT oi.order_id
        ) AS Orders,

        ROUND(
            SUM(oi.price)
            /
            NULLIF(
                COUNT(DISTINCT oi.order_id),
                0
            ),
            2
        ) AS Revenue_Per_Order

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    {where_clause}

    GROUP BY

        p.product_category_name_english

    ORDER BY

        Revenue DESC

    LIMIT 20;

    """

    return load_data(query)


# ============================================================
# 4. STATE PERFORMANCE
# ============================================================

def get_state_performance(where_clause=""):

    query = f"""

    SELECT

        c.customer_state AS State,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders,

        COUNT(
            DISTINCT o.customer_id
        ) AS Customers,

        ROUND(
            SUM(oi.price)
            /
            NULLIF(
                COUNT(DISTINCT o.order_id),
                0
            ),
            2
        ) AS Revenue_Per_Order

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        c.customer_state

    ORDER BY

        Revenue DESC;

    """

    return load_data(query)


# ============================================================
# 5. TOP PRODUCTS
# ============================================================

def get_product_performance():

    query = """
    SELECT
        p.product_id AS Product_ID,
        p.product_category_name_english AS Category,
        ROUND(SUM(oi.price), 2) AS Revenue,
        COUNT(DISTINCT oi.order_id) AS Orders

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY
        p.product_id,
        p.product_category_name_english

    ORDER BY
        Revenue DESC

    LIMIT 10;
    """

    return load_data(query)

# ============================================================
# 6. PAYMENT PERFORMANCE
# ============================================================

def get_payment_performance(where_clause=""):

    query = f"""

    SELECT

        op.payment_type AS Payment_Method,

        COUNT(*) AS Payments,

        ROUND(
            SUM(op.payment_value),
            2
        ) AS Payment_Value,

        ROUND(
            AVG(op.payment_value),
            2
        ) AS Average_Payment

    FROM payments op

    JOIN orders o
        ON op.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        op.payment_type

    ORDER BY

        Payment_Value DESC;

    """

    return load_data(query)


# ============================================================
# 7. OVERALL BUSINESS KPIs
# ============================================================

def get_business_kpis(where_clause=""):

    query = f"""

    SELECT

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders,

        COUNT(
            DISTINCT o.customer_id
        ) AS Customers,

        COUNT(
            DISTINCT oi.seller_id
        ) AS Sellers,

        ROUND(
            SUM(oi.price)
            /
            NULLIF(
                COUNT(DISTINCT o.order_id),
                0
            ),
            2
        ) AS Average_Order_Value

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause};

    """

    return load_data(query)


# ============================================================
# 8. TOP CATEGORY
# ============================================================

def get_top_category(where_clause=""):

    query = f"""

    SELECT

        p.product_category_name_english
            AS Category,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    {where_clause}

    GROUP BY

        p.product_category_name_english

    ORDER BY

        Revenue DESC

    LIMIT 1;

    """

    return load_data(query)


# ============================================================
# 9. BEST STATE
# ============================================================

def get_best_state(where_clause=""):

    query = f"""

    SELECT

        c.customer_state AS State,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        c.customer_state

    ORDER BY

        Revenue DESC

    LIMIT 1;

    """

    return load_data(query)


# ============================================================
# 10. TOP 10 CATEGORIES
# ============================================================

def get_top_categories(where_clause=""):

    query = f"""

    SELECT

        p.product_category_name_english
            AS Category,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT oi.order_id
        ) AS Orders

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    {where_clause}

    GROUP BY

        p.product_category_name_english

    ORDER BY

        Revenue DESC

    LIMIT 10;

    """

    return load_data(query)


# ============================================================
# 11. TOP 10 STATES
# ============================================================

def get_top_states(where_clause=""):

    query = f"""

    SELECT

        c.customer_state AS State,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        c.customer_state

    ORDER BY

        Revenue DESC

    LIMIT 10;

    """

    return load_data(query)


# ============================================================
# 12. TOP PRODUCTS BY REVENUE
# ============================================================

def get_top_products(where_clause=""):

    query = f"""

    SELECT

        oi.product_id AS Product_ID,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(*) AS Items_Sold

    FROM order_items oi

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        oi.product_id

    ORDER BY

        Revenue DESC

    LIMIT 10;

    """

    return load_data(query)


# ============================================================
# 13. PAYMENT METHOD SUMMARY
# ============================================================

def get_payment_methods(where_clause=""):

    query = f"""

    SELECT

        op.payment_type AS Payment_Method,

        COUNT(*) AS Transactions,

        ROUND(
            SUM(op.payment_value),
            2
        ) AS Total_Value

    FROM order_payments op

    JOIN orders o
        ON op.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        op.payment_type

    ORDER BY

        Total_Value DESC;

    """

    return load_data(query)


# ============================================================
# 14. ORDER STATUS PERFORMANCE
# ============================================================

def get_order_status_performance(where_clause=""):

    query = f"""

    SELECT

        o.order_status AS Order_Status,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        o.order_status

    ORDER BY

        Orders DESC;

    """

    return load_data(query)


# ============================================================
# 15. SELLER PERFORMANCE
# ============================================================

def get_seller_performance(where_clause=""):

    query = f"""

    SELECT

        oi.seller_id AS Seller_ID,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT oi.order_id
        ) AS Orders,

        COUNT(*) AS Items_Sold

    FROM order_items oi

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        oi.seller_id

    ORDER BY

        Revenue DESC

    LIMIT 20;

    """

    return load_data(query)


# ============================================================
# 16. AVERAGE ORDER VALUE
# ============================================================

def get_average_order_value(where_clause=""):

    query = f"""

    SELECT

        ROUND(
            SUM(oi.price)
            /
            NULLIF(
                COUNT(DISTINCT o.order_id),
                0
            ),
            2
        ) AS Average_Order_Value

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause};

    """

    return load_data(query)


# ============================================================
# 17. REVENUE BY MONTH
# ============================================================

def get_revenue_by_month(where_clause=""):

    query = f"""

    SELECT

        o.purchase_month AS Month,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        o.purchase_month

    ORDER BY

        Revenue DESC;

    """

    return load_data(query)


# ============================================================
# 18. CUSTOMER PERFORMANCE
# ============================================================

def get_customer_performance(where_clause=""):

    query = f"""

    SELECT

        COUNT(
            DISTINCT o.customer_id
        ) AS Customers,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders,

        ROUND(
            SUM(oi.price),
            2
        ) AS Revenue,

        ROUND(
            SUM(oi.price)
            /
            NULLIF(
                COUNT(DISTINCT o.customer_id),
                0
            ),
            2
        ) AS Revenue_Per_Customer

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause};

    """

    return load_data(query)


# ============================================================
# END OF BUSINESS QUERIES
# ============================================================