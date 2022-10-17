from tkinter_utility import *
from utility import *
from colour_utility import *
import matplotlib.pyplot as plt
import numpy as np
from main import series_list

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)


# runtime
# count episodes

# x-axis = series
#   sort by
#       alpha
#       most
#       least

# y-axis = data point
#   is a value or a date value
#

# ability to transpose the graph data

def gen_data(field=None, op_args=0):
    if field:
        field_pt = field
        data_points = []
        name_points = []
        for s in series_list:
            value_retrieved = getattr(s, field_pt)
            if isclassmethod(value_retrieved):
                value_retrieved = value_retrieved()
            data_points.append(value_retrieved)
            name_points.append(s.name)

        match field:
            case "how_long_is_series":
                data_points = [dp[op_args] for dp in data_points]
            case _:
                print("pass on format")
        print(f"\t{data_points=}")

        return data_points, name_points


def show_graph(
        data_in,
        mode="alpha",
        reverse=False,
        title="Shows by length in minutes",
        xlabel="time (mins)",
        orientation="horizontal"
):
    # plt.hist(*data_in)
    # plt.show()

    data_points, show_names = data_in

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # alpha
    if mode == "alpha":
        show_names, data_points = [list(x) for x in zip(*sorted(zip(show_names, data_points), key=itemgetter(0), reverse=reverse))]
    elif mode == "value":
        data_points, show_names = [list(x) for x in zip(*sorted(zip(data_points, show_names), key=itemgetter(0), reverse=reverse))]
    # data_points, show_names = [list(x) for x in zip(*sorted(zip(data_points, show_names), key=itemgetter(0)))]

    y_pos = np.arange(len(show_names))
    if orientation == "horizontal":
        ax.barh(y_pos, data_points, align="center")
        ax.set_yticks(y_pos, labels=show_names)
        ax.invert_yaxis()
        ax.set_xlabel(xlabel)
        ax.set_title(title)
    else:
        ax.bar(y_pos, data_points, align="center")
        ax.set_xticks(y_pos, labels=show_names)
        ax.tick_params(axis="x", rotation=90)
        ax.invert_xaxis()
        ax.set_ylabel(xlabel)
        ax.set_title(title)

    plot(fig)

    # swap(plot)

    # plt.show()
    # plot()


def plot(fig):
    global canvas, toolbar
    # the figure that will contain the plot
    # fig = Figure(figsize=(5, 5),
    #              dpi=100)

    # list of squares
    # y = [i ** 2 for i in range(101)]

    # adding the subplot
    # plot1 = fig.add_subplot(111)

    # plotting the graph
    # plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure

    if canvas is not None:
        canvas.get_tk_widget().pack_forget()
        toolbar.pack_forget()

    canvas = FigureCanvasTkAgg(fig,
                               master=WIN)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   WIN)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


def plot_g_1():
    data_series_by_minutes = gen_data("how_long_is_series")
    print(data_series_by_minutes)
    show_graph(
        data_series_by_minutes,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by length in minutes",
        xlabel="time (mins)",
        orientation=tv_orientation.get()
    )


def plot_g_2():
    data_series_by_episodes = gen_data("count_episodes")
    print(data_series_by_episodes)
    show_graph(
        data_series_by_episodes,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by number of episodes",
        xlabel="# episodes",
        orientation=tv_orientation.get()
    )


def plot_g_3():
    data_series_by_seasons = gen_data("number_seasons")
    print(data_series_by_seasons)
    show_graph(
        data_series_by_seasons,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by number of seasons",
        xlabel="# seasons",
        orientation=tv_orientation.get()
    )


def plot_g_4():
    data_series_by_end_year = gen_data("end_year")
    print(data_series_by_end_year)
    show_graph(
        data_series_by_end_year,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by end year",
        xlabel="End Year",
        orientation=tv_orientation.get()
    )


def plot_g_5():
    data_series_by_end_year = gen_data("start_year")
    print(data_series_by_end_year)
    show_graph(
        data_series_by_end_year,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by start year",
        xlabel="Start Year",
        orientation=tv_orientation.get()
    )


def plot_g_6():
    data_series_by_average_length_of_episode = gen_data("average_length_of_episode")
    print(data_series_by_average_length_of_episode)
    show_graph(
        data_series_by_average_length_of_episode,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by avg episode length",
        xlabel="Episode Length (mins)",
        orientation=tv_orientation.get()
    )


def plot_g_7():
    data_series_by_hours = gen_data("how_long_is_series", 1)
    print(data_series_by_hours)
    show_graph(
        data_series_by_hours,
        mode="value" if tv_sort_style.get() == "by value" else "alpha",
        reverse=tv_sort_direction.get() == "descending",
        title="Shows by length in hours",
        xlabel="time (hrs)",
        orientation=tv_orientation.get()
    )


