package com.saferoads.spark

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.storage.StorageLevel

/**
 * 23CSE352 - Big Data Analytics | Project Review 3 (15 Marks)
 * Apache Spark RDD Processing Pipeline (Scala + Spark)
 *
 * SafeRoads: Scalable Traffic Incident & Road Hazard Intelligence
 * Group 12:
 *  - NNN Tejesh (CB.SC.U4CSE23042)
 *  - A Taraka Srinivas (CB.SC.U4CSE23212)
 *  - K Jai Simha Reddy (CB.SC.U4CSE23219)
 *  - K Girish (CB.SC.U4CSE23223)
 *
 * Rubric Coverage (10 Marks):
 * 1. RDD Creation from raw/processed real-world dataset
 * 2. Transformations: filter(), map(), flatMap(), reduceByKey(), mapValues(), aggregateByKey(), join(), sortBy()
 * 3. Actions: count(), take(), first(), reduce(), countByKey(), collect()
 * 4. Key-Value RDD operations: pair RDD reductions, joins, groupings
 * 5. Spark Concepts: Partitions inspection (glom), Lineage & DAG (toDebugString),
 *    Fault tolerance mechanisms, and Cache/Persist benchmarking.
 */

// Strongly typed case class representing an accident telemetry record
case class AccidentRecord(
  id: String,
  severity: Int,
  startTime: String,
  endTime: String,
  startLat: Double,
  startLng: Double,
  distanceMi: Double,
  city: String,
  county: String,
  state: String,
  timezone: String,
  tempF: Double,
  humidityPct: Double,
  visibilityMi: Double,
  windSpeedMph: Double,
  precipIn: Double,
  weatherCondition: String,
  amenityFlag: Int,
  crossingFlag: Int,
  junctionFlag: Int,
  trafficSignalFlag: Int,
  sunriseSunset: String,
  accidentYear: Int,
  accidentMonth: Int,
  accidentHour: Int,
  accidentDayOfWeek: String,
  durationMinutes: Double
)

object SafeRoadsSparkApp {

