# SafeRoads: Scalable Traffic Accident Severity & Road Hazard Intelligence
### Course: 23CSE352 - Big Data Analytics
### Project Review 3 - Apache Spark (15 Marks)
**Core Technologies:** Apache Spark, Scala RDDs, PySpark MLlib, Distributed Machine Learning, Python 3

---

## 👥 Group 12 - Team Details

| S.No. | Student Name | Register Number | Role & Primary Technical Contribution |
|:---:|:---|:---:|:---|
| **1** | **NNN Tejesh** | `CB.SC.U4CSE23042` | Scala Spark RDD Engine, DAG & Lineage Architecture |
| **2** | **A Taraka Srinivas** | `CB.SC.U4CSE23212` | PySpark MLlib Feature Engineering & Modeling Pipeline |
| **3** | **K Jai Simha Reddy** | `CB.SC.U4CSE23219` | Preprocessing, Exploratory Data Analysis & Visualizations |
| **4** | **K Girish** | `CB.SC.U4CSE23223` | Partitions Scaling, Cache Benchmarking & Documentation |

---

## 📋 Evaluation Rubric Alignment (15 Marks Total)

| Component | Target Syllabus Criteria | Marks | Status |
|:---|:---|:---:|:---:|
| **Component 1** | **Scala + Spark RDD Processing:** RDD creation, transformations (`map`, `filter`, `flatMap`, `reduceByKey`, `aggregateByKey`, `join`, `sortBy`, `mapValues`), actions (`count`, `take`, `first`, `reduce`, `countByKey`, `collect`), key/value operations, and Spark Concepts (partitions, lineage, DAG, fault tolerance, and cache/persist). | **10 Marks** | **Completed & Verified** |
| **Component 2** | **PySpark ML Model:** Feature preparation (`StringIndexer`, `VectorAssembler`, `StandardScaler`), 80/20 train/test split, 4 ML models (Random Forest, Gradient-Boosted Trees, Decision Tree, Logistic Regression), and quantitative evaluation (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix). | **3 Marks** | **Completed & Verified** |
| **Component 3** | **Visualization & Results:** At least 3+ meaningful charts with deep analytical commentary and strategic real-world takeaways. | **2 Marks** | **Completed & Verified (5 Figures)** |
| **Total** | **Comprehensive Apache Spark Big Data Analytics System** | **15 Marks** | **100% Complete** |

---

## 1. Executive Summary & Problem Statement

### 1.1 Societal & Economic Significance
Surface vehicular transportation is the essential backbone of national freight distribution and commuter mobility. However, traffic collisions remain one of the foremost causes of preventable mortality, trauma injuries, and economic losses globally. According to the United States Department of Transportation (USDOT) and Federal Highway Administration (FHWA):
* Over **42,000 fatalities** and **2.5 million disabling injuries** occur annually across the US.
* Over **$340 billion** is lost annually to roadway property damage, emergency medical dispatch, infrastructure repair, and travel delay.

### 1.2 The Big Data Imperative
Crash events are governed by complex, multi-variate dependencies across atmospheric weather phenomena (freezing rain, heavy snow, fog), road geometry bottlenecks (highway interchange ramps, signalized intersections, pedestrian crosswalks), and diurnal commute traffic spikes. Traditional relational database management systems (RDBMS) such as PostgreSQL or MySQL suffer from severe memory exhaustion (OOM) and sluggish query latencies when analyzing millions of records. Distributed computing via **Apache Spark** is strictly required for sub-second transformations, fault-tolerant DAG scheduling, and iterative machine learning.

---

## 2. Dataset Description

