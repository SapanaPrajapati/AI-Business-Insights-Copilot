import streamlit as st
import pandas as pd
import plotly.express as px

from database import load_data
from alerts import get_all_alerts
from ai import (
    ask_ai,
    get_business_data,
    generate_business_recommendations
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Business Insights Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background-color: #F8FAFC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #111827;
}

section[data-testid="stSidebar"] p {
    color: #6B7280;
}


/* ============================================================
   HEADINGS
   ============================================================ */

.dashboard-title {
    font-size: 32px;
    font-weight: 750;
    color: #111827;
    margin-bottom: 2px;
}

.dashboard-subtitle {
    font-size: 14px;
    color: #6B7280;
    margin-bottom: 22px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-top: 25px;
    margin-bottom: 3px;
}

.section-description {
    font-size: 13px;
    color: #6B7280;
    margin-bottom: 15px;
}


/* ============================================================
   KPI METRICS
   ============================================================ */

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 17px 18px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #6B7280 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 25px !important;
    font-weight: 750 !important;
}


/* ============================================================
   CONTAINERS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    min-height: 40px;
}

.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="select"] > div {
    border-radius: 8px;
}

div[data-testid="stTextInput"] input {
    border-radius: 8px;
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 10px;
}


/* ============================================================
   CHARTS
   ============================================================ */

.js-plotly-plot {
    border-radius: 10px;
}


/* ============================================================
   TABLES
   ============================================================ */

div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}


/* ============================================================
   AI SECTION
   ============================================================ */

.ai-header {
    background-color: #EFF6FF;
    border: 1px solid #DBEAFE;
    border-radius: 12px;
    padding: 16px 18px;
    margin-top: 10px;
    margin-bottom: 15px;
}

.ai-header-title {
    color: #1E3A8A;
    font-size: 20px;
    font-weight: 750;
}

.ai-header-text {
    color: #4B5563;
    font-size: 13px;
    margin-top: 3px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: #9CA3AF;
    font-size: 12px;
    padding-top: 30px;
    line-height: 1.7;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .dashboard-title {
        font-size: 27px;
    }

    .section-title {
        font-size: 20px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 22px !important;
    }
}


@media (max-width: 600px) {

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .dashboard-title {
        font-size: 23px;
    }

    .dashboard-subtitle {
        font-size: 12px;
    }

    .section-title {
        font-size: 18px;
    }

    .section-description {
        font-size: 12px;
    }

    div[data-testid="stMetric"] {
        padding: 14px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def show_section(title, description=None):

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )

    if description:
        st.markdown(
            f'<div class="section-description">{description}</div>',
            unsafe_allow_html=True
        )


def format_currency(value):
    try:
        return f"₹{float(value):,.0f}"
    except Exception:
        return "₹0"


def format_number(value):
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"


def show_business_alert(alert):

    alert_type = alert.get("type", "info")

    title = alert.get(
        "title",
        "Business Alert"
    )

    message = alert.get(
        "message",
        ""
    )

    if alert_type == "danger":

        st.error(
            f"**{title}**\n\n{message}"
        )

    elif alert_type == "warning":

        st.warning(
            f"**{title}**\n\n{message}"
        )

    elif alert_type == "success":

        st.success(
            f"**{title}**\n\n{message}"
        )

    else:

        st.info(
            f"**{title}**\n\n{message}"
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">📊 AI Business Insights Copilot</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="dashboard-subtitle">
        Brazilian Olist E-Commerce Intelligence Platform
        &nbsp;•&nbsp; Python
        &nbsp;•&nbsp; MySQL
        &nbsp;•&nbsp; Power BI
        &nbsp;•&nbsp; Streamlit
        &nbsp;•&nbsp; Gemini AI
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Dashboard")

st.sidebar.caption(
    "Use the filters to explore business performance."
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎛️ Filters")


# ============================================================
# LOAD FILTER VALUES
# ============================================================

years = load_data(
    """
    SELECT DISTINCT purchase_year
    FROM orders
    WHERE purchase_year IS NOT NULL
    ORDER BY purchase_year
    """
)

months = load_data(
    """
    SELECT DISTINCT purchase_month
    FROM orders
    WHERE purchase_month IS NOT NULL
    """
)

states = load_data(
    """
    SELECT DISTINCT customer_state
    FROM customers
    WHERE customer_state IS NOT NULL
    ORDER BY customer_state
    """
)

categories = load_data(
    """
    SELECT DISTINCT product_category_name_english
    FROM products
    WHERE product_category_name_english IS NOT NULL
    ORDER BY product_category_name_english
    """
)


# ============================================================
# MONTH ORDER
# ============================================================

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


if not months.empty:

    available_months = [
        month
        for month in month_order
        if month in months[
            "purchase_month"
        ].astype(str).tolist()
    ]

else:

    available_months = []


# ============================================================
# CLEAR FILTERS
# ============================================================

def clear_filters():

    st.session_state["year_filter"] = "All"
    st.session_state["month_filter"] = "All"
    st.session_state["state_filter"] = "All"
    st.session_state["category_filter"] = "All"


# ============================================================
# FILTERS
# ============================================================

selected_year = st.sidebar.selectbox(
    "📅 Year",
    ["All"] + (
        years["purchase_year"]
        .astype(str)
        .tolist()
        if not years.empty
        else []
    ),
    key="year_filter"
)


selected_month = st.sidebar.selectbox(
    "📆 Month",
    ["All"] + available_months,
    key="month_filter"
)


selected_state = st.sidebar.selectbox(
    "📍 State",
    ["All"] + (
        states["customer_state"]
        .astype(str)
        .tolist()
        if not states.empty
        else []
    ),
    key="state_filter"
)


selected_category = st.sidebar.selectbox(
    "🏷️ Category",
    ["All"] + (
        categories[
            "product_category_name_english"
        ]
        .astype(str)
        .tolist()
        if not categories.empty
        else []
    ),
    key="category_filter"
)


st.sidebar.button(
    "🧹 Clear Filters",
    on_click=clear_filters,
    use_container_width=True
)


# ============================================================
# SIDEBAR ABOUT
# ============================================================

st.sidebar.markdown("---")

with st.sidebar.expander("ℹ️ About"):

    st.write(
        """
        **AI Business Insights Copilot**

        An end-to-end analytics application built using
        the Brazilian Olist E-Commerce dataset.

        **Stack**

        • Python  
        • MySQL  
        • Power BI  
        • Streamlit  
        • Gemini AI

        **Features**

        • Business KPIs  
        • Revenue analysis  
        • Category analysis  
        • Product analysis  
        • State analysis  
        • Payment analysis  
        • Business alerts  
        • AI Q&A  
        • AI recommendations
        """
    )


# ============================================================
# SQL FILTER CONDITIONS
# ============================================================

conditions = []


if selected_year != "All":

    conditions.append(
        f"o.purchase_year = {int(selected_year)}"
    )


if selected_month != "All":

    safe_month = selected_month.replace(
        "'",
        "''"
    )

    conditions.append(
        f"o.purchase_month = '{safe_month}'"
    )


if selected_state != "All":

    safe_state = selected_state.replace(
        "'",
        "''"
    )

    conditions.append(
        f"c.customer_state = '{safe_state}'"
    )


if selected_category != "All":

    safe_category = selected_category.replace(
        "'",
        "''"
    )

    conditions.append(
        "p.product_category_name_english "
        f"= '{safe_category}'"
    )


if conditions:

    where_clause = (
        "WHERE "
        + " AND ".join(conditions)
    )

else:

    where_clause = ""


# ============================================================
# FILTER STATUS
# ============================================================

active_filters = []

if selected_year != "All":
    active_filters.append(
        f"Year: {selected_year}"
    )

if selected_month != "All":
    active_filters.append(
        f"Month: {selected_month}"
    )

if selected_state != "All":
    active_filters.append(
        f"State: {selected_state}"
    )

if selected_category != "All":
    active_filters.append(
        f"Category: {selected_category}"
    )


if active_filters:

    st.info(
        "🔎 **Active Filters:** "
        + "  •  ".join(active_filters)
    )

else:

    st.success(
        "🌎 **Overall Business View** — "
        "Showing complete business performance."
    )


# ============================================================
# KPI QUERY
# ============================================================

kpi_query = f"""
SELECT

    COUNT(DISTINCT o.order_id) AS Orders,

    COUNT(DISTINCT o.customer_id) AS Customers,

    ROUND(
        COALESCE(SUM(oi.price), 0),
        2
    ) AS Revenue,

    COUNT(DISTINCT oi.seller_id) AS Sellers

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN products p
    ON oi.product_id = p.product_id

{where_clause}
"""


kpi = load_data(
    kpi_query
)


# ============================================================
# KPI VALUES
# ============================================================

if not kpi.empty:

    revenue = kpi["Revenue"].iloc[0] or 0
    orders = kpi["Orders"].iloc[0] or 0
    customers = kpi["Customers"].iloc[0] or 0
    sellers = kpi["Sellers"].iloc[0] or 0

else:

    revenue = 0
    orders = 0
    customers = 0
    sellers = 0


# ============================================================
# BUSINESS OVERVIEW
# ============================================================

show_section(
    "📌 Business Overview",
    "Key business metrics for the selected filters."
)


kpi1, kpi2, kpi3, kpi4 = st.columns(
    4,
    gap="medium"
)


with kpi1:

    st.metric(
        label="💰 Total Revenue",
        value=format_currency(revenue)
    )


with kpi2:

    st.metric(
        label="📦 Total Orders",
        value=format_number(orders)
    )


with kpi3:

    st.metric(
        label="👥 Customers",
        value=format_number(customers)
    )


with kpi4:

    st.metric(
        label="🏪 Sellers",
        value=format_number(sellers)
    )


# ============================================================
# BUSINESS SNAPSHOT
# ============================================================

show_section(
    "💡 Business Snapshot",
    "A quick view of the current business position."
)


snapshot1, snapshot2 = st.columns(
    [2, 1],
    gap="medium"
)


with snapshot1:

    with st.container(border=True):

        st.markdown("### Current Performance")

        snapshot_col1, snapshot_col2 = st.columns(2)

        with snapshot_col1:

            st.write(
                f"**Revenue:** {format_currency(revenue)}"
            )

            st.write(
                f"**Orders:** {format_number(orders)}"
            )

        with snapshot_col2:

            st.write(
                f"**Customers:** {format_number(customers)}"
            )

            st.write(
                f"**Sellers:** {format_number(sellers)}"
            )


with snapshot2:

    if orders > 0:

        aov = revenue / orders

    else:

        aov = 0

    with st.container(border=True):

        st.metric(
            "💳 Average Order Value",
            f"₹{aov:,.2f}"
        )

        st.caption(
            "Revenue ÷ unique orders"
        )


# ============================================================
# BUSINESS ALERTS
# ============================================================

show_section(
    "🚨 Business Alerts",
    "Automated signals from the current business data."
)


try:

    alerts = get_all_alerts(
        where_clause
    )

except Exception as e:

    alerts = []

    st.warning(
        "Business alerts could not be loaded."
    )

    with st.expander(
        "View technical details"
    ):

        st.code(
            str(e)
        )


if alerts:

    alert_columns = st.columns(
        min(3, len(alerts)),
        gap="medium"
    )

    for index, alert in enumerate(alerts):

        with alert_columns[
            index % len(alert_columns)
        ]:

            show_business_alert(alert)

else:

    st.info(
        "No business alerts are available "
        "for the current filters."
    )


# ============================================================
# MONTHLY REVENUE
# ============================================================

monthly_revenue_query = f"""
SELECT

    o.purchase_year,

    o.purchase_month,

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

    o.purchase_year,
    o.purchase_month
"""


monthly_revenue = load_data(
    monthly_revenue_query
)


if not monthly_revenue.empty:

    monthly_revenue[
        "month_number"
    ] = (
        monthly_revenue[
            "purchase_month"
        ].map(
            {
                month: index
                for index, month
                in enumerate(
                    month_order,
                    1
                )
            }
        )
    )

    monthly_revenue = (
        monthly_revenue
        .sort_values(
            [
                "purchase_year",
                "month_number"
            ]
        )
    )


# ============================================================
# CATEGORY DATA
# ============================================================

category_query = f"""
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

LIMIT 10
"""


category_df = load_data(
    category_query
)


# ============================================================
# PRODUCT DATA
# ============================================================

product_query = f"""
SELECT

    oi.product_id AS Product,

    ROUND(
        SUM(oi.price),
        2
    ) AS Revenue

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

LIMIT 10
"""


product_df = load_data(
    product_query
)


# ============================================================
# STATE DATA
# ============================================================

state_query = f"""
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

LIMIT 10
"""


state_df = load_data(
    state_query
)


# ============================================================
# BUSINESS PERFORMANCE
# ============================================================

show_section(
    "📊 Business Performance",
    "Interactive analysis of revenue, categories, products and geography."
)


# ============================================================
# CHART TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Revenue",
        "🏷️ Categories",
        "📦 Products",
        "📍 States"
    ]
)


# ============================================================
# TAB 1 — REVENUE
# ============================================================

with tab1:

    if not monthly_revenue.empty:

        fig_month = px.line(
            monthly_revenue,
            x="purchase_month",
            y="Revenue",
            color=(
                "purchase_year"
                if monthly_revenue[
                    "purchase_year"
                ].nunique() > 1
                else None
            ),
            markers=True,
            hover_data={
                "purchase_year": True,
                "Revenue": ":,.2f"
            }
        )

        fig_month.update_traces(
            line_width=3,
            marker_size=7
        )

        fig_month.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10
            ),
            xaxis_title="Month",
            yaxis_title="Revenue",
            hovermode="x unified",
            legend_title="Year"
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )

    else:

        st.info(
            "No monthly revenue data available "
            "for the selected filters."
        )


