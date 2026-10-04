# 🤖 AI Business Insights Copilot

> **An AI-powered business analytics application that transforms e-commerce data into actionable insights using SQL, Python, interactive dashboards, and natural-language business queries.**

## 📌 Overview

**AI Business Insights Copilot** is an end-to-end e-commerce analytics project built to help business users explore sales data, identify trends, monitor key performance indicators, and generate actionable business insights without requiring them to write SQL queries manually.

The project uses the **Brazilian Olist E-commerce dataset** and combines data engineering, SQL analytics, Python-based analysis, visualization, and an AI-powered interface into a single business intelligence application.

The goal is to bridge the gap between **raw business data and decision-making** by allowing users to interact with data in a simple and business-friendly way.

---

## 🎯 Business Objectives

The project focuses on answering practical business questions such as:

* 📈 How are sales and revenue performing over time?
* 🛍️ Which product categories generate the most revenue?
* 🌎 Which locations contribute the most to sales?
* 👥 What customer trends can be identified?
* 🚚 How does delivery performance affect customer experience?
* ⭐ Which factors are associated with better or worse reviews?
* 💳 What are the major payment patterns?
* ⚠️ Are there unusual changes or business performance alerts?
* 💡 What actions can the business take based on the available data?

---

## ✨ Key Features

### 📊 Interactive Business Dashboard

Provides an interactive view of important business KPIs and trends, including:

* Revenue and sales performance
* Order volume
* Customer activity
* Product/category performance
* Payment analysis
* Review insights
* Geographic analysis
* Time-based trends

### 🤖 AI Business Insights

Users can ask business questions using natural language instead of manually writing SQL queries.

For example:

```text
Which product categories generated the highest revenue?

What were the sales trends over time?

Which states have the highest number of orders?

What business areas require attention?
```

The application converts business questions into data-driven insights to support faster decision-making.

### 🗄️ SQL-Based Data Analysis

The project uses a relational database to store and analyze multiple interconnected e-commerce datasets.

Key analytical areas include:

* Sales analysis
* Customer analysis
* Product analysis
* Payment analysis
* Seller analysis
* Review analysis
* Order and delivery analysis

### 🚨 Business Alerts

The application includes business-focused alerts to help identify unusual or important changes in performance.

### 📈 Data Visualization

Interactive charts and visualizations are used to make trends, patterns, and business performance easier to understand.

---

## 🗂️ Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains multiple interconnected tables covering different aspects of the e-commerce business.

### Main datasets

| Dataset              | Description                          |
| -------------------- | ------------------------------------ |
| Customers            | Customer information and locations   |
| Orders               | Order lifecycle and timestamps       |
| Order Items          | Products included in each order      |
| Payments             | Payment types and transaction values |
| Products             | Product-level information            |
| Sellers              | Seller information and locations     |
| Reviews              | Customer review scores and comments  |
| Geolocation          | Brazilian geographic information     |
| Category Translation | Product category translations        |

These datasets are combined to create a comprehensive view of the e-commerce business.

---

## 🏗️ Project Architecture

```text
                    Olist E-Commerce Dataset
                              │
                              ▼
                    Data Cleaning & Preparation
                              │
                              ▼
                    ┌──────────────────────┐
                    │      MySQL Database  │
                    └──────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          SQL Business Analysis      Python Analysis
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    Business Insights Layer
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Interactive Dashboard       AI Copilot
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    Business Decision Support
```

---

## 🛠️ Tech Stack

### Programming & Data Analysis

* **Python**
* **Pandas**
* **NumPy**

### Database & SQL

* **MySQL**
* SQL queries
* Joins
* Aggregations
* Window functions
* Business analysis queries

### Visualization & BI

* **Power BI**
* Interactive data visualizations
* KPI analysis
* Business dashboards

### Application

* **Streamlit**
* Python-based interactive web application

### AI

* AI-powered natural-language business analysis
* Natural-language business queries
* Automated insight generation

### Development Tools

* VS Code
* Jupyter / Google Colab
* Git
* GitHub

---

## 📁 Project Structure

