import datetime
import pandas as pd

import holidays

from datetime_utility import first_of_month, first_of_week
from utility import next_available_file_name


# can_holidays = holidays.Canada()


col_date: str = "CalendarDate"


output_file: str = next_available_file_name(r"C:\Users\abrig\Documents\Coding_Practice\Python\Resource\Dates\dates_output.xlsx")


def new_inserts():
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2025, 12, 31)
    dates = [(start + datetime.timedelta(days=i)).date() for i in range((end - start).days)]

    holidays_list = {}
    # Print all the holidays in UnitedKingdom in year 2018
    for ptr in holidays.Canada(years=list(range(2017, 2026))).items():
        date, holiday_name = ptr
        holidays_list.update({date: holiday_name.replace("'", "''")})

    top_template = f"INSERT INTO [Calendar] ([Date], [Day], [DayOfWeek], [SAT Holiday], [STAT Holiday], " \
                   f"[HolidayName]) VALUES"
    i_template = "('{date}', '{day}', {dow}, {sat_h}, {stat_h}, {hn})"
    i_templates_list = []

    print(f"{holidays_list=}")
    print(f"{dates=}")

    for date in dates:
        hn = "NULL"
        dow = date.isoweekday()
        sat_h = 1 if (dow > 5) else 0
        stat_h = 0
        if date in holidays_list:
            hn = f"'{holidays_list[date]}'"
            stat_h = 1

        i_templates_list.append(
            i_template.format(date=date, day=date.strftime("%A"), dow=dow, sat_h=sat_h, stat_h=stat_h, hn=hn))

    for i in range(0, len(i_templates_list), 1000):
        print(f"\n" + top_template)
        print(",\n".join(i_templates_list[i: i + 1000]))
        print(f";\n")


def old_updates():
    start = datetime.datetime(2011, 1, 1)
    end = datetime.datetime(2018, 1, 1)
    dates = [(start + datetime.timedelta(days=i)).date() for i in range((end - start).days)]

    holidays_list = {}
    # Print all the holidays in UnitedKingdom in year 2018
    for ptr in holidays.Canada(years=list(range(start.year, end.year + 1))).items():
        date, holiday_name = ptr
        holidays_list.update({date: holiday_name.replace("'", "''")})

    i_template = "UPDATE [Calendar] SET [HolidayName] = {hn} WHERE [Date] = '{date} 00:00:00.000';"
    i_templates_list = []

    print(f"{holidays_list=}")
    print(f"{dates=}")

    for date in dates:
        hn = "NULL"
        if date in holidays_list:
            hn = f"'{holidays_list[date]}'"

        i_templates_list.append(
            i_template.format(date=date, hn=hn))

    for i in range(0, len(i_templates_list), 1000):
        print("\n".join(i_templates_list[i: i + 1000]) + "\n")


