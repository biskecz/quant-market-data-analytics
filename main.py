import yfinance as yf
import numpy as np
import matplotlib.pyplot as mpl
from matplotlib.ticker import PercentFormatter


# Data
ticker = 'AAPL'

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2025-01-01"
)

close = data['Close']
prices = close['AAPL']


# Returns
daily_return = prices.pct_change()
daily_return_average = daily_return.mean()

median_return = daily_return.median()

best_return = daily_return.max()
worst_return = daily_return.min()
best_return_date = daily_return.idxmax()
worst_return_date = daily_return.idxmin()

cumulative_return = (daily_return + 1).cumprod() - 1

# Volatility
daily_volatility = daily_return.std()
annualized_volatility = daily_volatility * np.sqrt(252)
rolling_volatility = daily_return.rolling(20).std()

# Drawdown
running_max = prices.cummax()
drawdown = (prices / running_max) - 1
max_drawdown = drawdown.min()
max_drawdown_date = drawdown.idxmin()


# Summary
print("Average Daily Return:", (daily_return_average * 100).round(2), "%")

print("Median Return:", (median_return * 100).round(2), "%")

print("Best Return:", (best_return * 100).round(2), "%")
print("Best Return Date:", best_return_date)
print("Worst Return:", (worst_return * 100).round(2), "%")
print("Worst Return Date:", worst_return_date)

print("Daily Volatility:", (daily_volatility * 100).round(2), "%")
print("Annualized Volatility:", (annualized_volatility * 100).round(2), "%")

print("Cumulative Return:", (cumulative_return.iloc[-1] * 100).round(2), "%")

print("Maximum Drawdown:", (max_drawdown * 100).round(2), "%")
print("Maximum Drawdown Date:", max_drawdown_date)

print("Period:", prices.index[0], "to", prices.index[-1])


# Visualization

# AAPL Closing Chart
mpl.figure(
    figsize=(12, 6)
)

mpl.plot(prices)

mpl.title("AAPL Closing chart")
mpl.xlabel("Date")
mpl.ylabel("Price")
mpl.grid(alpha = 0.4)


# Daily Return
mpl.figure(
    figsize=(12, 6)
)
mpl.plot(daily_return)

mpl.title("Daily Return")
mpl.xlabel("Date")
mpl.ylabel("Daily Return")
mpl.grid(alpha = 0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))


# 20-day rolling volatility
mpl.figure(
    figsize=(12, 6)
)
mpl.plot(rolling_volatility)

mpl.title("20-Day Rolling Volatility")
mpl.xlabel("Date")
mpl.ylabel("Volatility")
mpl.grid(alpha = 0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))


# Drawdown
mpl.figure(
    figsize=(12, 6)
)
mpl.plot(drawdown)

mpl.title('Drawdown')
mpl.xlabel("Date")
mpl.ylabel("Drawdown")
mpl.grid(alpha = 0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))

mpl.show()