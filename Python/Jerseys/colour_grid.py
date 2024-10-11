from colour_utility import gradient
from customtkinter_utility import *


if __name__ == "__main__":

    t_width = 1600
    t_height = 950
    c_width = int(t_width * 0.95)
    c_height = int(t_height * 0.98)
    c_width, c_height = [min(c_width, c_height) for _ in range(2)]
    n_cols = 32
    n_rows = 32

    app = ctk.CTk()
    app.geometry(calc_geometry_tl(t_width, t_height))

    team_colours = {
        0: {
            "acr": "ANA",
            "bg": Colour("#DAA100"),
            "fg": Colour("#000000")
        },
        1: {
            "acr": "BOS",
            "bg": Colour("#000000"),
            "fg": Colour("#F7E609")
        },
        2: {
            "acr": "BUF",
            "bg": Colour("#0054BA"),
            "fg": Colour("#F7E609")
        },
        3: {
            "acr": "CAR",
            "bg": Colour("#C00000"),
            "fg": Colour("#000000")
        },
        4: {
            "acr": "CBJ",
            "bg": Colour("#153D64"),
            "fg": Colour("#C00000")
        },
        5: {
            "acr": "CGY",
            "bg": Colour("#C00000"),
            "fg": Colour("#F7E609")
        },
        6: {
            "acr": "CHI",
            "bg": Colour("#FF3300"),
            "fg": Colour("#000000")
        },
        7: {
            "acr": "COL",
            "bg": Colour("#861818"),
            "fg": Colour("#215C98")
        },
        8: {
            "acr": "DAL",
            "bg": Colour("#00B050"),
            "fg": Colour("#F2F2F2")
        },
        9: {
            "acr": "DET",
            "bg": Colour("#FF0000"),
            "fg": Colour("#FFFFFF")
        },
        10: {
            "acr": "EDM",
            "bg": Colour("#1530A5"),
            "fg": Colour("#E97132")
        },
        11: {
            "acr": "FLA",
            "bg": Colour("#FF0000"),
            "fg": Colour("#FFCC66")
        },
        12: {
            "acr": "LAK",
            "bg": Colour("#000000"),
            "fg": Colour("#D0D0D0")
        },
        13: {
            "acr": "MIN",
            "bg": Colour("#126000"),
            "fg": Colour("#C00000")
        },
        14: {
            "acr": "MTL",
            "bg": Colour("#FF0000"),
            "fg": Colour("#0033CC")
        },
        15: {
            "acr": "NJD",
            "bg": Colour("#FF0000"),
            "fg": Colour("#000000")
        },
        16: {
            "acr": "NSH",
            "bg": Colour("#F2E600"),
            "fg": Colour("#1530A5")
        },
        17: {
            "acr": "NYI",
            "bg": Colour("#215C98"),
            "fg": Colour("#FF6709")
        },
        18: {
            "acr": "NYR",
            "bg": Colour("#0000FF"),
            "fg": Colour("#FF0000")
        },
        19: {
            "acr": "OTT",
            "bg": Colour("#000000"),
            "fg": Colour("#C00000")
        },
        20: {
            "acr": "PHI",
            "bg": Colour("#FA8F00"),
            "fg": Colour("#000000")
        },
        21: {
            "acr": "PIT",
            "bg": Colour("#000000"),
            "fg": Colour("#FDF55F")
        },
        22: {
            "acr": "SEA",
            "bg": Colour("#153D64"),
            "fg": Colour("#73FDD9")
        },
        23: {
            "acr": "SJS",
            "bg": Colour("#009999"),
            "fg": Colour("#FA8F00")
        },
        24: {
            "acr": "STL",
            "bg": Colour("#1B6BCB"),
            "fg": Colour("#FFFF00")
        },
        25: {
            "acr": "TBL",
            "bg": Colour("#153D64"),
            "fg": Colour("#FFFFFF")
        },
        26: {
            "acr": "TOR",
            "bg": Colour("#153D64"),
            "fg": Colour("#FFFFFF")
        },
        27: {
            "acr": "UTA",
            "bg": Colour("#0B3040"),
            "fg": Colour("#CAEDFB")
        },
        28: {
            "acr": "VAN",
            "bg": Colour("#215C98"),
            "fg": Colour("#00B050")
        },
        29: {
            "acr": "VGK",
            "bg": Colour("#777777"),
            "fg": Colour("#F9ED05")
        },
        30: {
            "acr": "WPG",
            "bg": Colour("#153D64"),
            "fg": Colour("#83CCEB")
        },
        31: {
            "acr": "WSH",
            "bg": Colour("#FF0000"),
            "fg": Colour("#153D64")
        }
    }

    can = ctk.CTkCanvas(
        app,
        width=c_width,
        height=c_height,
        background="#AEAEAE"
    )

    gc = grid_cells(
        c_width,
        n_cols,
        c_height,
        n_rows
    )

    rects = {}

    for i, row in enumerate(gc):
        for j, gc_data in enumerate(row):
            r_bg = team_colours.get(i, {}).get("bg", Colour(random_colour(rgb=False))).hex_code
            c_bg = team_colours.get(j, {}).get("bg", Colour(random_colour(rgb=False))).hex_code
            r_fg = team_colours.get(i, {}).get("fg", Colour(random_colour(rgb=False))).hex_code
            c_fg = team_colours.get(j, {}).get("fg", Colour(random_colour(rgb=False))).hex_code
            acr = team_colours.get(i if j == 0 else j, {}).get("acr", "")
            # r_acr = team_colours.get(i, {}).get("acr", "")
            # c_acr = team_colours.get(j, {}).get("acr", "")
            # rects[(i, j)] = {"fill": random_colour(rgb=False)}
            # if (i == 0) and (j == 0):
            if i == j:
                rects[(i, j)] = {
                    "r_fill": "#000000",
                    "t_fill": "#FFFFFF"
                }
            elif i == 0:
                rects[(i, j)] = {
                    "r_fill": c_bg,
                    "t_fill": c_fg
                }
            elif j == 0:
                rects[(i, j)] = {
                    "r_fill": r_bg,
                    "t_fill": r_fg
                }
            else:
                rects[(i, j)] = {
                    "r_fill": gradient(1, 2, c_bg, r_bg, rgb=False),
                    "t_fill": gradient(1, 2, c_fg, r_fg, rgb=False)
                }

            rects[(i, j)].update({
                "r_fill": Colour(rects[(i, j)]["r_fill"]).brighten(0.25).hex_code,
                "t_fill": Colour(rects[(i, j)]["t_fill"]).brighten(0.25).hex_code
            })

            rects[(i, j)].update({
                "rect": can.create_rectangle(
                    *gc_data,
                    fill=rects[(i, j)]["r_fill"]
                )
            })
            if ((i == 0) or (j == 0)) and not (i == j == 0):
                cw = gc_data[2] - gc_data[0]
                ch = gc_data[3] - gc_data[1]
                txt = acr
                print(f"{i=}, {j=}, {txt=}")
                if txt:
                    rects[(i, j)].update({
                        "text": can.create_text(
                            gc_data[0] + (cw / 2),
                            gc_data[1] + (ch / 2),
                            text=txt.upper(),
                            fill=rects[(i, j)]["t_fill"]
                        )
                    })

    can.pack()
    app.mainloop()
