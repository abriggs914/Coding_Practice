from utility import *
from tkinter import *
import tkinter as tk


#################################################
## Program to convert distances between units. ##
## Supports both metric and imperial.          ##
##                                             ##
## Date: 2021-11-28                            ##
#################################################


class Node:

    def __init__(self, id_num, name):
        self.id_num = id_num
        self.name = name
        self.connected_nodes = []

    def add_connection(self, node, cost, dag=True, ret_cost="negative"):
        assert isinstance(node, Node)
        valid = ["negative", "inverse", "same"]
        if not isinstance(ret_cost, list):
            ret_cost = [ret_cost]
        new_rc = []
        for rc in ret_cost:
            if rc.lower() not in valid:
                rc = "negative"
            new_rc.append(rc)
        ret_cost = new_rc
        self.connected_nodes.append((node, cost))
        if not dag:
            if self not in [n for n, c in node.connected_nodes]:
                if "negative" in ret_cost:
                    cost = -cost
                if "inverse" in ret_cost:
                    cost = 1 / cost

                node.add_connection(self, cost)

    def __eq__(self, other):
        return isinstance(other, Node) and self.id_num == other.id_num

    def __lt__(self, other):
        return isinstance(other, Node) and self.id_num < other.id_num

    # def __key(self):
    #     return tuple(v for k, v in sorted(self.__dict__.items()))

    def __repr__(self):
        return "Node #{}: \"{}\", BF: {}".format(self.id_num, self.name, len(self.connected_nodes))


class Graph:

    def __init__(self):
        self.nodes = []

    def __getitem__(self, key):
        print("key:", key, ", t:", type(key))
        for n in self.nodes:
            print("\tn:", n, ", n == key:", n == key, ", t:", type(n))
            if n == key or str(key) == str(n.name):
                return n

    def add_node(self, id_num, name=None):
        if name is None:
            assert isinstance(id_num, Node)
            n = id_num
        else:
            assert isnumber(id_num) and isinstance(name, str)
            n = Node(id_num, name)
        self.nodes.append(n)

    # def convert(self, start, end):
    #     def helper(nodes_to_check, target, path, checked):
    #         print("nodes_to_check: {}, target: {}, path: {}, checked: {}".format(nodes_to_check, target, path, checked))
    #         to_add = []
    #         for n in nodes_to_check:
    #             print("n: ", n)
    #             if n == target:
    #                 print("Found target")
    #                 return path + [target]
    #             else:
    #                 if n not in checked:
    #                     to_add = to_add + [n for n, c in n.connected_nodes]
    #         print("to_add: ", to_add)
    #         return path + helper(to_add, target, path, checked + nodes_to_check)
    #     path = helper([start], end, [], [])
    #     print("Calculated Path:", path)

    def bfs(self, start_vertex, target_value):
        path = [start_vertex]
        vertex_and_path = [start_vertex, path]
        bfs_queue = [vertex_and_path]
        visited = set()
        while bfs_queue:
            current_vertex, path = bfs_queue.pop(0)
            visited.add(str(current_vertex))
            print("current_vertex: ", current_vertex)
            print("self[current_vertex].connected_nodes:", self[current_vertex].connected_nodes)
            for neighbor in [n for n, c in self[current_vertex].connected_nodes]:
                if str(neighbor) not in visited:
                    if neighbor is target_value:
                        return path + [neighbor]
                    else:
                        bfs_queue.append([neighbor, path + [neighbor]])
        return path

    def convert(self, n, unit_from, unit_to):
        res = self.bfs(unit_from, unit_to)
        t_cost = 1
        costs_used = []
        i = 0
        while i < len(res) - 1:
            k1 = res[i]
            k2 = res[i + 1]
            c_nodes = g[k1].connected_nodes
            cost = [c for n, c in c_nodes if n == k2][0]
            costs_used.append(cost)
            t_cost *= cost
            i += 1
        res = [n.name for n in res]
        # print("bfs:", res)
        # print("conversion factor:", t_cost)
        # print("costs_used:", costs_used)
        return n / t_cost


