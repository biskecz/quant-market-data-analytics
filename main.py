import yfinance as yf

ticker = 'AAPL'

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2025-01-01"
)

close = data['Close']
prices = close['AAPL']
daily_return = prices.pct_change()


print(data.head())
print()
print(data.info())

print(data.shape)
print(data.tail(5))
print(data.columns)

print(close.head())
print(type(close))
print(close.shape)

print(type(prices))
print(prices.head())

print(daily_return.head(10))