# ============================================================
# TAB 2 — CATEGORIES
# ============================================================

with tab2:

    if not category_df.empty:

        category_chart = (
            category_df
            .sort_values(
                "Revenue",
                ascending=True
            )
        )

        fig_category = px.bar(
            category_chart,
            x="Revenue",
            y="Category",
            orientation="h",
            text_auto=".2s",
            hover_data={
                "Revenue": ":,.2f"
            }
        )

        fig_category.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10
            ),
            xaxis_title="Revenue",
            yaxis_title=None
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    else:

        st.info(
            "No category data available "
            "for the selected filters."
        )


# ============================================================
# TAB 3 — PRODUCTS
# ============================================================

with tab3:

    if not product_df.empty:

        product_chart = (
            product_df
            .sort_values(
                "Revenue",
                ascending=True
            )
            .copy()
        )

        product_chart[
            "Product Display"
        ] = (
            product_chart["Product"]
            .astype(str)
            .str[:12]
        )

        fig_product = px.bar(
            product_chart,
            x="Revenue",
            y="Product Display",
            orientation="h",
            text_auto=".2s",
            hover_data={
                "Product": True,
                "Revenue": ":,.2f"
            }
        )

        fig_product.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10
            ),
            xaxis_title="Revenue",
            yaxis_title="Product ID"
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True
        )

        st.caption(
            "Olist provides Product IDs rather than descriptive product names."
        )

    else:

        st.info(
            "No product data available "
            "for the selected filters."
        )