```text
AI-Business-Insights-Copilot/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── docs/
│
├── powerbi/
│
├── python/
│   └── Data processing & database scripts
│
├── streamlit/
│   ├── app.py
│   ├── ai.py
│   ├── alerts.py
│   ├── business_queries.py
│   ├── charts.py
│   ├── database.py
│   └── ...
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🔄 Data & Analysis Workflow

The project follows an end-to-end analytics workflow:

### 1. Data Collection

Collected and organized the Olist e-commerce datasets.

### 2. Data Cleaning

Performed data preparation and cleaning using Python, including handling:

* Missing values
* Duplicate records
* Data types
* Date/time fields
* Inconsistent values
* Relationships between datasets

### 3. Database Integration

Loaded the cleaned datasets into **MySQL** and created a relational data structure for analysis.

### 4. SQL Analysis

Developed business queries to calculate KPIs and answer business questions using SQL.

### 5. Data Visualization

Created dashboards and visualizations to identify trends and patterns.

### 6. AI Integration

Added an AI-powered business analysis layer that allows users to interact with the data using natural-language questions.

### 7. Streamlit Application

Integrated the analytics components into an interactive Streamlit application.

---

## 📊 Example Business Insights

The application is designed to help answer questions such as:

### Sales Performance

* Revenue trends by month
* Order volume over time
* Average order value
* Sales performance by category

### Customer Analysis

* Customer distribution
* Customer locations
* Repeat purchasing patterns
* Customer activity trends

### Product Analysis

* Top-performing categories
* Product sales performance
* Revenue contribution by category

### Delivery & Customer Experience

* Delivery performance
* Review score distribution
* Relationship between delivery experience and reviews

### Payment Analysis

* Payment method distribution
* Payment value analysis
* Installment patterns

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.x
* MySQL
* Git

### 1. Clone the repository

```bash
git clone https://github.com/SapanaPrajapati/AI-Business-Insights-Copilot.git
```

```bash
cd AI-Business-Insights-Copilot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file for your local configuration.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ai_business_insights
DB_USER=your_username
DB_PASSWORD=your_password
```

Add any required AI/API configuration to your local `.env` file as well.

> ⚠️ **Never commit your `.env` file or API keys to GitHub.**

### 5. Configure the database

Create the required MySQL database and load the cleaned datasets using the database/import scripts provided in the project.

### 6. Run the Streamlit application

```bash
cd streamlit
streamlit run app.py
```

The application will open in your browser.

---



---

## 📸 Application Preview

> Screenshots and dashboard previews will be added here.

### Dashboard

```text
Executive Dashboard 
```
<img width="928" height="506" alt="Executive Dashboard" src="https://github.com/user-attachments/assets/82dc29f3-afb2-43f0-8762-4bf7717a87be" />

```text
Sales Dashboard 
```
<img width="924" height="506" alt="Sales Dashboard" src="https://github.com/user-attachments/assets/ebfa48fa-ba1c-4df2-89fc-ba9681eca788" />

```text
Customer Dashboard 
```
<img width="907" height="506" alt="customer" src="https://github.com/user-attachments/assets/c825c413-bcb2-4cd4-baf1-42ffc9fee105" />

```text
Products Dashboard 
```
<img width="888" height="501" alt="Product" src="https://github.com/user-attachments/assets/49e876ad-880a-4794-a3a5-d1cd4f79d5b4" />

```text
Sellers Dashboard 
```
<img width="897" height="504" alt="seller" src="https://github.com/user-attachments/assets/fa059392-addd-48f6-81b8-04b220f8a7f0" />


```text
Summary Dashboard 
```
<img width="896" height="508" alt="Summary" src="https://github.com/user-attachments/assets/3fbf39dc-f2f8-447b-a288-2726ec6a6e62" />


### AI Business Copilot

```text
Streamlit AI interface Screenshots 
```
<img width="1366" height="545" alt="image" src="https://github.com/user-attachments/assets/6361fd5e-9cb6-443d-a1d9-2e63ae49e769" />

<img width="1363" height="645" alt="image" src="https://github.com/user-attachments/assets/7fe549eb-9841-4b63-a85c-56c092a7d771" />
<img width="1116" height="585" alt="image" src="https://github.com/user-attachments/assets/e067c11a-0681-479b-a193-8b7c41b6b3e0" />

<img width="1129" height="548" alt="image" src="https://github.com/user-attachments/assets/d7129592-c8f2-4457-8531-e5d86ab438f9" />
<img width="1146" height="564" alt="image" src="https://github.com/user-attachments/assets/4313f32c-5c0a-4a73-be2d-f6398bc7662a" />
<img width="1137" height="567" alt="image" src="https://github.com/user-attachments/assets/238625bf-2a2d-4070-832d-ab2a0779fb64" />


### Business Insights

```text
 Bussines insights/chart screenshot
```
<img width="1062" height="451" alt="category" src="https://github.com/user-attachments/assets/015dfcf6-a97e-4ad1-bb71-c1911d6b6a8f" />
<img width="1050" height="495" alt="product" src="https://github.com/user-attachments/assets/d376f1fb-6c5d-44f3-bed6-2857e9af403f" />
<img width="1087" height="440" alt="revenue" src="https://github.com/user-attachments/assets/21f2b3e5-055e-427e-91f0-d415ce0e3969" />
<img width="1073" height="464" alt="state" src="https://github.com/user-attachments/assets/996f4587-78e8-469b-9b1d-28b6fe220892" />

---

## 🚧 Future Improvements

Planned improvements include:

* [ ] Deploy the Streamlit application
* [ ] Add a live demo
* [ ] Improve AI-generated business recommendations
* [ ] Add more advanced business alerts
* [ ] Add additional KPI dashboards
* [ ] Improve query handling and validation
* [ ] Add automated data refresh
* [ ] Add user-friendly documentation
* [ ] Add more advanced predictive analytics

---

## 💼 Skills Demonstrated

This project demonstrates practical experience in:

**Data Analysis**

* Data cleaning
* Exploratory data analysis
* KPI development
* Business analysis
* Trend analysis

**SQL**

* Joins
* Aggregations
* Subqueries
* Window functions
* Business-oriented queries

**Python**

* Pandas
* NumPy
* Data processing
* Visualization
* Application development

**Business Intelligence**

* Power BI
* Dashboard development
* KPI visualization
* Data storytelling

**AI & Analytics**

* Natural-language business queries
* AI-assisted data analysis
* Automated business insights

**Tools**

* MySQL
* Streamlit
* Git
* GitHub
* VS Code

---

## 🎓 Project Purpose

This project was developed as a practical **Data Analytics + AI portfolio project** to demonstrate how raw e-commerce data can be transformed into meaningful business insights through a combination of:

```text
Data → SQL → Python → Visualization → AI → Business Insights
```

The focus is not only on analyzing data, but also on making the insights **accessible and useful for business decision-making**.

---

## 👩‍💻 Author

**Sapana Prajapati**

Aspiring Data Analyst

📌 GitHub:
https://github.com/SapanaPrajapati

---

## ⭐ If you find this project useful

Feel free to explore the repository, provide feedback, or ⭐ the project.
