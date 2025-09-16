# 🪙 Crypto Assets Analysis with Python

This project was developed to practice **data analysis and forecasting applied to the cryptocurrency market**, using Python and Jupyter Notebook.  
The main goal is to explore different techniques for **data collection, visualization, and predictive modeling** in order to identify patterns and insights from digital assets.

---

## 🚀 Features

- **Data Collection**
  - Historical data from Yahoo Finance and Binance API

- **Exploratory Data Analysis (EDA)**
  - Automated profiling report (see [`docs/relatorio_cripto.html`](docs/relatorio_cripto.html))
  - Correlation analysis between crypto assets
  - Statistical hypothesis testing:
    - Best month to invest in BTC
    - Best day to invest in BTC

- **Time Series Analysis**
  - Trend, seasonality, and residual decomposition
  - Moving averages to analyze price behavior
  - **Prophet model for time series forecasting**
  - Seasonal impact on Bitcoin price

- **Visualizations**
  - Candlestick charts
  - Heatmaps
  - Trend projections
  - Seasonality plots

---

## 🛠️ Technologies & Libraries

- **Core**: Python, Jupyter Notebook  
- **Data Handling**: Pandas, NumPy  
- **Visualization**: Matplotlib, Seaborn, Plotly  
- **Stats & Forecasting**: Statsmodels, Prophet  
- **Data Sources**: YFinance, Binance API  
- **EDA**: ydata-profiling  

---

## 📂 Project Structure
├── crypto_analysis.ipynb # Main notebook with analysis
├── crypto_analysis.py # Dependency extraction (can be removed if unused)
├── requirements.txt # Project dependencies
├── docs/
│ └── relatorio_cripto.html # Automated EDA report
└── README.md

>  **Note**: The automated EDA report (`relatorio_cripto.html`) is stored inside the `docs/` folder.  
> You can open it directly by downloading and opening it in your browser.

---

## 📈 Example Visualizations

- 📊 BTC price forecasting with Prophet  
- 📉 Trend and seasonality decomposition  
- 🕯️ Candlestick chart of Bitcoin  
- 🔥 Correlation heatmaps  

<img width="904" height="437" alt="image" src="https://github.com/user-attachments/assets/ab1c36e0-a036-4841-8159-74de27921157" />


---

## ▶ How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/MariaEduardaTDev/stock-crypto-analysis.git

2. Create and activate a virtual environment:
	python -m venv venv
	source venv/bin/activate   # Linux/Mac  
	venv\Scripts\activate      # Windows

3. Install dependencies: 
	pip install -r requirements.txt

4. Run jupyter notwbook
   jupyter notebook




## 📂 Project Structure