# ============================================================
# TAB 4 — STATES
# ============================================================

with tab4:

    if not state_df.empty:

        state_chart = (
            state_df
            .sort_values(
                "Revenue",
                ascending=True
            )
        )

        fig_state = px.bar(
            state_chart,
            x="Revenue",
            y="State",
            orientation="h",
            text_auto=".2s",
            hover_data={
                "Revenue": ":,.2f"
            }
        )

        fig_state.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10
            ),
            xaxis_title="Revenue",
            yaxis_title="State"
        )

        st.plotly_chart(
            fig_state,
            use_container_width=True
        )

    else:

        st.info(
            "No state data available "
            "for the selected filters."
        )


# ============================================================
# PERFORMANCE HIGHLIGHTS
# ============================================================

show_section(
    "🏆 Performance Highlights",
    "Top-performing areas based on the current dashboard filters."
)


highlight1, highlight2, highlight3, highlight4 = st.columns(
    4,
    gap="medium"
)


with highlight1:

    if not category_df.empty:

        st.metric(
            "🏷️ Top Category",
            str(
                category_df.iloc[0]["Category"]
            )
        )

        st.caption(
            "Revenue: "
            + format_currency(
                category_df.iloc[0]["Revenue"]
            )
        )

    else:

        st.metric(
            "🏷️ Top Category",
            "N/A"
        )


with highlight2:

    if not state_df.empty:

        st.metric(
            "📍 Best State",
            str(
                state_df.iloc[0]["State"]
            )
        )

        st.caption(
            "Revenue: "
            + format_currency(
                state_df.iloc[0]["Revenue"]
            )
        )

    else:

        st.metric(
            "📍 Best State",
            "N/A"
        )