def add_st_patricks_days(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    h = "St. Patrick''s Day"
    h = h if not df_mode else h.replace("''", "'")
    i_templates_list = []
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)
    for y in range(s_y, e_y + 1):
        d = datetime.date(y, 3, 17)
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append("UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} "
                                    "WHERE [{col_date}] = '{d}';".format(h=h, d=f"{d:%Y-%m-%d}"))
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def add_valentines_days(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    h = "Valentine''s Day"
    h = h if not df_mode else h.replace("''", "'")
    i_templates_list = []
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)
    for y in range(s_y, e_y + 1):
        d = datetime.date(y, 2, 14)
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append("UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} "
                                    "WHERE [{col_date}] = '{d}';".format(h=h, d=f"{d:%Y-%m-%d}"))
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def add_halloweens(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    h = "Halloween"
    i_templates_list = []
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)
    for y in range(s_y, e_y + 1):
        d = datetime.date(y, 10, 31)
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append("UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} "
                                    "WHERE [{col_date}] = '{d}';".format(h=h, d=f"{d:%Y-%m-%d}"))
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def add_rememberance_day(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    h = "Rememberance Day"
    i_templates_list = []
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)
    for y in range(s_y, e_y + 1):
        d = datetime.date(y, 11, 11)
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append("UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} "
                                    "WHERE [{col_date}] = '{d}';".format(h=h, d=f"{d:%Y-%m-%d}"))
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def add_mothers_day(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    # second sunday in May, https://www.calendardate.com/mothers_day_2023.htm
    
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)  

    h = "Mother''s Day"
    h = h if not df_mode else h.replace("''", "'")
    i_templates_list = []
    for y in range(s_y, e_y + 1):
        dm = first_of_month(datetime.datetime(y, 5, 1))
        dw = first_of_week(dm)
        dy = 14
        if dm == dw:
            dy = 7
        d = (dw + datetime.timedelta(days=dy)).date()
        # print(f"{d:%Y-%m-%d}")
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append(f"UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} WHERE [{col_date}] = '{d:%Y-%m-%d}';")
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def add_fathers_day(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    # third sunday in June, https://www.calendardate.com/mothers_day_2023.htm
    
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)  

    h = "Father''s Day"
    h = h if not df_mode else h.replace("''", "'")
    i_templates_list = []
    for y in range(s_y, e_y + 1):
        dm = first_of_month(datetime.datetime(y, 6, 1))
        dw = first_of_week(dm)
        dy = 21
        if dm == dw:
            dy = 14
        d = (dw + datetime.timedelta(days=dy)).date()
        # print(f"{d:%Y-%m-%d}")
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append(f"UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} WHERE [{col_date}] = '{d:%Y-%m-%d}';")
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def add_new_brunswick_day(start=2011, end=2025, df_mode: bool = True, stat_holiday: bool = False):
    # first monday of august
    
    s_y, s_m, s_d = start, 1, 1
    e_y, e_m, e_d = end, 1, 1
    if isinstance(start, (datetime.datetime, datetime.date)):
        s_y, s_m, s_d = start.year, start.month, start.day
    if isinstance(end, (datetime.datetime, datetime.date)):
        e_y, e_m, e_d = end.year, end.month, end.day
    start = datetime.date(s_y, s_m, s_d)
    end = datetime.date(e_y, e_m, e_d)  

    h = "New Brunswick Day"
    h = h if not df_mode else h.replace("''", "'")
    i_templates_list = []
    for y in range(s_y, e_y + 1):
        dm = datetime.datetime(y, 8, 1)
        dw = (first_of_week(dm) + datetime.timedelta(days=1))
        # dy = 1
        # if dm == dw:
        #     dy = 1
        # d = (dw + datetime.timedelta(days=dy)).date()
        # print(f"{d:%Y-%m-%d}")
        d = (dw + datetime.timedelta(days=7) if dw.month == 7 else dw).date()
        if start <= d <= end:
            if df_mode:
                i_templates_list.append((d, h, stat_holiday))
            else:
                i_templates_list.append(f"UPDATE [Calendar] SET [HolidayName] = '{h}', [StatHoliday] = {int(stat_holiday)} WHERE [{col_date}] = '{d:%Y-%m-%d}';")
    # print("\n" + "\n".join(i_templates_list) + "\n")
    return i_templates_list


def past_inserts():
    start = datetime.datetime(1900, 1, 1)
    start = datetime.datetime(1951, 1, 1)
    end = datetime.datetime(2010, 12, 31)

    start = datetime.datetime(2026, 1, 1)
    end = datetime.datetime(2041, 1, 1)

    dates = [(start + datetime.timedelta(days=i)).date() for i in range((end - start).days)]

    holidays_list = {}
    # Print all the holidays in UnitedKingdom in year 2018
    for ptr in holidays.Canada(years=list(range(2017, 2026))).items():
        date, holiday_name = ptr
        holidays_list.update({date: holiday_name.replace("'", "''")})

    top_template = f"INSERT INTO [Calendar] ([Date], [Day], [DayOfWeek], [SAT Holiday], [STAT Holiday], " \
                   f"[HolidayName]) VALUES"
    i_template = "('{date}', '{day}', {dow}, {sat_h}, {stat_h}, {hn})"
    i_templates_list = []

    print(f"{holidays_list=}")
    print(f"{dates=}")

    for date in dates:
        hn = "NULL"
        dow = date.isoweekday()
        sat_h = 1 if (dow > 5) else 0
        stat_h = 0
        if date in holidays_list:
            hn = f"'{holidays_list[date]}'"
            stat_h = 1

        i_templates_list.append(
            i_template.format(date=date, day=date.strftime("%A"), dow=dow, sat_h=sat_h, stat_h=stat_h, hn=hn))

    for i in range(0, len(i_templates_list), 1000):
        print(f"\n" + top_template)
        print(",\n".join(i_templates_list[i: i + 1000]))
        print(f";\n")


