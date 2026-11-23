from pyspark.sql import SparkSession
from pathlib import Path

spark = (
    SparkSession.builder
    .appName("ReadParquetData")
    .master("local[*]")
    .getOrCreate()
)

ROOT = Path(__file__).resolve().parents[1]

city_path = ROOT / "data/processed/spark_output/revenue_by_city"
category_path = ROOT / "data/processed/spark_output/revenue_by_category"

# Read city-wise Parquet data
city_df = spark.read.parquet(str(city_path))

print("CITY-WISE DATA FROM PARQUET")
city_df.show(truncate=False)

# Read category-wise Parquet data
category_df = spark.read.parquet(str(category_path))

print("CATEGORY-WISE DATA FROM PARQUET")
category_df.show(truncate=False)

spark.stop()