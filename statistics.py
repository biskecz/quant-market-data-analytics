def calculate_correlation_matrix(daily_return):
    correlation_matrix = daily_return.corr()

    return correlation_matrix