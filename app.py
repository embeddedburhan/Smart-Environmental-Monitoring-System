
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import random
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Environmental Control Center",
    page_icon="🌍",
    layout="wide"
)

DB_PATH = os.path.join("data", "environment.db")
os.makedirs("data", exist_ok=True)

# ---------------- DATABASE ----------------
def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature REAL,
                humidity REAL,
                air_quality REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                alert_message TEXT,
                severity TEXT
            )
        """)
def save_reading(temp, humidity, air):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO readings
            (timestamp, temperature, humidity, air_quality)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), temp, humidity, air))
def save_alert(message, severity):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO alert_history
            (timestamp, alert_message, severity)
            VALUES (?, ?, ?)
        """, (
            datetime.now().isoformat(),
            message,
            severity
        ))
def get_history():
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM readings ORDER BY id DESC LIMIT 200",
            conn
        )

initialize_database()

# ---------------- FUTURISTIC DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#07111f,#101d32,#091321);
    color: #e5f3ff;
}
[data-testid="stSidebar"] {
    background: #0b1728;
    border-right: 1px solid #1d3b58;
}
h1,h2,h3 {
    color: #e5f3ff !important;
}
.metric-box {
    background: linear-gradient(145deg,#102c46,#142238);
    border: 1px solid #1d6480;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 0 15px rgba(0,210,255,.08);
}
.small-label {
    color: #91b6cc;
    font-size: 13px;
}
.big-value {
    color: #45d9ff;
    font-size: 32px;
    font-weight: 700;
}
div[data-testid="stMetric"] {
    background: #10243a;
    border: 1px solid #1b4c69;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 ECO CONTROL")
st.sidebar.caption("ENVIRONMENTAL INTELLIGENCE")

page = st.sidebar.radio(
    "SYSTEM NAVIGATION",
    ["Dashboard", "Analytics", "History", "About"]
)

st.sidebar.divider()
st.sidebar.success("SYSTEM ONLINE")
st.sidebar.caption("Sensor Mode: SIMULATED")
st.sidebar.divider()
st.sidebar.subheader("⚙️ Alert Settings")

temp_limit = st.sidebar.slider(
    "Temperature limit (°C)", 20, 40, 30
)

humidity_limit = st.sidebar.slider(
    "Humidity limit (%)", 40, 90, 70
)

air_limit = st.sidebar.slider(
    "Air quality limit", 50, 200, 100
)


st.sidebar.caption("Developed by Burhan Shafi Kar")

# ---------------- SENSOR SIMULATOR ----------------
# Demo readings only; no physical sensors connected.
if "sensor_values" not in st.session_state:
    st.session_state.sensor_values = {
        "temperature": 25.0,
        "humidity": 60.0,
        "air_quality": 45.0
    }

if page == "Dashboard":
    st_autorefresh(interval=5000, key="dashboard_refresh")

    values = st.session_state.sensor_values
    temperature = round(max(15, min(40, values["temperature"] + random.uniform(-0.5, 0.5))), 1)
    humidity = round(max(20, min(90, values["humidity"] + random.uniform(-1, 1))), 1)
    air_quality = round(max(0, min(200, values["air_quality"] + random.uniform(-3, 3))), 1)

    st.session_state.sensor_values = {
        "temperature": temperature,
        "humidity": humidity,
        "air_quality": air_quality
    }

    save_reading(temperature, humidity, air_quality)

    st.title("🌍 ENVIRONMENTAL CONTROL CENTER")
    st.caption("LIVE ENVIRONMENTAL INTELLIGENCE | AUTO-REFRESH: 5 SECONDS")
    st.divider()

    st.subheader("LIVE SENSOR MONITORING")

    def make_gauge(title, value, maximum, unit, color):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": unit, "font": {"color": "white", "size": 27}},
            title={"text": title, "font": {"color": "#b9dff5", "size": 16}},
            gauge={
                "axis": {"range": [0, maximum], "tickcolor": "#9bb5c9"},
                "bar": {"color": color},
                "bgcolor": "#10243a",
                "borderwidth": 1,
                "bordercolor": "#28516d",
                "steps": [
                    {"range": [0, maximum * 0.5], "color": "#18334b"},
                    {"range": [maximum * 0.5, maximum], "color": "#10243a"}
                ]
            }
        ))
        fig.update_layout(
            height=260,
            margin=dict(l=20, r=20, t=55, b=15),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )
        return fig

    c1, c2, c3 = st.columns(3)

    with c1:
        st.plotly_chart(
            make_gauge("TEMPERATURE", temperature, 50, " °C", "#00d9ff"),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            make_gauge("HUMIDITY", humidity, 100, " %", "#35e0a1"),
            use_container_width=True
        )

    with c3:
        st.plotly_chart(
            make_gauge("AIR QUALITY (DEMO)", air_quality, 200, " AQI", "#a78bfa"),
            use_container_width=True
        )
    # NEW LIVE TREND CHART CODE HERE

    st.divider()
    st.subheader("⚠️ SMART ENVIRONMENTAL ALERTS")
    
    alerts = []
    if temperature > 30:
        alerts.append("High temperature detected.")
    if humidity > 70:
        alerts.append("High humidity detected.")
    if air_quality > 100:
        alerts.append("Poor air-quality demo reading detected.")

    if alerts:
        for alert in alerts:
            st.error("⚠️ " + alert)
    else:
        st.success("All readings are within the configured demo thresholds.")

    st.caption("Last updated: " + datetime.now().strftime("%d %b %Y, %I:%M:%S %p"))
    st.caption("All readings are simulated. No physical sensor is connected.")

elif page == "Analytics":
    st.title("📊 ENVIRONMENTAL ANALYTICS")
    st.caption("Interactive sensor trends")

    history = get_history()

    if not history.empty:
        history = history.sort_values("timestamp")
        st.line_chart(
            history.set_index("timestamp")[
                ["temperature", "humidity", "air_quality"]
            ]
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Temperature", f"{history.temperature.mean():.1f} °C")
        col2.metric("Average Humidity", f"{history.humidity.mean():.1f} %")
        col3.metric("Average Air Quality", f"{history.air_quality.mean():.1f}")
    else:
        st.info("No historical readings available yet.")

elif page == "History":
    st.title("🗂️ ENVIRONMENTAL DATA HISTORY")
    history = get_history()

    if not history.empty:
        st.dataframe(history, use_container_width=True)

        csv = history.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Historical Data (CSV)",
            csv,
            "environmental_history.csv",
            "text/csv"
        )
    else:
        st.info("No readings recorded yet.")

elif page == "About":
    st.title("ABOUT THE PROJECT")

    st.markdown("""
    ### Smart Environmental Monitoring System

    A Python-based environmental monitoring dashboard demonstrating
    temperature, humidity and air-quality data visualization.

    **Technology stack**
    - Python
    - Streamlit
    - Plotly
    - SQLite
    - Pandas

    **Current implementation:** Simulated environmental readings.

    **Future scope:** ESP32, DHT22 and MQ135 physical sensor integration.

    **Developer:** Burhan Shafi Kar
    """)

st.divider()
st.caption("ECO CONTROL CENTER | SMART ENVIRONMENTAL MONITORING SYSTEM")
