import yfinance as yf
import pandas as pd

# 设置下载数据的时间范围为过去一个月
end_date = pd.Timestamp.now()
start_date = end_date - pd.DateOffset(months=1)

try:
    # 下载英伟达股票数据
    nvda_data = yf.download('NVDA', start=start_date, end=end_date)

    # 计算股价变化百分比
    nvda_data['Price_Change_Percent'] = nvda_data['Close'].pct_change() * 100

    # 打印过去一个月的股价数据
    print(nvda_data.tail())

    # 打印过去一个月的股价变化百分比
    print("过去一个月的股价变化百分比:")
    print(nvda_data['Price_Change_Percent'].tail())

except Exception as e:
    print("发生错误：", e)