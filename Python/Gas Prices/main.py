import datetime

from calendar import monthrange
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# df = pd.read_excel('Historical Petroleum Prices.xls', sheet_name=None)
# df = pd.read_excel('Historical Petroleum Prices 2006-07-01 -- 2022-03-07.xls', sheet_name=None)
df = pd.read_excel('Historical Petroleum Prices (1).xls', sheet_name=None)

all_data = {}
years = list(df.keys())
for year in years:
    weeks_df = df[year]
    weeks = weeks_df.keys()
    print(f"weeks: {weeks}")
    for week in weeks:
        data = list(weeks_df[week].items())
        print(f"data: {data}")
        if len(data) > 6:
            try:
                date = data[1][1]
                price_regular_unleaded = data[6][1]
                print(f"week: {week}, weeks_df[week]: {data}")
                all_data.update({date.strftime("%Y-%m-%d"): price_regular_unleaded})
            except:
                print(f"fail: \'{date}\', price: \'{price_regular_unleaded}\'")
                # raise ValueError("stop")

print(f"all_data: {all_data}")
# print(f"1: {df}")
# print(f"2: {df.keys()}")
# print(f"3: {list(df[list(df.keys())[1]].items())}")
# D = {u'Label1':26, u'Label2': 17, u'Label3':30}


def plt_1():
    plt.bar(range(len(all_data)), list(all_data.values()), align='center')
    plt.xticks(range(len(all_data)), list(all_data.keys()))
    plt.show()


def plt_2():
    global all_data
    all_data = [(k, v) for k, v in all_data.items()]
    all_data.sort(key=lambda t: t[0])
    all_data = {v[0]: v[1] for v in all_data}
    print(f"all_data: {all_data}")
    all_data = {k: v for k, v in all_data.items() if "2022-12-31" >= k >= "2021-01-01"}
    plt.bar(range(len(all_data)), list(all_data.values()), align='center')
    plt.xticks(range(len(all_data)), list(all_data.keys()), rotation=90)
    plt.show()


def plt_3():
    global all_data
    all_data = [(k, v) for k, v in all_data.items()]
    all_data.sort(key=lambda t: t[0])
    all_data = {v[0]: v[1] for v in all_data}
    print(f"all_data: {all_data}")
    all_data = {k: v for k, v in all_data.items() if "2022-12-31" >= k >= "2021-01-01"}
    data = {
        "Dates": [],
        "Gas Prices (%/L)": []
    }
    date_to_v = lambda d: int((d.year * 1000000) + ((d.month / 12) * 10000) + ((d.day / monthrange(d.year, d.month)[1]) * 100))
    for k, v in all_data.items():
        data["Dates"].append(date_to_v(datetime.datetime.strptime(k, "%Y-%m-%d")))
        data["Gas Prices (%/L)"].append(v)
    data = pd.DataFrame(data)

    # sns.regplot(range(len(all_data)), list(all_data.values()))
    sns.regplot(data["Dates"], data["Gas Prices (%/L)"])
    # plt.bar(range(len(all_data)), list(all_data.values()), align='center')
    # sns.xticks(range(len(all_data)), list(all_data.keys()), rotation=90)
    plt.show()


if __name__ == "__main__":
    plt_2()
    # plt_3()

