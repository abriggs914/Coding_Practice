import datetime
from utility import *

today = datetime.datetime.today()
# today = datetime.date.fromisoformat("2021-12-31")
year_t, week_t, weekday_t = today.isocalendar()
pay_day_of_week = 4
year_temp, week_temp, weekday_temp = today.isocalendar()

def days_to_payday(isoweekday):
	val = abs(isoweekday - 11) % 7
	return val if val != 0 else 7


weekday_temp += days_to_payday(weekday_t)
if weekday_temp > 6:
	weekday_temp -= 7
	week_temp += 1
	if week_temp > 51:
		week_temp -= 52
		year_temp += 1
		
next_pay_day = datetime.date.fromisocalendar(year_temp, week_temp, weekday_temp)
last_day = datetime.date.fromisoformat("2021-12-31")
year_l, week_l, weekday_l = last_day.isocalendar()

pay_per_week = 612.55
starting_balance = 4000
remaining_pay_periods = (last_day - next_pay_day).days // 7
pay_remaining = remaining_pay_periods * pay_per_week


print(dict_print({
	"today": today,
	"year_t": year_t,
	"week_t": week_t,
	"weekday_t": weekday_t,
	"pay_day_of_week": pay_day_of_week,
	"year_temp": year_temp,
	"week_temp": week_temp,
	"weekday_temp": weekday_temp,
	"next_pay_day": next_pay_day,
	"last_day": last_day,
	"year_l": year_l,
	"week_l": week_l,
	"weekday_l": weekday_l,
	"pay_per_week": pay_per_week,
	"starting_balance": starting_balance,
	"remaining_pay_periods": remaining_pay_periods,
	"pay_remaining": pay_remaining,
	"Balance on last day:": pay_remaining + starting_balance
}, "Data"))

print("""
	Starting on {} and Ending {},
	Earning: {} per week.
	{} paycheck{} remaining.
	Totaling: {}.
	Starting with {}

		Finally on {} I should have {} earned.
""".format(today,
 last_day,
 money(pay_per_week),
 remaining_pay_periods,
 "s" if remaining_pay_periods != 0 else "s",
 pay_remaining,
 money(starting_balance),
 last_day,
 money(pay_remaining + starting_balance)))