* **Dataset Origin:** [Kaggle US Accidents Dataset (2016 - 2023)](https://www.kaggle.com/datasets/sobhanmohammadpour/us-accidents) by Sobhan Moosavi.
* **Raw Dataset Size:** **1.42 GB CSV file** containing **3,864,198 granular records** across 49 states.
* **Sanitized Starter Data:** `data/processed/accidents_cleaned_sample.tsv` (100,000 records, 27 engineered attributes, 16.3 MB) committed with the repository for zero-dependency reproducible execution.
* **Target Variable:** `severity` (1 to 4) / Binary classification: `is_severe = 1 if severity >= 3 else 0`.
* **Key Feature Domains:**
  * **Spatial:** `state`, `city`, `county`, `start_lat`, `start_lng`, `timezone`.
  * **Temporal:** `accident_hour` (0-23), `accident_day_of_week`, `accident_month`, `accident_year`, `duration_minutes`.
  * **Atmospheric:** `temperature_f`, `humidity_pct`, `visibility_mi`, `wind_speed_mph`, `precipitation_in`, `weather_condition`.
  * **Road Infrastructure:** `traffic_signal_flag`, `junction_flag`, `crossing_flag`, `amenity_flag`, `sunrise_sunset`.

---

## 3. Four Core Framed Analysis Questions (15-Minute Discussion Plan)

1. **Question 1 (Temporal Risk Dynamics):** How does crash intensity vary across diurnal 24-hour cycles and weekdays, and when do commuter corridors face peak congestion?
2. **Question 2 (Meteorological Severity Multipliers):** Which atmospheric weather conditions (e.g., Freezing Rain, Heavy Snow, Fog) generate the highest mean severity and roadway delay?
3. **Question 3 (Roadway Infrastructure Bottlenecks):** How do specific road geometry features (Highway Junctions, Traffic Signals, Pedestrian Crossings) correlate with high-severity collisions?
4. **Question 4 (Predictive Safety Modeling):** Can distributed Machine Learning classifiers accurately predict whether an accident will be severe (Severity $\ge 3$) using pre-incident spatial, temporal, and atmospheric features?

---

## 4. Apache Spark RDD Implementation (Scala & PySpark)

### 4.1 RDD Creation and Partitioning
The dataset is loaded into Spark using `sc.textFile("data/processed/accidents_cleaned_sample.tsv", minPartitions=4)`:
* Partition count inspected via `rdd.getNumPartitions`: **4 partitions**.
* Record distribution inspected via `rdd.glom().map(len).collect()`: **~25,000 records per partition**.

### 4.2 Transformations Demonstrated (6+ Implemented)
1. `filter()`: Strips header line, purges malformed rows, and isolates catastrophic incidents (`severity >= 3`).
2. `map()`: Parses tab-separated raw text into structured Scala `AccidentRecord` case classes / Python dictionaries.
3. `flatMap()`: Tokenizes composite roadway hazard identifiers (`Hazard_HighwayJunction`, `Hazard_TrafficSignal`, etc.) for multi-key fan-out.
4. `reduceByKey()`: Aggregates accident volume per State and per Weather Condition using associative combining functions.
5. `aggregateByKey()`: Accumulates total clearance duration and incident counts in a single pass across partitions to compute mean clearance delay.
6. `join()`: Performs key-value join between State Volume Pair RDD and State Mean Clearance Delay Pair RDD.
7. `sortBy()`: Ranks states and hazards in descending order of incident frequency.
8. `mapValues()`: Calculates state crash percentages relative to continental totals.

### 4.3 Actions Demonstrated (5+ Implemented)
1. `count()`: Computes total verified records (**100,000 rows**).
2. `take(10)`: Retrieves Top-10 crash hotspot states to driver console.
3. `first()`: Captures dataset header and validates initial record structure.
4. `reduce()`: Computes continental cumulative traffic delay (**176,366.7 vehicle-hours**).
5. `countByKey()`: Computes frequency distribution across discrete severity classes.
6. `collect()`: Gathers aggregated infrastructure hazard statistics to driver.

### 4.4 Spark Concepts: Lineage, DAG, Fault Tolerance & Caching
* **Directed Acyclic Graph (DAG):** Spark constructs a logical stage graph lazily. Consecutive narrow transformations (`map`, `filter`) are pipelined into a single execution stage, while wide transformations (`reduceByKey`, `join`) trigger a network shuffle stage boundary.
* **RDD Lineage (`toDebugString`):**
  ```text
  (4) MapPartitionsRDD[8] at join []
   |  MapPartitionsRDD[7] at join []
   |  CoGroupedRDD[6] at join []
   |--(4) ParallelCollectionRDD[4] at parallelize []
   |--(4) MapPartitionsRDD[5] at mapValues []
       |  ParallelCollectionRDD[4] at parallelize []
  ```
* **Fault Tolerance:** Unlike Hadoop MapReduce, which writes intermediate states to physical HDFS disks, Spark relies on deterministic lineage recomputation. If an executor node crashes, Spark re-evaluates only the lost partition from the parent RDD without restarting the job.
* **In-Memory Caching (`persist(StorageLevel.MEMORY_AND_DISK)`):**
  * Uncached execution time (Cold run): **1,680 ms**
  * Cached execution time (Warm run): **180 ms**
  * Speedup achieved: **9.3x faster!**

---

## 5. PySpark Machine Learning Modeling Pipeline

### 5.1 Pipeline Architecture
* **Categorical Encoding:** `StringIndexer` converts `state`, `weather_condition`, `sunrise_sunset`, and `accident_day_of_week` into numeric indices.
* **Vector Assembly:** `VectorAssembler` merges 15 continuous and binary road geometry features into a single feature vector (`raw_features`).
* **Standardization:** `StandardScaler` standardizes continuous features to zero mean and unit variance.
* **Split:** 80% Training (**80,182 records**) and 20% Holdout Testing (**19,818 records**) with seed=42.

### 5.2 Supervised Classifier Benchmarks (4 Distributed ML Models)

| Model | Accuracy | Weighted Precision | Weighted Recall | F1-Score | Area Under ROC | Training Time |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Gradient-Boosted Trees (GBT) (Champion)** | **66.49%** | **0.6592** | **0.6649** | **0.6587** | **0.7338** | **15.25s** |
| **Random Forest** | 65.37% | 0.6470 | 0.6537 | 0.6378 | 0.7242 | 19.89s |
| **Decision Tree** | 64.16% | 0.6339 | 0.6416 | 0.6327 | 0.6193 | 4.87s |
| **Logistic Regression** | 62.51% | 0.6140 | 0.6251 | 0.6007 | 0.6819 | 6.26s |

### 5.3 Top Feature Importance Attribution (Random Forest Gini Weight)
1. `traffic_signal_flag`: **43.22%** (Primary predictor of intersection collisions)
2. `crossing_flag`: **25.55%** (Pedestrian conflict zone influence)
3. `state_idx`: **12.86%** (Regional traffic density and highway design standards)
4. `junction_flag`: **4.95%** (Highway interchange merge bottleneck impact)
5. `duration_minutes`: **2.93%** (Roadway blockage duration correlation)
6. `temperature_f`: **1.87%** (Sub-freezing road freeze indicator)
7. `weather_condition_idx`: **1.79%** (Precipitation / visibility hazard multiplier)
8. `accident_day_of_week_idx`: **1.66%** (Weekday vs. weekend commute profiles)

---

## 6. Analytical Visualizations

| Figure | Title | File Path | Core Finding |
|:---:|:---|:---|:---|
| **Fig 1** | **Continental Accident Intensity Heatmap** | `visualizations/vis_1_hourly_crash_heatmap.png` | Morning (7-9 AM) and evening (4-6 PM) weekday rush-hour crash volume spikes (3.8x baseline). |
| **Fig 2** | **Weather Impact vs. Severity & Volume** | `visualizations/vis_2_weather_severity_impact.png` | Freezing Rain, Heavy Snow, and Fog generate highest mean severity indices (>3.1/4.0). |
| **Fig 3** | **Infrastructure Hazard vs. Severe Crash Rate** | `visualizations/vis_3_infrastructure_risk.png` | Traffic signals have highest incident volume; Highway junctions generate highest severe crash rate (31.8%). |
| **Fig 4** | **PySpark ML Evaluation & Feature Importance** | `visualizations/vis_4_ml_model_evaluation.png` | Random Forest champion performance (0.724 AUC-ROC); traffic signals and crossings account for >68% Gini weight. |
| **Fig 5** | **Spark In-Memory Cache & Partition Scaling** | `visualizations/vis_5_spark_cache_benchmark.png` | 9.3x cache speedup (180 ms vs 1,680 ms) across 4 partitions. |

---

## 7. Strategic Real-World Decision Intelligence

1. **Proactive 911 Trauma Dispatch:** Emergency management agencies can dynamically pre-position emergency ambulances and extraction gear near high-risk junctions during predicted winter freeze events.
2. **Intelligent Transportation Systems (ITS):** Variable Speed Limit Signs (VSLS) on interstate highways can be dynamically lowered based on real-time weather and crash probability feeds.
3. **Municipal Road Restructuring:** State DOTs can prioritize signalized intersections and high-speed highway merges for barrier cushions, improved merge ramps, and high-visibility pedestrian signage.

---

## 8. Project Artifacts & File Structure

```text
e:\Bigdata_review3\
├── SafeRoads_ApacheSpark_Complete_Analysis.ipynb  <-- Master pre-executed Jupyter Notebook
├── REPORT.md                                     <-- Complete Markdown project report
├── data/
│   ├── raw/US_Accidents_1.4GB.csv                <-- 1.42 GB Raw US Accidents dataset
│   └── processed/accidents_cleaned_sample.tsv    <-- 100,000 clean records (16.3 MB)
├── scala_spark/
│   ├── SafeRoadsSparkApp.scala                   <-- Complete Scala Spark RDD application
│   ├── build.sbt                                 <-- sbt build configuration
│   └── pom.xml                                   <-- Maven build configuration
├── pyspark_ml/
│   └── pyspark_accident_ml.py                    <-- Standalone PySpark MLlib pipeline
├── presentation/
│   ├── SafeRoads_ApacheSpark_Review3.pptx         <-- Official 12-Slide PowerPoint presentation
│   └── create_presentation.py                    <-- Automated presentation generator
├── report/
│   ├── SafeRoads_ApacheSpark_Review3_Report.docx  <-- Publication-grade 15-20 page Word report
│   └── generate_report_docx.py                   <-- Automated report generator
└── visualizations/
    ├── vis_1_hourly_crash_heatmap.png            <-- Temporal heatmap
    ├── vis_2_weather_severity_impact.png         <-- Weather severity analysis
    ├── vis_3_infrastructure_risk.png             <-- Infrastructure hazard breakdown
    ├── vis_4_ml_model_evaluation.png             <-- ML models & feature importance
    ├── vis_5_spark_cache_benchmark.png           <-- Spark caching benchmark
    └── ml_evaluation_results.json                <-- JSON export of metrics
```
