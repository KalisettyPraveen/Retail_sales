# Retail Sales ETL Data Pipeline

Intermediate beginner-friendly Data Engineering project using Python, NumPy,
Pandas, SQL (SQLite), and PySpark. The included CSV files are synthetic practice data.

## Architecture
Raw CSV files -> Python/Pandas/NumPy cleaning and enrichment -> SQLite tables
-> PySpark aggregations -> Parquet analytics output.

## Project structure
- `data/raw/`: synthetic customers, products, and orders input data
- `data/processed/`: cleaned CSVs and generated Spark Parquet outputs
- `src/etl_pipeline.py`: extract, transform, load pipeline
- `src/pyspark_analytics.py`: Spark analytics and Parquet output
- `sql/analysis_queries.sql`: business SQL queries
- `retail_sales.db`: generated when the ETL script runs

## Setup (Windows PowerShell / VS Code)
1. Install Python 3.10+ and Java compatible with your PySpark version.
2. Open this folder in VS Code and create a virtual environment:
   `python -m venv .venv`
3. Activate it:
   PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install packages:
   `python -m pip install -r requirements.txt`
5. Run the ETL:
   `python src/etl_pipeline.py`
6. Run Spark analytics:
   `python src/pyspark_analytics.py`

SQLite is included with Python; no separate database server is needed.
If Spark fails to start, check your Java installation and `JAVA_HOME`.

## SQL
The ETL creates `retail_sales.db` with `customers`, `products`, `orders`,
and enriched `sales` tables. Open it with a SQLite viewer or Python's sqlite3
module and execute `sql/analysis_queries.sql`.

## Three-day learning plan
Day 1: Understand the data, run the Python ETL, learn extract/transform/load,
duplicate removal, missing-value handling, joins, and NumPy vectorization.
Day 2: Inspect the SQLite tables and execute each SQL query; explain GROUP BY,
aggregate functions, joins, and monthly reporting.
Day 3: Run the PySpark job; understand DataFrame, groupBy, agg, orderBy,
show, and Parquet output. Push the finished project to GitHub.

## Important
This is a learning project using synthetic data, not a production deployment.
Do not claim production scale, cloud deployment, scheduling, or performance
improvements unless you independently implement and measure them.
