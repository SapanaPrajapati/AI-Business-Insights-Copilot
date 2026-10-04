# ============================================================
# alerts.py
# AI Business Insights Copilot
# Step 5.2A - Reliable Business Alert Engine
# ============================================================

from database import load_data


# ============================================================
# MONTH ORDER
# ============================================================

MONTH_ORDER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


# ============================================================
# REMOVE MONTH FILTER FOR MONTH-OVER-MONTH ALERTS
# ============================================================

def remove_month_filter(where_clause):
    """
    Removes the purchase_month condition from the WHERE clause.

    Why?
    Revenue and order growth need two months of data:
    
        Previous Month → Current Month

    Therefore, selecting a single month in the dashboard
    should not remove the previous month from the alert calculation.
    """

    if not where_clause:
        return ""

    conditions = where_clause.replace(
        "WHERE ",
        "",
        1
    ).split(" AND ")

    filtered_conditions = []

    for condition in conditions:

        if "o.purchase_month" not in condition:
            filtered_conditions.append(condition)

    if not filtered_conditions:
        return ""

    return "WHERE " + " AND ".join(
        filtered_conditions
    )


# ============================================================
# HELPER FUNCTION
# ============================================================

def sort_monthly_data(df):
    """
    Sort revenue/order data chronologically.

    This prevents problems caused by SQL sorting month names
    alphabetically instead of chronologically.
    """

    if df.empty:
        return df

    df = df.copy()

    # Convert month names into month numbers
    df["Month_Number"] = (
        df["Month"]
        .astype(str)
        .str.strip()
        .map(MONTH_ORDER)
    )

    # Sort by year and month
    df = df.sort_values(
        by=["Year", "Month_Number"]
    ).reset_index(drop=True)

    return df


# ============================================================
# 1. REVENUE ALERT
# ============================================================

def get_revenue_alert(where_clause=""):

    # --------------------------------------------------------
    # IMPORTANT:
    # Remove Month filter so we can compare:
    #
    # Previous Month → Current Month
    #
    # Other filters such as Year, State and Category
    # are still preserved.
    # --------------------------------------------------------

    alert_where_clause = remove_month_filter(
        where_clause
    )

    query = f"""
    SELECT

        o.purchase_year AS Year,

        o.purchase_month AS Month,

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

    {alert_where_clause}

    GROUP BY

        o.purchase_year,
        o.purchase_month;
    """

    df = load_data(query)

    # --------------------------------------------------------
    # Not enough data
    # --------------------------------------------------------

    if df.empty or len(df) < 2:

        return {
            "type": "info",
            "title": "📊 Revenue Alert",
            "message": (
                "Not enough monthly revenue data "
                "to calculate growth."
            )
        }

    # --------------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------------

    df = sort_monthly_data(df)

    df = df.dropna(
        subset=["Month_Number"]
    )

    if len(df) < 2:

        return {
            "type": "info",
            "title": "📊 Revenue Alert",
            "message": (
                "Not enough valid monthly revenue data "
                "to calculate growth."
            )
        }

    # --------------------------------------------------------
    # Previous and current month
    # --------------------------------------------------------

    previous_row = df.iloc[-2]
    current_row = df.iloc[-1]

    previous_revenue = float(
        previous_row["Revenue"]
    )

    current_revenue = float(
        current_row["Revenue"]
    )

    # --------------------------------------------------------
    # Prevent division by zero
    # --------------------------------------------------------

    if previous_revenue == 0:

        return {
            "type": "info",
            "title": "📊 Revenue Alert",
            "message": (
                "Revenue cannot be compared because "
                "the previous month had zero revenue."
            )
        }

    # --------------------------------------------------------
    # Calculate growth
    # --------------------------------------------------------

    growth = (
        (current_revenue - previous_revenue)
        / previous_revenue
    ) * 100

    # --------------------------------------------------------
    # Revenue decline
    # --------------------------------------------------------

    if growth < 0:

        return {
            "type": "danger",
            "title": "📉 Revenue Decline",
            "message": (
                f"Revenue decreased by "
                f"{abs(growth):.1f}% "
                f"compared with the previous month."
            )
        }

    # --------------------------------------------------------
    # Revenue growth
    # --------------------------------------------------------

    elif growth > 0:

        return {
            "type": "success",
            "title": "🚀 Revenue Growth",
            "message": (
                f"Revenue increased by "
                f"{growth:.1f}% "
                f"compared with the previous month."
            )
        }

    # --------------------------------------------------------
    # No change
    # --------------------------------------------------------

    else:

        return {
            "type": "info",
            "title": "📊 Revenue Stable",
            "message": (
                "Revenue remained unchanged "
                "compared with the previous month."
            )
        }

    
# ============================================================
# 2. ORDER ALERT
# ============================================================

