"""
23CSE352 - Big Data Analytics | Project Review 3 (15 Marks)
Component 2 (3 Marks): PySpark Data Preprocessing & Feature Engineering Pipeline

SafeRoads: Scalable Traffic Incident & Road Hazard Intelligence
Group 12:
 - NNN Tejesh (CB.SC.U4CSE23042)
 - A Taraka Srinivas (CB.SC.U4CSE23212)
 - K Jai Simha Reddy (CB.SC.U4CSE23219)
 - K Girish (CB.SC.U4CSE23223)

Rubric Alignment:
1. Data Ingestion & Schema Validation
2. Null Value Auditing & Imputation (Handling Missing Data)
3. Outlier Filtering & Data Sanitization
4. Feature Engineering:
   - Binary Target Variable (is_severe = 1 if Severity >= 3 else 0)
   - Commute Rush-Hour Flag (7-9 AM & 4-6 PM)
   - Low Visibility & Freeze Hazards Flag
   - Composite Infrastructure Vulnerability Index
5. PySpark ML Feature Transformations:
   - StringIndexer (Categorical Indexing)
   - VectorAssembler (Dense Feature Assembly)
   - StandardScaler (Zero-mean / Unit-variance Standardization)
6. Partition Profiling & Summary Statistics Export
"""

import os
import sys
import time
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, count, isnan, avg, stddev, min as spark_min, max as spark_max, round as spark_round
)
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler, Imputer

