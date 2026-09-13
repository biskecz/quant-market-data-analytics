def calculate_daily_returns(prices):
    daily_return = prices.pct_change()

    return daily_return


def calculate_cumulative_returns(daily_return):
    cumulative_return = (daily_return + 1).cumprod() - 1

    return cumulative_return