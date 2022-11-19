import pandas as pd
import numpy as np
from calendar import monthrange
import matplotlib.pyplot as plt


def compareDCAFrequencies():
    """
    5 years
    12 months
    US$ 200 by month
    """

    btcPriceHistory = pd.read_csv("BTC_1h.csv", parse_dates=False)
    btcPriceHistory['date'] = pd.to_datetime(btcPriceHistory['date'])

    bitcoinEveryDayAccumulator = 0
    bitcoinEveryMonthAccumulator = 0

    btcEveryDayLine = []
    btcEveryMonthLine = []

    monthlyBuy = 200

    years = [2018, 2019, 2020, 2021, 2022]
    months = range(1, 13)

    for year in years:

        if year == 2022:
            months = range(1, 11)

        for month in months:

            def getBtcPrice(year, month, day):
                startSearch = pd.to_datetime(f'{year}-{month}-{day} 09:00:00')
                endSearch = pd.to_datetime(f'{year}-{month}-{day} 23:00:00')

                filtered = btcPriceHistory[(btcPriceHistory['date'] >= startSearch) &
                                    (btcPriceHistory['date'] <= endSearch)]

                try:
                    return filtered.iloc[0]['close']
                except:
                    startSearch = pd.to_datetime(
                        f'{year}-{month}-{day-1} 00:00:00')
                    endSearch = pd.to_datetime(
                        f'{year}-{month}-{day} 23:00:00')

                    filtered = btcPriceHistory[(btcPriceHistory['date'] >= startSearch) &
                                        (btcPriceHistory['date'] <= endSearch)]
                    return filtered.iloc[0]['close']

            _, days = monthrange(year, month)

            def buyBtc(btcPrice, amount):
                return amount / btcPrice

            compraDiaria = monthlyBuy / days

            for day in range(1, days + 1):
                btcPrice = getBtcPrice(year, month, day)
                bitcoinEveryDayAccumulator += buyBtc(btcPrice, compraDiaria)

            btcPrice = getBtcPrice(year, month, 5)
            bitcoinEveryMonthAccumulator += buyBtc(btcPrice, monthlyBuy)

            btcEveryDayLine.append(bitcoinEveryDayAccumulator)
            btcEveryMonthLine.append(bitcoinEveryMonthAccumulator)

    plt.plot(np.array(btcEveryDayLine), c='r')
    plt.plot(np.array(btcEveryMonthLine))
    plt.show()

    print('Final result')
    print(f'BTC every day: {round(bitcoinEveryDayAccumulator, 8)}')
    print(f'BTC every month: {round(bitcoinEveryMonthAccumulator, 8)}')
    print(f'Difference: {round(bitcoinEveryMonthAccumulator - bitcoinEveryDayAccumulator, 8)}',
          f'or {round(((bitcoinEveryMonthAccumulator / bitcoinEveryDayAccumulator)-1)*100)}%')

compareDCAFrequencies()