def get_order_alert(where_clause=""):

    query = f"""
    SELECT

        o.purchase_year AS Year,

        o.purchase_month AS Month,

        COUNT(
            DISTINCT o.order_id
        ) AS Orders

    FROM orders o

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    {where_clause}

    GROUP BY

        o.purchase_year,
        o.purchase_month;
    """

    df = load_data(query)

    # --------------------------------------------------------
    # Not enough data
    # --------------------------------------------------------

    if df.empty or len(df) < 2:

        return {
            "type": "info",
            "title": "📦 Order Alert",
            "message": (
                "Not enough monthly order data "
                "to calculate a reliable trend."
            )
        }

    # --------------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------------

    df = sort_monthly_data(df)

    df = df.dropna(
        subset=["Month_Number"]
    )

    if len(df) < 2:

        return {
            "type": "info",
            "title": "📦 Order Alert",
            "message": (
                "Not enough valid monthly order data."
            )
        }

    # --------------------------------------------------------
    # Get previous and current month
    # --------------------------------------------------------

    previous_row = df.iloc[-2]
    current_row = df.iloc[-1]

    previous_orders = float(
        previous_row["Orders"]
    )

    current_orders = float(
        current_row["Orders"]
    )

    current_month = current_row["Month"]
    current_year = current_row["Year"]

    previous_month = previous_row["Month"]

    # --------------------------------------------------------
    # Division by zero
    # --------------------------------------------------------

    if previous_orders == 0:

        return {
            "type": "info",
            "title": "📦 Order Alert",
            "message": (
                f"{current_month} {current_year} recorded "
                f"{int(current_orders):,} orders, but the "
                f"previous month had zero orders."
            )
        }

    # --------------------------------------------------------
    # Growth
    # --------------------------------------------------------

    growth = (
        (current_orders - previous_orders)
        / previous_orders
    ) * 100

    # --------------------------------------------------------
    # Order decline
    # --------------------------------------------------------

    if growth <= -10:

        return {
            "type": "warning",
            "title": "📦 Order Decline",
            "message": (
                f"Orders decreased by {abs(growth):.1f}% "
                f"from {previous_month} to "
                f"{current_month} {current_year}."
            )
        }

    # --------------------------------------------------------
    # Order growth
    # --------------------------------------------------------

    elif growth >= 10:

        return {
            "type": "success",
            "title": "📦 Order Growth",
            "message": (
                f"Orders increased by {growth:.1f}% "
                f"from {previous_month} to "
                f"{current_month} {current_year}."
            )
        }

    # --------------------------------------------------------
    # Stable
    # --------------------------------------------------------

    else:

        return {
            "type": "info",
            "title": "📦 Orders Stable",
            "message": (
                f"Orders changed by {growth:.1f}% "
                f"from {previous_month} to "
                f"{current_month} {current_year}."
            )
        }


# ============================================================
# 3. CATEGORY ALERT
# ============================================================

def get_category_alert(where_clause=""):

    query = f"""
    SELECT

        p.product_category_name_english AS Category,

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

    LIMIT 10;
    """

    df = load_data(query)

    if df.empty:

        return {
            "type": "info",
            "title": "🏷 Category Alert",
            "message": (
                "No category data available."
            )
        }

    top_category = df.iloc[0]["Category"]

    top_revenue = float(
        df.iloc[0]["Revenue"]
    )

    return {
        "type": "success",
        "title": "🏆 Top Category",
        "message": (
            f"{top_category} is currently the "
            f"highest revenue-generating category "
            f"with ₹{top_revenue:,.2f} in revenue."
        )
    }


# ============================================================
# 4. STATE ALERT
# ============================================================

def get_state_alert(where_clause=""):

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

    LIMIT 10;
    """

    df = load_data(query)

    if df.empty:

        return {
            "type": "info",
            "title": "📍 State Alert",
            "message": (
                "No state data available."
            )
        }

    best_state = df.iloc[0]["State"]

    best_revenue = float(
        df.iloc[0]["Revenue"]
    )

    return {
        "type": "success",
        "title": "📍 Best State",
        "message": (
            f"{best_state} is the highest "
            f"revenue-generating state with "
            f"₹{best_revenue:,.2f} in revenue."
        )
    }


# ============================================================
# 5. PAYMENT ALERT
# ============================================================

def get_payment_alert(where_clause=""):

    query = f"""
    SELECT

        op.payment_type AS Payment_Method,

        ROUND(
            SUM(op.payment_value),
            2
        ) AS Payment_Value

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

    df = load_data(query)

    if df.empty:

        return {
            "type": "info",
            "title": "💳 Payment Alert",
            "message": (
                "No payment data available."
            )
        }

    top_payment = df.iloc[0]["Payment_Method"]

    top_value = float(
        df.iloc[0]["Payment_Value"]
    )

    return {
        "type": "info",
        "title": "💳 Top Payment Method",
        "message": (
            f"{top_payment} has the highest "
            f"payment value at "
            f"₹{top_value:,.2f}."
        )
    }


# ============================================================
# 6. GET ALL ALERTS
# ============================================================

def get_all_alerts(where_clause=""):

    alerts = []

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    try:

        alerts.append(
            get_revenue_alert(
                where_clause
            )
        )

    except Exception as e:

        alerts.append({
            "type": "danger",
            "title": "🚨 Revenue Alert Error",
            "message": str(e)
        })

    # --------------------------------------------------------
    # Orders
    # --------------------------------------------------------

    try:

        alerts.append(
            get_order_alert(
                where_clause
            )
        )

    except Exception as e:

        alerts.append({
            "type": "danger",
            "title": "🚨 Order Alert Error",
            "message": str(e)
        })

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    try:

        alerts.append(
            get_category_alert(
                where_clause
            )
        )

    except Exception as e:

        alerts.append({
            "type": "danger",
            "title": "🚨 Category Alert Error",
            "message": str(e)
        })

    # --------------------------------------------------------
    # State
    # --------------------------------------------------------

    try:

        alerts.append(
            get_state_alert(
                where_clause
            )
        )

    except Exception as e:

        alerts.append({
            "type": "danger",
            "title": "🚨 State Alert Error",
            "message": str(e)
        })

    # --------------------------------------------------------
    # Payment
    # --------------------------------------------------------

    try:

        alerts.append(
            get_payment_alert(
                where_clause
            )
        )

    except Exception as e:

        alerts.append({
            "type": "danger",
            "title": "🚨 Payment Alert Error",
            "message": str(e)
        })

    return alerts


# ============================================================
# END OF FILE
# ============================================================