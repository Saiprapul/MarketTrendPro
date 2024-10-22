import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

# Initialize Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# App Title
st.set_page_config(page_title="MarketTrendPro - Trending Product Insights", layout="wide")
st.title("MarketTrendPro - Trending Product Insights")

# Sidebar Inputs for customization
with st.sidebar:
    st.header("Customize Your Analysis")
    # User Input for product keywords
    keywords = st.text_input("Enter products (comma-separated):", "Electric Scooter, Wireless Earbuds")

    # Timeframe Selection
    timeframe = st.selectbox("Select timeframe:", [
        "now 7-d", "now 1-d", "now 1-H", "today 3-m", "today 12-m", "today 5-y", "all"
    ], index=0)

    # Region Selection
    region = st.text_input("Enter geographical region (e.g., US, IN, FR):", "US")

# Get Trends button
if st.button("Get Trends"):
    # Prepare and clean up keyword list
    keyword_list = [kw.strip() for kw in keywords.split(",")]
    pytrends.build_payload(keyword_list, cat=0, timeframe=timeframe, geo=region)

    # Fetch and display trend data
    data = pytrends.interest_over_time()
    if not data.empty:
        st.subheader("Trend Analysis")
        st.line_chart(data[keyword_list])

        # Display Insights and Metrics
        st.subheader("Insights and Metrics")
        for keyword in keyword_list:
            st.markdown(f"### {keyword} Metrics")
            highest_value = data[keyword].max()
            lowest_value = data[keyword].min()
            avg_value = data[keyword].mean()
            st.metric(label="Highest Trend Value", value=highest_value)
            st.metric(label="Lowest Trend Value", value=lowest_value)
            st.metric(label="Average Trend Value", value=round(avg_value, 2))
    else:
        st.warning("No data available for the selected keywords or region.")

# Beautify the Dashboard
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 10px;
    }
    .stTextInput > div > input {
        background-color: #f0f0f0;
        color: #333;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .stMetric-value {
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <div style="text-align: center;">
        <h4>Enhance Your Market Research!</h4>
        <p>Use MarketTrendPro to stay on top of trending products and make data-driven decisions for your business.</p>
    </div>
""", unsafe_allow_html=True)
