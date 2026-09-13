def calculate_volatility(daily_return):
    volatility = daily_return.std()

    return volatility



def calculate_annualized_volatility(daily_return):
    annualized_volatility = daily_return.std() * (252 ** 0.5)

    return annualized_volatility



def calculate_rolling_volatility(daily_return, window):
    rolling_volatility = daily_return.rolling(window).std()

    return rolling_volatility



def calculate_drawdown(prices):
    running_max = prices.cummax()
    
    drawdown = prices / running_max - 1
    
    return drawdown


def calculate_max_drawdown(drawdown):
    max_drawdown = drawdown.min()
    
    return max_drawdown
    


def calculate_covariance_with_benchmark(daily_return, benchmark_return):
    covariance = daily_return.apply(
        lambda x: x.cov(benchmark_return)
    )

    return covariance


def calculate_beta(daily_return, benchmark_return):
    covariance = calculate_covariance_with_benchmark(
        daily_return,
        benchmark_return
    )

    benchmark_variance = benchmark_return.var()

    beta = covariance / benchmark_variance

    return beta