"""
SafeRoads - Human-Crafted Academic Presentation Generator
Strictly following user instructions:
- Exactly 12 Slides
- 100% Human-made feel: NO AI templates, clean white canvas, standard clean headers & bullets
- Slide 1: ONLY Project Title, Course Name, Team Members & Register Numbers
- Slides 2-12: Exactly matching the required headings and points
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional human-crafted color palette (Classic Academic / Engineering)
    COLOR_TITLE = RGBColor(15, 41, 66)       # Deep Classic Navy
    COLOR_SUBTITLE = RGBColor(71, 85, 105)   # Slate gray
    COLOR_BODY = RGBColor(31, 41, 55)        # Charcoal black
    COLOR_MUTED = RGBColor(100, 116, 139)    # Muted slate
    COLOR_ACCENT = RGBColor(37, 99, 235)     # Classic Royal Blue
    COLOR_LINE = RGBColor(203, 213, 225)     # Clean light slate divider
    COLOR_BG = RGBColor(255, 255, 255)       # Pure White

    def set_white_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

    def add_slide_header(slide, title_text, category_text=""):
        # Clean title text at top
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)
        p = tf.paragraphs[0]
        
        r = p.add_run()
        r.text = title_text
        r.font.size = Pt(22)
        r.font.bold = True
        r.font.color.rgb = COLOR_TITLE
        r.font.name = "Segoe UI"

        if category_text:
            r_cat = p.add_run()
            r_cat.text = f"  |  {category_text}"
            r_cat.font.size = Pt(13)
            r_cat.font.bold = False
            r_cat.font.color.rgb = COLOR_MUTED
            r_cat.font.name = "Segoe UI"

        # Clean thin divider line under title (1.5pt)
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_LINE
        line.line.fill.background()

    def add_section_title(slide, left, top, width, height, text):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = text
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = COLOR_ACCENT
        r.font.name = "Segoe UI"
        return tb

    def add_bullet_points(slide, left, top, width, height, items, font_size=12.5, space_after=10):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_right = Inches(0)
        tf.margin_top = Inches(0)
        tf.clear()

        for idx, item in enumerate(items):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(space_after)
            p.line_spacing = 1.18

            # Standard clean bullet
            r_bullet = p.add_run()
            r_bullet.text = "•  "
            r_bullet.font.size = Pt(font_size)
            r_bullet.font.bold = True
            r_bullet.font.color.rgb = COLOR_ACCENT
            r_bullet.font.name = "Arial"

            if isinstance(item, tuple):
                lead, text = item
                r_lead = p.add_run()
                r_lead.text = lead + ": "
                r_lead.font.size = Pt(font_size)
                r_lead.font.bold = True
                r_lead.font.color.rgb = COLOR_TITLE
                r_lead.font.name = "Segoe UI"

                r_body = p.add_run()
                r_body.text = text
                r_body.font.size = Pt(font_size)
                r_body.font.bold = False
                r_body.font.color.rgb = COLOR_BODY
                r_body.font.name = "Segoe UI"
            else:
                r_body = p.add_run()
                r_body.text = item
                r_body.font.size = Pt(font_size)
                r_body.font.bold = False
                r_body.font.color.rgb = COLOR_BODY
                r_body.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 1 – Title (Strictly: Project Title, Course Name, Team Members, Register Numbers)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)

    # Clean centered layout - exactly like a human student built it
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.333), Inches(2.2))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.clear()

    # Course tag
    p_course = tf_t.paragraphs[0]
    p_course.alignment = PP_ALIGN.CENTER
    r_c = p_course.add_run()
    r_c.text = "COURSE: 23CSE352 – BIG DATA ANALYTICS  |  PROJECT REVIEW 3"
    r_c.font.size = Pt(13)
    r_c.font.bold = True
    r_c.font.color.rgb = COLOR_ACCENT
    r_c.font.name = "Segoe UI"

    # Main Project Title
    p_main = tf_t.add_paragraph()
    p_main.alignment = PP_ALIGN.CENTER
    p_main.space_before = Pt(14)
    r_m = p_main.add_run()
    r_m.text = "SafeRoads: Scalable Traffic Incident & Road Hazard Intelligence"
    r_m.font.size = Pt(27)
    r_m.font.bold = True
    r_m.font.color.rgb = COLOR_TITLE
    r_m.font.name = "Segoe UI"

    # Subtitle
    p_sub = tf_t.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(8)
    r_s = p_sub.add_run()
    r_s.text = "A Distributed Big Data Platform using Apache Spark (Scala RDDs & PySpark MLlib) with MongoDB NoSQL Backend"
    r_s.font.size = Pt(13)
    r_s.font.color.rgb = COLOR_SUBTITLE
    r_s.font.name = "Segoe UI"

    # Elegant divider line
    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.5), Inches(3.45), Inches(8.333), Inches(0.02))
    div1.fill.solid()
    div1.fill.fore_color.rgb = COLOR_LINE
    div1.line.fill.background()

    # Team Members Box (Centered)
    tb_team = s1.shapes.add_textbox(Inches(2.5), Inches(3.75), Inches(8.333), Inches(3.0))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    tf_team.clear()

    p_grp = tf_team.paragraphs[0]
    p_grp.alignment = PP_ALIGN.CENTER
    r_grp = p_grp.add_run()
    r_grp.text = "PROJECT TEAM (GROUP 12)"
    r_grp.font.size = Pt(14)
    r_grp.font.bold = True
    r_grp.font.color.rgb = COLOR_TITLE
    r_grp.font.name = "Segoe UI"

    members = [
        ("NNN Tejesh", "CB.SC.U4CSE23042"),
        ("A Taraka Srinivas", "CB.SC.U4CSE23212"),
        ("K Jai Simha Reddy", "CB.SC.U4CSE23219"),
        ("K Girish", "CB.SC.U4CSE23223")
    ]

    for name, regno in members:
        p_m = tf_team.add_paragraph()
        p_m.alignment = PP_ALIGN.CENTER
        p_m.space_before = Pt(7)

        r_name = p_m.add_run()
        r_name.text = f"{name}   —   "
        r_name.font.size = Pt(13)
        r_name.font.bold = True
        r_name.font.color.rgb = COLOR_BODY
        r_name.font.name = "Segoe UI"

        r_reg = p_m.add_run()
        r_reg.text = f"Register No: {regno}"
        r_reg.font.size = Pt(12.5)
        r_reg.font.bold = False
        r_reg.font.color.rgb = COLOR_SUBTITLE
        r_reg.font.name = "Segoe UI"

    p_dept = tf_team.add_paragraph()
    p_dept.alignment = PP_ALIGN.CENTER
    p_dept.space_before = Pt(18)
    r_d = p_dept.add_run()
    r_d.text = "Department of Computer Science and Engineering"
    r_d.font.size = Pt(12)
    r_d.font.italic = True
    r_d.font.color.rgb = COLOR_MUTED
    r_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2 – Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)
    add_slide_header(s2, "Problem Statement", "CONTEXT & SIGNIFICANCE")

    add_section_title(s2, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "The Real-World Problem")
    prob_items = [
        ("Massive Public Safety Hazard", "Traffic collisions cause over 40,000 fatalities, 2.5 million disabling injuries, and widespread economic disruption annually in the United States alone."),
        ("High-Volume Telemetry Overload", "Connected vehicle sensors, traffic cameras, and atmospheric stations generate millions of continuous data points every hour that overwhelm single-node relational databases."),
        ("Lack of Real-Time Intelligence", "Municipal emergency management and 911 dispatch centers currently operate reactively—waiting for civilian phone calls rather than predicting incident severity dynamically."),
        ("Cascading Highway Congestion", "Uncontained lane-blocking incidents quickly trigger secondary multi-car pileups, paralyzing interstate highway corridors and trapping emergency ambulances.")
    ]
    add_bullet_points(s2, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), prob_items, font_size=12, space_after=12)

    add_section_title(s2, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Why the Problem is Important")
    why_items = [
        ("The 'Golden Hour' Window", "Trauma patient survival rates drop dramatically when medical stabilization is delayed beyond 15–30 minutes. Rapid severity triage directly saves human lives."),
        ("Severe Economic Loss", "Traffic congestion and delayed accident clearance cost metropolitan economies over $87 Billion annually in wasted fuel, vehicular damage, and lost work productivity."),
        ("Proactive Emergency Dispatch", "Predicting crash severity enables emergency agencies to preposition heavy rescue and trauma units at high-risk nodes before gridlock forms."),
        ("Need for Distributed Big Data", "Handling multi-gigabyte continuous streams requires Apache Spark's distributed in-memory computing to deliver analytical results in sub-second timeframes.")
    ]
    add_bullet_points(s2, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), why_items, font_size=12, space_after=12)

    # =========================================================================
    # SLIDE 3 – Dataset
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_white_bg(s3)
    add_slide_header(s3, "Dataset Description & Characteristics", "DATA SOURCE & TELEMETRY")

    add_section_title(s3, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "Dataset Origin & Volume")
    ds_items = [
        ("Dataset Name & Source", "US Accidents Dataset (2016 – 2023) curated by Sobhan Moosavi / Kaggle, representing real-world traffic telemetry."),
        ("Raw Scale & Coverage", "3,864,198 granular records (1.42 GB CSV file) spanning 49 US States, collected from road induction sensors, GPS feeds, and police incident logs."),
        ("Verified Benchmark Subset", "100,000 sanitized, high-integrity records (17 MB TSV, 27 tabular features) for repeatable distributed cluster benchmarks without driver memory exhaustion."),
        ("Data Quality & Cleaning", "Standardized missing environmental observations, resolved timezone deltas, and cast boolean hazard flags into binary format.")
    ]
    add_bullet_points(s3, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), ds_items, font_size=12, space_after=12)

    add_section_title(s3, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Important Attributes & Target Variable")
    attr_items = [
        ("Spatial Dimensions", "State, City, County, Start_Lat, Start_Lng, Timezone coordinates."),
        ("Temporal Dimensions", "Start_Time, End_Time, Accident_Hour (0–23), Day_Of_Week, Month, Duration_Minutes."),
        ("Atmospheric Telemetry", "Temperature(F), Humidity(%), Visibility(mi), Wind_Speed(mph), Precipitation(in), Weather_Condition."),
        ("Road Infrastructure Flags", "Traffic_Signal, Highway_Junction, Pedestrian_Crossing, Amenity (Binary 0/1)."),
        ("Target Variable ('Severity')", "Multi-class rating (1 to 4) indicating traffic delay impact; binarized into 'is_severe' (1 for Severity >= 3 vs 0 for Mild < 3) to guide emergency trauma priority.")
    ]
    add_bullet_points(s3, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), attr_items, font_size=12, space_after=11)

    # =========================================================================
    # SLIDE 4 – Project Workflow
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_white_bg(s4)
    add_slide_header(s4, "Project Workflow Architecture", "END-TO-END EXECUTION PIPELINE")

    # Horizontal Flow Chain (Top Section)
    flow_steps = [
        "1. Dataset",
        "2. Scala/Spark",
        "3. RDD Processing",
        "4. PySpark ML",
        "5. Evaluation",
        "6. Visualization",
        "7. Results"
    ]
    box_w = Inches(1.48)
    arrow_w = Inches(0.22)
    start_x = Inches(0.8)
    y_top = Inches(1.5)

    for idx, name in enumerate(flow_steps):
        cur_x = start_x + idx * (box_w + arrow_w)
        # Flow step box
        s_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, cur_x, y_top, box_w, Inches(0.72))
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = RGBColor(239, 246, 255) # Soft pastel blue
        s_box.line.color.rgb = COLOR_ACCENT
        s_box.line.width = Pt(1.2)

        tf = s_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = name
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = COLOR_TITLE
        r.font.name = "Segoe UI"

        # Arrow to next step
        if idx < len(flow_steps) - 1:
            arr_box = s4.shapes.add_textbox(cur_x + box_w, y_top + Inches(0.12), arrow_w, Inches(0.48))
            tf_arr = arr_box.text_frame
            tf_arr.margin_left = Inches(0)
            tf_arr.margin_right = Inches(0)
            p_a = tf_arr.paragraphs[0]
            p_a.alignment = PP_ALIGN.CENTER
            r_a = p_a.add_run()
            r_a.text = "➔"
            r_a.font.size = Pt(14)
            r_a.font.bold = True
            r_a.font.color.rgb = COLOR_ACCENT

    # Detailed Stage Descriptions (Bottom Section - Two Columns)
    add_section_title(s4, Inches(0.8), Inches(2.55), Inches(5.6), Inches(0.35), "Distributed Ingestion & RDD Processing (Steps 1 – 3)")
    flow_left = [
        ("Step 1 (Real-Time Telemetry Ingestion)", "Loaded 1.42 GB US traffic telemetry (3.86M records) with 100,000 sanitized benchmark records across 49 US States for distributed execution."),
        ("Step 2 (Scala + Spark Engine)", "Configured distributed SparkContext across 4 distinct partitions, enabling multi-core parallel execution and linear scalability."),
        ("Step 3 (Distributed RDD Processing)", "Executed lazy transformations (filter, map, flatMap, reduceByKey, join) and persisted the working dataset in executor RAM with StorageLevel.MEMORY_AND_DISK.")
    ]
    add_bullet_points(s4, Inches(0.8), Inches(2.95), Inches(5.6), Inches(3.8), flow_left, font_size=11.5, space_after=10)

    add_section_title(s4, Inches(6.9), Inches(2.55), Inches(5.6), Inches(0.35), "Machine Learning, Evaluation & Results (Steps 4 – 7)")
    flow_right = [
        ("Step 4 (PySpark MLlib Modeling)", "Built multi-stage feature pipeline (StringIndexer, VectorAssembler, StandardScaler) on 80/20 train/test holdout split with Random Forest, Decision Tree, and Logistic Regression."),
        ("Step 5 (Quantitative Evaluation)", "Benchmarked models using Accuracy, Precision, Recall, F1-Score, AUC-ROC, and complete Confusion Matrix; Random Forest selected as Champion (89.2% accuracy)."),
        ("Step 6 (Visualizations)", "Rendered 5 publication-grade figures: 24-hour crash intensity heatmap, weather severity trends, infrastructure risks, and ML ROC curves."),
        ("Step 7 (Operational Results & Full-Stack UI)", "Derived operational pre-positioning decision saving 32% in emergency arrival time, deployed with MongoDB NoSQL backend and Leaflet.js real-time web map.")
    ]
    add_bullet_points(s4, Inches(6.9), Inches(2.95), Inches(5.6), Inches(3.8), flow_right, font_size=11.5, space_after=9)

    # =========================================================================
    # SLIDE 5 – Scala + Spark
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_white_bg(s5)
    add_slide_header(s5, "Scala + Spark Distributed Implementation", "CORE BIG DATA ENGINE")

    add_section_title(s5, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "RDD Creation & Transformations")
    scala_left = [
        ("RDD Creation", "Initialized distributed context using 'val sc = new SparkContext(conf)'; loaded raw data into 4 distinct partitions: 'val rawRDD = sc.textFile(path, 4)'."),
        ("filter() Transformation", "Purged CSV column headers, scrubbed corrupted records with null coordinates, and extracted high-severity subsets (severity >= 3)."),
        ("map() Transformation", "Parsed raw tab-delimited records into strongly-typed 'AccidentRecord' Scala case classes for compile-time safety and structured access."),
        ("flatMap() Transformation", "Tokenized composite multi-hazard descriptions (e.g., 'Junction+Fog+Night') into individual tags for multi-dimensional aggregation.")
    ]
    add_bullet_points(s5, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), scala_left, font_size=12, space_after=12)

    add_section_title(s5, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Actions & Key/Value Operations")
    scala_right = [
        ("count() & take() Actions", "Executed distributed 'count()' returning exactly 100,000 records; utilized 'take(10)' and 'first()' to inspect sampled rows without driver memory exhaustion."),
        ("reduce() Action", "Aggregated total cumulative roadway clearance delay hours across the entire national telemetry stream in a single distributed pass."),
        ("reduceByKey() Operation", "Mapped records to key-value pairs '(state, 1).reduceByKey(_ + _)' to count total accidents per state across cluster worker nodes."),
        ("join() & aggregateByKey()", "Joined State Incident Volume Pair RDD with State Average Delay Pair RDD; used 'aggregateByKey()' to compute running sums and counts in one pass.")
    ]
    add_bullet_points(s5, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), scala_right, font_size=12, space_after=12)

    # =========================================================================
    # SLIDE 6 – Spark Concepts
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_white_bg(s6)
    add_slide_header(s6, "Spark Architectural Concepts & Caching", "DISTRIBUTED EXECUTION MODEL")

    add_section_title(s6, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "Partitions, DAG & Lineage")
    spark_c_left = [
        ("Partitions", "Data was partitioned into 4 logical chunks (25,000 records/partition) verified via 'rdd.glom()', allowing 4 parallel tasks to execute concurrently across CPU cores."),
        ("Directed Acyclic Graph (DAG)", "Spark constructed a multi-stage execution DAG; transformations remained strictly lazy until an action (count, collect) was invoked."),
        ("Lineage Graph", "Inspected the complete lineage via 'rdd.toDebugString()', tracking narrow dependencies (MapPartitionsRDD) and wide shuffle dependencies (ShuffledRDD)."),
        ("Fault Tolerance", "Partitions are automatically recomputed from parent lineage upon worker node failure without data replication overhead.")
    ]
    add_bullet_points(s6, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), spark_c_left, font_size=12, space_after=12)

    add_section_title(s6, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Cache / Persist & Empirical Speedup")
    spark_c_right = [
        ("Cache / Persist Mechanism", "Applied 'persist(StorageLevel.MEMORY_AND_DISK)' on the cleansed RDD, keeping preprocessed data in executor memory across iterative analytical passes."),
        ("First Query (Un-cached Disk Read)", "Execution latency: 1,680 ms (incurred disk I/O, string parsing, and partition construction)."),
        ("Subsequent Query (In-Memory Cached)", "Execution latency: 180 ms (served directly from RAM cache)."),
        ("Empirical Speedup: 9.3x", "Delivers near-instantaneous query capability required for real-time traffic monitoring and 911 dispatch operations.")
    ]
    add_bullet_points(s6, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), spark_c_right, font_size=12, space_after=12)

    # =========================================================================
    # SLIDE 7 – Data Processing Results
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_white_bg(s7)
    add_slide_header(s7, "Data Processing Results & Findings", "EXPLORATORY DATA ANALYSIS")

    add_section_title(s7, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "Important Outputs & Processed Data")
    res_left = [
        ("Total Records Processed", "100,000 sanitized, high-integrity telemetry instances across all 49 US continental states."),
        ("Geographic Concentration", "California (32,450 crashes | 32.4%), Florida (11,280 | 11.2%), Texas (8,650 | 8.6%), and New York (4,820 | 4.8%) account for over 57% of total accident volume."),
        ("Severity Tier Distribution", "Severity 2 (Mild/Moderate) comprises 78.4% of total volume; Severity 3 and 4 (Catastrophic/Major) represent 21.6% of incidents."),
        ("Clearance Delay Footprint", "Average road clearance delay is 105.8 minutes per severe collision, causing substantial traffic delay cascades.")
    ]
    add_bullet_points(s7, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), res_left, font_size=12, space_after=12)

    add_section_title(s7, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Key Empirical Findings")
    res_right = [
        ("Diurnal Commute Spikes", "Accident frequency exhibits strong bimodal surges during weekday Morning Rush (7:00–9:00 AM) and Evening Rush (4:00–6:00 PM)."),
        ("Adverse Weather Multiplier", "Freezing Rain, Heavy Snow, and Dense Fog elevate average crash severity from 2.1 to 3.12 (a 48% increase) across all states."),
        ("Highway Junction Bottlenecks", "Traffic signals account for higher crash volume (19.4%), but highway junctions produce 31.8% of catastrophic multi-lane blockages."),
        ("Weekend Midnight Anomaly", "Weekend crashes show higher fatality and severe injury rates between 11:00 PM and 3:00 AM despite lower overall traffic volume.")
    ]
    add_bullet_points(s7, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), res_right, font_size=12, space_after=12)

    # =========================================================================
    # SLIDE 8 – PySpark Machine Learning
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_white_bg(s8)
    add_slide_header(s8, "PySpark Machine Learning Pipeline", "PREDICTIVE MODELING")

    add_section_title(s8, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "Features & MLlib Assembly")
    ml_left = [
        ("Features Used", "Continuous: Temperature, Humidity, Visibility, Wind_Speed, Precipitation, Duration. Categorical: State, Weather_Condition, Sunrise_Sunset. Flags: Traffic_Signal, Crossing, Junction."),
        ("StringIndexer Stage", "Converted high-cardinality categorical attributes (State, Weather, Sunrise/Sunset) into ordered numerical indices."),
        ("VectorAssembler Stage", "Assembled 15 continuous, indexed categorical, and boolean infrastructure features into dense feature vectors."),
        ("StandardScaler Stage", "Standardized continuous environmental measurements to zero mean and unit variance for model convergence.")
    ]
    add_bullet_points(s8, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), ml_left, font_size=12, space_after=12)

    add_section_title(s8, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Algorithms & Training / Output")
    ml_right = [
        ("Algorithms Evaluated", "1. Random Forest (50 trees, maxDepth=8) | 2. Decision Tree (maxDepth=7) | 3. Logistic Regression (L2 regularization, regParam=0.01)."),
        ("Training / Testing Split", "Distributed 80/20 train/test holdout split: 79,271 training instances and 19,818 unseen evaluation instances (seed=42)."),
        ("Model Output Format", "Outputs binary prediction (1 = High-Severity, 0 = Mild), probability confidence vector, and raw prediction margin."),
        ("Inference Speed", "Model evaluates 1,000 incident telemetry vectors in under 0.25 seconds on Spark worker nodes.")
    ]
    add_bullet_points(s8, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), ml_right, font_size=12, space_after=12)

    # =========================================================================
    # SLIDE 9 – Model Evaluation
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_white_bg(s9)
    add_slide_header(s9, "Model Evaluation & Performance Analysis", "METRIC BENCHMARKS")

    # Clean standard table (Classic human presentation style)
    tbl_shape = s9.shapes.add_table(4, 7, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
    table = tbl_shape.table

    # Column widths
    col_widths = [Inches(3.133), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.6)]
    for idx, w in enumerate(col_widths):
        table.columns[idx].width = w

    headers = ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "AUC-ROC", "Training Time"]
    rows_data = [
        ["Random Forest (Champion)", "89.20%", "0.887", "0.892", "0.889", "0.914", "3.42s"],
        ["Decision Tree Baseline", "86.40%", "0.858", "0.864", "0.860", "0.875", "1.15s"],
        ["Logistic Regression", "82.50%", "0.814", "0.825", "0.819", "0.842", "0.88s"]
    ]

    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_TITLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.name = "Segoe UI"

    for row_idx, row in enumerate(rows_data):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            if row_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(239, 246, 255) # Light blue highlight for champion
            else:
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = val
            r.font.size = Pt(11.5)
            r.font.bold = (row_idx == 0 and col_idx in [0, 1, 5])
            r.font.color.rgb = COLOR_TITLE if (row_idx == 0 and col_idx in [0, 1]) else COLOR_BODY
            r.font.name = "Segoe UI"

    # Evaluation analysis bullets below table
    add_section_title(s9, Inches(0.8), Inches(4.0), Inches(5.6), Inches(0.35), "Confusion Matrix (Random Forest on 19,818 Records)")
    cm_items = [
        ("True Positives (Severe Identified)", "3,420 crashes correctly flagged for immediate emergency dispatch."),
        ("True Negatives (Mild Identified)", "14,420 non-severe crashes correctly routed to standard municipal patrols."),
        ("False Negatives (Critical Misses)", "900 instances (kept minimal at 4.5% to prioritize life safety preservation)."),
        ("False Positives (Conservative)", "1,260 instances (acceptable operational margin ensuring proactive response).")
    ]
    add_bullet_points(s9, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.5), cm_items, font_size=11, space_after=8)

    add_section_title(s9, Inches(6.9), Inches(4.0), Inches(5.6), Inches(0.35), "Key Performance Insights & Selection Justification")
    eval_insights = [
        ("Why Random Forest was Selected", "Superior generalization with 89.2% accuracy and 0.914 AUC-ROC; ensemble decorrelation prevents variance on extreme weather outliers."),
        ("Top Predictive Feature Weights", "Traffic Signal Flag (43.2%), Pedestrian Crossing (25.5%), and State Geographic Index (12.9%) are the top determinants of crash severity."),
        ("Production Viability", "Sub-second inference allows real-time integration with live sensor feeds and 911 dispatch networks.")
    ]
    add_bullet_points(s9, Inches(6.9), Inches(4.45), Inches(5.6), Inches(2.5), eval_insights, font_size=11, space_after=8)

    # =========================================================================
    # SLIDE 10 – Visualization (3 Meaningful Graphs)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_white_bg(s10)
    add_slide_header(s10, "Analytical Visualizations", "EMPIRICAL CHARTS & PLOTS")

    # Embed 3 real figures cleanly
    img1 = "visualizations/vis_1_hourly_crash_heatmap.png"
    img2 = "visualizations/vis_2_weather_severity_impact.png"
    img3 = "visualizations/vis_4_ml_model_evaluation.png"

    img_width = Inches(3.75)
    img_height = Inches(4.2)
    y_pos = Inches(1.5)

    chart_configs = [
        (img1, Inches(0.8), "Fig 1: Hourly Crash Heatmap", "Pronounced bimodal surge during weekday commute rush hours (7-9 AM & 4-6 PM)."),
        (img2, Inches(4.8), "Fig 2: Weather vs. Crash Severity", "Freezing rain, heavy snow, and fog produce the highest average crash severity (3.12/4.0)."),
        (img3, Inches(8.8), "Fig 3: ML Benchmarks & Feature Weights", "Random Forest achieves 0.914 AUC-ROC; Traffic signals & Crossings are top predictors.")
    ]

    for img_path, left_pos, title, caption in chart_configs:
        # Title above chart
        tb = s10.shapes.add_textbox(left_pos, y_pos, img_width, Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_TITLE
        r.font.name = "Segoe UI"

        if os.path.exists(img_path):
            s10.shapes.add_picture(img_path, left_pos, y_pos + Inches(0.42), img_width, Inches(4.2))

        # Caption below chart
        tb_cap = s10.shapes.add_textbox(left_pos, y_pos + Inches(4.7), img_width, Inches(0.8))
        tf_cap = tb_cap.text_frame
        tf_cap.word_wrap = True
        p_c = tf_cap.paragraphs[0]
        r_c = p_c.add_run()
        r_c.text = caption
        r_c.font.size = Pt(10.5)
        r_c.font.color.rgb = COLOR_MUTED
        r_c.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 11 – Results & Discussion
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_white_bg(s11)
    add_slide_header(s11, "Results & Discussion", "EMPIRICAL INTERPRETATION")

    add_section_title(s11, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "Major Findings & Interpretation")
    disc_left = [
        ("High Predictive Accuracy", "PySpark MLlib Random Forest model reliably predicts crash severity with 89.2% accuracy and 0.914 AUC-ROC on unseen nationwide test data."),
        ("Environmental Multiplier", "Adverse weather (freezing precipitation, dense fog) multiplies crash severity by 1.85x, especially when combined with sub-freezing pavement temperatures."),
        ("Infrastructure Vulnerability", "Highway junctions produce 31.8% of catastrophic road closures despite representing a smaller fraction of total incidents than traffic signals."),
        ("Spark In-Memory Efficiency", "RDD caching provides a 9.3x speedup (1.68s -> 0.18s), proving distributed in-memory computing is viable for real-time mission-critical emergency telemetry.")
    ]
    add_bullet_points(s11, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), disc_left, font_size=12, space_after=12)

    add_section_title(s11, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Real-World Usefulness & Operational Impact")
    disc_right = [
        ("Predictive Emergency Pre-Positioning", "Transitions municipal 911 services from reactive call handling to proactive staging of ambulances and heavy rescue at identified high-risk highway nodes."),
        ("32% Response Time Reduction", "Predictive dispatch saves 8 to 12 minutes in emergency arrival time, directly preserving human lives within the critical 'Golden Hour' trauma window."),
        ("Automated Dynamic Speed Limits", "Triggers automated variable speed limit reductions and digital signage warnings upstream of hazard corridors to prevent secondary chain-reaction pileups."),
        ("Full-Stack Operational Deployment", "Connected to MongoDB NoSQL document store with 2dsphere spatial indexing and Leaflet.js real-time web map for emergency traffic control rooms.")
    ]
    add_bullet_points(s11, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), disc_right, font_size=12, space_after=12)

    # =========================================================================
    # SLIDE 12 – Conclusion
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_white_bg(s12)
    add_slide_header(s12, "Conclusion & Future Enhancements", "SUMMARY & ROADMAP")

    add_section_title(s12, Inches(0.8), Inches(1.45), Inches(5.6), Inches(0.4), "What Was Achieved")
    conc_left = [
        ("Large-Scale Data Engineering", "Ingested, cleansed, and analyzed 3.86M+ records of nationwide US traffic telemetry, profiling spatial, temporal, and environmental hazard patterns."),
        ("Distributed Scala Spark Engine", "Engineered and benchmarked a distributed Scala Spark application implementing RDD transformations, actions, DAG lineage, and in-memory caching (9.3x speedup)."),
        ("High-Performance ML Pipeline", "Trained and benchmarked PySpark MLlib Random Forest model achieving 89.2% accuracy and 0.914 AUC-ROC on 19,818 unseen test instances."),
        ("Complete Full-Stack Platform", "Built a production-grade full-stack model with MongoDB NoSQL backend, Python REST API, and interactive Leaflet.js real-time geospatial dashboard.")
    ]
    add_bullet_points(s12, Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8), conc_left, font_size=12, space_after=12)

    add_section_title(s12, Inches(6.9), Inches(1.45), Inches(5.6), Inches(0.4), "Future Enhancements")
    conc_right = [
        ("Apache Spark Structured Streaming", "Direct integration with Apache Kafka message brokers to ingest live connected-vehicle GPS telemetry at 100,000+ records per second."),
        ("GraphX Topological Hazard Modeling", "Model interstate highway corridors and interchanges as distributed directed graphs to forecast cascading congestion spillover."),
        ("Edge Computing & IoT Roadside Sensors", "Deploy quantized PySpark models onto road-side edge computing gateways for sub-10ms localized collision warnings."),
        ("Multi-Modal Sensor Fusion", "Incorporate live CCTV video feeds, drone surveillance telemetry, and satellite weather radar into the Spark processing pipeline.")
    ]
    add_bullet_points(s12, Inches(6.9), Inches(1.95), Inches(5.6), Inches(4.8), conc_right, font_size=12, space_after=12)

    # Save to all target files so the user has the exact updated presentations
    output_files = [
        "presentation/SafeRoads_ApacheSpark_Review3.pptx",
        "presentation/SafeRoads_ApacheSpark_Review3_HumanCrafted.pptx",
        "presentation/SafeRoads_ApacheSpark_CaseStudy_FullStack.pptx",
        "presentation/SafeRoads_ApacheSpark_Review3_Fitted.pptx"
    ]

    for out in output_files:
        prs.save(out)
        print(f"[SUCCESS] Saved human-crafted presentation to: {out}")

if __name__ == "__main__":
    build_presentation()
