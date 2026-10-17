# SafeRoads: Continental Traffic Incident & Road Hazard Intelligence
> **Course:** 23CSE352 — Big Data Analytics | **Project Review 3 (15 Marks)**  
> **Technologies:** Apache Spark 4.2.0, Scala 2.13, PySpark MLlib, Distributed Machine Learning, Python 3.13, Leaflet.js, Flask

---

## 👥 Group 12 — Team Details

| S.No. | Student Name | Register Number | Role & Technical Contribution |
|:---:|:---|:---:|:---|
| **1** | **NNN Tejesh** | `CB.SC.U4CSE23042` | Scala Spark RDD Processing Engine, DAG Lineage Graph & Architecture |
| **2** | **A Taraka Srinivas** | `CB.SC.U4CSE23212` | PySpark MLlib Pipeline, Preprocessing & 4 Distributed ML Models |
| **3** | **K Jai Simha Reddy** | `CB.SC.U4CSE23219` | Preprocessing, Exploratory Data Analysis & 5 Publication Visualizations |
| **4** | **K Girish** | `CB.SC.U4CSE23223` | Partitions Scaling, In-Memory Caching Benchmarking & Full-Stack UI |

---

## 📋 Evaluation Rubric Alignment (15 Marks Total)

| Component | Target Syllabus Criteria | Marks | Status |
|:---|:---|:---:|:---:|
| **Component 1** | **Scala + Spark RDD Processing:** RDD creation, transformations (`map`, `filter`, `flatMap`, `reduceByKey`, `aggregateByKey`, `join`, `sortBy`, `mapValues`), actions (`count`, `take`, `first`, `reduce`, `countByKey`, `collect`), key/value operations, and Spark Concepts (partitions, lineage, DAG, fault tolerance, and cache/persist). | **10 Marks** | **100% Completed in Scala** |
| **Component 2** | **PySpark ML Model:** Preprocessing (`StringIndexer`, `VectorAssembler`, `StandardScaler`, `Imputer`), 80/20 train/test split, 4 ML models (Gradient-Boosted Trees, Random Forest, Decision Tree, Logistic Regression), and quantitative evaluation (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix). | **3 Marks** | **100% Completed** |
| **Component 3** | **Visualization & Results:** 5 Publication-grade charts with deep analytical commentary and strategic real-world decision takeaways. | **2 Marks** | **100% Completed** |
| **TOTAL** | **Full Distributed Big Data Analytics Pipeline** | **15 Marks** | **15 / 15 Verified** |

---

## 🚀 Quick Start & Master Command Reference

### 1. Run Scala + Spark RDD Engine (10 Marks Component)
```powershell
# Interactive Spark Shell (Recommended for Live Viva Demo):
spark-shell -I scala_spark/run_pipeline.scala
```
*(Type `:quit` to exit when done)*

### 2. Run PySpark Preprocessing Pipeline (Component 2: Preprocessing)
```powershell
python pyspark_preprocessing/pyspark_data_preprocessing.py
```

### 3. Run PySpark 4-Model ML Pipeline (Component 2: Modelling & Evaluation)
```powershell
python pyspark_ml/pyspark_accident_ml.py
```

### 4. Generate 5 High-Resolution Visualizations (2 Marks Component)
```powershell
python visualizations/generate_charts.py
```

### 5. Launch Pre-Executed Master Jupyter Notebook
```powershell
jupyter notebook SafeRoads_ApacheSpark_Complete_Analysis.ipynb
```

### 6. Generate Academic Report & PowerPoint Presentation
```powershell
# Word Document Report (.docx):
python report/generate_report_docx.py

# PowerPoint Presentation (.pptx):
python presentation/create_presentation.py
```

### 7. Launch Interactive Full-Stack Dashboard
```powershell
python dashboard/server.py
# Open browser at: http://localhost:5000
```

### 8. Run Automated Project Verification Audit
```powershell
python verify_project.py
```

---

## 📊 PySpark Machine Learning Benchmark (4 Models)

Evaluated on **19,818 unseen holdout test records** (80/20 Stratified Split):

| Model | Accuracy | Weighted Precision | Weighted Recall | F1-Score | Area Under ROC | Training Time |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. Gradient-Boosted Trees (GBT) [CHAMPION]** | **66.49%** | **0.6592** | **0.6649** | **0.6587** | **0.7338** | **15.25s** |
| **2. Random Forest Classifier** | 65.37% | 0.6470 | 0.6537 | 0.6378 | 0.7242 | 18.54s |
| **3. Decision Tree Classifier** | 64.16% | 0.6339 | 0.6416 | 0.6327 | 0.6193 | 4.79s |
| **4. Logistic Regression** | 62.51% | 0.6140 | 0.6251 | 0.6007 | 0.6819 | 5.97s |

---

## 📁 Repository Directory Structure

```text
├── SafeRoads_ApacheSpark_Complete_Analysis.ipynb  <-- Master pre-executed Jupyter Notebook
├── README.md                                     <-- Project overview and command guide
├── REPORT.md                                     <-- Complete Markdown technical report
├── verify_project.py                             <-- Automated 15-mark rubric verification suite
├── data/
│   ├── raw/US_Accidents_1.4GB.csv                <-- Raw dataset
│   └── processed/accidents_cleaned_sample.tsv    <-- 100,000 clean records sample
├── scala_spark/
│   ├── run_pipeline.scala                        <-- Pure Scala Spark RDD pipeline for spark-shell
│   ├── SafeRoadsSparkApp.scala                   <-- Standalone Scala Spark Application
│   ├── build.sbt                                 <-- SBT build definition
│   └── pom.xml                                   <-- Maven build definition
├── pyspark_preprocessing/
│   ├── pyspark_data_preprocessing.py             <-- Dedicated PySpark Preprocessing pipeline
│   └── pyspark_rdd_preprocessing.py              <-- RDD preprocessing
├── pyspark_ml/
│   └── pyspark_accident_ml.py                    <-- PySpark MLlib 4-model training & evaluation
├── visualizations/
│   ├── generate_charts.py                        <-- Chart generator
│   ├── vis_1_hourly_crash_heatmap.png            <-- Temporal crash heatmap
│   ├── vis_2_weather_severity_impact.png         <-- Weather impact chart
│   ├── vis_3_infrastructure_risk.png             <-- Infrastructure hazard chart
│   ├── vis_4_ml_model_evaluation.png             <-- 4-model evaluation & feature importance
│   ├── vis_5_spark_cache_benchmark.png           <-- Spark cache & partition scaling benchmark
│   └── ml_evaluation_results.json                <-- Exported ML evaluation metrics
├── dashboard/
│   ├── index.html                                <-- Full-stack interactive Leaflet.js UI
│   └── server.py                                 <-- Flask REST backend server
├── presentation/
│   ├── SafeRoads_ApacheSpark_Review3.pptx         <-- 12-slide PowerPoint presentation
│   └── create_presentation.py                    <-- Automated PPTX generator
└── report/
    ├── SafeRoads_ApacheSpark_Review3_Report.docx  <-- 20-page comprehensive Word report
    └── generate_report_docx.py                   <-- Automated docx generator
```