def update_graph_choice(*args):
    graph_choice = tv_combo_graph_chooser.get()
    match graph_choice:
        case "Total Time in Minutes":
            plot_button.configure(command=plot_g_1)
        case "Number of Episodes":
            plot_button.configure(command=plot_g_2)
        case "Number of Seasons":
            plot_button.configure(command=plot_g_3)
        case "End Year":
            plot_button.configure(command=plot_g_4)
        case "Start Year":
            plot_button.configure(command=plot_g_5)
        case "Average Episode Length in Minutes":
            plot_button.configure(command=plot_g_6)
        case "Total Time in Hours":
            plot_button.configure(command=plot_g_7)
        case _:
            raise Exception("ERROR")

def update_orientation_choice(*args):
    pass



def swap(*line_list):
    """
    Example
    -------
    line = plot(linspace(0, 2, 10), rand(10))
    swap(line)
    """
    for lines in line_list:
        try:
            iter(lines)
        except:
            lines = [lines]

        for line in lines:
            xdata, ydata = line.get_xdata(), line.get_ydata()
            line.set_xdata(ydata)
            line.set_ydata(xdata)
            line.axes.autoscale_view()


if __name__ == '__main__':
    WIN = tkinter.Tk()
    WIN.geometry(f"900x600")

    canvas = None
    toolbar = None

    print(series_list)
    print(sum([s.how_long_is_series()[0] for s in series_list]))


    # data_series_by_episodes = gen_data("count_episodes")
    # print(data_series_by_episodes)
    # show_graph(
    #     data_series_by_episodes,
    #     mode="value",
    #     reverse=True,
    #     title="Shows by number of episodes",
    #     xlabel="# episodes",
    #     orientation="vertical"
    # )
    #
    #
    # data_series_by_seasons = gen_data("number_seasons")
    # print(data_series_by_seasons)
    # show_graph(
    #     data_series_by_seasons,
    #     mode="value",
    #     reverse=True,
    #     title="Shows by number of seasons",
    #     xlabel="# seasons",
    #     orientation="vertical"
    # )

    tv_label_graph_chooser,\
    label_graph_chooser,\
    tv_combo_graph_chooser,\
    combo_graph_chooser \
        = combo_factory(
            WIN,
            tv_label="Choose a graph",
            kwargs_combo={
                "values": [
                    "Total Time in Minutes",
                    "Total Time in Hours",
                    "Number of Episodes",
                    "Number of Seasons",
                    "End Year",
                    "Start Year",
                    "Average Episode Length in Minutes"
                ]
            }
    )

    tv_combo_graph_chooser.trace_variable("w", update_graph_choice)

    plot_button = Button(master=WIN,
                         command=plot_g_1,
                         height=2,
                         width=10,
                         text="Plot")

    frame_radio_groups = Frame(WIN)
    frame_rb_group_1 = Frame(frame_radio_groups)
    frame_rb_group_2 = Frame(frame_radio_groups)
    frame_rb_group_3 = Frame(frame_radio_groups)

    tv_orientation = StringVar(WIN, value="vertical")
    tv_orientation_h = StringVar(WIN, value="horizontal")
    tv_orientation_v = StringVar(WIN, value="vertical")
    rb_h = Radiobutton(frame_rb_group_1, variable=tv_orientation, value="horizontal", textvariable=tv_orientation_h)
    rb_v = Radiobutton(frame_rb_group_1, variable=tv_orientation, value="vertical", textvariable=tv_orientation_v)

    tv_sort_style = StringVar(WIN, value="by value")
    tv_sort_style_a = StringVar(WIN, value="alphabetical")
    tv_sort_style_v = StringVar(WIN, value="by value")
    rb_sa = Radiobutton(frame_rb_group_2, variable=tv_sort_style, value="alphabetical", textvariable=tv_sort_style_a)
    rb_sv = Radiobutton(frame_rb_group_2, variable=tv_sort_style, value="by value", textvariable=tv_sort_style_v)

    tv_sort_direction = StringVar(WIN, value="descending")
    tv_sort_dir_a = StringVar(WIN, value="ascending")
    tv_sort_dir_d = StringVar(WIN, value="descending")
    rb_sda = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="ascending", textvariable=tv_sort_dir_a)
    rb_sdd = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="descending", textvariable=tv_sort_dir_d)

    tv_orientation.trace_variable("w", update_orientation_choice)

    label_graph_chooser.pack()
    combo_graph_chooser.pack()
    rb_h.pack()
    rb_v.pack()
    rb_sa.pack()
    rb_sv.pack()
    rb_sda.pack()
    rb_sdd.pack()
    frame_radio_groups.pack()
    frame_rb_group_1.pack(side=LEFT)
    frame_rb_group_2.pack(side=LEFT)
    frame_rb_group_3.pack(side=LEFT)
    plot_button.pack()

    WIN.state("zoomed")

    WIN.mainloop()
