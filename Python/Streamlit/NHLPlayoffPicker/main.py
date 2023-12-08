import os.path
from typing import Literal

from PIL import Image
import streamlit as st


root_image_logos = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"


metropolitan = {
    "Carolina": {"acr": "CAR", "mascot": "Hurricanes", "masc_short": "Hurricanes"},
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


# league = {
#     "eastern": {
#         "metropolitan": [metropolitan[t]["acr"] for t in metropolitan],
#         "atlantic": [atlantic[t]["acr"] for t in atlantic]
#     },
#     "western": {
#         "central": [central[t]["acr"] for t in central],
#         "pacific": [pacific[t]["acr"] for t in pacific]
#     }
# }
league = {
    "eastern": {
        "metropolitan": metropolitan,
        "atlantic": atlantic
    },
    "western": {
        "central": central,
        "pacific": pacific
    }
}


@st.cache_data
def load_image_logos(base_width=100, base_height=100):
    for conf, conf_data in league.items():
        for div, div_lst in conf_data.items():
            for team, team_data in div_lst.items():
                masc = team_data["mascot"].replace(" ", "_").lower()
                tn = team.replace(' ', '_').replace(".", "").lower()
                if (mn := f"_{masc}") in tn:
                    tn = tn.replace(mn, "")
                if (mn := f"ny") == tn:
                    tn = tn.replace(mn, "new_york")
                if (mn := f"columbus") == tn:
                    # typo that cant be fixed without modifying the access program.
                    tn = tn.replace(mn, "colombus")
                # print(f"{tn=}, {masc=}", end=", ")
                path_logo = f"{root_image_logos}\\logo_{tn}_{masc}.png"
                if masc == "jets":
                    path_logo = "logo_winnipeg_jets.png"
                image = None
                # print(f"{path_logo}")
                if os.path.exists(path_logo):
                    # with open(path_logo, "rb") as f:
                    #     image = f.read()
                    # image = path_logo

                    # maintains aspect ratio of width
                    # image = Image.open(path_logo)
                    # wpercent = (base_width / float(image.size[0]))
                    # hsize = int((float(image.size[1]) * float(wpercent)))
                    # image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)

                    image = Image.open(path_logo)
                    image = image.resize((base_width, base_height))
                else:
                    print(f"FAILURE {path_logo=}")
                league[conf][div][team].update({"logo": image})

        st.session_state["loaded_images"] = True


if __name__ == '__main__':

    if (ss_k := "loaded_images") not in st.session_state:
        st.session_state[ss_k] = False

    if not st.session_state[ss_k]:
        load_image_logos()

    multiselects = {}
    for conf, conf_data in league.items():
        cn = conf.title()
        # st.write(f"{cn}")
        # st.divider()
        for div, div_data in conf_data.items():
            dn = div.title()
            # st.write(f"{dn}")
            # st.divider()
            # for team, team_data in div_data.items():
                # tn = team.title()
                # st.write(f"{tn}")
            multiselects.update({
                div: st.multiselect(
                    label=div,
                    # options=list(div_data.keys()),
                    # options=[team_attribute(t) for t in div_data.keys()],
                    options=[team_attribute(t, "mascot") for t in div_data.keys()],
                    max_selections=3,
                    placeholder="Top 3 Teams"
            )})

    # for div, ms in multiselects.items():
    #     st.write(ms)

    pt_cols = st.columns(7)
    pt_c0, pt_c1, pt_c2, pt_c3, pt_c4, pt_c5, pt_c6 = pt_cols
    cells = {}

    for i in range(8):
        cells[i] = {}
        for j, col in enumerate(pt_cols):
            cells[i][j] = col.container()
            cells[i][j].write(" ")
        # for div, div_data in multiselects.items():
        #     multiselects[div].update({i: col.container()})

    # important_cells
    important_cells = {
        # round 1
        # west
        "P__W_0": cells[0][0],
        "WC_WX0": cells[1][0],
        "P__W_1": cells[2][0],
        "P__W_2": cells[3][0],
        "C__W_2": cells[4][0],
        "C__W_1": cells[5][0],
        "WC_WX1": cells[6][0],
        "C__W_0": cells[7][0],
        # east
        "A__E_0": cells[0][6],
        "WC_EX0": cells[1][6],
        "A__E_1": cells[2][6],
        "A__E_2": cells[3][6],
        "M__E_2": cells[4][6],
        "M__E_1": cells[5][6],
        "WC_EX1": cells[6][6],
        "M__E_0": cells[7][6],

        # division finals
        # west
        "PF_W_0": cells[2][1],
        "PF_W_1": cells[3][1],
        "CF_W_1": cells[4][1],
        "CF_W_0": cells[5][1],
        # east
        "AF_W_0": cells[2][5],
        "AF_W_1": cells[3][5],
        "MF_W_1": cells[4][5],
        "MF_W_0": cells[5][5],

        # conference finals
        # west
        "WF_W_0": cells[3][2],
        "WF_W_1": cells[4][2],
        # east
        "EF_E_0": cells[3][4],
        "EF_E_1": cells[4][4],

        # stanley cup final
        "F__W_0": cells[3][4],
        "F__E_1": cells[4][4]
    }

    ms_pacific = multiselects["pacific"]
    ms_central = multiselects["central"]
    ms_atlantic = multiselects["atlantic"]
    ms_metropolitan = multiselects["metropolitan"]

    if ms_pacific:
        entered = [t for t in ms_pacific] + [None, None, None, None]
        a, b, c, *r = entered
        if a:
            important_cells["P__W_0"].write(a)
        if b:
            important_cells["P__W_1"].write(b)
        if c:
            important_cells["P__W_2"].write(c)

    if ms_central:
        entered = [t for t in ms_central] + [None, None, None, None]
        a, b, c, *r = entered
        if a:
            important_cells["C__W_0"].write(a)
        if b:
            important_cells["C__W_1"].write(b)
        if c:
            important_cells["C__W_2"].write(c)

    if ms_atlantic:
        entered = [t for t in ms_atlantic] + [None, None, None, None]
        a, b, c, *r = entered
        if a:
            important_cells["A__E_0"].write(a)
        if b:
            important_cells["A__E_1"].write(b)
        if c:
            important_cells["A__E_2"].write(c)

    if ms_metropolitan:
        entered = [t for t in ms_metropolitan] + [None, None, None, None]
        a, b, c, *r = entered
        if a:
            important_cells["M__E_0"].write(a)
        if b:
            important_cells["M__E_1"].write(b)
        if c:
            important_cells["M__E_2"].write(c)
        # "P__W_1",
        # "P__W_2"

    # for div, ms in multiselects.items():
    #     if ms:
    #         for team in ms:

