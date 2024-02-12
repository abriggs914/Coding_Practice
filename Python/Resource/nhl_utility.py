import pandas as pd
from typing import Literal
import json_utility

# metropolitan = {
#     "Carolina": {"acr": "CAR"},
#     "New Jersey": {"acr": "NJD"},
#     "NY Rangers": {"acr": "NYR"},
#     "Washington": {"acr": "WSH"},
#     "NY Islanders": {"acr": "NYI"},
#     "Pittsburgh": {"acr": "PIT"},
#     "Philadelphia": {"acr": "PHI"},
#     "Columbus": {"acr": "CBJ"}
# }
#
# atlantic = {
#     "Boston": {"acr": "BOS"},
#     "Toronto": {"acr": "TOR"},
#     "Tampa Bay": {"acr": "TBL"},
#     "Buffalo": {"acr": "BUF"},
#     "Florida": {"acr": "FLA"},
#     "Detroit": {"acr": "DET"},
#     "Ottawa": {"acr": "OTT"},
#     "Montreal": {"acr": "MTL"}
# }
#
# central = {
#     "Winnipeg": {"acr": "WPG"},
#     "Dallas": {"acr": "DAL"},
#     "Minnesota": {"acr": "MIN"},
#     "Colorado": {"acr": "COL"},
#     "St. Louis": {"acr": "STL"},
#     "Nashville": {"acr": "NSH"},
#     "Arizona": {"acr": "ARI"},
#     "Chicago": {"acr": "CHI"}
# }
#
# pacific = {
#     "Vegas": {"acr": "VGK"},
#     "Seattle": {"acr": "SEA"},
#     "Los Angeles": {"acr": "LAK"},
#     "Edmonton": {"acr": "EDM"},
#     "Calgary": {"acr": "CGY"},
#     "Vancouver": {"acr": "VAN"},
#     "San Jose": {"acr": "SJS"},
#     "Anaheim": {"acr": "ANA"}
# }

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
        for k, dat in div.items( ):
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



divisions_list = ["metropolitan", "central", "atlantic", "pacific"]


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

    excel = r"D:\NHL Jerseys.xlsm"
    df = pd.read_excel(excel, sheet_name="NHLTeams")
    # print(df)
    # print(json_utility.jsonify(df))
    print(df.to_dict())
