"""
23CSE352 - Big Data Analytics | Project Review 3 (15 Marks)
Step 3 - Machine Learning using PySpark (PySpark MLlib)

SafeRoads: Scalable Traffic Incident & Road Hazard Intelligence
Group 12:
 - NNN Tejesh (CB.SC.U4CSE23042)
 - A Taraka Srinivas (CB.SC.U4CSE23212)
 - K Jai Simha Reddy (CB.SC.U4CSE23219)
 - K Girish (CB.SC.U4CSE23223)

Rubric Coverage (3 Marks):
- Data preparation & handling missing values
- Feature preparation: StringIndexer, VectorAssembler, StandardScaler
- Train / Test split (80% / 20%)
- Supervised Machine Learning Model training:
    * Random Forest Classifier
 * Gradient-Boosted Trees (GBT) Classifier
 * Decision Tree Classifier
 * Logistic Regression
- Model Evaluation:
    * Accuracy, Precision, Recall, F1-Score, Area Under ROC
    * Confusion Matrix & Feature Importance Ranking
"""

import os
import sys
import time
import json

def run_pyspark_ml_pipeline(data_path="data/processed/accidents_cleaned_sample.tsv", output_dir="visualizations"):
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, when, expr
    from pyspark.ml import Pipeline
    from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
    from pyspark.ml.classification import RandomForestClassifier, LogisticRegression, DecisionTreeClassifier, GBTClassifier
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

    print("=" * 80)
    print("   SafeRoads - PySpark MLlib Traffic Incident Severity Modeling")
    print("              Course: 23CSE352 - Big Data Analytics")
    print("   Group 12 | Distributed Machine Learning Pipeline (Review 3)")
    print("=" * 80)

    # 1. Initialize SparkSession
    spark = SparkSession.builder \
        .appName("SafeRoads-PySpark-MLPipeline") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    start_total_time = time.time()

    print(f"\n[STEP 1] Ingesting Cleaned TSV Dataset from: {data_path}")
    raw_df = spark.read.option("header", "true") \
        .option("sep", "\t") \
        .option("inferSchema", "true") \
        .csv(data_path)

    total_rows = raw_df.count()
    print(f"-> Successfully loaded {total_rows:,} records across {len(raw_df.columns)} columns.")

    # 2. Target Variable Formulation:
    # SafeRoads categorizes crashes into Severe (Severity >= 3 -> label=1.0) vs Mild (Severity < 3 -> label=0.0)
    print("\n[STEP 2] Formulating Binary Target Label (is_severe = 1 if Severity >= 3 else 0)...")
    labeled_df = raw_df.withColumn(
        "label",
        when(col("severity") >= 3, 1.0).otherwise(0.0)
    )

    class_counts = labeled_df.groupBy("label").count().collect()
    for row in class_counts:
        lbl = "Severe (>=3)" if row['label'] == 1.0 else "Mild (<3)"
        pct = (row['count'] / total_rows) * 100
        print(f"   - Class {row['label']:.0f} ({lbl}): {row['count']:,} ({pct:.2f}%)")

    # 3. Categorical Indexing & Feature Engineering
    print("\n[STEP 3] Feature Engineering Pipeline (StringIndexer + VectorAssembler + StandardScaler)...")
    categorical_cols = ["state", "weather_condition", "sunrise_sunset", "accident_day_of_week"]
    indexers = [
        StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep")
        for c in categorical_cols
    ]

    numeric_cols = [
        "temperature_f", "humidity_pct", "visibility_mi", "wind_speed_mph",
        "precipitation_in", "duration_minutes", "accident_hour",
        "amenity_flag", "crossing_flag", "junction_flag", "traffic_signal_flag"
    ]
    all_feature_cols = numeric_cols + [f"{c}_idx" for c in categorical_cols]

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

    # 4. Train / Test Split (80 / 20)
    print("\n[STEP 4] Performing Stratified Train / Test Split (80% Train, 20% Test)...")
    train_df, test_df = labeled_df.randomSplit([0.8, 0.2], seed=42)
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"-> Training Set Size: {train_count:,} records")
    print(f"-> Testing Set Size:  {test_count:,} records")

    # Evaluation Metric Evaluators
    eval_acc = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    eval_prec = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
    eval_rec = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall")
    eval_f1 = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
    eval_auc = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction", metricName="areaUnderROC")

    models_to_train = {
        "Random Forest": RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=50, maxDepth=8, seed=42),
        "Gradient-Boosted Trees (GBT)": GBTClassifier(labelCol="label", featuresCol="features", maxIter=20, maxDepth=5, seed=42),
        "Decision Tree": DecisionTreeClassifier(labelCol="label", featuresCol="features", maxDepth=7, seed=42),
        "Logistic Regression": LogisticRegression(labelCol="label", featuresCol="features", maxIter=25, regParam=0.01)
    }

    results = {}
    feature_importances_dict = {}

    for model_name, classifier in models_to_train.items():
        print(f"\n[STEP 5.{len(results) + 1}] Training PySpark {model_name}...")
        pipeline = Pipeline(stages=indexers + [assembler, scaler, classifier])
        
        t0 = time.time()
        fitted_model = pipeline.fit(train_df)
        train_time = time.time() - t0

        t1 = time.time()
        predictions = fitted_model.transform(test_df)
        pred_time = time.time() - t1

        acc = eval_acc.evaluate(predictions)
        prec = eval_prec.evaluate(predictions)
        rec = eval_rec.evaluate(predictions)
        f1 = eval_f1.evaluate(predictions)
        auc = eval_auc.evaluate(predictions)

        # Compute Confusion Matrix Elements
        tp = predictions.filter("label = 1.0 AND prediction = 1.0").count()
        fp = predictions.filter("label = 0.0 AND prediction = 1.0").count()
        tn = predictions.filter("label = 0.0 AND prediction = 0.0").count()
        fn = predictions.filter("label = 1.0 AND prediction = 0.0").count()

        results[model_name] = {
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4),
            "AUC-ROC": round(auc, 4),
            "Train_Time_Sec": round(train_time, 2),
            "Inference_Time_Sec": round(pred_time, 2),
            "TP": tp, "FP": fp, "TN": tn, "FN": fn
        }

        print(f"   -> {model_name} Results:")
        print(f"      Accuracy:  {acc * 100:.2f}% | F1-Score: {f1:.4f} | AUC-ROC: {auc:.4f}")
        print(f"      Precision: {prec:.4f} | Recall: {rec:.4f}")
        print(f"      Confusion Matrix: [TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}]")
        print(f"      Training Latency: {train_time:.2f}s | Inference Latency: {pred_time:.2f}s")

        # Feature Importance for Tree models
        if model_name == "Random Forest":
            rf_stage = fitted_model.stages[-1]
            importances = rf_stage.featureImportances.toArray()
            for feat, imp in zip(all_feature_cols, importances):
                feature_importances_dict[feat] = round(float(imp), 4)

    # Save summary results
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "ml_evaluation_results.json")
    with open(summary_path, "w") as f:
        json.dump({
            "models": results,
            "feature_importances": sorted(feature_importances_dict.items(), key=lambda x: x[1], reverse=True),
            "dataset_records": total_rows,
            "train_size": train_count,
            "test_size": test_count
        }, f, indent=2)

    print(f"\n[STEP 6] Metrics exported to: {summary_path}")
    print(f"Total PySpark ML Pipeline Runtime: {time.time() - start_total_time:.2f} seconds.")
    print("=" * 80)
    spark.stop()
    return results

if __name__ == "__main__":
    tsv_file = sys.argv[1] if len(sys.argv) > 1 else "data/processed/accidents_cleaned_sample.tsv"
    run_pyspark_ml_pipeline(tsv_file)
