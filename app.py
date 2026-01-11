import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Stock Dashboard")

# --- Sidebar: User Inputs ---
st.sidebar.header("Stock Parameters")

# 1. Market Selection (To fix the Indian stocks issue)
market = st.sidebar.selectbox("Market", ["US (NASDAQ/NYSE)", "India (NSE)", "India (BSE)"])

# 2. Ticker Input
symbol = st.sidebar.text_input("Ticker Symbol", value="AAPL" if "US" in market else "RELIANCE").upper()

# Logic to handle suffixes automatically
if market == "India (NSE)":
    suffix = ".NS"
elif market == "India (BSE)":
    suffix = ".BO"
else:
    suffix = ""

# Ensure we don't double-add the suffix if the user typed it
if not symbol.endswith(suffix):
    ticker = f"{symbol}{suffix}"
else:
    ticker = symbol

# 3. Date Range
start_date = st.sidebar.date_input("Start Date", date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", date.today())

# 4. Chart Style (To fix the "dotty" issue)
chart_style = st.sidebar.radio("Chart Type", ["Line (Smooth)", "Candlestick (Detailed)"])

# --- Main Page ---
st.title(f"📈 {ticker} Stock Dashboard")

# --- Data Fetching ---
@st.cache_data
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, progress=False)
        
        # Flatten MultiIndex columns if present (Fix for empty graphs)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        return None

if start_date < end_date:
    data = get_stock_data(ticker, start_date, end_date)
else:
    st.error("Error: End date must be after start date.")
    data = None

# --- Display Logic ---
if data is not None and not data.empty:
    
    tab1, tab2 = st.tabs(["Interactive Chart", "Raw Data"])

    with tab1:
        fig = go.Figure()

        if chart_style == "Line (Smooth)":
            # Use a Line chart (Scatter) for the smooth look
            fig.add_trace(go.Scatter(
                x=data['Date'], 
                y=data['Close'], 
                mode='lines', 
                name='Close Price',
                line=dict(color='#00F0FF', width=2) # Cyan color for visibility
            ))
            # Optional: Add a filled area under the curve for a modern look
            fig.update_traces(fill='tozeroy', fillcolor='rgba(0, 240, 255, 0.1)')
            
        else:
            # Use Candlestick for the detailed/technical look
            fig.add_trace(go.Candlestick(
                x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ))

        fig.update_layout(
            title=f'{ticker} Share Price',
            yaxis_title='Price',
            xaxis_rangeslider_visible=True,
            hovermode="x unified",
            height=600,
            template="plotly_dark" # Dark mode matches Streamlit nicely
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Historical Data")
        st.dataframe(data, use_container_width=True)
        
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f'{ticker}_data.csv',
            mime='text/csv',
        )

elif data is not None and data.empty:
    st.warning(f"No data found for '{ticker}'. Try changing the Market selection.")
