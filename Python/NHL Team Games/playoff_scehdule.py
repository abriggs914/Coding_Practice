from collections import OrderedDict
from enum import Enum

from utility import dict_print, flatten

schedule_template = [
    ["1 {conf_oal} {div_oal} {team_00} \\", 45, "/ {team_00} {div_oal} {conf_oal} 1",
     ["team_00", "div_oal", "conf_oal"]],
    ["8 {conf_oal} {div_oal} {team_07} /", 45, "\\ {team_08} {div_oal} {conf_oal} 8",
     ["team_07", "div_oal", "conf_oal"]]
]

template_1 = """
  N  |  CO  |  DO  |  DT  |  PT  |  TN  |   
{N}|{CO}|{DO}|{DT}|{PT}|{T} \\
                                      = 
{N}|{CO}|{DO}|{DT}|{PT}|{T} /      \\
                       = TOR
{N}|{CO}|{DO}|{DT}|{PT}|{T} \      /      \\
                = FLA         \\
{N}|{CO}|{DO}|{DT}|{PT}|{T} /               \
                                = TOR vs. VGK =
{N}|{CO}|{DO}|{DT}|{PT}|{T} \               /
                = WSH         /
{N}|{CO}|{DO}|{DT}|{PT}|{T} /      \      /
                       = CAR
{N}|{CO}|{DO}|{DT}|{PT}|{T} \      /
                = CAR
{N}|{CO}|{DO}|{DT}|{PT}|{T} /
""".strip()

data_1 = eval("""
[['TOR', 'atlantic', 'eastern', 'A__E_0', 0, 107, 0],
['CAR', 'metropolitan', 'eastern', 'M__E_0', 0, 106, 7],
['WSH', 'metropolitan', 'eastern', 'M__E_1', 1, 102, 4],
['TBL', 'atlantic', 'eastern', 'A__E_1', 1, 98, 2],
['PHI', 'metropolitan', 'eastern', 'M__E_2', 2, 98, 5],
['FLA', 'atlantic', 'eastern', 'A__E_2', 2, 98, 3],
['OTT', 'atlantic', 'eastern', 'WC_E_0', 6, 97, 6],
['MTL', 'atlantic', 'eastern', 'WC_E_1', 7, 97, 1],
['EDM', 'pacific', 'western', 'P__W_0', 0, 107, 0],
['NSH', 'central', 'western', 'C__W_0', 0, 100, 7],
['ARI', 'central', 'western', 'C__W_1', 1, 98, 4],
['SEA', 'pacific', 'western', 'P__W_1', 1, 98, 2],
['ANA', 'pacific', 'western', 'P__W_2', 2, 98, 3],
['WPG', 'central', 'western', 'C__W_2', 2, 93, 5],
['MIN', 'central', 'western', 'WC_W_0', 6, 93, 6],
['VAN', 'pacific', 'western', 'WC_W_1', 7, 93, 1]]
""".strip())

data = eval("""
[['TOR', 'atlantic', 'eastern', 'A__E_0', 0, 107, 0],
['CAR', 'metropolitan', 'eastern', 'M__E_0', 0, 106, 7],
['WSH', 'metropolitan', 'eastern', 'M__E_1', 1, 102, 4],
['TBL', 'atlantic', 'eastern', 'A__E_1', 1, 98, 2],
['PHI', 'metropolitan', 'eastern', 'M__E_2', 2, 98, 5],
['FLA', 'atlantic', 'eastern', 'A__E_2', 2, 98, 3],
['OTT', 'atlantic', 'eastern', 'WC_E_0', 6, 97, 6],
['MTL', 'atlantic', 'eastern', 'WC_E_1', 7, 97, 1],
['EDM', 'pacific', 'western', 'P__W_0', 0, 107, 0],
['NSH', 'central', 'western', 'C__W_0', 0, 100, 7],
['ARI', 'central', 'western', 'C__W_1', 1, 98, 4],
['SEA', 'pacific', 'western', 'P__W_1', 1, 98, 2],
['ANA', 'pacific', 'western', 'P__W_2', 2, 98, 3],
['WPG', 'central', 'western', 'C__W_2', 2, 93, 5],
['MIN', 'central', 'western', 'WC_W_0', 6, 93, 6],
['VAN', 'pacific', 'western', 'WC_W_1', 7, 93, 1]]
""".strip())


