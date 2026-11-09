import streamlit as st

st.set_page_config(
    page_title="Smart Environmental Monitor",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Smart Environmental Monitoring System")

st.write("Monitor environmental conditions through an intelligent dashboard.")

st.sidebar.title("Navigation")
st.sidebar.info("Environmental Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature", "25 °C")

with col2:
    st.metric("Humidity", "60 %")

with col3:
    st.metric("Air Quality", "Good")

st.success("Environmental monitoring dashboard initialized!")