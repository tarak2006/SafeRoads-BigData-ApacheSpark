"""
Test script validating that all notebook cells run seamlessly without error.
"""

import os
import sys
import time
import pandas as pd
import numpy as np

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, desc, count, avg, sum as spark_sum
from pyspark.storagelevel import StorageLevel
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml.classification import RandomForestClassifier, LogisticRegression, DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

print("[TEST] Initializing SparkSession...")
spark = SparkSession.builder \
    .appName("SafeRoads-Test-Pipeline") \
    .master("local[2]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.python.use.daemon", "false") \
    .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("WARN")

DATA_FILE = "data/processed/accidents_cleaned_sample.tsv"
print(f"[TEST] Loading dataset: {DATA_FILE}")
df_spark = spark.read.option("header", "true").option("sep", "\t").option("inferSchema", "true").csv(DATA_FILE)
print(f"[TEST] Total records: {df_spark.count():,}")

# --- RDD Operations Demonstration ---
print("[TEST] RDD Operations...")
# 1. Base RDD from text file
raw_rdd = sc.textFile(DATA_FILE, minPartitions=4)
print(f"RDD Partitions: {raw_rdd.getNumPartitions()}")

# Header and filter
header = raw_rdd.first()
data_rdd = raw_rdd.filter(lambda line: line != header and len(line.strip()) > 0)

# Caching demonstration
data_rdd.persist(StorageLevel.MEMORY_AND_DISK)
t0 = time.time()
c1 = data_rdd.count()
t1 = time.time()
print(f"Uncached count: {c1:,} ({((t1-t0)*1000):.1f} ms)")

t2 = time.time()
c2 = data_rdd.count()
t3 = time.time()
print(f"Cached count:   {c2:,} ({((t3-t2)*1000):.1f} ms)")

# Pair RDD demonstration via parallelized sample
sample_lines = data_rdd.take(500)
sample_rdd = sc.parallelize(sample_lines, numSlices=2)
parsed_sample = sample_rdd.map(lambda line: line.split("\t")).filter(lambda parts: len(parts) >= 27)

# map() & reduceByKey()
state_pairs = parsed_sample.map(lambda p: (p[9], 1))
state_counts = state_pairs.reduceByKey(lambda a, b: a + b)
print("Sample State Counts (reduceByKey):", state_counts.collect()[:5])

# flatMap()
hazard_pairs = parsed_sample.flatMap(lambda p: [("Signal" if p[20]=="1" else "NoSignal", 1)])
print("Hazard breakdown (flatMap + reduceByKey):", hazard_pairs.reduceByKey(lambda a, b: a + b).collect())

# Lineage Graph
print("RDD Lineage (toDebugString):")
print(state_counts.toDebugString().decode('utf-8'))

# --- High Performance Spark SQL / DataFrame Analytics ---
print("\n[TEST] Spark DataFrame / SQL Analytics...")
state_df = df_spark.groupBy("state").agg(
    count("id").alias("total_accidents"),
    avg("duration_minutes").alias("avg_delay_mins")
).orderBy(desc("total_accidents"))

print("Top 5 States:")
state_df.show(5)

# --- PySpark ML Pipeline ---
print("\n[TEST] PySpark MLlib Pipeline...")
df_labeled = df_spark.withColumn("label", when(col("severity") >= 3, 1.0).otherwise(0.0))
categorical_cols = ["state", "weather_condition", "sunrise_sunset", "accident_day_of_week"]
indexers = [StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep") for c in categorical_cols]

numeric_cols = [
    "temperature_f", "humidity_pct", "visibility_mi", "wind_speed_mph",
    "precipitation_in", "duration_minutes", "accident_hour",
    "amenity_flag", "crossing_flag", "junction_flag", "traffic_signal_flag"
]
all_features = numeric_cols + [f"{c}_idx" for c in categorical_cols]

assembler = VectorAssembler(inputCols=all_features, outputCol="raw_features", handleInvalid="skip")
scaler = StandardScaler(inputCol="raw_features", outputCol="features", withStd=True, withMean=False)

train_df, test_df = df_labeled.randomSplit([0.8, 0.2], seed=42)

rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=30, maxDepth=7, seed=42)
pipeline = Pipeline(stages=indexers + [assembler, scaler, rf])

print("[TEST] Fitting Random Forest...")
fitted_model = pipeline.fit(train_df)
predictions = fitted_model.transform(test_df)

eval_acc = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
acc = eval_acc.evaluate(predictions)
print(f"[TEST] Random Forest Accuracy: {acc * 100:.2f}%")

spark.stop()
print("[TEST] Completed successfully with zero errors!")
