import os
import tkinter
from PIL import ImageTk, Image
from itertools import combinations
from random import shuffle


def click(t1, t2):
    default = {
        "+/-": 0,
        "+": 0,
        "-": 0,
        "wins": [],
        "losses": []
    }
    for t in [t1, t2]:
        if t not in history:
            history[t] = {k: v for k, v in default.items()}

    history[t1]["+/-"] += 1
    history[t1]["+"] += 1
    history[t1]["wins"].append(t2)

    history[t2]["+/-"] -= 1
    history[t2]["-"] += 1
    history[t2]["wins"].append(t1)

    next_question()


def tie_break(lst):
    i, c = 0, len(lst)
    res = []
    while i < (c - 1):
        team_1, val1 = lst[i]
        j = i
        ties = [lst[i]]
        while ((i + 1) < c) and (val1 == lst[i + 1][1]):
            team_2, val2 = lst[i + 1]
            ties.append(lst[i + 1])
            # if history[team_1]["wins"]:
            i += 1
        i = j + 1
        res.append((team_1, val1))



def show_results():

    frame.pack_forget()
    top_n = 8

    frame_results_pm = tkinter.Frame(app, highlightbackground="#010101", highlightthickness=2)
    label_pm = tkinter.Label(frame_results_pm, text="+/-")
    frame_top_results_pm = tkinter.Frame(frame_results_pm)
    frame_bottom_results_pm = tkinter.Frame(frame_results_pm)
    lbl_1 = tkinter.Label(frame_top_results_pm, text=f"Top {top_n}")
    lbl_2 = tkinter.Label(frame_bottom_results_pm, text=f"Bottom {top_n}")
    lbl_1.pack(side=tkinter.TOP)
    lbl_2.pack(side=tkinter.TOP)
    sorted_teams_pm = [(k, v["+/-"]) for k, v in history.items()]
    sorted_teams_pm.sort(key=lambda tup: tup[1])
    # sorted_teams_pm = tie_break(sorted_teams_pm)

    print(f"{history=}\n{sorted_teams_pm=}")

    for team, pm in sorted_teams_pm[len(sorted_teams_pm) - 1: len(sorted_teams_pm) - (top_n + 1): -1]:
        print(f"TOP5 {team=}, {pm=}")
        f = tkinter.Frame(frame_top_results_pm)
        btn = tkinter.Button(f, image=res_images[team])
        lbl = tkinter.Label(f, text=f"{pm}")
        f.pack()
        btn.pack(side=tkinter.LEFT)
        lbl.pack(side=tkinter.RIGHT)

    for team, pm in sorted_teams_pm[:top_n]:
        print(f"BOT5 {team=}, {pm=}")
        f = tkinter.Frame(frame_bottom_results_pm)
        btn = tkinter.Button(f, image=res_images[team])
        lbl = tkinter.Label(f, text=f"{pm}")
        f.pack()
        btn.pack(side=tkinter.LEFT)
        lbl.pack(side=tkinter.RIGHT)

    frame_results_pm.pack()
    label_pm.pack(side=tkinter.TOP)
    frame_top_results_pm.pack(side=tkinter.LEFT)
    frame_bottom_results_pm.pack(side=tkinter.RIGHT)


def next_question():
    if not total_games:
        show_results()
    else:
        choice = total_games.pop(0)
        team_1, team_2 = choice
        button_1.configure(image=btn_images[team_1], command=lambda t1=team_1, t2=team_2: click(t1, t2))
        button_2.configure(image=btn_images[team_2], command=lambda t1=team_2, t2=team_1: click(t1, t2))


if __name__ == '__main__':

    app = tkinter.Tk()
    app.geometry("900x500")

    image_directory = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"
    btn_images = {}
    res_images = {}
    history = {}
    full_size_image = (200, 200)
    small_size_image = (50, 50)

    for pth in os.listdir(image_directory):
        team = pth.replace("logo", "").replace("_", " ").replace(".png", "").replace(".jpg", "").strip()
        if "division" in team or "conference" in team:
            continue
        im_pth = os.path.join(image_directory, pth)
        img = Image.open(im_pth)
        img_c = img.copy()
        btn_image = ImageTk.PhotoImage(img.resize(full_size_image))
        res_image = ImageTk.PhotoImage(img.resize(small_size_image))
        btn_images[team] = btn_image
        res_images[team] = res_image

    print(f"{len(btn_images)=}")

    total_games = list(combinations(btn_images, 2))
    shuffle(total_games)
    total_games = total_games
    print(f"{len(total_games)=}")
    # for team_1, team_2 in total_games:
    #     print(f"{team_1=}, {team_2=}")
    choice_1 = total_games.pop(0)
    team_1, team_2 = choice_1

    frame = tkinter.Frame(app)
    # canvas_1 = tkinter.Canvas(frame, width=250, height=250)
    # canvas_2 = tkinter.Canvas(frame, width=250, height=250)
    #
    # canvas_1.create_image(
    #     10,
    #     0,
    #     anchor=tkinter.N,
    #     image=btn_images[team_1]
    # )
    #
    # canvas_2.create_image(
    #     10,
    #     10,
    #     anchor=tkinter.N,
    #     image=btn_images[team_2]
    # )

    button_1 = tkinter.Button(frame, image=btn_images[team_1], command=lambda t1=team_1, t2=team_2: click(t1, t2))
    button_2 = tkinter.Button(frame, image=btn_images[team_2], command=lambda t1=team_2, t2=team_1: click(t1, t2))

    frame.pack(side=tkinter.TOP)
    # canvas_1.pack(side=tkinter.LEFT)
    # canvas_2.pack(side=tkinter.RIGHT)
    button_1.pack(side=tkinter.LEFT)
    button_2.pack(side=tkinter.RIGHT)

    app.mainloop()
