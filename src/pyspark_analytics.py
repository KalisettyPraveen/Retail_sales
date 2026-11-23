
from pathlib import Path

from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    sum as spark_sum,
    count,
    avg,
    desc
)

# STEP 1: Project paths

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "sales_enriched.csv"

OUTPUT = ROOT / "data" / "processed" / "spark_output"


# STEP 2: Create Spark session

spark = (
    SparkSession.builder
    .appName("RetailSalesETL")
    .master("local[*]")
    .getOrCreate()
)


# STEP 3: Read cleaned CSV data

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(INPUT))
)

print("Total Records:", df.count())

df.printSchema()


# STEP 4: City-wise revenue

city_sales = (
    df.groupBy("city")
    .agg(
        spark_sum("revenue").alias("total_revenue"),
        count("order_id").alias("total_orders"),
        avg("revenue").alias("average_revenue")
    )
    .orderBy(desc("total_revenue"))
)

print("CITY-WISE SALES")

city_sales.show(truncate=False)


# STEP 5: Category-wise revenue

category_sales = (
    df.groupBy("category")
    .agg(
        spark_sum("revenue").alias("total_revenue")
    )
    .orderBy(desc("total_revenue"))
)

print("CATEGORY-WISE SALES")

category_sales.show(truncate=False)


# STEP 6: Save results as Parquet

city_sales.write.mode("overwrite").parquet(
    str(OUTPUT / "revenue_by_city")
)

category_sales.write.mode("overwrite").parquet(
    str(OUTPUT / "revenue_by_category")
)


print("PySpark analytics completed successfully!")

spark.stop()
