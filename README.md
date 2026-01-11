# 📈 Interactive Stock Dashboard

A real-time stock market data presenter built with **Streamlit**, **yfinance**, and **Plotly**. This dashboard allows users to analyze stock performance across US and Indian markets with interactive charts.

## 🚀 Features

* **Global Market Support:**
    * 🇺🇸 US Markets (NASDAQ, NYSE)
    * 🇮🇳 Indian Markets (NSE, BSE) - *Auto-handles `.NS` and `.BO` suffixes.*
* **Interactive Visualizations:**
    * **Line Chart:** Smooth trend visualization with area fill.
    * **Candlestick Chart:** Detailed view (Open, High, Low, Close).
    * **Interactivity:** Zoom, pan, and hover to see exact price points.
* **Data Access:** View raw historical data and download it as a **CSV file**.

## 🛠️ Installation & Setup

1.  **Clone the repository** (or download the files).
2.  **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If you haven't set up `requirements.txt` yet, see below).*

3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

4.  **Open your browser**: The app will launch automatically at `(https://view-stocks.streamlit.app/)`.

## 📂 Project Structure

* `app.py`: The main application logic and UI code.
* `requirements.txt`: List of Python dependencies.

## 📦 Dependencies

Ensure your `requirements.txt` contains the following:

```text
streamlit
yfinance
plotly
pandas
