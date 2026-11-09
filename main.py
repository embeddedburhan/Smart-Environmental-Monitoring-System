
import streamlit as st
import pandas as pd
import random
from sensors.simulator import EnvironmentalSensorSimulator
from data.database import initialize_database, save_reading, get_readings
import time

from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Environmental Monitor",
    page_icon="🌍",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071c20, #102f32, #10252c);
    color: #ecf5f0;
}
[data-testid="stSidebar"] {
    background: #0b2528;
}
h1, h2, h3, p, label {
    color: #e8f5ed !important;
}
.metric-card {
    background: linear-gradient(145deg, #163c3c, #102c32);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #28645a;
    box-shadow: 0 5px 18px #00000035;
}
.metric-label {
    color: #a9c9bc;
    font-size: 14px;
}
.metric-value {
    color: #68e0ae;
    font-size: 30px;
    font-weight: bold;
    margin-top: 8px;
}
.status-good {
    color: #55e6a5;
    font-weight: bold;
}
.status-moderate {
    color: #ffc857;
    font-weight: bold;
}
.status-poor {
    color: #ff7373;
    font-weight: bold;
}
div.stButton > button {
    background: #16876b;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}
div.stButton > button:hover {
    background: #20a783;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🌍 SMART ENVIRONMENTAL MONITOR")
st.caption("INTELLIGENT IoT ENVIRONMENTAL ANALYTICS PLATFORM")

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌿 CONTROL PANEL")
st.sidebar.write("Environmental Monitoring")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Sensor Analytics", "Data History", "About Project"]
)

st.sidebar.markdown("---")
st.sidebar.info("System Status: Online")
st.sidebar.caption("Version 2.0 | Python + Streamlit")

# ---------------- SENSOR DATA ----------------
if "history" not in st.session_state:
    st.session_state.history = [{
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Temperature": 25.0,
        "Humidity": 60.0,
        "Air Quality": 45.0
    }]

if st.sidebar.button("🔄 Refresh Sensor Readings"):
    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Temperature": round(random.uniform(20, 40), 1),
        "Humidity": round(random.uniform(35, 85), 1),
        "Air Quality": round(random.uniform(20, 180), 1)
    })

    st.session_state.history = st.session_state.history[-100:]

latest = st.session_state.history[-1]
df = pd.DataFrame(st.session_state.history)

air = latest["Air Quality"]

if air <= 50:
    air_status = "GOOD"
    air_class = "status-good"
elif air <= 100:
    air_status = "MODERATE"
    air_class = "status-moderate"
else:
    air_status = "POOR"
    air_class = "status-poor"

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.subheader("📊 Environmental Overview")
    st.caption("Your environment at a glance")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">🌡️ TEMPERATURE</div>
        <div class="metric-value">{latest['Temperature']} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">💧 HUMIDITY</div>
        <div class="metric-value">{latest['Humidity']} %</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">🌫️ AIR QUALITY</div>
        <div class="metric-value">{air_status}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📈 Environmental Trends")

    tab1, tab2, tab3 = st.tabs([
        "Temperature",
        "Humidity",
        "Air Quality"
    ])

    with tab1:
        st.line_chart(df.set_index("Time")[["Temperature"]])

    with tab2:
        st.line_chart(df.set_index("Time")[["Humidity"]])

    with tab3:
        st.line_chart(df.set_index("Time")[["Air Quality"]])

    st.markdown("---")

    st.subheader("🚦 Air Quality Assessment")

    st.markdown(
        f"Current Air Quality: <span class='{air_class}'>{air_status}</span>",
        unsafe_allow_html=True
    )

    st.progress(min(int(air / 200 * 100), 100))

    st.caption("Air quality indicator: simulated index, not an official AQI measurement.")

    st.success("Monitoring dashboard is operational.")

# ---------------- SENSOR ANALYTICS ----------------
elif page == "Sensor Analytics":

    st.subheader("🔬 Sensor Analytics")

    st.write("Temperature Sensor")
    st.metric("Temperature", f"{latest['Temperature']} °C")
    st.line_chart(df.set_index("Time")[["Temperature"]])

    st.divider()

    st.write("Humidity Sensor")
    st.metric("Humidity", f"{latest['Humidity']} %")
    st.line_chart(df.set_index("Time")[["Humidity"]])

    st.divider()

    st.write("Air Quality Sensor")
    st.metric("Air Quality Index", f"{air:.1f}")
    st.line_chart(df.set_index("Time")[["Air Quality"]])

# ---------------- DATA HISTORY ----------------
elif page == "Data History":

    st.subheader("📁 Environmental Data Records")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇️ Download Environmental Report",
        data=csv,
        file_name="environmental_report.csv",
        mime="text/csv"
    )

    if st.button("Clear Sensor History"):
        st.session_state.history = [{
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Temperature": 25.0,
            "Humidity": 60.0,
            "Air Quality": 45.0
        }]
        st.rerun()

# ---------------- ABOUT ----------------
elif page == "About Project":

    st.subheader("🌍 About the Project")

    st.write("""
    The Smart Environmental Monitoring System is an
    intelligent monitoring platform designed to observe
    environmental conditions.

    **Main Parameters**
    - Temperature monitoring
    - Relative humidity monitoring
    - Air quality monitoring

    **Technology Stack**
    - Python
    - Streamlit
    - Pandas
    - IoT sensor integration (planned)

    **Future Hardware Integration**
    - ESP32 Microcontroller
    - DHT22 Temperature and Humidity Sensor
    - MQ135 Air Quality Sensor
    """)

    st.info("This dashboard currently uses simulated sensor readings.")

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:20px;">
    <h4>🌍 Smart Environmental Monitoring System</h4>
    <p>Designed & Developed by
    <b style="color:#20c997;">Burhan Shafi Kar</b></p>
    <p>Electronics & Instrumentation Engineer</p>
    <small>Python | Streamlit | IoT | Environmental Analytics</small>
</div>
""", unsafe_allow_html=True)