def draw_shedule(standings_in, half=None):
    team_list_data = OrderedDict()
    team_data = {}
    for i in range(len(standings_in)):
        print(f"{i=}")
        team = standings_in[i][0]
        team_list_data.update({
            f"team_{('00' + str(i))[-2:]}": team
        })
        team_data[team] = {
            'div_oal': standings_in[i][6],
            'conf_oal': i % 8
        }

    print(team_list_data)
    print(team_data)
    print(f"{team_list_data['team_00']=}")

    if not isinstance(half, str):
        half = ""
    result = ""
    for i, template_line in enumerate(schedule_template):
        left, n_spaces, right, keys = template_line
        fmts = dict(zip(keys, [v for k, v in team_list_data.items() if k in keys]))
        team = list(fmts.values())[0]
        print(f"A\n{left=}\n{n_spaces=}\n{right=}\n{keys=}\n{fmts=}")
        fmts.update({k: str(team_data[team][k]).center(3) for k in keys if k in team_data[team]})
        print(f"B\n{left=}\n{n_spaces=}\n{right=}\n{keys=}\n{fmts=}")
        left = left.format(**fmts)
        if half.lower() == "eastern":
            result += left
        # if half.lower() == "western":
        #     left = left.format(**fmts)
        #     print()
        # else:
        #     print()
        result += "\n"
    return result


def sched():
    header_l = "  N  |  CO |  DO |  DT  |  PT |  TN  "
    team_line_l = "{N}|{CO}|{DO}|{DT}|{PT}|{T} "
    header_r = "|".join(header_l.split("|")[::-1])
    team_line_r = "|".join(team_line_l.split("|")[::-1])
    results = ""
    lm = " " * (len(header_l) + 1)
    ms = " " * 53
    both_brackets = len(data_1) > 8
    times = 2 if both_brackets else 1
    data_1.sort(key=lambda tup: (tup[2], tup[-1]))
    ti = 0
    for i in range(1 + ((1 + (times % 2)) * 8)):
        if i == 0:
            results += header_l
            if both_brackets:
                results += ms + header_r
            results += "\n"

        else:

            minus = 0
            for j in range(times):
                tii = ti + (j * 8)
                print(f"ld={len(data_1)}, {i=}, {j=}, {ti=}, {tii=}")
                co_ = str(data_1[tii][4]).center(5)
                do_ = str(data_1[tii][-1]).center(5)
                dt_ = str(data_1[tii][3]).center(6)
                pt_ = str(data_1[tii][5]).center(5)
                tn_ = str(data_1[tii][0]).center(5)
                n_ = str(data_1[tii][6] + 1).center(5)
                if (i - 1) % 2 == 0:
                    suf = "\\" if j == 0 else "/"
                else:
                    suf = "/" if j == 0 else "\\"
                if j == 0:
                    results += team_line_l.format(CO=co_, DO=do_, DT=dt_, PT=pt_, T=tn_, N=n_) + f"{suf}"
                    if ti % 4 == 1:
                        results += f"{' ' * 6}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7
                    elif ti % 4 == 2:
                        results += f"{' ' * 6}/"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7

                    if ti == 2:
                        results += f"{' ' * 7}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}/"
                            minus += 22
                    elif ti == 3:
                        results += f"{' ' * 16}\\"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}/"
                            minus += 18
                    elif ti == 4:
                        results += f"{' ' * 16}/"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}\\"
                            minus += 18
                    elif ti == 5:
                        results += f"{' ' * 7}/"
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}\\"
                            minus += 22

                    if ti == 1:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}/"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                    elif ti == 2:
                        if both_brackets:
                            results += f"{' ' * 7}\\"
                            minus += 8
                    elif ti == 5:
                        if both_brackets:
                            results += f"{' ' * 7}/"
                            minus += 8
                    elif ti == 6:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}\\"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                else:
                    results += f"{ms[:len(ms) - (2 + minus)]}{suf}" + team_line_r.format(CO=co_, DO=do_, DT=dt_, PT=pt_,
                                                                                         T=tn_, N=n_)
                    minus = 0

            if i == 4:
                results += f"\n{lm}{ms[:(len(ms) // 2) - 8]}= ___ vs. ___ ="
            else:
                results += f"\n{lm}"
            if ti % 2 == 0:
                if ti == 0 or ti == 6:
                    results += f"= ___{ms[:(len(ms) // 2) + 15]}___ ="
                else:
                    if ti == 2:
                        results += f"= ___{' ' * 10}\\{ms[:(len(ms) // 4) + 6]}/{' ' * 10}___ ="
                    else:
                        results += f"= ___{' ' * 10}/{ms[:(len(ms) // 4) + 6]}\\{' ' * 10}___ ="
            elif ti % 4 == 1:
                results += f"{' ' * 8}= ___{ms[:(len(ms) // 4) + 12]}___ ="
            results += f"\n"
            ti += 1

    return results