if __name__ == '__main__':
    def t1():
        n1 = Node(1, "Node 1")
        n2 = Node(2, "Node 2")
        n3 = Node(3, "Node 3")
        n1.add_connection(n2, 3, 0, ["negative", "inverse"])
        n2.add_connection(n3, 8)
        g = Graph()
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)

        print(n1)
        print(n2)

        g.convert(n1, n2)
        g.convert(n1, n3)

        print("bfs:", g.bfs(n1, n3))

    im_twip = Node(1, "Twip")
    im_point = Node(2, "Point")
    im_pica = Node(3, "Pica")
    im_line = Node(4, "Line")
    im_poppyseed = Node(5, "Poppyweed")
    im_barleycorn = Node(6, "Barleycorn")
    im_finger = Node(7, "Finger")
    im_stick = Node(8, "Stick")
    im_inch = Node(9, "Inch")
    im_foot = Node(10, "Foot")
    im_yard = Node(11, "Yard")
    im_fathom = Node(12, "Fathom")
    im_shackle = Node(13, "Shackle")
    im_cable = Node(14, "Cable")
    im_nautic_mile = Node(15, "Nautic Mile")
    im_league = Node(16, "League")
    im_mile = Node(17, "Mile")
    im_furlong = Node(18, "Furlong")
    im_gunters_chain = Node(19, "Gunter's Chain")
    im_rod = Node(20, "Rod")
    im_pole = Node(21, "Pole")
    im_perch = Node(22, "Perch")
    im_pace = Node(23, "Pace")
    im_shaftment = Node(24, "Shaftment")
    im_digit = Node(25, "Digit")
    im_palm = Node(26, "Palm")
    im_link = Node(27, "Link")
    im_cubit = Node(28, "Cubit")
    im_grade = Node(29, "Grade")
    im_step = Node(30, "Step")
    im_rope = Node(31, "Rope")
    im_ramsdens_chain = Node(32, "Ramsden's Chain")
    im_roman_mile = Node(33, "Roman Mile")
    im_nail = Node(34, "Nail")
    im_span = Node(35, "Span")
    im_ell = Node(36, "Ell")
    im_skein = Node(37, "Skein")
    im_spindle = Node(38, "Spindle")  # spindles of jute https://www.wolframalpha.com/input/?i=746496000+twip+to+spindle&assumption=%22UnitClash%22+-%3E+%7B%22spindle%22%2C+%7B%22SpindlesJute%22%7D%7D
    im_hand = Node(39, "Hand")
    im_meter = Node(40, "Meter")
    im_dekameter = Node(41, "Dekameter")
    im_hectometer = Node(42, "Hectometer")
    im_kilometer = Node(43, "Kilometer")
    im_megameter = Node(44, "Megameter")
    im_gigameter = Node(45, "Gigameter")
    im_terameter = Node(46, "Terameter")
    im_petameter = Node(47, "Petameter")
    im_exameter = Node(48, "Exameter")
    im_decimeter = Node(49, "Decimeter")
    im_centimeter = Node(50, "centimeter")
    im_millimeter = Node(51, "millimeter")
    im_micrometer = Node(52, "micrometer")
    im_nanometer = Node(53, "nanometer")
    im_picometer = Node(54, "picometer")
    im_femtometer = Node(55, "femtometer")
    im_attometer = Node(56, "attometer")

    im_parsec = Node(57, "Parsec")
    im_lightyear = Node(58, "Lightyear")


    im_twip.add_connection(im_point, 20, False, "inverse")
    im_point.add_connection(im_pica, 12, False, "inverse")
    im_point.add_connection(im_finger, 63, False, "inverse")
    im_point.add_connection(im_line, 6, False, "inverse")
    im_line.add_connection(im_inch, 12, False, "inverse")
    im_pica.add_connection(im_inch, 6, False, "inverse")
    im_line.add_connection(im_poppyseed, 1, False, "inverse")
    im_poppyseed.add_connection(im_barleycorn, 4, False, "inverse")
    im_barleycorn.add_connection(im_inch, 3, False, "inverse")
    im_inch.add_connection(im_finger, 7/8, False, "inverse")
    im_inch.add_connection(im_stick, 2, False, "inverse")
    im_inch.add_connection(im_foot, 12, False, "inverse")
    im_inch.add_connection(im_palm, 3, False, "inverse")
    im_stick.add_connection(im_hand, 2, False, "inverse")
    im_hand.add_connection(im_foot, 3, False, "inverse")
    im_foot.add_connection(im_yard, 3, False, "inverse")
    im_yard.add_connection(im_fathom, 2, False, "inverse")
    im_fathom.add_connection(im_shackle, 15, False, "inverse")
    im_fathom.add_connection(im_cable, 100, False, "inverse")
    im_cable.add_connection(im_nautic_mile, 10, False, "inverse")
    im_foot.add_connection(im_nautic_mile, 6080, False, "inverse")
    im_nautic_mile.add_connection(im_league, 3, False, "inverse")
    im_yard.add_connection(im_mile, 1760, False, "inverse")
    im_fathom.add_connection(im_gunters_chain, 11, False, "inverse")
    im_gunters_chain.add_connection(im_furlong, 10, False, "inverse")
    im_furlong.add_connection(im_mile, 8, False, "inverse")
    im_rod.add_connection(im_gunters_chain, 4, False, "inverse")
    im_pole.add_connection(im_gunters_chain, 4, False, "inverse")
    im_perch.add_connection(im_gunters_chain, 4, False, "inverse")
    im_digit.add_connection(im_palm, 4, False, "inverse")
    im_digit.add_connection(im_nail, 3, False, "inverse")
    im_nail.add_connection(im_span, 4, False, "inverse")
    im_palm.add_connection(im_span, 3, False, "inverse")
    im_palm.add_connection(im_shaftment, 2, False, "inverse")
    im_shaftment.add_connection(im_foot, 2, False, "inverse")
    im_shaftment.add_connection(im_pace, 5, False, "inverse")
    im_shaftment.add_connection(im_cubit, 3, False, "inverse")
    im_span.add_connection(im_cubit, 2, False, "inverse")
    im_link.add_connection(im_rod, 25, False, "inverse")
    im_link.add_connection(im_pole, 25, False, "inverse")
    im_link.add_connection(im_perch, 25, False, "inverse")
    im_pace.add_connection(im_grade, 2, False, "inverse")
    im_pace.add_connection(im_step, 2, False, "inverse")
    im_cubit.add_connection(im_rod, 11, False, "inverse")
    im_cubit.add_connection(im_pole, 11, False, "inverse")
    im_cubit.add_connection(im_perch, 11, False, "inverse")
    im_grade.add_connection(im_rope, 4, False, "inverse")
    im_step.add_connection(im_rope, 4, False, "inverse")
    im_rope.add_connection(im_ramsdens_chain, 5, False, "inverse")
    im_ramsdens_chain.add_connection(im_roman_mile, 50, False, "inverse")
    im_span.add_connection(im_ell, 5, False, "inverse")
    im_ell.add_connection(im_skein, 96, False, "inverse")
    im_skein.add_connection(im_spindle, 120, False, "inverse")
    im_yard.add_connection(im_meter, 1/0.9144, False, "inverse")
    im_dekameter.add_connection(im_meter, 1/10, False, "inverse")
    im_hectometer.add_connection(im_dekameter, 1/10, False, "inverse")
    im_kilometer.add_connection(im_hectometer, 1/10, False, "inverse")
    im_megameter.add_connection(im_kilometer, 1/10, False, "inverse")
    im_gigameter.add_connection(im_megameter, 1/10, False, "inverse")
    im_terameter.add_connection(im_gigameter, 1/10, False, "inverse")
    im_petameter.add_connection(im_terameter, 1/10, False, "inverse")
    im_exameter.add_connection(im_petameter, 1/10, False, "inverse")
    im_decimeter.add_connection(im_meter, 10, False, "inverse")
    im_centimeter.add_connection(im_decimeter, 10, False, "inverse")
    im_millimeter.add_connection(im_centimeter, 10, False, "inverse")
    im_micrometer.add_connection(im_millimeter, 10, False, "inverse")
    im_nanometer.add_connection(im_micrometer, 10, False, "inverse")
    im_picometer.add_connection(im_nanometer, 10, False, "inverse")
    im_femtometer.add_connection(im_picometer, 10, False, "inverse")
    im_attometer.add_connection(im_femtometer, 10, False, "inverse")
    im_parsec.add_connection(im_kilometer, 1/30856780000000, False, "inverse")
    im_lightyear.add_connection(im_kilometer, 1/9460730000000, False, "inverse")

    nodes = [im_twip,
             im_point,
             im_pica,
             im_line,
             im_poppyseed,
             im_barleycorn,
             im_finger,
             im_stick,
             im_inch,
             im_foot,
             im_yard,
             im_fathom,
             im_shackle,
             im_cable,
             im_nautic_mile,
             im_league,
             im_mile,
             im_furlong,
             im_gunters_chain,
             im_rod,
             im_pole,
             im_perch,
             im_pace,
             im_shaftment,
             im_digit,
             im_palm,
             im_link,
             im_cubit,
             im_grade,
             im_step,
             im_rope,
             im_ramsdens_chain,
             im_roman_mile,
             im_nail,
             im_span,
             im_ell,
             im_skein,
             im_spindle,
             im_hand,
             im_meter,
             im_dekameter,
             im_hectometer,
             im_kilometer,
             im_megameter,
             im_gigameter,
             im_terameter,
             im_petameter,
             im_exameter,
             im_decimeter,
             im_centimeter,
             im_millimeter,
             im_micrometer,
             im_nanometer,
             im_picometer,
             im_femtometer,
             im_attometer,
             im_parsec,
             im_lightyear
             ]

    g = Graph()
    for n in nodes:
        g.add_node(n)

    # res = g.bfs(im_twip, im_spindle)
    res = g.bfs(im_twip, im_skein)
    t_cost = 1
    costs_used = []
    i = 0
    while i < len(res) - 1:
        k1 = res[i]
        k2 = res[i + 1]
        c_nodes = g[k1].connected_nodes
        cost = [c for n, c in c_nodes if n == k2][0]
        costs_used.append(cost)
        t_cost *= cost
        i += 1
    res = [n.name for n in res]
    print("bfs:", res)
    print("conversion factor:", t_cost)
    print("costs_used:", costs_used)


    win = Tk()
    win.title("Imperial Converison Calculator")
    win.geometry("700x300")
    label = Label(win, text="Convert Distances:", font=("", 10))
    label.pack(pady=30)

    # Access the Menu Widget using StringVar function
    input_val = StringVar()
    clicked_a = StringVar()
    clicked_b = StringVar()
    output_val = StringVar()

    input_entry = Entry(win, textvariable=input_val)
    input_entry.pack()

    # Create an instance of Menu in the frame
    from_menu = OptionMenu(win, clicked_a, *[n.name for n in nodes])
    from_menu.pack()

    to_menu = OptionMenu(win, clicked_b, *[n.name for n in nodes])
    to_menu.pack()

    def change_b(*args):
        to_menu["menu"].delete(0, 'end')
        new_choices = [n.name for n in nodes if n.name != clicked_a.get()]
        for choice in new_choices:
            to_menu["menu"].add_command(label=choice, command=tk._setit(clicked_b, choice))


    def convert_callback():
        print("isnumber(input_val.get()):", isnumber(input_val.get()))
        if input_val.get() and isnumber(input_val.get()):
            if clicked_a.get() and clicked_b.get():
                if clicked_a.get() != clicked_b.get():
                    n = float(input_val.get())
                    unit_from = g[clicked_a.get()]
                    unit_to = g[clicked_b.get()]
                    print("n: {}, unit_from: {}, unit_to: {}, clicked_a.get(): {}, clicked_a.get(): {}".format(n, unit_from, unit_to, clicked_a.get(), clicked_b.get()))
                    res = g.convert(n, unit_from, unit_to)
                    res = "{} {} == {} {}".format(n, clicked_a.get(), res, clicked_b.get())
                    output_val.set(res)
                    return
        output_val.set("ERROR")


    B = Button(win, text="convert", command=convert_callback)

    B.pack()

    output_entry = Entry(win, textvariable=output_val, width=50)
    output_entry.pack()

    clicked_a.trace_add("write", change_b)

    win.mainloop()
