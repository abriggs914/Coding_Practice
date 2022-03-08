import datetime

day_1 = datetime.datetime(1, 1, 1)
now = day_1
today = datetime.datetime.now()

date_sums = {}


def date_val(date):
    return (date.year % 100) + (date.year // 100) + date.month + date.day


while (today - now).days > 1:
    # date_str = now.strftime("%Y-%m-%d")
    date_str = date_val(now)
    if date_str not in date_sums:
        date_sums[date_str] = (0, [now])
    date_sums.update({date_str: (date_sums[date_str][0] + 1, [now] + date_sums[date_str][1][:9])})
    now += datetime.timedelta(days=1)

for k, v in date_sums.items():
    print(f"k: {k}, v: {v}")
