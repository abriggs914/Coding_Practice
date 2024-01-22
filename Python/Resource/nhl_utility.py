import pandas as pd

import json_utility

metropolitan = {
    "Carolina": {"acr": "CAR"},
    "New Jersey": {"acr": "NJD"},
    "NY Rangers": {"acr": "NYR"},
    "Washington": {"acr": "WSH"},
    "NY Islanders": {"acr": "NYI"},
    "Pittsburgh": {"acr": "PIT"},
    "Philadelphia": {"acr": "PHI"},
    "Columbus": {"acr": "CBJ"}
}

atlantic = {
    "Boston": {"acr": "BOS"},
    "Toronto": {"acr": "TOR"},
    "Tampa Bay": {"acr": "TBL"},
    "Buffalo": {"acr": "BUF"},
    "Florida": {"acr": "FLA"},
    "Detroit": {"acr": "DET"},
    "Ottawa": {"acr": "OTT"},
    "Montreal": {"acr": "MTL"}
}

central = {
    "Winnipeg": {"acr": "WPG"},
    "Dallas": {"acr": "DAL"},
    "Minnesota": {"acr": "MIN"},
    "Colorado": {"acr": "COL"},
    "St. Louis": {"acr": "STL"},
    "Nashville": {"acr": "NSH"},
    "Arizona": {"acr": "ARI"},
    "Chicago": {"acr": "CHI"}
}

pacific = {
    "Vegas": {"acr": "VGK"},
    "Seattle": {"acr": "SEA"},
    "Los Angeles": {"acr": "LAK"},
    "Edmonton": {"acr": "EDM"},
    "Calgary": {"acr": "CGY"},
    "Vancouver": {"acr": "VAN"},
    "San Jose": {"acr": "SJS"},
    "Anaheim": {"acr": "ANA"}
}

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
