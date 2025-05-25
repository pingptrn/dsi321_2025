# Real-Time PM 2.5 Air Quality Data Pipeline with Interactive Visualization
Author: Pattaranit Jaronnaovapat

Course: DSI321 – Big Data Infrastructure

Institution: Data Science and Innovation, Thammasat University

# 🌐 Introduction
This project implements a Real-Time Air Quality Data Pipeline with Interactive Visualization, designed to monitor and analyze PM2.5 pollution levels across Thailand. It integrates a modern, production-grade data stack to automate the full lifecycle of data — from ingestion and cleaning to versioned storage and interactive analytics.

- The primary objectives were to:

- Automate daily data collection from Bangkok's air quality sensors.

- Clean, normalize, and partition the data using Prefect workflows.

- Store the output in a version-controlled Parquet format using lakeFS, enabling time-based querying and reproducibility.

- Enable real-time data exploration via Jupyter Notebooks connected to lakeFS.

- Build an interactive dashboard with Streamlit for visualization.

- Apply K-Means clustering to identify geographical and temporal PM2.5 pollution patterns.

The system is fully containerized using Docker Compose, which orchestrates the following services:

1. **lakeFS (Git-like data version control):**
Manages structured Parquet files under a partitioned folder hierarchy (/year/month/day/hour), allowing rollback, branching, and reproducibility of datasets.

2. **Prefect (workflow automation):**
Schedules and monitors data pipelines through its UI, ensuring daily ingestion, transformation, and delivery of cleaned data into lakeFS.

3. **JupyterLab (EDA and development):**
Enables real-time exploration of air quality data pulled directly from lakeFS via the S3 protocol, facilitating experimentation and notebook-based analysis.

4. **Streamlit (user-facing dashboard):**
Offers an intuitive, web-based interface for users to view trends and anomalies in PM2.5 data, powered by lakeFS-backed storage.


        
# Evidence for the Previous 
1. **Repository Setup & Code Management**
All source code, notebooks, and configuration files are organized under:

🔗  [GitHub Repository - pingptrn/dsi321_2025](https://github.com/pingptrn/dsi321_2025/tree/main)
          
- Project structure follows modular best practices, including:
        
    - work/ for Prefect workflows and pipeline scripts
        
    - app/ for Streamlit dashboard code
        
    - docker-compose.yml for multi-service orchestration
        
 - Version control used throughout development, with meaningful commits and consistent history.

2. **Dataset Preparation and Integration**
   
🔗 The pipeline fetches live PM2.5 data from [Air4Thai](http://air4thai.pcd.go.th/webV3/#/Home).
        
- Data is:
        
  - Cleaned and normalized with Pandas
        
  - Partitioned by year/month/day/hour using datetime fields
        
  - Stored in Parquet format under lakeFS, e.g.:
        lakefs://dsi321-air-quality/main/airquality.parquet/year=2025
<img width="1283" alt="Screenshot 2568-05-25 at 15 07 53" src="https://github.com/user-attachments/assets/718ea6de-3d7f-40b2-ad23-30adaf27360b" />

   - Schema enforcement is performed using a schema.md file to ensure column consistency and reduce data drift.

3. **Workflow Automation with Prefect**
- Prefect workflows were created to:
        
   - Retrieve data
        
   - Process and validate schema
        
   -  Load into lakeFS via S3-compatible path
        
- The flow was deployed via deploy.py and monitored on Prefect UI, with retries and logs handled automatically.

4.**Visualization Infrastructure**
- Streamlit was used to build a responsive dashboard with:
        
   - Dropdown filters (Province / Station)
        
   - Metric boxes, bar charts, and map views
        
- Data is pulled **directly from lakeFS** via s3fs integration.

5. **Challenges and Resolutions**

| Challenge                                       | Solution                                                            |
| ----------------------------------------------- | ------------------------------------------------------------------- |
| Prefect flow not showing on UI                  | Re-deployed using `python deploy.py` after `docker-compose down/up` |
| Timestamp format issues in Parquet              | Fixed by using `.dt.strftime('%Y-%m-%d %H:%M:%S')`                  |
| Schema mismatches                               | Enforced `schema.md` validation inside the pipeline                 |
| Loss of previously collected data after rebuild | Validated lakeFS persisted history and used commit log to recover   |


# Visualization of the Gathered Data
This section showcases interactive and static visualizations from the Streamlit dashboard, developed using Matplotlib and Plotly, to explore trends in Thailand’s PM2.5 air quality data.

🔍 ***Interactive Filtering: Province & Station Selectors***

<img width="970" alt="Screenshot 2568-05-18 at 20 23 19" src="https://github.com/user-attachments/assets/304dd800-7c92-4b85-92a2-884303bb2624" />

<ins>Description:</ins>
The dashboard includes dropdown filters for:

   - Province

   - Station

These filters allow users to narrow down PM2.5 data visualizations to specific regions or stations. When applied, all charts and KPIs dynamically update to reflect only the selected subset of data.

<ins>**Value:**</ins>
This interactivity enhances user engagement and supports location-specific insights — enabling policymakers or researchers to focus on areas of concern.

<ins>**Insight:**</ins>
EX. By selecting "Bangkok", users can immediately explore inner-city air quality and identify high-risk monitoring points.

📍***Visualization 1: PM2.5 Scorecard Summary***
<img width="957" alt="Screenshot 2568-05-25 at 15 08 48" src="https://github.com/user-attachments/assets/03f5f58e-154c-4c93-86b7-780d64a915d7" />
<ins>Description:</ins>
The top of the dashboard features a KPI scorecard that summarizes real-time data status:

   - Total Records collected

   - Maximum PM2.5 value with location

   - Minimum PM2.5 value with location

These metrics are updated dynamically with each new data ingestion and help users grasp the current air quality situation at a glance.

<ins>Insight:</ins>

   - The dataset currently includes 17,484 records, indicating strong temporal coverage.

   - The highest PM2.5 value is 123.0 μg/m³ recorded at National Housing Authority Bangplee, Samut Prakan, which may reflect local emission sources.

   - The lowest PM2.5 value is -1.0 μg/m³ (likely a sensor error) recorded at  Sisaket Meteorological Center, Sisaket, which should be flagged for data cleaning or anomaly detection.

📍 ***Visualization 2: Top 10 Provinces by Max PM2.5***

<img width="478" alt="Screenshot 2568-05-25 at 15 10 25" src="https://github.com/user-attachments/assets/59aae5e4-55a6-4e04-a428-a13f19d3b276" />

<ins>Description:</ins>
   - A horizontal bar chart ranks provinces based on their highest recorded PM2.5 levels. Each bar represents a province with color intensity corresponding to pollution severity.

<ins>Insight:</ins>
   - Yasothon, Kanchanaburi, and Rayong are among the top provinces with the highest PM2.5 values, indicating potential pollution hotspots.


📍 ***Visualization 3: PM2.5 Distribution (Boxplot)***

<img width="509" alt="Screenshot 2568-05-25 at 15 10 55" src="https://github.com/user-attachments/assets/25ed42d8-e778-462a-baa4-a4eecc8bc912" />

<ins>Description:</ins>
   - A boxplot displays the distribution of PM2.5 levels for the top 5 provinces. It shows quartiles, outliers, and spread across measurements.

<ins>Insight:</ins>
   - The distribution reveals that while all top provinces experience pollution spikes, some like Saraburi and Nan have more frequent extreme PM2.5 levels.


📍 ***Visualization 4: Raw Data Table***

<img width="943" alt="Screenshot 2568-05-25 at 15 11 37" src="https://github.com/user-attachments/assets/5c2047ca-6434-46e2-931d-dfc65c62c51d" />

<ins>Description:</ins>
   - An interactive table displays recent PM2.5 data pulled from lakeFS via S3. Columns include timestamp, station info, and PM2.5 readings. A download button allows data export.

<ins>Insight:</ins>
   - Useful for quick inspection and verification of live records, enabling transparency and traceability.


# Machine Learning Application 
- **Problem Statement**
This project applies unsupervised machine learning to analyze air pollution patterns across Thailand using PM2.5 sensor data. The objective is to group air quality monitoring stations into clusters based on pollution levels, without prior labels, to reveal natural groupings of environmental risk.

- **Model and Approach**
  
   - Model Used: **K-Means Clustering (unsupervised learning)(Visualization 5)**

   - Features: Average PM2.5 values by station

   - Preprocessing Steps:

        - Aggregated PM2.5 values by station

        - Normalized features

        - Specified number of clusters: k = 3 to reflect low, moderate, and high PM2.5 levels

   - Clustering Output:

        - Each station was assigned a cluster label (0, 1, or 2)

- **Results and Evaluation**
   - Cluster Interpretation:

        🔵 Cluster 0 – Low PM2.5: Stations with clean air
        
        🟢 Cluster 1 – Moderate PM2.5: Stations with noticeable but not severe pollution
        
        🔴 Cluster 2 – High PM2.5: Stations with serious pollution concerns

   - Visualization: Displayed as colored bubbles on a geographic map using Streamlit

<img width="968" alt="Screenshot 2568-05-25 at 15 12 46" src="https://github.com/user-attachments/assets/4b1d9184-c5e3-4a1e-94c6-425603620987" />

   - Insight: Urban areas and industrial provinces are more frequently represented in the "High PM2.5" cluster.

- **Key Learnings**
  
   - K-Means effectively separated air quality stations into interpretable categories.

   - The results aligned with real-world expectations — high-PM2.5 clusters were often located in industrial or densely populated areas.

   - This unsupervised method provided a scalable way to monitor pollution without labeled training data.


# Conclusion
This project successfully delivered a **real-time air quality data pipeline** with automated data ingestion, processing, storage, and visualization — covering the full data engineering lifecycle. By leveraging tools like **Prefect, lakeFS, Jupyter, and Streamlit**, the system enables continuous monitoring and insightful analysis of PM2.5 levels across Thailand.

- **Key Achievements:**

   - Built a scheduled workflow using Prefect to ingest live PM2.5 data daily.

   - Implemented data version control with lakeFS, ensuring reproducibility and traceability.

   - Designed an interactive Streamlit dashboard with filtering, charts, and clustering views.

   - Applied K-Means clustering to group stations by pollution severity, uncovering spatial patterns in air quality.

- **Future Improvements:**

   - **Data enrichment:** Integrate weather data (e.g., humidity, temperature) for deeper analysis.

   - **Model expansion:** Add supervised models to predict future PM2.5 values.

   - **Alert system:** Implement automated alerts for dangerously high PM2.5 levels.

   - **Scalability:** Deploy on cloud infrastructure to handle more stations and longer timeframes.

