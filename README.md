# Retail Sales ETL Data Pipeline

An intermediate beginner-friendly Data Engineering project built using Python, NumPy, Pandas, MySQL, SQL, PySpark, and Parquet. This project uses synthetic retail sales data for learning and demonstration.

## Architecture

Raw CSV Files → Python/Pandas/NumPy (Extract, Transform and Clean) → MySQL (Load) → PySpark (Analytics) → Parquet (Output)

## Project Structure

- `data/raw/` – Synthetic customers, products, and orders input data.
- `data/processed/` – Cleaned CSV files and generated analytics outputs.
- `src/etl_pipeline.py` – Extract, transform, clean, and load pipeline.
- `src/pyspark_analytics.py` – PySpark analytics and Parquet generation.
- `src/read_parquet.py` – Reads and displays generated Parquet files.
- `sql/analysis_queries.sql` – SQL queries for business analysis.
- `.env` – Local MySQL credentials (not uploaded to GitHub).
- `requirements.txt` – Python project dependencies.

## Technologies Used

- Python
- NumPy
- Pandas
- MySQL
- SQL
- PySpark
- Parquet
- Git and GitHub

## Setup (Windows PowerShell / VS Code)

1. Install Python 3.10+ and a Java version compatible with your PySpark installation.
2. Clone this repository and open the project folder in VS Code.
3. Create a virtual environment:

   `python -m venv .venv`

4. Activate it:

   `.\.venv\Scripts\Activate.ps1`

5. Install dependencies:

   `python -m pip install -r requirements.txt`

6. Create a `.env` file in the project root and configure your local MySQL credentials:

   `MYSQL_HOST=localhost`  
   `MYSQL_PORT=3306`  
   `MYSQL_USER=root`  
   `MYSQL_PASSWORD=your_password`  
   `MYSQL_DATABASE=retail_sales`

7. Create the `retail_sales` database in MySQL before running the ETL pipeline.
8. Run the ETL pipeline:

   `python src/etl_pipeline.py`

9. Run PySpark analytics:

   `python src/pyspark_analytics.py`

10. Read the generated Parquet output:

    `python src/read_parquet.py`

## SQL Analysis

The project loads customer, product, order, and enriched sales data into MySQL tables.

Execute the queries in `sql/analysis_queries.sql` using MySQL Workbench to analyze:

- Total revenue
- Monthly sales
- City-wise revenue
- Product performance
- Category-wise revenue
- Customer analysis

## Important Notes

- This project uses synthetic practice data, not real company data.
- MySQL credentials are stored locally in `.env` and should never be committed to GitHub.
- Generated Spark output and virtual environment files are excluded using `.gitignore`.
- This is a learning project, not a production deployment.
- Do not claim cloud deployment, automated scheduling, real-time processing, or measured performance improvements unless independently implemented and verified.