with highlight3:

    if not product_df.empty:

        st.metric(
            "📦 Top Product ID",
            str(
                product_df.iloc[0]["Product"]
            )[:12]
        )

        st.caption(
            "Revenue: "
            + format_currency(
                product_df.iloc[0]["Revenue"]
            )
        )

    else:

        st.metric(
            "📦 Top Product ID",
            "N/A"
        )


with highlight4:

    st.metric(
        "💳 Average Order Value",
        f"₹{aov:,.2f}"
    )

    st.caption(
        "Revenue ÷ unique orders"
    )


# ============================================================
# PAYMENT ANALYSIS
# ============================================================

show_section(
    "💳 Payment Method Analysis",
    "Distribution of payment methods in the selected data."
)


payment_query = f"""
SELECT

    op.payment_type AS Payment_Type,

    COUNT(*) AS Total_Payments

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

    Total_Payments DESC
"""


try:

    payment_df = load_data(
        payment_query
    )

except Exception:

    payment_df = pd.DataFrame()


if not payment_df.empty:

    payment1, payment2 = st.columns(
        [1.7, 1],
        gap="medium"
    )

    with payment1:

        fig_payment = px.pie(
            payment_df,
            names="Payment_Type",
            values="Total_Payments",
            hole=0.55
        )

        fig_payment.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            )
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )

    with payment2:

        with st.container(border=True):

            st.markdown(
                "### Payment Summary"
            )

            st.dataframe(
                payment_df,
                use_container_width=True,
                hide_index=True
            )

else:

    st.info(
        "Payment data is currently unavailable."
    )


# ============================================================
# DOWNLOAD ANALYTICS
# ============================================================

show_section(
    "⬇️ Download Analytics",
    "Export the analytical datasets displayed in the dashboard."
)


download1, download2, download3 = st.columns(
    3,
    gap="medium"
)


with download1:

    st.markdown("**🏷️ Category Analysis**")

    st.caption(
        "Top categories by revenue"
    )

    if not category_df.empty:

        st.download_button(
            "⬇️ Download CSV",
            data=category_df.to_csv(
                index=False
            ),
            file_name="top_categories.csv",
            mime="text/csv",
            use_container_width=True
        )


with download2:

    st.markdown("**📍 State Analysis**")

    st.caption(
        "Top states by revenue"
    )

    if not state_df.empty:

        st.download_button(
            "⬇️ Download CSV",
            data=state_df.to_csv(
                index=False
            ),
            file_name="revenue_by_state.csv",
            mime="text/csv",
            use_container_width=True
        )


