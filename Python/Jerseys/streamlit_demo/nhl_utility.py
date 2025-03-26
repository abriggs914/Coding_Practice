import pandas as pd
from typing import Literal
import json_utility

# 2025-01-09 2245
# 2025-03-26 1753


metropolitan = {
    "Carolina": {"acr": "CAR", "mascot": "Hurricanes", "masc_short": "Canes"},
    "New Jersey": {"acr": "NJD", "mascot": "Devils", "masc_short": "Devils"},
    "NY Rangers": {"acr": "NYR", "mascot": "Rangers", "masc_short": "Rangers"},
    "Washington": {"acr": "WSH", "mascot": "Capitals", "masc_short": "Caps"},
    "NY Islanders": {"acr": "NYI", "mascot": "Islanders", "masc_short": "Iles"},
    "Pittsburgh": {"acr": "PIT", "mascot": "Penguins", "masc_short": "Pens"},
    "Philadelphia": {"acr": "PHI", "mascot": "Flyers", "masc_short": "Flyers"},
    "Columbus": {"acr": "CBJ", "mascot": "Blue Jackets", "masc_short": "Jackets"}
}

atlantic = {
    "Boston": {"acr": "BOS", "mascot": "Bruins", "masc_short": "Bruins"},
    "Toronto": {"acr": "TOR", "mascot": "Maple Leafs", "masc_short": "Leafs"},
    "Tampa Bay": {"acr": "TBL", "mascot": "Lightning", "masc_short": "Bolts"},
    "Buffalo": {"acr": "BUF", "mascot": "Sabres", "masc_short": "Sabres"},
    "Florida": {"acr": "FLA", "mascot": "Panthers", "masc_short": "Panthers"},
    "Detroit": {"acr": "DET", "mascot": "Red Wings", "masc_short": "Wings"},
    "Ottawa": {"acr": "OTT", "mascot": "Senators", "masc_short": "Sens"},
    "Montreal": {"acr": "MTL", "mascot": "Canadiens", "masc_short": "Habs"}
}

central = {
    "Winnipeg": {"acr": "WPG", "mascot": "Jets", "masc_short": "Jets"},
    "Dallas": {"acr": "DAL", "mascot": "Stars", "masc_short": "Stars"},
    "Minnesota": {"acr": "MIN", "mascot": "Wild", "masc_short": "Wild"},
    "Colorado": {"acr": "COL", "mascot": "Avalanche", "masc_short": "Avs"},
    "St. Louis": {"acr": "STL", "mascot": "Blues", "masc_short": "Blues"},
    "Nashville": {"acr": "NSH", "mascot": "Predators", "masc_short": "Preds"},
    "Arizona": {"acr": "ARI", "mascot": "Coyotes", "masc_short": "Coyotes"},
    "Chicago": {"acr": "CHI", "mascot": "Blackhawks", "masc_short": "Hawks"}
}

pacific = {
    "Vegas": {"acr": "VGK", "mascot": "Golden Knights", "masc_short": "Knights"},
    "Seattle": {"acr": "SEA", "mascot": "Kraken", "masc_short": "Kraken"},
    "Los Angeles": {"acr": "LAK", "mascot": "Kings", "masc_short": "Kings"},
    "Edmonton": {"acr": "EDM", "mascot": "Oilers", "masc_short": "Oilers"},
    "Calgary": {"acr": "CGY", "mascot": "Flames", "masc_short": "Flames"},
    "Vancouver": {"acr": "VAN", "mascot": "Canucks", "masc_short": "Canucks"},
    "San Jose": {"acr": "SJS", "mascot": "Sharks", "masc_short": "Sharks"},
    "Anaheim": {"acr": "ANA", "mascot": "Ducks", "masc_short": "Ducks"}
}


