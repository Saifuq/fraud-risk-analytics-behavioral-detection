# FinSafe: Fraud Risk Analytics & Behavioral Detection

**FinSafe** is a comprehensive end-to-end analytics and machine learning project designed to monitor, detect, and analyze fraudulent activities in financial transactions, specifically focused on the Nigerian financial landscape. This repository integrates data engineering, advanced SQL analytics, machine learning modeling (XGBoost), and interactive visualizations via Streamlit and Power BI.

---

## 🚀 Key Features
* **Source of the Data** :https://huggingface.co/datasets/electricsheepafrica/Nigerian-Financial-Transactions-and-Fraud-Detection-Dataset/viewer?views%5B%5D=train
* **Real-time Monitoring Dashboard**: An interactive Streamlit application to visualize transaction distributions and calculate individual risk scores.
* **Machine Learning Pipeline**: A complete XGBoost-based classification pipeline for fraud detection, including data preprocessing and model persistence.
* **Tri-Tier Risk Scoring**: A behavioral risk bucketing system (High, Medium, and Low risk) implemented through both SQL logic and Python.
* **Advanced SQL Analytics**: Deep-dive queries for merchant category analysis, persona-based risk distribution, and time-based fraud trends.
* **Multi-Platform Reporting**: Robust visual storytelling using a Power BI dashboard for executive-level insights.
* **Flexible Data Handling**: Support for both real-world data (via Hugging Face) and synthetic data generation for testing environments.

---

## 📁 Project Structure

### 1. Data & Analytics (SQL)

* **`ffinance.sql`**: Contains the core analytical logic for the project, including:
* **Data Validation**: Fraud vs. Non-fraud distribution.
* **Risk Bucketing**: A tri-tier scoring system based on velocity, spending deviation, and geo-anomaly.
* **Merchant Analysis**: Identifying high-risk categories and fraud rates.
* **Behavioral Trends**: Analyzing night-time transactions and salary-week patterns.



### 2. Source Code (`/src`)

* **`app.py`**: The main entry point for the Streamlit dashboard. It features KPIs (Total Volume, Fraud Rate), transaction charts, and a "Custom Transaction Risk Scorer".
* **`data_loader.py`**: Handles data ingestion from the "Nigerian Financial Transactions and Fraud Detection Dataset" or generates synthetic test data.
* **`db_connector.py`**: Manages the connection to SQL Server (MSSQL) using SQLAlchemy to upload processed data for further analysis.
* **`preprocessing.py`**: A robust `FinancialPreprocessor` class that handles data cleaning, label encoding for categorical variables, and standard scaling for numerical features.
* **`train_model.py`**: The training script that fits an XGBoost classifier to the data, evaluates performance, and saves the model artifacts (`.pkl`).
* **`risk_score.py`**: An engine that utilizes the trained model to calculate a 0-100 risk score for any given transaction.
* **`export_to_excel.py`**: Utility script to export filtered or processed transaction data into Excel format for offline auditing.

### 3. Business Intelligence & Raw Data

* **`finance_pbi.pbix`**: The master Power BI file containing advanced data modeling and interactive visualizations.
* **`page_1.png` to `page_33.png**`: High-resolution screenshots of the Power BI dashboard segments.
* **`finance.csv` / `finance.xlsx**`: Raw transaction data used as the foundation for analysis and modeling.

---

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Libraries**: Pandas, NumPy, Scikit-learn, XGBoost, Plotly, Streamlit, SQLAlchemy
* **Database**: SQL Server (MSSQL)
* **Visualization**: Power BI & Plotly
* **Data Source**: Hugging Face Datasets (Nigerian Financial Transactions)

---

## 📊 Analytics Deep Dive

The project utilizes a specific **Tri-Tier Risk Scoring System** implemented in SQL to segment transactions:

| Risk Segment | Criteria | Action |
| --- | --- | --- |
| **High Risk** | Velocity > 15 OR Spending Deviation > 3.0 OR Geo-anomaly > 0.8 | Immediate Flag/Block |
| **Medium Risk** | Velocity 10-15 OR Spending Deviation 1.5-3.0 | Manual Review |
| **Low Risk** | All other parameters | Allow |

---

## 💻 Setup & Usage

### 1. Model Training

To train the fraud detection model using real data:

```bash
python src/train_model.py --use-real --limit 50000

```

### 2. Run the Dashboard

Launch the Streamlit monitoring interface:

```bash
streamlit run src/app.py

```

### 3. Database Integration

Ensure your `.env` file is configured with your SQL Server credentials, then run:

```bash
python src/db_connector.py

```

---

## 📈 Power BI Dashboard

The Power BI dashboard provides a strategic overview of the data, focusing on:

* **Fraud Distribution by Sender Persona**: Identifying which user types are most vulnerable.
* **Merchant Category Risk**: Visualizing which sectors (e.g., Betting, E-commerce) experience the highest fraud rates.
* **Temporal Analysis**: Tracking fraud spikes during night hours and specific weeks of the month.
