import os.path
from typing import Literal

from PIL import Image
import streamlit as st


root_image_logos = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"


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
    "western": {
        "pacific": pacific,
        "central": central
    },
    "eastern": {
        "atlantic": atlantic,
        "metropolitan": metropolitan
    }
}


@st.cache_data
def load_image_logos(base_width=100, base_height=100):
    global root_image_logos, league

    print(f"load_image_logos")
    if os.environ["COMPUTERNAME"] == "CADSTATION18":
        print(f"NEW LOGO")
        root_image_logos = r"C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Python\Hockey pool\Images"
    else:
        print(f"OLD LOGO")

    print(f"{league=}")

    for conf, conf_data in league.items():
        print(f"{conf=}")
        for div, div_lst in conf_data.items():
            print(f"{div=}")
            for team, team_data in div_lst.items():
                print(f"{team=}")
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


def change_pts_slider(k_, ck_, ss_, exp_):
    ss_val = st.session_state[ss_]
    c_val = sliders[k_][ck_]
    print(f"CPS {k_=}, {ck_=}, {sliders[k_][ck_]=}, ss={ss_val}, {c_val=}")

    ck_let = ck_[-1]
    left = ["a", "b"] if ck_let == "c" else (("b", "c") if ck_let == "a" else ("a", "c"))
    left = [f"choice_pts_{let}" for let in left]
    # others = [st.session_state[k] for k in left]
    others = [sliders[k_][k] for k in left]

    print(f"{left=}, {others=}")

    if ck_let == "a":
        print(f"-PA")
        # should be the greatest value
        if c_val < max(others):
            print(f"-PB")
            exp_.warning(f"Not the highest pts value in the division.")

    # st.session_state.set_option(ck_, )


