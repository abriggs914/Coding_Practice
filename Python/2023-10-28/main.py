import datetime


if __name__ == '__main__':

    fmt = "%H:%M %p"
    g1_st = datetime.datetime(2023, 10, 28, 15, 30)  # 2023-10-28 2:30 PM ET
    g2_st = datetime.datetime(2023, 10, 28, 20)  # 2023-10-28 7:00 PM ET
    early_time_fifa = datetime.timedelta(minutes=-60)  # arrive 1 hr early
    early_time_nhl = datetime.timedelta(minutes=-60)  # arrive 1 hr early

    t_soccer = datetime.timedelta(minutes=165)  # roughly 150 mins + (60 - 15) min early time
    t_hockey = datetime.timedelta(minutes=200)  # roughly 255 mins - 60 min early time

    # apply early arrivals
    g1_st += early_time_fifa
    g1_et = g1_st + t_soccer
    g2_st += early_time_nhl
    g2_et = g2_st + t_hockey

    print(f"{g1_st=}")

    dt_h_m = datetime.timedelta(hours=7.75)  # 7.75 Hrs drive Home to Montreal
    dpt_h_m = g1_st - dt_h_m

    t_between_games = g2_st - g1_et

    print(f"We need to leave at {dpt_h_m:{fmt}} AT to arrive in Montreal early for the soccer game.")
    print(f"We will be at the soccer game from {g1_st:{fmt}} AT to {g1_et:{fmt}} AT ({t_soccer.seconds/3600.0:0.2f} H)")
    print(f"We have {t_between_games.seconds/60:0.2f} minutes to travel between games.")
    print(f"We will be at the hockey game from {g2_st:{fmt}} AT to {g2_et:{fmt}} AT ({t_hockey.seconds/3600.0:0.2f} H)")
