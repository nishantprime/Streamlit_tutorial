import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Stock Dashboard")

# --- Sidebar: User Inputs ---
st.sidebar.header("Stock Parameters")

# 1. Ticker Input (Default to AAPL)
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL").upper()

# 2. Date Range Selection
# Default to showing the last 365 days
start_date = st.sidebar.date_input("Start Date", date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", date.today())

# --- Main Page ---
st.title(f"📈 {ticker} Stock Dashboard")

# --- Data Fetching ---
# We use @st.cache_data to prevent reloading data on every interaction (dragging/zooming)
@st.cache_data
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, progress=False)
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        return None

# Load data
if start_date < end_date:
    data = get_stock_data(ticker, start_date, end_date)
else:
    st.error("Error: End date must be after start date.")
    data = None

# --- Display Logic ---
if data is not None and not data.empty:
    
    # Create Tabs for better organization
    tab1, tab2 = st.tabs(["Interactive Chart", "Raw Data"])

    with tab1:
        # --- Plotly Interactive Chart ---
        fig = go.Figure()

        # Candlestick (Open, High, Low, Close)
        fig.add_trace(go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ))

        # Layout customization for "dragging" and interactivity
        fig.update_layout(
            title=f'{ticker} Share Price',
            yaxis_title='Stock Price (USD)',
            xaxis_rangeslider_visible=True, # Adds the bottom slider for time zooming
            hovermode="x unified",          # Shows all data points when hovering over a specific date
            height=600
        )

        # Render the chart
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("Tip: You can drag on the chart to zoom, or use the range slider at the bottom.")

    with tab2:
        # --- Raw Data Display ---
        st.subheader("Historical Data")
        st.dataframe(data, use_container_width=True)

        # Download button
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f'{ticker}_stock_data.csv',
            mime='text/csv',
        )

elif data is not None and data.empty:
    st.warning(f"No data found for ticker '{ticker}'. Please check the symbol.")