if __name__ == '__main__':

    if (ss_k := "loaded_images") not in st.session_state:
        st.session_state[ss_k] = False
    if not st.session_state[ss_k]:
        load_image_logos()

    if (ss_k := "choice_show_place") not in st.session_state:
        st.session_state[ss_k] = False

    lst_divs = list(league["western"]) + list(league["eastern"])
    print(f"{lst_divs=}")
    expanders = {div: st.expander(div.title()) for div in lst_divs}

    multiselects = {}
    left_over = {}
    # left_central = []
    # left_pacific = []
    # left_atlantic = []
    # left_metropolitan = []
    for conf, conf_data in league.items():
        cn = conf.title()
        # st.write(f"{cn}")
        # st.divider()
        for div, div_data in conf_data.items():
            exp = expanders[div]
            dn = div.title()
            # st.write(f"{dn}")
            # st.divider()
            # for team, team_data in div_data.items():
                # tn = team.title()
                # st.write(f"{tn}")
            # options=list(div_data.keys()),
            # options=[team_attribute(t) for t in div_data.keys()],
            # options = [team_attribute(t, "mascot") for t in div_data.keys()]
            options = [team_attribute(t, "masc_short") for t in div_data.keys()]
            multiselects.update({
                div: exp.multiselect(
                    label=div,
                    options=options,
                    max_selections=3,
                    placeholder="Top 3 Teams",
                    label_visibility="hidden"
            )})
            # print(f"{options=}")
            left_over[div] = {"og": [o for o in options], "w": []}

    ms_pacific = multiselects["pacific"]
    ms_central = multiselects["central"]
    ms_atlantic = multiselects["atlantic"]
    ms_metropolitan = multiselects["metropolitan"]

    st.divider()

    # for div, ms in multiselects.items():
    #     st.write(ms)

    # pt_cols = st.columns(7)
    # pt_c0, pt_c1, pt_c2, pt_c3, pt_c4, pt_c5, pt_c6 = pt_cols
    # cells = {}
    # 
    # for i in range(8):
    #     cells[i] = {}
    #     for j, col in enumerate(pt_cols):
    #         cells[i][j] = col.container()
    #         cells[i][j].write(" ")
    #     # for div, div_data in multiselects.items():
    #     #     multiselects[div].update({i: col.container()})
    # 
    # # important_cells
    # important_cells = {
    #     # round 1
    #     # west
    #     "P__W_0": cells[0][0],
    #     "WC_WX0": cells[1][0],
    #     "P__W_1": cells[2][0],
    #     "P__W_2": cells[3][0],
    #     "C__W_2": cells[4][0],
    #     "C__W_1": cells[5][0],
    #     "WC_WX1": cells[6][0],
    #     "C__W_0": cells[7][0],
    #     # east
    #     "A__E_0": cells[0][6],
    #     "WC_EX0": cells[1][6],
    #     "A__E_1": cells[2][6],
    #     "A__E_2": cells[3][6],
    #     "M__E_2": cells[4][6],
    #     "M__E_1": cells[5][6],
    #     "WC_EX1": cells[6][6],
    #     "M__E_0": cells[7][6],
    # 
    #     # division finals
    #     # west
    #     "PF_W_0": cells[2][1],
    #     "PF_W_1": cells[3][1],
    #     "CF_W_1": cells[4][1],
    #     "CF_W_0": cells[5][1],
    #     # east
    #     "AF_W_0": cells[2][5],
    #     "AF_W_1": cells[3][5],
    #     "MF_W_1": cells[4][5],
    #     "MF_W_0": cells[5][5],
    # 
    #     # conference finals
    #     # west
    #     "WF_W_0": cells[3][2],
    #     "WF_W_1": cells[4][2],
    #     # east
    #     "EF_E_0": cells[3][4],
    #     "EF_E_1": cells[4][4],
    # 
    #     # stanley cup final
    #     "F__W_0": cells[3][4],
    #     "F__E_1": cells[4][4]
    # }
    # 
    # ms_pacific = multiselects["pacific"]
    # ms_central = multiselects["central"]
    # ms_atlantic = multiselects["atlantic"]
    # ms_metropolitan = multiselects["metropolitan"]
    #
    # if ms_pacific:
    #     entered = [t for t in ms_pacific] + [None, None, None, None]
    #     a, b, c, *r = entered
    #     if a:
    #         important_cells["P__W_0"].write(a)
    #     if b:
    #         important_cells["P__W_1"].write(b)
    #     if c:
    #         important_cells["P__W_2"].write(c)
    #
    # if ms_central:
    #     entered = [t for t in ms_central] + [None, None, None, None]
    #     a, b, c, *r = entered
    #     if a:
    #         important_cells["C__W_0"].write(a)
    #     if b:
    #         important_cells["C__W_1"].write(b)
    #     if c:
    #         important_cells["C__W_2"].write(c)
    #
    # if ms_atlantic:
    #     entered = [t for t in ms_atlantic] + [None, None, None, None]
    #     a, b, c, *r = entered
    #     if a:
    #         important_cells["A__E_0"].write(a)
    #     if b:
    #         important_cells["A__E_1"].write(b)
    #     if c:
    #         important_cells["A__E_2"].write(c)
    #
    # if ms_metropolitan:
    #     entered = [t for t in ms_metropolitan] + [None, None, None, None]
    #     a, b, c, *r = entered
    #     if a:
    #         important_cells["M__E_0"].write(a)
    #     if b:
    #         important_cells["M__E_1"].write(b)
    #     if c:
    #         important_cells["M__E_2"].write(c)
    #     # "P__W_1",
    #     # "P__W_2"
    #
    # c1 = st.container(border=True)
    # c1.write("HEY")

    # for div, ms in multiselects.items():
    #     if ms:
    #         for team in ms:

    # important_cells
    important_cells = {
        # round 1
        # west
        "P__W_0": (0, 1),
        "WC_WX0": (1, 1),
        "P__W_1": (2, 1),
        "P__W_2": (3, 1),
        "C__W_2": (4, 1),
        "C__W_1": (5, 1),
        "WC_WX1": (6, 1),
        "C__W_0": (7, 1),
        # east
        "A__E_0": (0, 7),
        "WC_EX0": (1, 7),
        "A__E_1": (2, 7),
        "A__E_2": (3, 7),
        "M__E_2": (4, 7),
        "M__E_1": (5, 7),
        "WC_EX1": (6, 7),
        "M__E_0": (7, 7),

        # division finals
        # west
        "PF_W_0": (2, 2),
        "PF_W_1": (3, 2),
        "CF_W_1": (4, 2),
        "CF_W_0": (5, 2),
        # east
        "AF_W_0": (2, 6),
        "AF_W_1": (3, 6),
        "MF_W_1": (4, 6),
        "MF_W_0": (5, 6),

        # conference finals
        # west
        "WF_W_0": (3, 3),
        "WF_W_1": (4, 3),
        # east
        "EF_E_0": (3, 5),
        "EF_E_1": (4, 5),

        # stanley cup final
        "F__W_0": (3, 5),
        "F__E_1": (4, 5)
    }

    placements = {
        "Pacific   1": (0, 0),
        "WC WEST   1": (1, 0),
        "Pacific   2": (2, 0),
        "Pacific   3": (3, 0),
        "Central   3": (4, 0),
        "Central   2": (5, 0),
        "WC WEST   2": (6, 0),
        "Central   1": (7, 0),

        "Atlantic  1": (0, 10),
        "WC EAST   1": (1, 10),
        "Atlantic  2": (2, 10),
        "Atlantic  3": (3, 10),
        "Metro     3": (4, 10),
        "Metro     2": (5, 10),
        "WC EAST   2": (6, 10),
        "Metro     1": (7, 10)
    }
    inv_placements = {v: k for k, v in placements.items()}

    if showing_placements := st.session_state["choice_show_place"]:
        for k, place in important_cells.items():
            i, j = place
            important_cells[k] = (i, j + 1)

        for i in range(8):
            for j in range(9):
                div_id = f"({i}, {j})"
                div_id_t = eval(div_id)
                if div_id_t in inv_placements:
                    k = inv_placements[div_id_t]
                    important_cells[k] = div_id_t

    inv_cells = {v: k for k, v in important_cells.items()}
    vals_cells = {v: "" for v in important_cells.values()}
    inv_vals_cells = {k: v for k, v in important_cells.items()}

    min_pts = 0
    def_pts_val = 97
    max_pts = 82 * 2

    sliders = {}

    slider_keys = {div: [f"{div[0].upper()}__{'W' if div in ['pacific', 'central'] else 'E'}_{i}" for i in range(3)] for div in lst_divs}
    for k, ck in slider_keys.items():
        sliders[k] = {}
        exp = expanders[k]
        ms = multiselects[k]
        entered = [t for t in ms] + [None, None, None, None]
        a, b, c, *r = entered
        left_over[k]["w"] = [o for o in left_over[k]["og"] if o not in entered]
        for i, kk_vv in enumerate({"a": a, "b": b, "c": c}.items()):
            kk, vv = kk_vv
            if vv:
                inv_vals_cells[ck[i]] = vv
                if (ckk := f"choice_pts_{kk}") in st.session_state:
                    i_value = st.session_state[ckk]
                else:
                    i_value = def_pts_val
                ss_ = f"{k}_{ckk}"
                print(f"{k=}, {ck=}, {kk=}, {vv=}, {ckk=}, {ss_=}, {i_value=}")
                sliders[k][ckk] = exp.slider(
                    label=vv,
                    min_value=min_pts,
                    max_value=max_pts,
                    value=i_value,
                    key=ss_,
                    on_change=lambda k_=k, ck_=ckk, exp_=exp: change_pts_slider(k_, ck_, ss_, exp_)
                )
    #
    #
    # if k := "atlantic":
    #     sliders[k] = {}
    #     exp = expanders[k]
    #     ms = multiselects[k]
    #     entered = [t for t in ms] + [None, None, None, None]
    #     a, b, c, *r = entered
    #
    #     w = [o for o in left_over[k]["og"]]
    #     for e in entered:
    #         if e in w:
    #             w.remove(e)
    #     left_over[k]["w"] = w
    #
    #     if a:
    #         inv_vals_cells["A__E_0"] = a
    #         if (ck := f"choice_pts_{a}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             a,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if b:
    #         inv_vals_cells["A__E_1"] = b
    #         if (ck := f"choice_pts_{b}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             b,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if c:
    #         inv_vals_cells["A__E_2"] = c
    #         if (ck := f"choice_pts_{c}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             c,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #
    # if k := "metropolitan":
    #     sliders[k] = {}
    #     exp = expanders[k]
    #     ms = multiselects[k]
    #     entered = [t for t in ms] + [None, None, None, None]
    #     a, b, c, *r = entered
    #
    #     w = [o for o in left_over[k]["og"]]
    #     for e in entered:
    #         if e in w:
    #             w.remove(e)
    #     left_over[k]["w"] = w
    #
    #     if a:
    #         inv_vals_cells["M__E_0"] = a
    #         if (ck := f"choice_pts_{a}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             a,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if b:
    #         inv_vals_cells["M__E_1"] = b
    #         if (ck := f"choice_pts_{b}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             b,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if c:
    #         inv_vals_cells["M__E_2"] = c
    #         if (ck := f"choice_pts_{c}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             c,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #
    # if k := "central":
    #     sliders[k] = {}
    #     exp = expanders[k]
    #     ms = multiselects[k]
    #     entered = [t for t in ms] + [None, None, None, None]
    #     a, b, c, *r = entered
    #
    #     w = [o for o in left_over[k]["og"]]
    #     for e in entered:
    #         if e in w:
    #             w.remove(e)
    #     left_over[k]["w"] = w
    #
    #     if a:
    #         inv_vals_cells["C__W_0"] = a
    #         if (ck := f"choice_pts_{a}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             a,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if b:
    #         inv_vals_cells["C__W_1"] = b
    #         if (ck := f"choice_pts_{b}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             b,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if c:
    #         inv_vals_cells["C__W_2"] = c
    #         if (ck := f"choice_pts_{c}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             c,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #
    # if k := "pacific":
    #     sliders[k] = {}
    #     exp = expanders[k]
    #     ms = multiselects[k]
    #     entered = [t for t in ms] + [None, None, None, None]
    #     a, b, c, *r = entered
    #
    #     w = [o for o in left_over[k]["og"]]
    #     for e in entered:
    #         if e in w:
    #             w.remove(e)
    #     left_over[k]["w"] = w
    #
    #     if a:
    #         inv_vals_cells["P__W_0"] = a
    #         if (ck := f"choice_pts_{a}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             a,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if b:
    #         inv_vals_cells["P__W_1"] = b
    #         if (ck := f"choice_pts_{b}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             b,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )
    #     if c:
    #         inv_vals_cells["P__W_2"] = c
    #         if (ck := f"choice_pts_{c}") in st.session_state:
    #             i_value = st.session_state[ck]
    #         else:
    #             i_value = def_pts_val
    #         sliders[k][ck] = exp.slider(
    #             c,
    #             min_pts,
    #             max_pts,
    #             i_value,
    #             key=ck,
    #             on_change=lambda k_=k, ck_=ck: change_pts_slider(k_, ck_)
    #         )

    print(f"{left_over=}")
    print(f"{len(ms_pacific)=}, {len(ms_central)=}, {len(ms_atlantic)=}, {len(ms_metropolitan)=}")
    ms_wc_w = None
    exp_wc_w = st.expander("West Wildcard")
    if len(ms_pacific) + len(ms_central) == 6:
        left_pac = left_over.get("pacific", {}).get("w", [])
        left_cen = left_over.get("central", {}).get("w", [])
        print(f"{left_pac=}, {left_cen=}")
        ms_wc_w = exp_wc_w.multiselect(
            label="West Wildcard",
            options=left_pac + left_cen,
            max_selections=2,
            label_visibility="hidden"
        )
    else:
        exp_wc_w.write(f"Choose Pacific and Central Teams First.")

    ms_wc_e = None
    exp_wc_e = st.expander("East Wildcard")
    if len(ms_atlantic) + len(ms_metropolitan) == 6:
        left_atl = left_over.get("atlantic", {}).get("w", [])
        left_met = left_over.get("metropolitan", {}).get("w", [])
        print(f"{left_atl=}, {left_met=}")
        ms_wc_e = exp_wc_e.multiselect(
            label="East Wildcard",
            options=left_atl + left_met,
            max_selections=2,
            label_visibility="hidden"
        )
    else:
        exp_wc_e.write(f"Choose Atlantic and Metropolitan Teams First.")

    ordered_west = [[], []]
    ordered_east = [[], []]

    if ms_wc_w:
        conf = "western"
        exp = exp_wc_w
        sliders[conf] = {}
        i_value = def_pts_val
        for i, t in enumerate(ms_wc_w):
            ss_ = f"{conf}_{i}"
            sliders[conf][i] = exp.slider(
                t,
                min_pts,
                max_pts,
                i_value,
                key=ss_
            )

        for div, ms in {"central": ms_central, "pacific": ms_pacific, "atlantic": ms_atlantic, "metropolitan": ms_metropolitan}.items():
            lst = ordered_west if div in ['pacific', 'central'] else ordered_east
            for i, ms_let in enumerate(zip(ms, ["a", "b", "c"])):
                team, let = ms_let
                val = st.session_state[f"{div}_choice_pts_{let}"]
                lst[0].append(team)
                lst[1].append(val)

    if ms_wc_e:
        conf = "eastern"
        exp = exp_wc_e
        sliders[conf] = {}
        i_value = def_pts_val
        for i, t in enumerate(ms_wc_e):
            ss_ = f"{conf}_{i}"
            sliders[conf][i] = exp.slider(
                t,
                min_pts,
                max_pts,
                i_value,
                key=ss_
            )

    print(f"{ordered_west=}")
    print(f"{ordered_east=}")

    st.divider()

    st.toggle("Show Place", key="choice_show_place")
    
    min_width = 30
    min_height = 20

    # Create the HTML divs
    divs = ""
    cols = 9 if not showing_placements else 11
    print(f"{cols=}")
    print(f"{sliders=}")
    for i in range(8):
        row_divs = ""
        for j in range(cols):
            # Set the minimum width and height and add HTML ids
            div_id = f"({i}, {j})"
            div_id_t = eval(div_id)
            # text = inv_cells.get(div_id_t, "")

            if j < (cols // 2):
                k_div = "pacific" if i < 4 else "central"
            else:
                k_div = "atlantic" if i < 4 else "metropolitan"

            if i == 0 or i == 7:
                k_place = "choice_pts_a"
            elif i == 2 or i == 5:
                k_place = "choice_pts_b"
            elif i == 3 or i == 4:
                k_place = "choice_pts_c"
            else:
                # wild card
                k_place = ""
            # text = sliders.get(k_div, {}).get(k_place, "")

            msg = ""
            if showing_placements:
                msg += "-A"
                if (j == 0 or (j == (cols - 1))):
                    msg += "-C"
                    text = inv_placements.get(div_id_t, "")
                elif (j == 1) or (j == (cols - 2)):
                    msg += "-D"
                    text = sliders.get(k_div, {}).get(k_place, "")
                else:
                    msg += "-E"
                    k = inv_cells.get(div_id_t, "")
                    text = inv_vals_cells.get(k, "")
            else:
                msg += "-B"
                if (j == 0 or (j == (cols - 1))):
                    msg += "-E"
                    # text = inv_placements.get(div_id_t, "")
                    text = sliders.get(k_div, {}).get(k_place, "")
                # elif (j == 1) or (j == (cols - 2)):
                else:
                    msg += "-F"
                    k = inv_cells.get(div_id_t, "")
                    text = inv_vals_cells.get(k, "")

            # if i == 1 or i == 6:
            #     if showing_placements:


            print(f"{msg=}, {i=}, {j=}, {k_div=}, {k_place=}, {text=}")

            # if showing_placements and (j == 0 or (j == (cols - 1))):
            #     text = inv_placements.get(div_id_t, "")
            # elif showing_placements and (j == 1) or (j == (cols - 2)):
            #     # text = sliders[k_div][k_place]
            #     if j == 1:
            #         k_div = "pacific" if i < 4 else "central"
            #     else:
            #         k_div = "atlantic" if i < 4 else "metropolitan"
            #
            #     if i == 0 or i == 7:
            #         k_place = "choice_pts_a"
            #     elif i == 2 or i == 5:
            #         k_place = "choice_pts_b"
            #     elif i == 3 or i == 4:
            #         k_place = "choice_pts_c"
            #     else:
            #         k_place = ""
            #
            #     text = sliders.get(k_div, {}).get(k_place, "")
            # else:
            #     k = inv_cells.get(div_id_t, "")
            #     text = inv_vals_cells.get(k, "")
            # # print(f"{i=}, {j=}, {text=}")
            text = "" if text == div_id_t else text
            row_divs += f"<td id='{div_id}' style='min-width: {min_width}px; min-height: {min_height}px;'>{text}</td>"
        divs += f"<tr>{row_divs}</tr>"

    divs = f"<table>{divs}</table>"

    st.markdown(divs, unsafe_allow_html=True)

