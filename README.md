# Real-Time PM 2.5 Air Quality Data Pipeline with Interactive Visualization
Author: Pattaranit Jaronnaovapat

Course: DSI321 – Big Data Infrastructure

Institution: Data Science and Innovation, Thammasat University

# 🌐 Project Description
This project implements a Real-Time Air Quality Data Pipeline with Interactive Visualization, focused on monitoring PM2.5 levels across Thailand. The system leverages modern open-source data infrastructure tools to create a full-stack pipeline — from data ingestion and versioned storage to automated workflows and web-based analytics.

It integrates the following key components using Docker Compose for seamless orchestration:

Docker Compose Orchestration
Using docker-compose up, the system spins up multiple interconnected services as containers:

1. lakeFS (Data Version Control)

- Acts as a Git-like interface for object storage, managing version-controlled data in airquality.parquet format.

- Data is organized and stored under structured partitions (e.g., /year=2025/month=05/day=14/) to enable easy time-based querying.

- Enables reproducibility, branching, and rollback of datasets, ensuring data integrity.

2. Prefect (Data Orchestration)

- Automates the daily ingestion, cleaning, and transformation of PM2.5 data.

- Workflows are deployed and monitored using Prefect UI, enabling visibility into execution status, success/failure logs, and historical runs.

- Ensures reliable and scheduled delivery of data to lakeFS.

3. Jupyter Notebook (Data Exploration & Development)

- Used for interactive development, debugging, and EDA (exploratory data analysis) of air quality data.

- Access version-controlled data directly from lakeFS (via S3 protocol using s3fs), allowing for live experimentation with up-to-date datasets.

4. Streamlit (Interactive Dashboard)

- Provides a real-time, filterable web dashboard visualizing key air quality metrics.

- Connects to lakeFS to read the current PM2.5 data using S3 paths.

# Project Structure
        dsi321_2025/
        │
        ├── lakefs-refs/
        │   └── airquality-lakefs-ref.txt         # lakeFS reference name for versioned PM2.5 dataset
        │
        ├── make/
        │   ├── Dockerfile.jupyter                # Dockerfile to launch a JupyterLab container
        │   ├── Dockerfile.prefect-worker        # Dockerfile for running Prefect agent
        │   ├── Dockerfile.streamlit             # Dockerfile for launching the Streamlit dashboard
        │
        ├── visualization/
        │   ├── app.py                            # Main Streamlit app with dynamic filters and charts
        │   ├── style.css                         # Custom styling for the dashboard
        │
        ├── work/
        │   └── Untitled.ipynb                    # Scratchpad or data exploration notebook
        │
        ├── deploy.py                             # lakeFS dataset deployment script
        ├── pipeline.py                           # Prefect flow that downloads + stages PM2.5 data
        │
        ├── requirements.txt                      # Python dependencies for all components
        ├── wait-for-server.sh                    # Startup script ensuring services start in the right order
        ├── docker-compose.yml                    # Defines services (lakeFS, Streamlit, Prefect, etc.)
        ├── .gitignore                            # Prevents local files from being committed
        ├── LICENSE
        └── README.md                             # You're here!

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



