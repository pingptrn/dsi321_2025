# Real-Time PM 2.5 Air Quality Data Pipeline with Interactive Visualization
Author: Pattaranit Jaronnaovapat

Course: DSI321 – Big Data Infrastructure

Institution: Data Science and Innovation, Thammasat University

# 🧠 Project Description
This project implements a Real-Time Air Quality Data Pipeline with Interactive Visualization, focused on monitoring PM2.5 levels across Thailand. The system leverages modern open-source data infrastructure tools to create a full-stack pipeline — from data ingestion and versioned storage to automated workflows and web-based analytics.

It integrates the following key components using Docker Compose for seamless orchestration:

⚙️ Docker Compose Orchestration
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

- Connects to lakeFS to read current PM2.5 data using S3 paths.

- Includes features such as:

        - Province and station-level filtering

        - PM2.5 distribution insights by time/location

        - Interactive charts (bar, boxplot, map)

        - Data export in CSV format


