import yfinance as yf
import datetime

# 获取英伟达股票数据
stock_symbol = 'NVDA'
stock_data = yf.download(stock_symbol, period='1mo', interval='1d')

# 计算股价变化百分比
stock_data['Price_Change_Percent'] = stock_data['Close'].pct_change() * 100

# 打印过去一个月的股价数据
print(stock_data.tail())

# 获取公司新闻
news_data = yf.news(stock_symbol)

# 打印最近几条新闻
print(news_data.head())