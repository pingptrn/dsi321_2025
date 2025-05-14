import os
import pandas as pd
import streamlit as st
import plotly.express as px
import s3fs

# --- Page Config ---
st.set_page_config(page_title="PM2.5 Dashboard", layout="wide")

# --- Load Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
menu = st.sidebar.radio("Navigation", ["Dashboard", "Map View", "Raw Data"], index=0)
st.sidebar.markdown("---")
st.sidebar.markdown("**User:** You\nVersion: 1.0")
st.sidebar.button("Logout")

# --- S3 Access Setup ---
fs = s3fs.S3FileSystem(
    key=os.getenv("LAKEFS_ACCESS_KEY"),
    secret=os.getenv("LAKEFS_SECRET_KEY"),
    client_kwargs={"endpoint_url": os.getenv("LAKEFS_ENDPOINT").replace("http", "https")},
    use_ssl=False
)

@st.cache_data(ttl=2400)
def load_data():
    path = "s3://dsi321-air-quality/main/airquality.parquet/year=2025"
    files = fs.glob(f"{path}/*/*/*/*")
    df = pd.concat([pd.read_parquet(f"s3://{f}", filesystem=fs) for f in files], ignore_index=True)
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['long'] = pd.to_numeric(df['long'], errors='coerce')
    df['PM25.value'] = pd.to_numeric(df['PM25.value'], errors='coerce')
    df['province'] = df['areaEN'].str.extract(r",\s*([^,]+)$")[0].str.strip()
    return df.dropna(subset=['lat', 'long', 'PM25.value'])

df = load_data()

# --- Title Header ---
st.title("🌫️ PM2.5 Air Quality Dashboard")

# --- Filters (used globally) ---
col1, col2 = st.columns(2)

with col1:
    selected_province = st.selectbox("📍 Province", ["All"] + sorted(df['province'].dropna().unique().tolist()), key="province")

with col2:
    if selected_province == "All":
        station_options = sorted(df["nameEN"].dropna().unique().tolist())
    else:
        station_options = sorted(df[df["province"] == selected_province]["nameEN"].dropna().unique().tolist())

    selected_station = st.selectbox("🏛️ Station", ["All"] + station_options, key="station")

# --- Apply Filter ---
df_filtered = df.copy()
if selected_province != "All":
    df_filtered = df_filtered[df_filtered["province"] == selected_province]
if selected_station != "All":
    df_filtered = df_filtered[df_filtered["nameEN"] == selected_station]

# --- Dashboard ---
if menu == "Dashboard":
    k1, k3, k4 = st.columns(3)

    with k1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Total Records</div>
                <div class="metric-value">{len(df_filtered)}</div>
            </div>
        """, unsafe_allow_html=True)

    df_valid = df_filtered.dropna(subset=["PM25.value", "province", "nameEN"])

    if not df_valid.empty:
        max_row = df_valid.loc[df_valid["PM25.value"].idxmax()]
        min_row = df_valid.loc[df_valid["PM25.value"].idxmin()]

        with k3:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Max PM2.5</div>
                    <div class="metric-value">{max_row['PM25.value']:.1f}</div>
                    <div class="metric-delta">📍 {max_row['nameEN']}, {max_row['province']}</div>
                </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Min PM2.5</div>
                    <div class="metric-value">{min_row['PM25.value']:.1f}</div>
                    <div class="metric-delta">📍 {min_row['nameEN']}, {min_row['province']}</div>
                </div>
            """, unsafe_allow_html=True)

    # --- Charts ---
    st.markdown("---")
    st.subheader("📊 PM2.5 Insights")

    c1, c2 = st.columns(2)

    with c1:
        if selected_province == "All":
            top10 = df_filtered.groupby("province", as_index=False)["PM25.value"].max()
            y_col = "province"
            chart_title = "Top 10 Provinces by Max PM2.5"
        else:
            top10 = df_filtered.groupby("nameEN", as_index=False)["PM25.value"].max()
            y_col = "nameEN"
            chart_title = f"Top 10 Stations in {selected_province} by Max PM2.5"

        top10 = top10.sort_values("PM25.value", ascending=False).head(10)
        fig1 = px.bar(
            top10,
            x="PM25.value",
            y=y_col,
            orientation="h",
            title=chart_title,
            labels={"PM25.value": "PM2.5", y_col: "Location"},
            color="PM25.value",
            color_continuous_scale="reds"
        )
        fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        df_compare = df_filtered.dropna(subset=["PM25.value", "province", "nameEN"])
        if not df_compare.empty:
            fig2 = px.scatter(
                df_compare,
                x="nameEN",
                y="PM25.value",
                color="province",
                title="PM2.5 by Station and Province",
                labels={"nameEN": "Station", "PM25.value": "PM2.5"},
                opacity=0.6
            )
            fig2.update_layout(xaxis_tickangle=-45, height=450)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No valid station-wise PM2.5 data to plot.")




# --- Map View ---
elif menu == "Map View":
    st.title("🗺️ Map View")
    df_map = df_filtered[df_filtered["PM25.value"] > 0]
    fig = px.scatter_mapbox(df_map, lat="lat", lon="long", size="PM25.value", color="PM25.value",
                            hover_name="nameEN", zoom=5, mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)

# --- Raw Data ---
elif menu == "Raw Data":
    st.title("📄 Raw Data Table")
    st.dataframe(df_filtered)
    st.download_button("Download CSV", data=df_filtered.to_csv(index=False), file_name="pm25_filtered.csv")
  