def sched():
    header_l = "  N  |  CO |  DO |  DT  |  PT |  TN  "
    team_line_l = "{N}|{CO}|{DO}|{DT}|{PT}|{T} "
    header_r = "|".join(header_l.split("|")[::-1])
    team_line_r = "|".join(team_line_l.split("|")[::-1])
    results = ""
    lm = " " * (len(header_l) + 1)
    ms = " " * 53
    both_brackets = len(data_1) > 8
    times = 2 if both_brackets else 1
    data_1.sort(key=lambda tup: (tup[2], tup[-1]))
    ti = 0
    for i in range(1 + ((1 + (times % 2)) * 8)):
        if i == 0:
            results += header_l
            if both_brackets:
                results += ms + header_r
            results += "\n"

        else:

            minus = 0
            for j in range(times):
                tii = ti + (j * 8)
                print(f"ld={len(data_1)}, {i=}, {j=}, {ti=}, {tii=}")
                co_ = str(data_1[tii][4]).center(5)
                do_ = str(data_1[tii][-1]).center(5)
                dt_ = str(data_1[tii][3]).center(6)
                pt_ = str(data_1[tii][5]).center(5)
                tn_ = str(data_1[tii][0]).center(5)
                n_ = str(data_1[tii][6] + 1).center(5)
                if (i - 1) % 2 == 0:
                    suf = "\\" if j == 0 else "/"
                else:
                    suf = "/" if j == 0 else "\\"
                if j == 0:
                    results += team_line_l.format(CO=co_, DO=do_, DT=dt_, PT=pt_, T=tn_, N=n_) + f"{suf}"
                    if ti % 4 == 1:
                        results += f"{' ' * 6}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7
                    elif ti % 4 == 2:
                        results += f"{' ' * 6}/"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7

                    if ti == 2:
                        results += f"{' ' * 7}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}/"
                            minus += 22
                    elif ti == 3:
                        results += f"{' ' * 16}\\"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}/"
                            minus += 18
                    elif ti == 4:
                        results += f"{' ' * 16}/"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}\\"
                            minus += 18
                    elif ti == 5:
                        results += f"{' ' * 7}/"
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}\\"
                            minus += 22

                    if ti == 1:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}/"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                    elif ti == 2:
                        if both_brackets:
                            results += f"{' ' * 7}\\"
                            minus += 8
                    elif ti == 5:
                        if both_brackets:
                            results += f"{' ' * 7}/"
                            minus += 8
                    elif ti == 6:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}\\"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                else:
                    results += f"{ms[:len(ms) - (2 + minus)]}{suf}" + team_line_r.format(CO=co_, DO=do_, DT=dt_, PT=pt_,
                                                                                         T=tn_, N=n_)
                    minus = 0

            if i == 4:
                results += f"\n{lm}{ms[:(len(ms) // 2) - 8]}= ___ vs. ___ ="
            else:
                results += f"\n{lm}"
            if ti % 2 == 0:
                if ti == 0 or ti == 6:
                    results += f"= ___{ms[:(len(ms) // 2) + 15]}___ ="
                else:
                    if ti == 2:
                        results += f"= ___{' ' * 10}\\{ms[:(len(ms) // 4) + 6]}/{' ' * 10}___ ="
                    else:
                        results += f"= ___{' ' * 10}/{ms[:(len(ms) // 4) + 6]}\\{' ' * 10}___ ="
            elif ti % 4 == 1:
                results += f"{' ' * 8}= ___{ms[:(len(ms) // 4) + 12]}___ ="
            results += f"\n"
            ti += 1

    return results


