import yfinance as yf
import numpy as np
import matplotlib.pyplot as mpl
from matplotlib.ticker import PercentFormatter
import pandas as pd

# Data
tickers = ['AAPL', 'MSFT', 'NVDA', 'SPY']
data = yf.download(
    tickers,
    start="2020-01-01",
    end="2025-01-01"
)
close = data['Close']
prices = close[['AAPL', 'MSFT', 'NVDA']]
benchmark = close['SPY']
asset_tickers = ['AAPL', 'MSFT', 'NVDA']

# Returns
daily_return = prices.pct_change()
daily_return_average = daily_return.mean()
median_return = daily_return.median()
best_return = daily_return.max()
worst_return = daily_return.min()
best_return_date = daily_return.idxmax()
worst_return_date = daily_return.idxmin()
cumulative_return = (daily_return + 1).cumprod() - 1
benchmark_returns = benchmark.pct_change()
benchmark_cumulative_return = (benchmark_returns + 1).cumprod() - 1
combined_returns = daily_return.copy()
combined_returns['SPY'] = benchmark_returns
correlations_with_spy = combined_returns.corr()['SPY'].drop('SPY')

# Volatility
daily_volatility = daily_return.std()
annualized_volatility = daily_volatility * np.sqrt(252)
rolling_volatility = daily_return.rolling(20).std()
benchmark_daily_volatility = benchmark_returns.std()
benchmark_annualized_volatility = benchmark_daily_volatility * np.sqrt(252)

# Drawdown
running_max = prices.cummax()
drawdown = (prices / running_max) - 1
max_drawdown = drawdown.min()
max_drawdown_date = drawdown.idxmin()
benchmark_running_max = benchmark.cummax()
benchmark_drawdown = (benchmark / benchmark_running_max) - 1
benchmark_max_drawdown = benchmark_drawdown.min()
benchmark_max_drawdown_date = benchmark_drawdown.idxmin()


# Matrices
correlation_matrix = daily_return.corr()
covariance_matrix = daily_return.cov()

covariances_with_spy = {}

for ticker in asset_tickers:
    covariance = combined_returns.cov().loc[ticker, 'SPY']
    covariances_with_spy[ticker] = covariance

spy_variance = benchmark_returns.var()

# Beta
betas = {}

for ticker in asset_tickers:
    covariance = combined_returns.cov().loc[ticker, 'SPY']
    beta = covariance / spy_variance
    betas[ticker] = beta
    
    
# Risk Performance

risk_performance = {}

for ticker in asset_tickers:
    risk_performance[ticker] = {
        "Average Return": daily_return_average[ticker],
        "Volatility": daily_volatility[ticker],
        "Annualized Volatility": annualized_volatility[ticker],
        "Cumulative Return": cumulative_return[ticker].iloc[-1],
        "Maximum Drawdown": max_drawdown[ticker],
        "Correlation with SPY": correlations_with_spy[ticker],
        "Beta": betas[ticker]
    }
    
risk_performance["SPY"] = {
    "Average Return": benchmark_returns.mean(),
    "Volatility": benchmark_daily_volatility,
    "Annualized Volatility": benchmark_annualized_volatility,
    "Cumulative Return": benchmark_cumulative_return.iloc[-1],
    "Maximum Drawdown": benchmark_max_drawdown,
    "Correlation with SPY": 1.0,
    "Beta": 1.0
}
risk_performance = pd.DataFrame(risk_performance).T


# Summary
print("Period:", prices.index[0], 'to', prices.index[-1])
print("Correlation Matrix:\n", correlation_matrix)
print('Covariance Matrix:\n', covariance_matrix)
print('Covariance with SPY:', covariances_with_spy)
print('SPY Variance:', spy_variance)
print('Betas:', betas)
print(risk_performance)

# Visualization

# Closing Prices
mpl.figure(figsize=(12, 6))
mpl.plot(prices)
mpl.title("Asset Closing Prices")
mpl.xlabel("Date")
mpl.ylabel("Price")
mpl.grid(alpha=0.4)

# Daily Return
mpl.figure(figsize=(12, 6))
mpl.plot(daily_return)
mpl.title("Daily Return")
mpl.xlabel("Date")
mpl.ylabel("Daily Return")
mpl.grid(alpha=0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))

# 20-Day Rolling Volatility
mpl.figure(figsize=(12, 6))
mpl.plot(rolling_volatility)
mpl.title("20-Day Rolling Volatility")
mpl.xlabel("Date")
mpl.ylabel("Volatility")
mpl.grid(alpha=0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))

# Drawdown
mpl.figure(figsize=(12, 6))
mpl.plot(drawdown)
mpl.title("Drawdown")
mpl.xlabel("Date")
mpl.ylabel("Drawdown")
mpl.grid(alpha=0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))

# Correlation Matrix
mpl.figure(figsize=(12, 6))
mpl.imshow(correlation_matrix)
for i in range(len(asset_tickers)):
    for j in range(len(asset_tickers)):
        mpl.text(
            j,
            i,
            round(correlation_matrix.iloc[i, j], 2),
            ha='center',
            va='center'
        )
mpl.xticks([0, 1, 2], asset_tickers)
mpl.yticks([0, 1, 2], asset_tickers)
mpl.colorbar()
mpl.title("Correlation Matrix")

# Covariance Matrix
mpl.figure(figsize=(12, 6))
mpl.imshow(covariance_matrix)
for i in range(len(asset_tickers)):
    for j in range(len(asset_tickers)):
        mpl.text(
            j,
            i,
            round(covariance_matrix.iloc[i, j], 6),
            ha='center',
            va='center'
        )
mpl.title("Covariance Matrix")
mpl.xticks([0, 1, 2], asset_tickers)
mpl.yticks([0, 1, 2], asset_tickers)
mpl.colorbar()

# Cumulative Return
mpl.figure(figsize=(12, 6))
mpl.plot(cumulative_return['AAPL'], label="AAPL")
mpl.plot(cumulative_return['MSFT'], label="MSFT")
mpl.plot(cumulative_return['NVDA'], label="NVDA")
mpl.plot(benchmark_cumulative_return, label="SPY")
mpl.title("Cumulative Return Comparison")
mpl.xlabel("Date")
mpl.ylabel("Cumulative Return")
mpl.legend()
mpl.grid(alpha=0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))

mpl.show()

