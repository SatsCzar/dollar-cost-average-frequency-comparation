""" Credits to @araujo88 github """
from binance.client import Client
from binance.enums import *
import pandas as pd
from datetime import datetime
client = Client('your_pub_key_here',
                'your_ptivate_key_here')
# valid intervals — 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M


def print_file(pair, interval, name):
    # request historical candle (or klines) data
    bars = client.get_historical_klines(
        pair, interval, "01 Jan, 2018", "18 Nov, 2022")

    print(bars)
    # delete unwanted data — just keep date, open, high, low, close
    for line in bars:
        del line[5:]

    # save as CSV file
    df = pd.DataFrame(bars, columns=["date", "open", "high", "low", "close"])
    df.drop(columns=['open', 'high', 'low'], inplace=True)

    for index, timeNotFormatted in enumerate(df.date):
        df.date[index] = datetime.fromtimestamp(timeNotFormatted/1000)

    df.set_index("date", inplace=True)
    df.to_csv(name)


print_file("BTCUSDT", "1h", "BTC_1h.csv")
