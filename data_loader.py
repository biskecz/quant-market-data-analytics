import yfinance as yf

from config import TICKERS, BENCHMARK, START_DATE, END_DATE


def load_data():
    tickers = TICKERS + [BENCHMARK]

    data = yf.download(
        tickers,
        start=START_DATE,
        end=END_DATE
    )

    return data