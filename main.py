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

# Matrixes
correlation_matrix = daily_return.corr()
covariance_matrix = daily_return.cov()

aapl_spy_covariance = combined_returns.cov().loc['AAPL', 'SPY']
msft_spy_covariance = combined_returns.cov().loc['MSFT', 'SPY']
nvda_spy_covariance = combined_returns.cov().loc['NVDA', 'SPY']

spy_variance = benchmark_returns.var()

aapl_beta = aapl_spy_covariance / spy_variance
msft_beta = msft_spy_covariance / spy_variance
nvda_beta = nvda_spy_covariance / spy_variance


risk_performance = {
    "AAPL": {
        "Average Return": daily_return_average["AAPL"],
        "Volatility": daily_volatility["AAPL"],
        "Annualized Volatility": annualized_volatility["AAPL"],
        "Cumulative Return": cumulative_return["AAPL"].iloc[-1],
        "Maximum Drawdown": max_drawdown["AAPL"],
        "Correlation with SPY": correlations_with_spy["AAPL"],
        "Beta": aapl_beta
    },
    "MSFT": {
            "Average Return": daily_return_average["MSFT"],
            "Volatility": daily_volatility["MSFT"],
            "Annualized Volatility": annualized_volatility["MSFT"],
            "Cumulative Return": cumulative_return["MSFT"].iloc[-1],
            "Maximum Drawdown": max_drawdown["MSFT"],
            "Correlation with SPY": correlations_with_spy["MSFT"],
            "Beta": msft_beta
        },
    "NVDA": {
            "Average Return": daily_return_average["NVDA"],
            "Volatility": daily_volatility["NVDA"],
            "Annualized Volatility": annualized_volatility["NVDA"],
            "Cumulative Return": cumulative_return["NVDA"].iloc[-1],
            "Maximum Drawdown": max_drawdown["NVDA"],
            "Correlation with SPY": correlations_with_spy["NVDA"],
            "Beta": nvda_beta
        }
    
}

risk_performance = pd.DataFrame(risk_performance).T



# Summary
print(prices)
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

print("Correlation Matrix\n", correlation_matrix)
print("Covariance Matrix \n", covariance_matrix)

print("SPY Cumulative Return: ", benchmark_cumulative_return.iloc[-1])
print("SPY Annualized Volatility:", (benchmark_annualized_volatility * 100).round(2), "%")

print("Maximum Benchmark Drawdown:", (benchmark_max_drawdown * 100).round(2), "%")
print("Maximum Benchmark Drawdown Date:", benchmark_max_drawdown_date)

print("SPY Daily Volatility:", (benchmark_daily_volatility * 100).round(2), "%")
print("Correlation with SPY:\n", correlations_with_spy)

print("AAPL-SPY Covariance:", aapl_spy_covariance)
print("MSFT-SPY Covariance:", msft_spy_covariance)
print("NVDA-SPY Covariance:", nvda_spy_covariance)

print("SPY Variance:", spy_variance)
print("AAPL Beta:", aapl_beta)
print("MSFT Beta:", msft_beta)
print("NVDA Beta:", nvda_beta)

print(risk_performance)


# Visualization

# AAPL Closing Chart
mpl.figure(
    figsize=(12, 6)
)

mpl.plot(prices)

mpl.title("Asset Closing Prices")
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

# Correlation matrix
mpl.figure(
    figsize=(12, 6)
)

mpl.imshow(correlation_matrix)
mpl.xticks([0, 1, 2], asset_tickers)
mpl.yticks([0, 1, 2], asset_tickers)
mpl.colorbar()

mpl.title("Correlation matrix")


# Covarelation matrix
mpl.figure(
    figsize=(12,6)
)

mpl.imshow(covariance_matrix)
mpl.title('Covariance Matrix')
mpl.xticks([0, 1, 2], asset_tickers)
mpl.yticks([0, 1, 2], asset_tickers)
mpl.colorbar()



# Cumulative return
mpl.figure(
    figsize=(12, 6)
)

mpl.plot(cumulative_return)
mpl.plot(benchmark_cumulative_return)

mpl.legend()

mpl.xlabel('Date')
mpl.ylabel('Cumulative return')
mpl.grid(alpha = 0.4)
mpl.gca().yaxis.set_major_formatter(PercentFormatter(1))





mpl.show() 