class Conference(Enum):
    EASTERN: str = "eastern"
    WESTERN: str = "western"


class Division(Enum):
    ATLANTIC: tuple[Conference, str] = (Conference.EASTERN, "atlantic")
    METROPOLITAN: tuple[Conference, str] = (Conference.EASTERN, "metropolitan")
    CENTRAL: tuple[Conference, str] = (Conference.WESTERN, "central")
    PACIFIC: tuple[Conference, str] = (Conference.WESTERN, "pacific")


class Team:
    def __init__(self, team_name, acronym, city, mascot, division, wikipedia_link):
        self.team_name = team_name
        self.acronym = acronym
        self.city_full = city
        self.city, self.province_state, self.country = self.city_full.split(",")
        self.mascot = mascot
        self.division_full = division.value
        self.conference, self.division = self.division_full
        self.conference = self.conference.value
        self.wikipedia_link = wikipedia_link

    def __repr__(self):
        return f"{self.acronym}"


class Season:
    def __init__(self, league, year):
        self.league = league
        self.year = year

        self.teams_list = self.league.history[self.year]["teams"]


class League:
    def __init__(self, league_name):
        self.league_name = league_name
        self.history = {}

    def add_team(self, year: int, team: Team):
        if year not in self.history:
            self.history[year] = {"season": None, "teams": [], "is_complete": False}
        if team not in self.history[year]["teams"]:
            self.history[year]["teams"].append(team)

    def start_season(self, year: int):
        year_title = f"{str(year)[-2:]} - {str(year + 1)[-2:]}"
        if year not in self.history:
            raise AttributeError(f"Error, year={year} has not been initialized in this league yet. Please add some teams first.")
        if self.history[year]["is_complete"]:
            raise ValueError(f"Error, the season {year_title} is already complete, cannot re-start.")
        if len(self.history[year]["teams"]) < 2:
            raise ValueError(f"Error, cannot begin {year_title} season without at least 2 teams.")
        season = Season(self, year)


