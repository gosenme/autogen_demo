import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Fetch the stock prices for NVDA and TESLA
nvda = yf.download('NVDA', start='2024-11-08', end=datetime.today().strftime('%Y-%m-%d'))
tsla = yf.download('TSLA', start='2024-11-08', end=datetime.today().strftime('%Y-%m-%d'))

# Calculate the YTD change for each stock
nvda_ytd_change = (nvda['Close'].iloc[-1] - nvda['Close'].iloc[0]) / nvda['Close'].iloc[0] * 100
tsla_ytd_change = (tsla['Close'].iloc[-1] - tsla['Close'].iloc[0]) / tsla['Close'].iloc[0] * 100

# Plot the YTD change
plt.figure(figsize=(10, 5))
plt.plot(nvda.index, nvda['Close'], label='NVDA YTD Change')
plt.plot(tsla.index, tsla['Close'], label='TSLA YTD Change')
plt.title('NVDA and TESLA Stock Price Change YTD')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

# Print the YTD change for each stock
print(f"NVDA YTD Change: {nvda_ytd_change:.2f}%")
print(f"TSLA YTD Change: {tsla_ytd_change:.2f}%")
