# 🚴 Bicycle Sales Dashboard – Interactive Analytics for Global Retail Performance
By working with real-world data, I’ll demonstrate how Pandas can efficiently handle and analyze complex, multi-file datasets typically encountered in data science projects.you’ll find it makes handling structured data much easier. It gives you flexible, intuitive tools to work with even the most complex datasets.

## Executive Summary
This interactive dashboard transforms raw bicycle sales data into actionable business intelligence using Python, Dash, and Plotly. Built from a real-world transactional dataset (sales.xlsx), it delivers real-time insights across product performance, regional sales, customer behavior, and operational metrics. Designed for sales leaders, product managers, and customer experience teams, the dashboard enables rapid decision-making—identifying top revenue drivers, regional gaps, and service improvement opportunities—all through an intuitive, browser-based interface.

## Business Problem
The organization faced fragmented visibility into its global bicycle sales operations:

* Sales data was trapped in static spreadsheets with no dynamic filtering or visualization.
* Leadership couldn’t quickly assess which product lines (e.g., E-Bikes, Mountain Bikes) or regions (North America, Europe, Asia) were outperforming or underperforming.
* Customer feedback and shipping/payment trends were not linked to sales outcomes, delaying service optimizations.

## Methodology
### Data Processing
* **Source:** data/sales.xlsx → "Sales Report" sheet (169+ records, 24 columns).
* **Cleaning:**
* Standardized European-style decimals (e.g., "1200,00" → 1200.0).
* Parsed Order Date using explicit format (%m/%d/%y).
* Excluded Cancelled orders for accurate KPI calculation.
* 
**Aggregation:** Grouped data by Product Category, Region, Month, Product Name, and Feedback for visualization.

**Dashboard Features**

* **KPI Summary:** Total Sales, Quantity, Avg. Order Value, Orders, Unique Customers.
* **Category & Regional Analysis:** Horizontal bar charts ranked by revenue.
* **Time Trends:** Monthly sales progression (Feb–May 2024).
* **Product Performance:** Top 10 best-selling models by revenue.
* **Customer Insights:** Feedback distribution (Positive/Neutral/Negative).
* **Operations:** Side-by-side comparison of Payment vs. Shipping method adoption.

**Tech Stack**
* **Backend:** Python (Pandas for ETL)
* **Frontend:** Dash + Plotly (responsive, interactive *charts)
* ** Styling:** Clean UI with flexbox layout, card-based KPIs, and consistent color semantics.
### Skills & Tools
* Languages=>Python
* Skills & ToolsData=>Pandas, Excel I/O, Data Cleaning
* Visualization=>Plotly Express, Plotly Graph Objects, Dash
* UI/UX=>HTML/CSS-in-Python, Responsive Design
* Deployment=>Local Flask server (debug=True)
### Results & Business Recommendations
**Key Findings from Live Data**
* **Top Revenue Category:** Mountain Bikes (≈45% of total active sales), led by Downhill and Cross Country subcategories.
* **Emerging Segment:** E-Bikes show high average order value ($3,000+), especially in Europe and North America.
* **Regional Leader:** North America drives the highest volume, but Europe shows strong premium product adoption.
* **Customer Sentiment:** 72% Positive, yet Negative feedback clusters around Road Bikes and Touring Bikes—flag for quality review.
* **Operational Preference:** Credit Card (60%) and Air Shipping (for premium orders) dominate.

**Strategic Recommendations**
* **Product Focus:** Scale inventory for high-margin models like DownhillDominator and E-TrailBlazer.
* **Regional Strategy:** Launch targeted E-Bike campaigns in Asia, where adoption is growing but still lags.
* **CX Improvement:** Investigate negative feedback on Road Bikes—potential issues with delivery speed or product specs.
* **Payment Optimization:** Promote PayPal for international orders (high usage in Europe/Asia).

### Next Steps
**Enhance Interactivity:**
* Add date-range slider and category/region filters.
* Enable drill-down from category → subcategory → product.

**Expand Metrics:**
* Include profit margins (if cost data becomes available).
* Track shipping time vs. customer satisfaction.

**Production Deployment:**
* Containerize with Docker.
* Deploy on cloud (e.g., AWS EC2 or Azure App Service) for team access.

**Data Pipeline Upgrade:**
* Replace Excel with live database (PostgreSQL/MySQL) for daily refreshes.

## How to run?
### STEPS:

Clone the repository

```bash
git clone https://github.com/jamshedfarzandpk/data-analytics-sales-dashboard-using-python-pandas-matplotlib-seaborn-openpyxl.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n dashboard python=3.12 -y
```

```bash
conda activate dashboard
```

### STEP 02- install the requirements
```bash
pip install -r requirements.txt --use-pep517

```
#
### STEP 03- run the following command
```bash
python main.py

```

### STEP 05- Screenshots of the app results:
Screenshot of the app results after running the main.py file:
1.after reading the xls file and creating the dashboard
![Screenshot](./bicycle_sales_dashboard.png)
```
```
## STEP 06 Screenshots of the app.py results:
Screenshot of the app results after running the app.py file:
1.after reading the xls file and creating the dash library dashboard in html 
![Screenshot](./ploty.png)
