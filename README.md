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

# How It Works
1. pipeline.py fetches and cleans data, then stores it in lakeFS under a structured path:
  
         s3://dsi321-air-quality/main/airquality.parquet/year=2025/month=.../day=.../

2. Data Versioning (lakeFS)


        - All PM2.5 data is versioned using lakeFS.
        - Reference (ref) info is stored in lakefs-refs/airquality-lakefs-ref.txt.

3. Data Visualization (Streamlit)
   
        - visualization/app.py builds the user interface.
        - Supports:

                - Province/Station filtering

                - Metrics (Max/Min PM2.5, Total Records)

                - Bar Chart of Top Provinces or Stations

                - Boxplot of PM2.5 by Province

                - Map View (Mapbox)

                - Raw Data Explorer + CSV download

4. Containerized Services
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

# 🧠 Learning Outcomes

- Applied data versioning for reproducibility
- Orchestrated workflows using Prefect
- Designed modular dashboards with Plotly + Streamlit
- Managed cloud datasets in Parquet with structured paths
- Deployed end-to-end pipelines with Docker Compose