def reverse_lookup(val, attribute: Literal["team", "acr", "mascot", "masc_short", "div", "conf"]):
    hier = {
        "team": 0,
        "acr": 0,
        "mascot": 0,
        "masc_short": 0,
        "div": 1,
        "conf": 2
    }
    l_val = str(val).lower()
    if l_val in list(league):
        raise ValueError(f"cannot lookup anything specific knowing only conference.")
    if l_val in divisions_list:
        v_hier = hier["div"]
        if attribute == "div":
            # raise ValueError(f"redundant lookup on '{attribute}'.")
            return val
        elif hier[attribute] < v_hier:
            raise ValueError(f"cannot look up '{attribute}' knowing only division.")
        try:
            return [c for c in league if l_val in league[c]][0]
        except IndexError:
            raise ValueError(f"could not use {val=} to lookup {attribute=}.")
    # for c_name, list_divs in [("eastern", eastern), ("western", western)]:
    for c_name, divs_data in league.items():
        for d_name in divs_data:
            teams_data = divisions_list[d_name]
            for t_name, t_data in teams_data.items():
                if t_name.replace(".", "").lower().strip() ==l_val.replace(".", "").lower().strip():
                    if attribute == "conf":
                        return c_name
                    if attribute == "div":
                        return d_name
                    if attribute == "team":
                        return t_name
                    try:
                        return t_data[attribute]
                    except KeyError:
                        raise ValueError(f"cannot find {attribute=} from {val=}.")
                for k in ["acr", "mascot", "masc_short"]:
                    if l_val == str(t_data[k]).lower():
                        if attribute == "conf":
                            return c_name
                        if attribute == "div":
                            return d_name
                        if attribute == "team":
                            return t_name
                        try:
                            # res = t_data[attribute]
                            # if str(res).lower() == l_val:
                            #     raise ValueError(f"redundant lookup on '{attribute}'")
                            return t_data[attribute]
                        except KeyError:
                            raise ValueError(f"cannot find {attribute=} from {val=}.")

    raise ValueError(f"cannot find {attribute=} from {val=}.")

    # for i, conf in enumerate(league):
    #     for j, team_acr in enumerate(league[conf]):
    #         if l_val == team_acr.lower():
    #             # v_hier = hier["acr"]



def team_attribute(team, attribute: Literal["acr", "mascot", "masc_short"] = "acr"):
    if team in metropolitan:
        return metropolitan[team][attribute]
    if team in central:
        return central[team][attribute]
    if team in atlantic:
        return atlantic[team][attribute]
    if team in pacific:
        return pacific[team][attribute]


def name_from_mascot(mascot: str) -> str:
    l_masc = mascot.lower()
    if not l_masc:
        raise ValueError(f"mascot param must not be empty.")
    for div in [atlantic, metropolitan, central, pacific]:
        for k, dat in div.items():
            if l_masc == dat.get("mascot", "").lower():
                return k
    raise ValueError(f"mascot '{mascot}' could not be found")
    # if mascot in :
    #     return metropolitan[team][attribute]
    # if team in central:
    #     return central[team][attribute]
    # if team in atlantic:
    #     return atlantic[team][attribute]
    # if team in pacific:
    #     return pacific[team][attribute]



eastern = [atlantic, metropolitan]
western = [pacific, central]


divisions_list = {
    "metropolitan": metropolitan,
    "central": central,
    "atlantic": atlantic,
    "pacific": pacific
}


league = {
    "eastern": {
        "metropolitan": [metropolitan[t]["acr"] for t in metropolitan],
        "atlantic": [atlantic[t]["acr"] for t in atlantic]
    },
    "western": {
        "central": [central[t]["acr"] for t in central],
        "pacific": [pacific[t]["acr"] for t in pacific]
    }
}



if __name__ == '__main__':
    #
    # excel = r"D:\NHL Jerseys.xlsm"
    # df = pd.read_excel(excel, sheet_name="NHLTeams")
    # # print(df)
    # # print(json_utility.jsonify(df))
    # print(df.to_dict())

    print(f"{reverse_lookup('pacific', 'div')=}")
    print(f"{reverse_lookup('pacific', 'conf')=}")
    print(f"{reverse_lookup('atlantic', 'conf')=}")
    print(f"{reverse_lookup('sharks', 'conf')=}")
    print(f"{reverse_lookup('sharks', 'masc_short')=}")
    print(f"{reverse_lookup('anaheim', 'mascot')=}")
    print(f"{reverse_lookup('ducks', 'mascot')=}")
    print(f"{reverse_lookup('ducks', 'masc_short')=}")
    print(f"{reverse_lookup('ducks', 'team')=}")
    print(f"{reverse_lookup('anaheim', 'team')=}")
    print(f"{reverse_lookup('anaheim', 'conf')=}")