with download3:

    st.markdown("**📦 Product Analysis**")

    st.caption(
        "Top products by revenue"
    )

    if not product_df.empty:

        st.download_button(
            "⬇️ Download CSV",
            data=product_df.to_csv(
                index=False
            ),
            file_name="top_products.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# AI BUSINESS COPILOT
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
<div class="ai-header">
<div class="ai-header-title">🤖 AI Business Copilot</div>
<div class="ai-header-text">
Ask Gemini questions about revenue, products, categories,
states, trends, risks and business opportunities.
</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

st.markdown(
    "#### 💡 Suggested Questions"
)


suggestions = [
    (
        "🏷️ Best Category",
        "Which product category generates the highest revenue and why?"
    ),
    (
        "📍 Best State",
        "Which state generates the highest revenue and what should the business do?"
    ),
    (
        "📈 Revenue Trend",
        "What are the most important revenue trends in the available data?"
    ),
    (
        "📦 Top Products",
        "Which products generate the most revenue?"
    ),
    (
        "🚨 Business Risk",
        "What are the biggest business risks visible in the current data?"
    ),
    (
        "🚀 Growth Opportunity",
        "What is the biggest growth opportunity for this business?"
    )
]


suggestion_columns = st.columns(
    3,
    gap="small"
)


for index, (
    label,
    prompt
) in enumerate(suggestions):

    with suggestion_columns[
        index % 3
    ]:

        if st.button(
            label,
            key=f"ai_suggestion_{index}",
            use_container_width=True
        ):

            st.session_state[
                "ai_question"
            ] = prompt


# ============================================================
# AI QUESTION
# ============================================================

question = st.text_input(
    "Ask your business question",
    value=st.session_state.get(
        "ai_question",
        ""
    ),
    placeholder=(
        "Example: Which category should I invest in?"
    ),
    key="question_input"
)


# ============================================================
# ASK GEMINI
# ============================================================

if st.button(
    "🤖 Ask Gemini",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a business question first."
        )

    else:

        try:

            # =================================================
            # BUILD BUSINESS CONTEXT
            # =================================================

            business_context = f"""
CURRENT DASHBOARD SUMMARY

Revenue:
₹{revenue:,.2f}

Orders:
{int(orders):,}

Customers:
{int(customers):,}

Sellers:
{int(sellers):,}


CURRENT FILTERS

Year:
{selected_year}

Month:
{selected_month}

State:
{selected_state}

Category:
{selected_category}
"""


            # =================================================
            # CATEGORY
            # =================================================

            if not category_df.empty:

                business_context += """

TOP CATEGORIES BY REVENUE

"""

                business_context += (
                    category_df.to_string(
                        index=False
                    )
                )


            # =================================================
            # STATES
            # =================================================

            if not state_df.empty:

                business_context += """

TOP STATES BY REVENUE

"""

                business_context += (
                    state_df.to_string(
                        index=False
                    )
                )


            # =================================================
            # PRODUCTS
            # =================================================

            if not product_df.empty:

                business_context += """

TOP PRODUCTS BY REVENUE

IMPORTANT:
The Olist dataset does not contain descriptive
product names. Product IDs are used instead.

"""

                business_context += (
                    product_df.to_string(
                        index=False
                    )
                )


            # =================================================
            # MONTHLY REVENUE
            # =================================================

            if not monthly_revenue.empty:

                business_context += """

MONTHLY REVENUE

"""

                monthly_ai_data = (
                    monthly_revenue[
                        [
                            "purchase_year",
                            "purchase_month",
                            "Revenue"
                        ]
                    ]
                    .copy()
                )

                business_context += (
                    monthly_ai_data.to_string(
                        index=False
                    )
                )


            # =================================================
            # PAYMENT
            # =================================================

            if not payment_df.empty:

                business_context += """

PAYMENT METHOD DATA

"""

                business_context += (
                    payment_df.to_string(
                        index=False
                    )
                )


            # =================================================
            # DATA PREVIEW
            # =================================================

            with st.expander(
                "🔎 View data used for analysis"
            ):

                st.text(
                    business_context
                )


            # =================================================
            # GEMINI
            # =================================================

            with st.spinner(
                "🤖 Gemini is analyzing the business data..."
            ):

                business_data = get_business_data(
                    question
                )

                answer = ask_ai(
                    question,
                    business_data
                )


            # =================================================
            # RESPONSE
            # =================================================

            st.markdown(
                "### 🤖 Gemini Business Analysis"
            )

            if answer:

                st.success(
                    "AI analysis completed successfully."
                )

                st.markdown(
                    answer
                )

            else:

                st.warning(
                    "Gemini did not return a response."
                )


        except Exception as e:

            st.error(
                "⚠️ Unable to generate the AI response."
            )

            with st.expander(
                "View technical details"
            ):

                st.code(
                    str(e)
                )


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

show_section(
    "💡 AI Business Recommendations",
    "Use Gemini to identify actionable business opportunities."
)


with st.container(border=True):

    st.markdown(
        "### 🚀 Discover Growth Opportunities"
    )

    st.caption(
        "The recommendation engine evaluates business "
        "performance and suggests practical actions."
    )

    if st.button(
        "🤖 Generate AI Recommendations",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 AI is analyzing business performance..."
        ):

            try:

                recommendations = (
                    generate_business_recommendations()
                )

                if recommendations:

                    st.success(
                        "AI recommendation analysis completed."
                    )

                    st.markdown(
                        recommendations
                    )

                else:

                    st.warning(
                        "No recommendations were generated."
                    )

            except Exception as e:

                st.error(
                    "⚠️ Unable to generate AI recommendations right now."
                )

                with st.expander(
                    "View technical details"
                ):

                    st.code(
                        str(e)
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
<strong>AI Business Insights Copilot</strong>
<br>
Python • MySQL • Power BI • Streamlit • Gemini AI
<br>
Brazilian Olist E-Commerce Dataset
<br>
End-to-End Business Intelligence & AI Analytics Project
</div>
""",
    unsafe_allow_html=True
)