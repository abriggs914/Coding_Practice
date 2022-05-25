import datetime

from league import *
from team import Team
from utility import dict_print
from itertools import combinations
from pandas import DataFrame

teams = {
    "Port City Fog": {
        "city": "Saint John",
        "province": "NB"
    },
    "Halifax Thunder": {
        "city": "Halifax",
        "province": "NS"
    },
    "Halifax Hornets": {
        "city": "Halifax",
        "province": "NS"
    },
    "Windsor Edge": {
        "city": "Windsor",
        "province": "NS"
    },
    "Moncton Mystics": {
        "city": "Moncton",
        "province": "NB"
    },
    "Fredericton Freeze": {
        "city": "Fredericton",
        "province": "NB"
    }
}


def n_games_rr(teams_dict, n_rr=1):
    n_teams = len(teams_dict) - 1
    # ab ac ad ae af
    #    bc bd be bf
    #       cd ce cf
    #          de df
    #             ef
    return n_rr * (((n_teams * (n_teams + 1))) // 2)


def read_html_table_values(file_name, r_type=dict):
    try:
        header = ["GP", "W", "L", "PF", "PA", "PTS"]
        with open(file_name, "r") as f:
            html = f.read()
            html = html.replace("\n", "")
            idx_1 = html.index("<tbody>")
            idx_2 = html.index("</tbody>")
            html_3 = html[idx_1: idx_2].strip().split("<td>")[1:]

            #    return [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in
            # enumerate([line for i, line in enumerate(html.replace("\n", "").split("<td>")[1:]) if i % 7 != 0])]
            # return {html_3[i].replace("</td>", "").strip(): [int(line.replace("</tr>", "").replace("</td>", "").replace("<tr>", "").strip()) for line in html_3[i + 1: i + 7]] for i in range(0, len(html_3), 7)}
            if r_type == dict:
                return {html_3[i].replace("</td>", "").strip(): dict(zip(header, [
                    int(line.replace("</tr>", "").replace("</td>", "").replace("<tr>", "").strip()) for line in
                    html_3[i + 1: i + 7]])) for i in range(0, len(html_3), 7)}
            if r_type == DataFrame:
                html_4 = [line for i, line in enumerate(html_3) if i % 7 != 0]
                html_5 = [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in
                          enumerate(html_4)]
                names = [line.replace("</td>", "").strip() for i, line in enumerate(html_3) if i % 7 == 0]
                values = [html_5[i: i + 6] for i in range(0, len(html_5), 6)]
                d2 = {header[j]: [values[i][j] for i in range(len(values))] for j in range(len(header))}
                d1 = {"Names": names}
                d1.update(d2)
                print(f"di: {d1}")
                return DataFrame(d1)
                # return DataFrame({html_3[i].replace("</td>", "").strip(): dict(zip(header, [int(line.replace("</tr>", "").replace("</td>", "").replace("<tr>", "").strip()) for line in html_3[i + 1: i + 7]])) for i in range(0, len(html_3), 7)})
    except ValueError as ve:
        raise ValueError(f"ValueError: {ve}")
    except FileExistsError as fe:
        raise ValueError(f"FileExistsError: {fe}")
    except FileNotFoundError as fn:
        raise ValueError(f"FileNotFoundError: {fn}")
    except IndexError as ie:
        raise ValueError(f"IndexError: {ie}")
    except AttributeError as ae:
        raise ValueError(f"AttributeError: {ae}")
    except TypeError as te:
        raise ValueError(f"TypeError: {te}")


def df_exports(df):
    dictionary = df.to_dict()
    print(f"dictionary: {dictionary}")
    print(dict_print(dictionary))
    html = df.to_html()
    print(f"html: {html}")
    json = df.to_json()
    print(f"json: {json}")
    # # df2 = pandas.DataFrame.from_dict(dictionary, orient="index", columns=dictionary.keys())
    # # df2 = pandas.DataFrame.from_dict(dictionary, orient="index")
    # # df2 = pandas.DataFrame.from_dict(dictionary).transpose()[list(dictionary.keys())]
    # dictionary2 = {k: list(v.values()) for k, v in dictionary.items()}
    # print(dict_print(dictionary2))
    # print(f"dictionary2: {dictionary2}")
    df2 = DataFrame(dictionary)
    print()
    print(df2)


def add_stats(df, pts_for_win, total_games, n_rr):
    df["DIFF"] = df["PF"] - df["PA"]
    df["LOSTPTS"] = (df["GP"] - df["W"]) * pts_for_win
    df["MAXPTS"] = (pts_for_win * total_games * n_rr) - ((df["GP"] - df["W"]) * pts_for_win)
    df["AVGPF"] = df["PF"] / df["GP"]
    df["AVGPA"] = df["PA"] / df["GP"]
    df["AVGDIFF"] = df["DIFF"] / df["GP"]
    df["RECORD"] = [f"{df['W'][i]}-{df['L'][i]}||{df['GP'][i]}" for i in range(len(df))]
    print()
    print(df)
    print("VVV")
    print(list(df["RECORD"]))


if __name__ == '__main__':

    # Show general team data and league stats:
    print(dict_print(teams, "MWBA Teams List:"))
    n_rr = 2
    n_pts_win = 2
    n_games = n_games_rr(teams, n_rr=n_rr)
    n_games_per_team = n_games_rr(teams, n_rr=n_rr) / len(teams)
    max_pts = n_rr * n_pts_win * (len(teams) - 1)
    print(
        f"Number of games for a group of {len(teams)} teams in a round robin season\nplaying {n_rr} game{'' if n_rr == 1 else 's'} each, is {n_games} game{'' if n_games == 1 else 's'}.\nMeaning that the best overall points record is {max_pts} point{'' if max_pts == 1 else 's'}.")

    print(dict_print({i + 1: {"A": dat[0], "B": dat[1]} for i, dat in enumerate(n_rr * list(combinations(teams, 2)))}, "All Game Combinations:"))

    # html = """<tr>
    #                         <td>Halifax Thunder</td>
    #                         <td>2</td>
    #                         <td>2</td>
    #                         <td>0</td>
    #                         <td>156</td>
    #                         <td>121</td>
    #                         <td>4</td>
    #                     </tr>
    #                         <tr>
    #                         <td>Halifax Hornets</td>
    #                         <td>2</td>
    #                         <td>2</td>
    #                         <td>0</td>
    #                         <td>157</td>
    #                         <td>132</td>
    #                         <td>4</td>
    #                     </tr>
    #                     <tr>
    #                         <td>Windsor</td>
    #                         <td>2</td>
    #                         <td>1</td>
    #                         <td>1</td>
    #                         <td>137</td>
    #                         <td>137</td>
    #                         <td>2</td>
    #                     </tr>
    #                     <tr>
    #                         <td>Fredericton</td>
    #                         <td>2</td>
    #                         <td>1</td>
    #                         <td>1</td>
    #                         <td>134</td>
    #                         <td>137</td>
    #                         <td>2</td>
    #                     </tr>
    #                     <tr>
    #                         <td>Moncton</td>
    #                         <td>2</td>
    #                         <td>0</td>
    #                         <td>2</td>
    #                         <td>129</td>
    #                         <td>149</td>
    #                         <td>0</td>
    #                     </tr>
    #                     <tr>
    #                         <td>Port City</td>
    #                         <td>2</td>
    #                         <td>0</td>
    #                         <td>2</td>
    #                         <td>131</td>
    #                         <td>151</td>
    #                         <td>0</td>
    #                     </tr>"""
    # html.replace("\n", "")
    # html_3 = html.replace("\n", "").split("<td>")[1:]
    # html_4 = [line for i, line in enumerate(html_3) if i % 7 != 0]
    # html_5 = [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in
    #           enumerate(html_4)]
    # html_6 = [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in
    #           enumerate([line for i, line in enumerate(html.replace("\n", "").split("<td>")[1:]) if i % 7 != 0])]
    # print(dict_print({
    #     "html": html,
    #     "html_3": html_3,
    #     "html_4": html_4,
    #     "html_5": html_5,
    #     "html_6": html_6,
    #     "sum(5)": sum(html_5),
    #     "sum(6)": sum(html_6)
    # }))

    # print(dict_print(read_html_table_values("2022-05-19.html"), "Stats as of 2022-05-19"))
    # print(dict_print(read_html_table_values("2022-05-20.html"), "Stats as of 2022-05-20"))
    print(dict_print(read_html_table_values("2022-05-25.html"), "Stats as of 2022-05-25"))
    # df1 = read_html_table_values("2022-05-19.html", r_type=DataFrame)
    # df1 = read_html_table_values("2022-05-20.html", r_type=DataFrame)
    df1 = read_html_table_values("2022-05-25.html", r_type=DataFrame)
    
    print()
    print(df1.loc[df1["PTS"] >= 3])
    print()
    print(df1)
    print()
    add_stats(df1, pts_for_win=n_pts_win, total_games=n_games_per_team, n_rr=n_rr)
    print()
    print(df1.to_html())
    print()
    print(f"Total games played: {sum(df1['GP']) // 2}")
    print(f"Total points scored: {sum(df1['PF'])}")

    history_str_1 = """
    Played May 15
    Moncton 63  Halifax Thunder 83
    Port City 68  Windsor 71
    Fredericton 66  Halifax Hornets 71

    Played May 15
    Port City 58  Halifax Thunder 73
    Moncton 66  Halifax Hornets 86
    Fredericton 69  Windsor 66
    """
    # {"date": [{"a (team name)": a_pts, "b (team name)": b_pts}}, ...]
    lst1 = history_str_1.split("\n")
    lst2 = [line.strip() for line in lst1 if line.strip()]
    ar_games = {}
    curr_date = None
    for i, line in enumerate(lst2):
        if line:
            # print(f"i: <{i}>, <{line}>")
            if i % 4 == 0:
                if line not in ar_games:
                    ar_games[line] = []
                curr_date = line
            else:
                game_dat = line.split("  ")
                # print(f"game_dat: <{game_dat}>")
                a = " ".join(game_dat[0].split(" ")[:-1])
                ap = int(game_dat[0].split(" ")[-1])
                b = " ".join(game_dat[1].split(" ")[:-1])
                bp = int(game_dat[1].split(" ")[-1])
                ar_games[curr_date].append({a: ap, b: bp})
    # print(lst)
    # print({lst[i]: None for i, line in enumerate(lst) if line})
    # ar_games = {line[0]: {"A": " ".join(line.split("  ")[0].split(" ")[:-1])} for i, line in enumerate(history_str_1.split("\n")[1::4]) if line}
    print("ar_games")
    print(ar_games)

    team_1 = Team(1, name="Port City Fog", city="Saint John", province="NB", _games_played=0, _points=0, _points_for=0, _points_against=0, _avg_pf=0, _avg_pa=0, _last_10=None, _record=None, games={})
    team_2 = Team(2, name="Moncton Mystics", city="Moncton", province="NB", _games_played=0, _points=0, _points_for=0, _points_against=0, _avg_pf=0, _avg_pa=0, _last_10=None, _record=None, games={})
    team_3 = Team(3, name="Fredericton Freeze", city="Fredericton", province="NB", _games_played=0, _points=0, _points_for=0, _points_against=0, _avg_pf=0, _avg_pa=0, _last_10=None, _record=None, games={})
    team_4 = Team(4, name="Halifax Hornets", city="Halifax", province="NS", _games_played=0, _points=0, _points_for=0, _points_against=0, _avg_pf=0, _avg_pa=0, _last_10=None, _record=None, games={})
    team_5 = Team(5, name="Halifax Thunder", city="Halifax", province="NS", _games_played=0, _points=0, _points_for=0, _points_against=0, _avg_pf=0, _avg_pa=0, _last_10=None, _record=None, games={})
    team_6 = Team(6, name="Windsor Edge", city="Windsor", province="NS", _games_played=0, _points=0, _points_for=0, _points_against=0, _avg_pf=0, _avg_pa=0, _last_10=None, _record=None, games={})
    # print(team_1)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # team_1.add_game(datetime.datetime(2022, 5, 21), "Halifax Thunder", 89, 92, 2)
    # print(team_1
    #       )
    # print(f"last_10: {team_1.last_10}")

    mwba_league = RoundRobinLeague("MWBA", "Basketball", datetime.datetime(2022, 5, 14), set(), dict(), number_round_robins=2, points_for_win=2)
    date_1 = datetime.datetime(2022, 5, 14)
    date_2 = datetime.datetime(2022, 5, 15)
    date_3 = datetime.datetime(2022, 5, 19)
    mwba_league.add_game(date_1, team_2, team_5, 63, 83)  # Moncton 63  Halifax Thunder 83
    mwba_league.add_game(date_1, team_1, team_6, 68, 71)  # Port City 68  Windsor 71
    mwba_league.add_game(date_1, team_3, team_4, 66, 71)  # Fredericton 66  Halifax Hornets 71
    mwba_league.add_game(date_2, team_1, team_5, 58, 73)  # Port City 58  Halifax Thunder 73
    mwba_league.add_game(date_2, team_2, team_4, 66, 86)  # Moncton 66  Halifax Hornets 86
    mwba_league.add_game(date_2, team_3, team_6, 69, 66)  # Fredericton 69  Windsor 66

    mwba_league.add_game(date_3, team_3, team_1, 60, 55)  # Fredericton 60  Port City 55
    mwba_league.add_game(date_3, team_6, team_5, 62, 66)  # Windsor 62  Halifax Thunder 66

    mwba_league.add_game(date_3, team_2, team_1, 66, 81)  # Moncton 66  Port City 81

    print(f"MWBA: {mwba_league}")
    print(f"MWBA total games: {mwba_league.total_games_rr()}")
    print(f"MWBA total points: {mwba_league.total_points_scored()}")

    tpf = 0
    for team in mwba_league.teams:
        o_record = mwba_league.overall_record(team)
        h_record = mwba_league.home_record(team)
        a_record = mwba_league.away_record(team)
        record = o_record
        record.update(h_record)
        record.update(a_record)
        tpf += record["overall"]["pf"]
        print(dict_print(record, f"Team: {team.name}, Overall record:"))
    print(f"calculated tpf: {tpf}")

    print(f"home record team_1 vs team_6: {mwba_league.home_record(team_1, team_6)}")
    print(f"home record team_6 vs team_1: {mwba_league.home_record(team_6, team_1)}")
    print(f"away record team_1 vs team_6: {mwba_league.away_record(team_1, team_6)}")
    print(f"away record team_6 vs team_1: {mwba_league.away_record(team_6, team_1)}")
    print(f"overall record team_1 vs team_6: {mwba_league.overall_record(team_1, team_6)}")
    print(f"overall record team_6 vs team_1: {mwba_league.overall_record(team_6, team_1)}")
    print(f"overall record team_1: {mwba_league.overall_record(team_1)}")
    print(f"home record team_1: {mwba_league.home_record(team_1)}")