def run_pyspark_preprocessing(input_path="data/processed/accidents_cleaned_sample.tsv", output_dir="visualizations"):
    print("=" * 80)
    print("   SafeRoads - PySpark Distributed Data Preprocessing & Feature Engineering")
    print("              Course: 23CSE352 - Big Data Analytics (Review 3)")
    print("   Group 12 | Component 2: Preprocessing, Modelling & Evaluation (3 Marks)")
    print("=" * 80)

    start_time = time.time()

    # 1. Initialize SparkSession
    spark = SparkSession.builder \
        .appName("SafeRoads-PySpark-Preprocessing") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # 2. Ingest Dataset
    print(f"\n[STEP 1] Ingesting Raw/Processed Telemetry Dataset from: {input_path}")
    df_raw = spark.read.option("header", "true") \
        .option("sep", "\t") \
        .option("inferSchema", "true") \
        .csv(input_path)

    total_records = df_raw.count()
    num_columns = len(df_raw.columns)
    print(f"-> Successfully Ingested: {total_records:,} records across {num_columns} columns.")
    print(f"-> Cluster Partitions Count: {df_raw.rdd.getNumPartitions()} partitions.")

    # 3. Missing Value Audit
    print("\n[STEP 2] Auditing Missing & Null Values Across Essential Attributes:")
    audit_cols = ["temperature_f", "humidity_pct", "visibility_mi", "wind_speed_mph", "precipitation_in", "duration_minutes"]
    null_counts = {}
    for c in audit_cols:
        null_count = df_raw.filter(col(c).isNull()).count()
        null_pct = (null_count / total_records) * 100
        null_counts[c] = {"missing_count": null_count, "missing_pct": round(null_pct, 3)}
        print(f"   - Attribute '{c:<18s}': {null_count:>5d} missing values ({null_pct:.2f}%)")

    # Impute continuous numerical columns if missing
    imputer = Imputer(inputCols=audit_cols, outputCols=[f"{c}_imp" for c in audit_cols]).setStrategy("median")
    df_imputed = imputer.fit(df_raw).transform(df_raw)
    print("-> Median Imputation Completed for numerical continuous attributes.")

    # 4. Outlier Filtering & Data Cleansing
    print("\n[STEP 3] Performing Outlier Filtering & Domain Validation:")
    df_clean = df_imputed.filter(
        (col("duration_minutes_imp") >= 0.0) & (col("duration_minutes_imp") <= 1440.0) &
        (col("temperature_f_imp") >= -50.0) & (col("temperature_f_imp") <= 140.0) &
        (col("visibility_mi_imp") >= 0.0) & (col("visibility_mi_imp") <= 100.0)
    )
    clean_count = df_clean.count()
    print(f"-> Verified Clean Rows: {clean_count:,} ({clean_count * 100.0 / total_records:.2f}% retained)")

    # 5. Domain Feature Engineering
    print("\n[STEP 4] Engineering Analytical & Machine Learning Features:")
    df_engineered = df_clean \
        .withColumn("is_severe", when(col("severity") >= 3, 1.0).otherwise(0.0)) \
        .withColumn("is_rush_hour", when((col("accident_hour").between(7, 9)) | (col("accident_hour").between(16, 18)), 1.0).otherwise(0.0)) \
        .withColumn("is_weekend", when(col("accident_day_of_week").isin(["Saturday", "Sunday"]), 1.0).otherwise(0.0)) \
        .withColumn("is_low_visibility", when(col("visibility_mi_imp") < 2.0, 1.0).otherwise(0.0)) \
        .withColumn("is_sub_freezing", when(col("temperature_f_imp") <= 32.0, 1.0).otherwise(0.0)) \
        .withColumn("infra_vulnerability_index", (
            col("junction_flag") + col("traffic_signal_flag") + col("crossing_flag") + col("amenity_flag")
        ).cast("double"))

    # Target class balance
    class_stats = df_engineered.groupBy("is_severe").count().collect()
    print("-> Supervised Target Class Distribution (is_severe):")
    for row in class_stats:
        cls_name = "Severe (Severity >= 3)" if row["is_severe"] == 1.0 else "Mild (Severity < 3)"
        pct = (row["count"] / clean_count) * 100
        print(f"   * Class {int(row['is_severe'])} [{cls_name}]: {row['count']:,} incidents ({pct:.2f}%)")

    # 6. PySpark ML Feature Transformation Pipeline
    print("\n[STEP 5] Building PySpark ML Pipeline (StringIndexer + VectorAssembler + StandardScaler):")
    categorical_cols = ["state", "weather_condition", "sunrise_sunset", "accident_day_of_week"]
    indexers = [
        StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep")
        for c in categorical_cols
    ]

    numeric_features = [
        "temperature_f_imp", "humidity_pct_imp", "visibility_mi_imp", "wind_speed_mph_imp",
        "precipitation_in_imp", "duration_minutes_imp", "accident_hour",
        "amenity_flag", "crossing_flag", "junction_flag", "traffic_signal_flag",
        "is_rush_hour", "is_weekend", "is_low_visibility", "is_sub_freezing", "infra_vulnerability_index"
    ]
    all_feature_cols = numeric_features + [f"{c}_idx" for c in categorical_cols]

    assembler = VectorAssembler(
        inputCols=all_feature_cols,
        outputCol="raw_features",
        handleInvalid="skip"
    )

    scaler = StandardScaler(
        inputCol="raw_features",
        outputCol="features",
        withStd=True,
        withMean=False
    )

    ml_pipeline = Pipeline(stages=indexers + [assembler, scaler])
    print(f"-> Assembling {len(all_feature_cols)} total predictive features into dense standardized feature vectors.")

    t_fit_start = time.time()
    fitted_pipeline = ml_pipeline.fit(df_engineered)
    df_preprocessed = fitted_pipeline.transform(df_engineered)
    t_fit_sec = time.time() - t_fit_start
    print(f"-> ML Pipeline fitted and transformed successfully in {t_fit_sec:.2f} seconds.")

    # 7. Sample Feature Vector Inspection
    sample_row = df_preprocessed.select("id", "is_severe", "features").first()
    print("\n[STEP 6] Sample Transformed Feature Record (Dense Representation):")
    print(f"  -> Incident ID : {sample_row['id']}")
    print(f"  -> Target Label: {sample_row['is_severe']}")
    print(f"  -> Features Vector Dimensions: {len(sample_row['features'])} assembled attributes")

    # 8. Export Preprocessing Metrics & Summary
    os.makedirs(output_dir, exist_ok=True)
    summary_file = os.path.join(output_dir, "pyspark_preprocessing_summary.json")
    summary_data = {
        "dataset_records_ingested": total_records,
        "clean_records_retained": clean_count,
        "columns_count": num_columns,
        "null_counts": null_counts,
        "target_class_distribution": {
            "mild_count": next((r["count"] for r in class_stats if r["is_severe"] == 0.0), 0),
            "severe_count": next((r["count"] for r in class_stats if r["is_severe"] == 1.0), 0)
        },
        "engineered_features": [
            "is_severe", "is_rush_hour", "is_weekend", "is_low_visibility",
            "is_sub_freezing", "infra_vulnerability_index"
        ],
        "total_vector_dimensions": len(all_feature_cols),
        "feature_list": all_feature_cols,
        "preprocessing_runtime_sec": round(time.time() - start_time, 2)
    }

    with open(summary_file, "w") as f:
        json.dump(summary_data, f, indent=2)

    print(f"\n[STEP 7] Preprocessing summary report exported to: {summary_file}")
    print(f"Total PySpark Preprocessing Pipeline Runtime: {time.time() - start_time:.2f} seconds.")
    print("=" * 80)
    print("   [SUCCESS] PYSPARK PREPROCESSING & FEATURE ENGINEERING COMPLETED!")
    print("=" * 80)

    spark.stop()
    return summary_data

if __name__ == "__main__":
    tsv_path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/accidents_cleaned_sample.tsv"
    run_pyspark_preprocessing(tsv_path)