NHL_TEAMS_LIST_2023 = [Team(*vals) for vals in [
        ("Carolina Hurricanes", "CAR", "Raleigh, North Carolina, USA", "Canes", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Carolina_Hurricanes"),
        ("New Jersey Devils", "NJD", "Newark, New Jersey, USA", "Devils", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/New_Jersey_Devils"),
        ("New York Rangers", "NYR", "Manhattan, New York, USA", "Rangers", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/New_York_Rangers"),
        ("Washington Capitals", "WSH", "Washington D.C., D.C., USA", "Caps", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Washington_Capitals"),
        ("New York Islanders", "NYI", "Elmont, New York, USA", "Isles", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/New_York_Islanders"),
        ("Pittsburgh Penguins", "PIT", "Pittsburgh, Pennsylvania, USA", "Pens", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Pittsburgh_Penguins"),
        ("Philadelphia Flyers", "PHI", "Philadelphia, Pennsylvania, USA", "Flyers", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Philadelphia_Flyers"),
        ("Columbus Blue Jackets", "CBJ", "Columbus, Ohio, USA", "Blue Jackets", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Columbus_Blue_Jackets"),

        ("Boston Bruins", "BOS", "Boston, Massachusetts, USA", "Bruins", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Boston_Bruins"),
        ("Toronto Maple Leafs", "TOR", "Toronto, Ontario, Canada", "Leafs", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Toronto_Maple_Leafs"),
        ("Tampa Bay Lighting", "TBL", "Tampa, Florida, USA", "Bolts", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Tampa_Bay_Lightning"),
        ("Buffalo Sabres", "BUF", "Buffalo, New York, USA", "Sabres", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Buffalo_Sabres"),
        ("Florida Panthers", "FLA", "Sunrise, Florida, USA", "Panthers", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Florida_Panthers"),
        ("Detroit Red Wings", "DET", "Detroit, Michigan, USA", "Red Wings", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Detroit_Red_Wings"),
        ("Ottawa Senators", "OTT", "Ottawa, Ontario, Canada", "Sens", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Ottawa_Senators"),
        ("Montreal Canadiens", "MTL", "Montreal, Quebec, Canada", "Habs", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Montreal_Canadiens"),

        ("Winnipeg Jets", "WPG", "Winnipeg, Manitoba, Canada", "Jets", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Winnipeg_Jets"),
        ("Dallas Stars", "DAL", "Dallas, Texas, USA", "Stars", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Dallas_Stars"),
        ("Minnesota Wild", "MIN", "Saint Paul, Minnesota, USA", "WILD", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Minnesota_Wild"),
        ("Colorado Avalanche", "COL", "Denver, Colorado, USA", "Avs", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Colorado_Avalanche"),
        ("St. Louis Blues", "STL", "St. Louis, Missouri, USA", "Blues", Division.CENTRAL, r"https://en.wikipedia.org/wiki/St._Louis_Blues"),
        ("Nashville Predators", "NSH", "Nashville, Tennessee, USA", "Preds", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Nashville_Predators"),
        ("Arizona Coyotes", "ARI", "Phoenix, Arizona, USA", "Yotes", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Arizona_Coyotes"),
        ("Chicago Blackhawks", "CHI", "Chicago, Illinois, USA", "Hawks", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Chicago_Blackhawks"),

        ("Las Vegas Golden Knights", "VGK", "Las Vegas, Nevada, USA", "Knights", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Vegas_Golden_Knights"),
        ("Seattle Kraken", "SEA", "Seattle, Washington, USA", "Kraken", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Seattle_Kraken"),
        ("Los Angeles Kings", "LAK", "Los Angeles, California, USA", "Kings", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Los_Angeles_Kings"),
        ("Edmonton Oilers", "EDM", "Edmonton, Alberta, Canada", "Oilers", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Edmonton_Oilers"),
        ("Calgary Flames", "CGY", "Calgary, Alberta, Canada", "Flames", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Calgary_Flames"),
        ("Vancouver Canucks", "VAN", "Vancouver, British-Columbia, Canada", "Canucks", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Vancouver_Canucks"),
        ("San Jose Sharks", "SJS", "San Jose, California, USA", "Sharks", Division.PACIFIC, r"https://en.wikipedia.org/wiki/San_Jose_Sharks"),
        ("Anaheim Ducks", "ANA", "Anaheim, California, USA", "Ducks", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Anaheim_Ducks")
]]

print(NHL_TEAMS_LIST_2023)

nhl = League("NHL")



if __name__ == '__main__':
    # print(draw_shedule(data, half="eastern"))
    data_1.sort(key=lambda tup: (tup[2], tup[-1]))
    lines = template_1.split("\n")
    result = lines[0] + "\n"
    for i in range(1, len(lines)):
        co_ = str(data_1[i][4]).center(5)
        do_ = str(data_1[i][-1]).center(5)
        dt_ = str(data_1[i][3]).center(5)
        pt_ = str(data_1[i][5]).center(5)
        tn_ = str(data_1[i][0]).center(5)
        n_ = str(data_1[i][6] + 1).center(5)
        result += lines[i].format(CO=co_, DO=do_, DT=dt_, PT=pt_, T=tn_, N=n_) + "\n"
    print(template_1)
    print(result)

    print("\n\n\tSCHED\n\n\n")
    print(sched())