  def main(args: Array[String]): Unit = {
    println("================================================================================")
    println("   SafeRoads - Continental Traffic Accident Big Data Analytics Pipeline")
    println("              Course: 23CSE352 - Big Data Analytics (Review 3)")
    println("   Group 12 | Apache Spark & Scala Distributed RDD Processing Engine")
    println("================================================================================")

    val inputPath = if (args.length > 0) args(0) else "data/processed/accidents_cleaned_sample.tsv"

    // -------------------------------------------------------------------------
    // STEP 1: INITIALIZE SPARK CONFIGURATION AND CONTEXT
    // -------------------------------------------------------------------------
    val conf = new SparkConf()
      .setAppName("SafeRoads-ScalaSpark-Analytics")
      .setMaster("local[*]") // Utilize all available CPU cores locally
      .set("spark.driver.memory", "4g")
      .set("spark.executor.memory", "4g")
      .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

    val sc = new SparkContext(conf)
    sc.setLogLevel("WARN")

    val startTimeMs = System.currentTimeMillis()

    // -------------------------------------------------------------------------
    // STEP 2: RDD CREATION & PARTITION INSPECTION
    // -------------------------------------------------------------------------
    println("\n[STEP 2.1] Creating Base RDD from Distributed Dataset...")
    val rawTextRDD = sc.textFile(inputPath, minPartitions = 4)

    println(s"-> Dataset Path: $inputPath")
    println(s"-> Initial RDD Partition Count: ${rawTextRDD.getNumPartitions}")

    // Inspect records per partition using glom()
    val recordsPerPartition = rawTextRDD.glom().map(_.length).collect()
    recordsPerPartition.zipWithIndex.foreach { case (count, idx) =>
      println(s"   - Partition [$idx] Size: $count raw records")
    }

    // -------------------------------------------------------------------------
    // STEP 3: TRANSFORMATIONS (Narrow & Wide)
    // -------------------------------------------------------------------------
    println("\n[STEP 3.1] Transformation 1: filter() Header & Malformed Lines")
    val header = rawTextRDD.first()
    val dataWithoutHeaderRDD = rawTextRDD.filter(line => line != header && line.trim.nonEmpty)

    println("\n[STEP 3.2] Transformation 2: map() TSV Parsing into Case Class")
    val parsedAccidentsRDD = dataWithoutHeaderRDD.flatMap { line =>
      val cols = line.split("\t")
      if (cols.length >= 27) {
        try {
          Some(AccidentRecord(
            id = cols(0).trim,
            severity = cols(1).trim.toInt,
            startTime = cols(2).trim,
            endTime = cols(3).trim,
            startLat = cols(4).trim.toDouble,
            startLng = cols(5).trim.toDouble,
            distanceMi = cols(6).trim.toDouble,
            city = cols(7).trim,
            county = cols(8).trim,
            state = cols(9).trim,
            timezone = cols(10).trim,
            tempF = cols(11).trim.toDouble,
            humidityPct = cols(12).trim.toDouble,
            visibilityMi = cols(13).trim.toDouble,
            windSpeedMph = cols(14).trim.toDouble,
            precipIn = cols(15).trim.toDouble,
            weatherCondition = cols(16).trim,
            amenityFlag = cols(17).trim.toInt,
            crossingFlag = cols(18).trim.toInt,
            junctionFlag = cols(19).trim.toInt,
            trafficSignalFlag = cols(20).trim.toInt,
            sunriseSunset = cols(21).trim,
            accidentYear = cols(22).trim.toInt,
            accidentMonth = cols(23).trim.toInt,
            accidentHour = cols(24).trim.toInt,
            accidentDayOfWeek = cols(25).trim,
            durationMinutes = cols(26).trim.toDouble
          ))
        } catch {
          case _: Exception => None
        }
      } else {
        None
      }
    }

    // -------------------------------------------------------------------------
    // DEMONSTRATION OF CACHE() & PERSIST()
    // -------------------------------------------------------------------------
    println("\n[SPARK CONCEPTS] Demonstrating RDD Cache / Persist Benchmarking:")
    println("-> Persisting parsedAccidentsRDD into MEMORY_AND_DISK for iterative operations...")
    parsedAccidentsRDD.persist(StorageLevel.MEMORY_AND_DISK)

    // Benchmark Run 1 (Cold / Uncached):
    val t0 = System.currentTimeMillis()
    val totalCount = parsedAccidentsRDD.count()
    val t1 = System.currentTimeMillis()
    println(s"-> Uncached Count: $totalCount records (Execution Time: ${t1 - t0} ms)")

    // Benchmark Run 2 (Warm / Cached):
    val t2 = System.currentTimeMillis()
    val cachedCount = parsedAccidentsRDD.count()
    val t3 = System.currentTimeMillis()
    println(s"-> Cached Count: $cachedCount records (Execution Time: ${t3 - t2} ms - ${(t1 - t0).toDouble / Math.max(1, (t3 - t2))}x speedup!)")

    // -------------------------------------------------------------------------
    // STEP 3.3: Transformation 3: filter() for High Severity Accidents (Severity >= 3)
    // -------------------------------------------------------------------------
    val severeAccidentsRDD = parsedAccidentsRDD.filter(_.severity >= 3)
    val severeCount = severeAccidentsRDD.count()
    println(s"\n-> Severe Accidents (Severity >= 3): $severeCount records (${(severeCount * 100.0 / totalCount).formatted("%.2f")}%)")

    // -------------------------------------------------------------------------
    // STEP 3.4: KEY-VALUE RDD OPERATIONS: reduceByKey & aggregateByKey
    // -------------------------------------------------------------------------
    println("\n[STEP 3.4] Key-Value Pair RDD Operation: Total Accidents by State (reduceByKey)")
    val stateCountPairsRDD = parsedAccidentsRDD.map(a => (a.state, 1))
    val stateTotalAccidentsRDD = stateCountPairsRDD.reduceByKey(_ + _)

    // Transformation: sortBy() descending
    val top10States = stateTotalAccidentsRDD.sortBy(_._2, ascending = false).take(10)
    println("   Top 10 States with Highest Accident Frequency:")
    top10States.zipWithIndex.foreach { case ((st, cnt), rank) =>
      println(f"   ${rank + 1}%2d. State: $st%4s | Total Accidents: $cnt%,7d (${cnt * 100.0 / totalCount}%5.2f%%)")
    }

    // Key-Value Operation: Average Delay Duration per State using aggregateByKey
    println("\n[STEP 3.5] Key-Value Pair RDD Operation: Average Duration per State (aggregateByKey)")
    // Zero value: (sumDuration: Double, count: Long)
    val stateDurationAggregate = parsedAccidentsRDD.map(a => (a.state, a.durationMinutes))
      .aggregateByKey((0.0, 0L))(
        seqOp = (acc, dur) => (acc._1 + dur, acc._2 + 1L),
        combOp = (acc1, acc2) => (acc1._1 + acc2._1, acc1._2 + acc2._2)
      )

    // Transformation: mapValues() to calculate arithmetic mean
    val stateAvgDurationRDD = stateDurationAggregate.mapValues { case (sum, cnt) =>
      if (cnt > 0) sum / cnt else 0.0
    }

    // Key-Value Operation: join() between State Crash Counts and State Avg Duration
    println("\n[STEP 3.6] Key-Value Pair RDD Operation: join() (State Volume JOIN State Delay)")
    val stateSummaryJoinedRDD = stateTotalAccidentsRDD.join(stateAvgDurationRDD)
    val topJoinedStates = stateSummaryJoinedRDD.sortBy(_._2._1, ascending = false).take(5)
    println("   Top 5 Joined State Hazard Metrics:")
    topJoinedStates.foreach { case (st, (cnt, avgDur)) =>
      println(f"   State: $st%4s | Total Crashes: $cnt%,7d | Mean Roadway Clearance Delay: $avgDur%6.1f mins")
    }

    // -------------------------------------------------------------------------
    // STEP 3.7: Transformation: flatMap() Multi-hazard Tokenization
    // -------------------------------------------------------------------------
    println("\n[STEP 3.7] Transformation 4: flatMap() Roadway Infrastructure Hazard Fan-Out")
    val infrastructureTokensRDD = parsedAccidentsRDD.flatMap { a =>
      val tokens = scala.collection.mutable.ListBuffer[String]()
      if (a.junctionFlag == 1) tokens += "Hazard_Junction"
      if (a.trafficSignalFlag == 1) tokens += "Hazard_TrafficSignal"
      if (a.crossingFlag == 1) tokens += "Hazard_PedestrianCrossing"
      if (a.amenityFlag == 1) tokens += "Hazard_CommercialAmenity"
      if (tokens.isEmpty) tokens += "Hazard_StandardRoadway"
      tokens.map(tag => (tag, 1))
    }
    val infrastructureBreakdown = infrastructureTokensRDD.reduceByKey(_ + _).collect()
    println("   Infrastructure Hazard Frequency:")
    infrastructureBreakdown.foreach { case (tag, count) =>
      println(f"   - $tag%-26s: $count%,7d crashes")
    }

    // -------------------------------------------------------------------------
    // STEP 4: SPARK ACTIONS (Demonstration of count, take, first, reduce, countByKey)
    // -------------------------------------------------------------------------
    println("\n================================================================================")
    println("                     APACHE SPARK ACTIONS DEMONSTRATION")
    println("================================================================================")
    // Action 1: first()
    val sampleRec = parsedAccidentsRDD.first()
    println(s"Action 1 [first()]: Sample ID: ${sampleRec.id}, State: ${sampleRec.state}, Severity: ${sampleRec.severity}")

    // Action 2: count()
    println(s"Action 2 [count()]: Verified RDD Row Count: $totalCount records")

    // Action 3: take(3)
    val sampleTake = parsedAccidentsRDD.take(3)
    println(s"Action 3 [take(3)]: Retrieved ${sampleTake.length} sample elements to driver")

    // Action 4: reduce() - Total cumulative delay across continental US
    val totalDelayMinutes = parsedAccidentsRDD.map(_.durationMinutes).reduce(_ + _)
    val totalDelayHours = totalDelayMinutes / 60.0
    println(f"Action 4 [reduce()]: Continental Traffic Delay Sum: $totalDelayHours%,10.1f hours")

    // Action 5: countByKey() - Severity distribution
    val severityPairRDD = parsedAccidentsRDD.map(a => (s"Severity_${a.severity}", 1))
    val severityDistribution = severityPairRDD.countByKey()
    println("Action 5 [countByKey()]: Severity Class Breakdown:")
    severityDistribution.toSeq.sortBy(_._1).foreach { case (sev, cnt) =>
      println(f"   - $sev%12s: $cnt%,7d incidents (${cnt * 100.0 / totalCount}%5.2f%%)")
    }

    // -------------------------------------------------------------------------
    // STEP 5: SPARK CONCEPTS: LINEAGE, DAG & FAULT TOLERANCE
    // -------------------------------------------------------------------------
    println("\n================================================================================")
    println("              SPARK CONCEPTS: RDD LINEAGE & DAG (toDebugString)")
    println("================================================================================")
    println("RDD Lineage Graph for stateSummaryJoinedRDD:")
    println(stateSummaryJoinedRDD.toDebugString)

    println("\nKey Spark Architecture Notes:")
    println("1. Lineage & DAG: Spark builds an execution plan of transformations lazily.")
    println("   No computation occurs until an Action (count, collect, reduce) is invoked.")
    println("2. Narrow vs Wide Dependencies:")
    println("   - Narrow (map, filter): Executed within the same partition without data shuffling.")
    println("   - Wide (reduceByKey, join): Requires data exchange across partitions (Shuffle Stage).")
    println("3. Fault Tolerance: If an executor node crashes or a partition is lost,")
    println("   Spark re-evaluates only the lost partition using the deterministic Lineage Graph.")
    println("4. In-Memory Persistence: Cache reduces disk I/O and CPU recomputation for ML iterations.")

    val endTimeMs = System.currentTimeMillis()
    println(f"\n[EXECUTION COMPLETED] Pipeline processed $totalCount%,d records in ${(endTimeMs - startTimeMs) / 1000.0}%.2f seconds.")
    println("================================================================================")

    sc.stop()
  }
}
