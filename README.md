# N100 Financial Intelligence Dashboard

A financial analytics platform built using Python, SQLite and Streamlit for analysing 92 Nifty 100 companies.

Features include:

- Company Profile
- Financial Statements
- Financial Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Map
- Annual Reports
- Valuation Analytics
## Installation

```bash
git clone <repository-url>

cd N100-Financial-Intelligence

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```
## Run Dashboard

Start the Streamlit dashboard using:

```bash
streamlit run src/dashboard/app.py
```
## Project Structure

src/
├── analytics/
├── dashboard/
│ ├── app.py
│ ├── pages/
│ └── utils/
├── screener/
├── etl/
├── tests/

db/
output/
## Dashboard Screens

### 1. Home

Dashboard overview showing key statistics and navigation.

---

### 2. Company Profile

Displays:

- Company overview
- Key KPIs
- Financial ratios
- Charts

---

### 3. Financial Screener

Supports:

- 10 filter sliders
- 6 preset screeners
- Live filtering
- CSV export

---

### 4. Peer Comparison

Shows:

- Radar chart
- Peer comparison table
- Benchmark company

---

### 5. Trend Analysis

Displays:

- 10-year trends
- Multiple metric comparison
- YoY analysis

---

### 6. Sector Analysis

Displays:

- Bubble chart
- Sector median KPIs

---

### 7. Capital Allocation

Treemap grouped by:

- Capital allocation pattern

---

### 8. Annual Reports

Displays:

- Available annual reports
- BSE PDF links