def holiday_updates(start, end, update_insert="insert", output_file=None, additional_days=None):
    df_mode: bool = output_file.lower().endswith(".xlsx") if isinstance(output_file, str) else False
    dates = [(start + datetime.timedelta(days=i)).date() for i in range((end - start).days)]

    holidays_list = {}
    # Print all the holidays in UnitedKingdom in year 2018
    for ptr in holidays.Canada(years=list(range(start.year, end.year+1))).items():
        date, holiday_name = ptr
        holidays_list.update({date: holiday_name.replace("'", "''" if df_mode else "'")})

    print(f"{holidays_list=}")
    # print(f"{dates=}")
    
    cols = [col_date, "DayOfWeek", "SATHoliday", "STATHoliday", "HolidayName"]
    i_templates_list = []
    if additional_days is None:
        additional_days = []
    other_holidays = [f[0](start, end, df_mode, stat_holiday=f[1]) if isinstance(f, tuple) else f(start, end, df_mode) for f in additional_days]
    print(f"{other_holidays=}")
    
    if isinstance(output_file, str) and output_file.lower().endswith(".xlsx"):
        for date in dates:
            hn = None
            dow = date.isoweekday()
            sat_h = 1 if (dow > 5) else 0
            stat_h = 0
            if date in holidays_list:
                hn = f"'{holidays_list[date]}'" if not df_mode else holidays_list[date]
                stat_h = 1

            h_names = ""
            for j, o_holiday in enumerate(other_holidays):
                if o_holiday:
                    if o_holiday[0][0] == date:
                        h_names += f"{o_holiday[0][1]};"
                        stat_h = int(bool(o_holiday[0][2]))
                        o_holiday.pop(0)
            h_names = h_names.removesuffix(";")
            
            if h_names:
                hn = h_names

            if isinstance(hn, str):
                hn = hn if not df_mode else hn.replace("''", "'")
            i_templates_list.append(dict(zip(cols, (date, date.strftime("%A"), sat_h, stat_h, hn))))
        
        df = pd.DataFrame(i_templates_list)
        df.to_excel(output_file)
        
    else:

        if update_insert == "insert":
            top_template = f"INSERT INTO [" + "], [".join(cols) + "], " + f"[HolidayName]) VALUES"
            i_template = "('{date}', '{day}', {dow}, {sat_h}, {stat_h}, {hn})"

            for date in dates:
                hn = "NULL"
                dow = date.isoweekday()
                sat_h = 1 if (dow > 5) else 0
                stat_h = 0
                if date in holidays_list:
                    hn = f"'{holidays_list[date]}'"
                    stat_h = 1

                i_templates_list.append(
                    i_template.format(date=date, day=date.strftime("%A"), dow=dow, sat_h=sat_h, stat_h=stat_h, hn=hn))

            oput = ""
            for i in range(0, len(i_templates_list), 1000):
                oput_ = f"\n" + top_template
                oput_ += ",\n".join(i_templates_list[i: i + 1000])
                oput_ += f";\n"
                print(oput_)
                oput += oput_

        else:
            top_template = f"UPDATE [Calendar] SET [HolidayName] = {{hn}}, [SATHoliday] = {{sat_h}}, [STATHoliday] = {{stat_h}} WHERE [{col_date}] = '{{date}}'"
            for date in dates:
                hn = "NULL"
                dow = date.isoweekday()
                sat_h = 1 if (dow > 5) else 0
                stat_h = 0
                if date in holidays_list:
                    hn = f"'{holidays_list[date]}'"
                    stat_h = 1

                if sat_h or stat_h:
                    i_templates_list.append(
                        top_template.format(date=date, sat_h=sat_h, stat_h=stat_h, hn=hn))

            oput = f"\n".join(i_templates_list)
            print(oput)

            # for i in range(0, len(i_templates_list), 1000):
            #     print(f"\n" + top_template)
            #     print(",\n".join(i_templates_list[i: i + 1000]))
            #     print(f";\n")

        if output_file is not None:
            with open(output_file, "w") as f:
                f.write(oput)


if __name__ == '__main__':

    # start_ = datetime.datetime(1900, 1, 1)
    # end_ = datetime.datetime(2041, 1, 1)

    # # # start_ = datetime.datetime(2020, 1, 1)
    # # # end_ = datetime.datetime(2021, 1, 1)
    # # o_file = "output.sql"
    # #
    # # # new_inserts()
    # # # old_updates()
    # # # past_inserts()
    # # holiday_updates(
    # #     start=start_,
    # #     end=end_,
    # #     update_insert="update",
    # #     output_file=o_file
    # # )
    # add_halloweens(start_.year, end_.year)
    # add_mothers_day(start_.year, end_.year)
    # add_fathers_day(start_.year, end_.year)

    sub_funcs = [
        add_valentines_days,
        add_st_patricks_days,
        add_mothers_day,
        add_fathers_day,
        (add_new_brunswick_day, 1),
        add_halloweens,
        (add_rememberance_day, 1)
    ]
    
    holiday_updates(
        start=datetime.datetime(2023, 1, 1),
        end=datetime.datetime(2031, 1, 1),
        update_insert="insert",
        output_file=output_file,
        additional_days=sub_funcs
    )