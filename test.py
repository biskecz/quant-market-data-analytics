from config import TICKERS
from data_loader import load_data
from returns import calculate_daily_returns, calculate_cumulative_returns
from risk import (
    calculate_volatility,
    calculate_annualized_volatility,
    calculate_rolling_volatility,
    calculate_drawdown,
    calculate_max_drawdown,
    calculate_covariance_with_benchmark,
    calculate_beta
)
from statistics import calculate_correlation_matrix


data = load_data()

close = data['Close']
prices = close[TICKERS]
benchmark = close['SPY']

daily_return = calculate_daily_returns(prices)
benchmark_return = benchmark.pct_change()
correlation_matrix = calculate_correlation_matrix(daily_return)

covariance = calculate_covariance_with_benchmark(
    daily_return,
    benchmark_return
)

beta = calculate_beta(
    daily_return,
    benchmark_return
)

cumulative_return = calculate_cumulative_returns(daily_return)
volatility = calculate_volatility(daily_return)
annualized_volatility = calculate_annualized_volatility(daily_return)
rolling_volatility = calculate_rolling_volatility(daily_return, 20)
drawdown = calculate_drawdown(prices)
max_drawdown = calculate_max_drawdown(drawdown)

print(daily_return)
print(cumulative_return)
print(volatility)
print(annualized_volatility)
print(rolling_volatility)
print(drawdown)
print(max_drawdown)
print(covariance)
print(beta)
print(correlation_matrix)