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


# Project Structure
        dsi321_2025/
        │
        ├── lakefs
        │   ├── airquality-lakefs-ref.txt         # lakeFS reference name for versioned PM2.5 dataset
        │   ├── sample_data.ipynb                 # Sample of stored data in lakeFS
        │
        ├── make/
        │   ├── Dockerfile.jupyter                # Dockerfile to launch a JupyterLab container
        │   ├── Dockerfile.prefect-worker         # Dockerfile for running Prefect agent
        │   ├── Dockerfile.streamlit              # Dockerfile for launching the Streamlit dashboard
        │   ├── requirements.txt                      # Python dependencies for all components
        │   ├── wait-for-server.sh                    # Startup script ensuring services start in the right order
        │    
        ├── visualization/
        │   ├── app.py                            # Main Streamlit app with dynamic filters and charts
        │   ├── style.css                         # Custom styling for the dashboard
        │
        ├── work/
        │   ├── Untitled.ipynb                    # Scratchpad or data exploration notebook
        │   ├── deploy.py                         # lakeFS dataset deployment script
        │   ├── pipeline.py                       # Prefect flow that downloads + stages PM2.5 data       
        │   ├── schema.md                         
        │
        ├── docker-compose.yml                    # Defines services (lakeFS, Streamlit, Prefect, etc.)
        ├── .gitignore                            # Prevents local files from being committed
        ├── LICENSE
        └── README.md                             # You're here!

        
# Evidence for the Previous 90 Marks
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
    
  🔗 [Sample dataset ](https://github.com/pingptrn/dsi321_2025/blob/main/lakefs/sample_data.ipynb)
<img width="1283" alt="Screenshot 2568-05-18 at 19 28 23" src="https://github.com/user-attachments/assets/33fdca48-4f38-42b3-b4a9-b125f20675b0" />
  
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
<img width="985" alt="Screenshot 2568-05-18 at 20 10 56" src="https://github.com/user-attachments/assets/427885b8-a184-4949-ac4b-9d0d2fae7137" />  
<ins>Description:</ins>
The top of the dashboard features a KPI scorecard that summarizes real-time data status:

   - Total Records collected

   - Maximum PM2.5 value with location

   - Minimum PM2.5 value with location

These metrics are updated dynamically with each new data ingestion and help users grasp the current air quality situation at a glance.

<ins>Insight:</ins>

   - The dataset currently includes 19,787 records, indicating strong temporal coverage.

   - The highest PM2.5 value is 46.8 μg/m³ recorded at Phaya Thaen Public Park, Yasothon, which may reflect local emission sources.

   - The lowest PM2.5 value is -1.0 μg/m³ (likely a sensor error) recorded at Samut Sakhon Wittayalai School, which should be flagged for data cleaning or anomaly detection.

📍 ***Visualization 2: Top 10 Provinces by Max PM2.5***

<img width="469" alt="Screenshot 2568-05-18 at 20 12 47" src="https://github.com/user-attachments/assets/5b8a0e69-888b-4b4f-8aae-4d6abf472c11" />

<ins>Description:</ins>
   - A horizontal bar chart ranks provinces based on their highest recorded PM2.5 levels. Each bar represents a province with color intensity corresponding to pollution severity.

<ins>Insight:</ins>
   - Yasothon, Kanchanaburi, and Rayong are among the top provinces with the highest PM2.5 values, indicating potential pollution hotspots.


📍 ***Visualization 3: PM2.5 Distribution (Boxplot)***

<img width="513" alt="Screenshot 2568-05-18 at 20 13 18" src="https://github.com/user-attachments/assets/8b811530-060d-48e6-8af5-1a5dc4af142a" />

<ins>Description:</ins>
   - A boxplot displays the distribution of PM2.5 levels for the top 5 provinces. It shows quartiles, outliers, and spread across measurements.

<ins>Insight:</ins>
   - The distribution reveals that while all top provinces experience pollution spikes, some like Saraburi and Nan have more frequent extreme PM2.5 levels.


📍 ***Visualization 4: Raw Data Table***

<img width="934" alt="Screenshot 2568-05-18 at 20 14 36" src="https://github.com/user-attachments/assets/ed20b3c4-5972-4b3e-b358-2c9ab8403874" />

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

<img width="969" alt="Screenshot 2568-05-18 at 20 13 55" src="https://github.com/user-attachments/assets/d5103b56-dd7b-4cd8-b578-a7eac4f76562" />

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


-------------------------------------------------------------------------------------------------------------------------------------------------------
        
# How It Works
1. pipeline.py fetches and cleans data, then stores it in lakeFS under a structured path:
  
         s3://dsi321-air-quality/main/airquality.parquet/year=2025/month=.../day=.../

3. Data Versioning (lakeFS)


        - All PM2.5 data is versioned using lakeFS.
        - Reference (ref) info is stored in lakefs-refs/airquality-lakefs-ref.txt.

4. Data Visualization (Streamlit)
   
        - visualization/app.py builds the user interface.
        - Supports:

                - Province/Station filtering

                - Metrics (Max/Min PM2.5, Total Records)

                - Bar Chart of Top Provinces or Stations

                - Boxplot of PM2.5 by Province

                - Map View (Mapbox)

                - Raw Data Explorer + CSV download

5. Containerized Services
- All services (dashboard, pipeline, workers) run in Docker using:
   
         docker-compose up --build

# 🖥️ Streamlit UI Features
**Filters**

-Province (All, Bangkok, Chiang Mai, etc.)
-Station (dependent on Province selection)

**Metrics**

-Total record count
-Max & Min PM2.5 value with location

**Charts**

- Bar Chart: Top 10 Provinces or Stations by PM2.5
- Box Plot: Top 5 Provinces PM2.5 distribution
- Map: PM2.5 intensity overlaid on Mapbox
- Raw Data table and CSV export

# ⚙️ Setup Instructions
1. **Clone the repository**

       git clone https://github.com/pingptrn/dsi321_2025.git
       cd dsi321_2025

2. **Set environment variables**
Set the following in your shell or .env:

       export LAKEFS_ACCESS_KEY=...
       export LAKEFS_SECRET_KEY=...
       export LAKEFS_ENDPOINT=http://lakefs:8000

3. **Launch everything**

       docker-compose up --build

4. **Access dashboards**

- Streamlit: http://localhost:8501
- Prefect: http://localhost:4200
- lakeFS UI: http://localhost:8000
- Jupyter: http://localhost:8888




