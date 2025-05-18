import requests
import pandas as pd
from prefect import flow, task, get_run_logger
import os



@task
def get_aqi_data() -> list[dict]:
    """
    Make an API request to the endpoint using URL.

    Parameters:
    None

    Returns:
    data: extracted data for further processing.
    """

    #API endpoint
    AQI_ENDPOINT = 'http://air4thai.pcd.go.th/services/getNewAQI_JSON.php'

    try:
        #Make API request
        response = requests.get(url=AQI_ENDPOINT)
        response.raise_for_status()

        #Transform data into dataframe
        response_json = response.json()
        data = response_json['stations']

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

@task
def data_processing(data: list[dict]) -> pd.DataFrame:
    """
    Process data, convert data types, minor cleaning, and keep necessary columns.

    Parameters:
    data: extracted data.

    Returns:
    df: DataFrame containing processed and schema-aligned data.
    """
    logger = get_run_logger()

    # 1. Remove records missing 'AQILast'
    data = [d for d in data if 'AQILast' in d and d['AQILast']]

    # 2. Convert list of dict to DataFrame
    df = pd.DataFrame(data)

    # 3. Normalize AQILast (nested dictionary) into flat columns
    expanded_aqi = pd.json_normalize(df['AQILast'])
    df = pd.concat([df, expanded_aqi], axis=1)

    # 4. Convert timestamp fields
    df['time'] = df[df['date'] == df['date'].max()]['time'].max()
    df['date'] = df['date'].max()
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])  # Convert to datetime
    
    # Extract year, month, day, hour while it's still datetime
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    
    # ✅ Overwrite timestamp with its string version
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    


    # 6. Convert numeric fields
    numeric_cols = ['PM25.color_id', 'PM25.aqi']
    df[numeric_cols] = df[numeric_cols].astype(float)

    # 7. Select and reorder columns
    datetime_cols = ['timestamp', 'year', 'month', 'day', 'hour']
    location_cols = ['stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN', 'stationType', 'lat', 'long']
    df = df[datetime_cols + location_cols + numeric_cols]

    logger.info(f"✅ Data processed, resulting shape: {df.shape}")
    logger.debug(f"Columns: {df.columns.tolist()}")

    return df

@task
def load_to_lakefs(df: pd.DataFrame, lakefs_s3_path: str, storage_options: dict):
    """
    Load data into lakeFS storage in S3 (Amazon Simple Storage Service) and in a parquent format.
    Patitions the parquet file based on 'year', 'month', 'day' and 'hour'.

    Parameters:
    df: Target DataFrame that will be loaded into the storage.
    lakefs_s3_path: S3-Supported API Gateway, layer in lakeFS reponsible for the compatibility with S3.
    storage_options: configured options for accessing lakeFS storage.

    Returns:
    None
    """
    df.to_parquet(
        lakefs_s3_path,
        storage_options=storage_options,
        partition_cols=['year', 'month', 'day', 'hour'],
    )

@flow(name='main-flow', log_prints=True)
def main_flow():

    # Task 1: Get data
    data = get_aqi_data()

    # Task 2: Process data
    df = data_processing(data)

    # ✅ Schema validation (optional but recommended)
    import json
    schema_path = os.path.join(os.path.dirname(__file__), "schema.md")
    with open(schema_path) as f:
        schema = json.load(f)

    expected_columns = schema["columns"]
    df = df[expected_columns]
    assert list(df.columns) == expected_columns, "Schema mismatch: Columns do not match the defined schema"

    # lakeFS credentials
    ACCESS_KEY = "access_key"
    SECRET_KEY = "secret_key"

    # lakeFS endpoint (running locally)
    lakefs_endpoint = "http://lakefs-dev:8000/"

    # lakeFS repo, branch, and file path
    repo = "air-quality"
    branch = "main"
    path = "airquality.parquet"
    lakefs_s3_path = f"s3a://dsi321-{repo}/{branch}/{path}"

    # Storage options for lakeFS (S3-compatible)
    storage_options = {
        "key": ACCESS_KEY,
        "secret": SECRET_KEY,
        "client_kwargs": {
            "endpoint_url": lakefs_endpoint
        }
    }

    # Task 3: Load data into lakeFS in Parquet format
    load_to_lakefs(df=df, lakefs_s3_path=lakefs_s3_path, storage_options=storage_options)


if __name__ == "__main__":
    main_flow()
