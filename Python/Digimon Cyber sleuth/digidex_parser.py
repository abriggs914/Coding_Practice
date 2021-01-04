import csv
import json
from enum import Enum

DigiStages = Enum("DigiStages", "BABY IN_TRAINING ROOKIE CHAMPION ULTIMATE MEGA ULTRA ARMOR NONE")


class Digimon:

    def __init__(self, number, name, stage, typ, attribute, memory, equip_slots, HP, SP, ATK, DEF, INT, SPD):
        self.number = number
        self.name = name
        self.stage = decode_stage(stage)
        self.typ = typ
        self.attribute = attribute
        self.memory = memory
        self.equip_slots = equip_slots
        self.HP = HP
        self.SP = SP
        self.ATK = ATK
        self.DEF = DEF
        self.INT = INT
        self.SPD = SPD

        self.digi_evolutions = []
        self.de_digi_evolutions = []

    def __repr__(self):
        return self.name

    def set_digi_evolutions(self, evolutions):
        if type(evolutions) is not list:
            evolutions = [evolutions]
        for digimon in evolutions:
            if valid_digimon(digimon):
                self.digi_evolutions.append(digimon)
            else:
                raise ValueError("{d} is not recognized as a valid digimon".format(d=digimon))

    def set_de_digi_evolutions(self, evolutions):
        if type(evolutions) is not list:
            evolutions = [evolutions]
        for digimon in evolutions:
            if valid_digimon(digimon):
                self.de_digi_evolutions.append(digimon)
            else:
                raise ValueError("{d} is not recognized as a valid digimon".format(d=digimon))

        # print("{0} DE_DIGI_EVOLUTIONS: {1}".format(self, self.de_digi_evolutions))

    def print_evolution_tree(self, digi_evolve=True):
        x = max([len(d.name) for d in list_of_digimon])
        stages = list(DigiStages)
        if digi_evolve:
            evolutions = all_possible_digi_evolutions(self, preserve_chains=True)
        else:
            evolutions = all_possible_de_digi_evolutions(self, preserve_chains=True)
            stages.reverse()
        m = "|" + "|".join([pad_centre(stage.name + " ->", x) for stage in stages]) + "|\n"
        for d, digi in enumerate([self] + evolutions):
            if d != 0 and d % 14 == 0:
                m += "|" + "|".join([pad_centre(stage.name + " ->", x) for stage in stages]) + "|\n"
            lvl = digi.stage.value - 1 if digi_evolve else len(DigiStages) - digi.stage.value
            m += ("|" if lvl > 0 else "") + "|".join(["".join([" " for j in range(x)]) for i in range(lvl)])
            m += "|" + pad_centre(repr(digi), x) + "|"
            m += "|".join(["".join([" " for j in range(x)]) for i in range(len(DigiStages) - lvl)])
            m += "\n"
        print(m)


# Used in get_attr to arrange digimon names to evolutions.json format.
# (Uses "_" instead of " ")
F_lowerName = lambda x: x.lower().replace(" ", "_")


def pad_centre(text, l, pad_str=" "):
        if l > 0:
            h = (l - len(text)) // 2
            odd = (((2 * h) + len(text)) == l)
            text = text.rjust(h + len(text), pad_str)
            h += 1 if not odd else 0
            text = text.ljust(h + len(text), pad_str)
            return text
        else:
            return ""


def decode_stage(stage):
    return DigiStages[stage.upper().replace("-", "_")]


def write_evolutions_file(DE_file_str):
    with open(DE_file_str, "w") as DE_file:
        for k, v in digimon_dict.items():
            print("\n\tk: {0}\n\tv: {1}\n".format(k, v))
            DE_file.write(v[features[1]] + "\n")


# Does this digimon's name appear in the valid digimon list
def valid_digimon(digi):
    return digi in list_of_digimon


# return digi.lower() in get_attr(list_of_digimon, "name", F_lowerName)

# Return every digimon's associated attribute. Attribute is found using string lookup.
# A secondary function may be applied  
# def get_attr(lst_of_digis, attr, adj_func=None):
#     return [getattr(digi, attr) if adj_func == None else adj_func(getattr(digi, attr)) for digi in lst_of_digis]


# def can_digi_evolve_to(digimon, digi_evolution):
# def evolution_path(digi, target, visited=None):
# print("visited: {c}".format(c=visited))
# if not visited:
# visited = []
# visited.append(digi)
# x = len(visited)
# if digi == target:
# return visited

# for i, evolution in enumerate(digi.digi_evolutions):
# if evolution not in visited:
# path = evolution_path(evolution, target, visited)
# if path:
# return path
# else:
# visited = visited[:x]
# return evolution_path(digimon, digi_evolution)


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

# Return every digimon's associated attribute. Attribute is found using string lookup.
# Use "self" to get the object instead of one of it's attributes.
# A secondary function may be applied to alter values (upper/lower...)
# A filter function may also be applied, however the original order for lookup purposes
# will have changed, because every filtered list is at most the original list's length.
def get_attr(lst_of_digis, attr, adj_func=None, filter_func=lambda x: True):
    if attr == "self":
        return [digi if adj_func == None else adj_func(digi) for digi in lst_of_digis if filter_func(digi)]
    return [getattr(digi, attr) if adj_func == None else adj_func(getattr(digi, attr)) for digi in lst_of_digis if
            filter_func(digi)]


# return [getattr(digi, attr) if adj_func == None else adj_func(getattr(digi, attr)) for digi in lst_of_digis]


def evolution_path(digi, target, digi_evolve=True, visited=None, exhaustive=False):
    exhaustive = list() if exhaustive is True else (False if exhaustive is False else exhaustive)

    def rec(digi, target, digi_evolve, visited, exhaustive):
        if not visited:
            visited = []
        visited.append(digi)
        x = len(visited)
        if digi == target:
            return visited

        digis = digi.digi_evolutions if digi_evolve else digi.de_digi_evolutions
        i = 0
        while i < len(digis):
            evolution = digis[i]
            i += 1
            if evolution not in visited:
                path = rec(evolution, target, digi_evolve, visited, exhaustive)
                if path:
                    if exhaustive is not False:
                        if path not in exhaustive:
                            exhaustive.append(path)
                            return []
                    else:
                        return path
                else:
                    visited = visited[:x]

    res = rec(digi, target, digi_evolve, visited, exhaustive)
    # print("res: " + str(res) + ", exh: " + str(exhaustive))
    if exhaustive is not False:
        return exhaustive
    return res


# Digimon evolution logic

# TODO fix the exhaustive functionality
def can_digi_evolve_to(digimon, digi_evolution, exhaustive=False):
    return evolution_path(digimon, digi_evolution, digi_evolve=True, exhaustive=exhaustive)


# TODO update all de-digi-evolution data
def can_de_digi_evolve_to(digimon, digi_evolution, exhaustive=False):
    res = evolution_path(digimon, digi_evolution, digi_evolve=False, exhaustive=exhaustive)
    print("EXHAUSTIVE after: " + str(exhaustive))
    return res


def possible_evolns(digis, digi_evolve=True):
    if not digis:
        return []
    e = []
    for d in digis:
        e.append(d)
        if digi_evolve:
            e += possible_evolns(d.digi_evolutions, digi_evolve)
        else:
            e += possible_evolns(d.de_digi_evolutions, digi_evolve)
    return e


def all_possible_digi_evolutions(digimon, preserve_chains=False):
    res = list(possible_evolns(digimon.digi_evolutions, digi_evolve=True))
    if not preserve_chains:
        return set(res)
    return res


def all_possible_de_digi_evolutions(digimon, preserve_chains=False):
    res = list(possible_evolns(digimon.de_digi_evolutions, digi_evolve=False))
    if not preserve_chains:
        return set(res)
    return res


# Printing and testing functions


def show_all_possible_digi_evolutions(digimon, preserve_chains=False):
    if type(digimon) is list:
        for digi in digimon:
            show_all_possible_digi_evolutions(digi, preserve_chains)
    else:
        de = all_possible_digi_evolutions(digimon, preserve_chains)
        l = len(de)
        print("{d} all possible digi-evolutions ({l}):\n\t{de}".format(d=digimon, l=l, de=de))


def show_all_possible_de_digi_evolutions(digimon, preserve_chains=False):
    if type(digimon) is list:
        for digi in digimon:
            show_all_possible_de_digi_evolutions(digi, preserve_chains)
    else:
        de = all_possible_de_digi_evolutions(digimon, preserve_chains)
        l = len(de)
        print("{d} all possible de-digi-evolutions ({l}):\n\t{de}".format(d=digimon, l=l, de=de))


if __name__ == "__main__":
    DD_file_str = "digidex.csv"
    DE_file_str = "digi_evolutions.json"
    with open(DD_file_str, "r") as digidexCSV, open(DE_file_str, "r") as DE_file:
        lines = digidexCSV.readlines()
        lines = [line.replace("\n", "").strip() for line in lines]

        features = [s.lower() for s in lines[0].split(",")]
        digimon_dict = {}
        list_of_digimon = []
        for i in range(1, len(lines), len(features)):
            digimon = {}
            for j, header in enumerate(features):
                val = lines[i + j].replace(",", "")
                try:
                    val = float(val)
                except ValueError:
                    pass
                digimon[header.lower()] = val
            digi = Digimon(*digimon.values())
            list_of_digimon.append(digi)
            digimon_dict[digimon[list(digimon.keys())[0]]] = digimon

        num_featuures = len(features)
        print("num_featuures: " + str(num_featuures) + "\n\tFeatures:\n" + str(features))
        # for d in list_of_digimon:
        # print(d)
        # for k, v in digimon_dict.items():
        # print("\t{0} - {1}".format(k, v))
        # digidex = csv.DictReader(digidexCSV)
        # print(dir(digidex))
        # print("readig\n" + str(digidexCSV.read()))
        # print("Header: " + str(digidex))
        # digimon_names = [row["Name"] for row in digidex]
        # print("Name: " + str(digimon_names))
        # for digimon in digidex:
        # print(digimon)

        # write_evolutions_file(DE_file_str)

        # print("DEFILE: " + str(DE_file))
        evolutions_json = json.load(DE_file)
        digi_names = get_attr(list_of_digimon, "name", F_lowerName)
        for digi, evolutions in evolutions_json.items():
            evolns = [list_of_digimon[digi_names.index(e.lower())] for e in evolutions if e]
            if "+" in digi:
                digis = [d.strip() for d in digi.split("+")]
                for d in digis:
                    # print(list_of_digimon[digi_names.index(d.lower())])
                    list_of_digimon[digi_names.index(d.lower())].set_digi_evolutions(evolns)
                # evol.set_de_digi_evolutions(list_of_digimon[digi_names.index(d.lower())])
            else:
                # print(list_of_digimon[digi_names.index(digi.lower())])
                list_of_digimon[digi_names.index(digi.lower())].set_digi_evolutions(evolns)

        for digimon in list_of_digimon:
            evolns = digimon.digi_evolutions
            for evol in evolns:
                evol.set_de_digi_evolutions(digimon)

        d1 = list_of_digimon[digi_names.index("Koromon".lower())]
        d1 = list_of_digimon[digi_names.index("botamon".lower())]
        d2 = list_of_digimon[digi_names.index("WarGrowlmon".lower())]
        # d2 = list_of_digimon[digi_names.index("bukamon".lower())]
        beelzemonBM = list_of_digimon[digi_names.index("Beelzemon_BM".lower())]

        print("\nd1: {d}, type: {t}\ndigi-evolutions:     {de}\nde-digi-evolutions:  {dde}\nall de_evolutions:   {adde}".format(d=d1, t=type(d1),
                                                                                                   de=d1.digi_evolutions,
                                                                                                   dde=d1.de_digi_evolutions,
                                                                                                                                adde=all_possible_de_digi_evolutions(d1)))
        print("\nd2: {d}, type: {t}\ndigi-evolutions:     {de}\nde-digi-evolutions:  {dde}\nall de_evolutions:   {adde}".format(d=d2, t=type(d2),
                                                                                                   de=d2.digi_evolutions,
                                                                                                   dde=d2.de_digi_evolutions,
                                                                                                                                adde=all_possible_de_digi_evolutions(d2)))
        print("{d1} can digi-evolve to {d2}: {p}".format(d1=d1, d2=d2, p=can_digi_evolve_to(d1, d2, exhaustive=True)))
        print("{d2} can de-digi-evolve to {d1}: {p}".format(d1=d1, d2=d2,
                                                            p=can_de_digi_evolve_to(d2, d1, exhaustive=True)))

        champion_digimon = get_attr(list_of_digimon, "self", filter_func=lambda d: d.stage == DigiStages.CHAMPION)
        print("champion digimon:\t" + str(champion_digimon))
        # show_all_possible_digi_evolutions(d2)
        show_all_possible_digi_evolutions(d1, preserve_chains=True)
        d1.print_evolution_tree(digi_evolve=True)
        d2.print_evolution_tree(digi_evolve=False)

        beelzemonBM.print_evolution_tree(digi_evolve=False)
        list_of_digimon[digi_names.index("bakemon".lower())].print_evolution_tree(digi_evolve=True)
        # show_all_possible_de_digi_evolutions(d2)
        # show_all_possible_de_digi_evolutions(d1)

        # for k, v in evolutions_json.items():
        # print("k {0}: - v {1}".format(k, v))

# Increase your ABI, ABI grant bonus to the maximum stats you can achieve (ABI/2 = your bonus) , so if you have 100 ABI, you can have 50 bonus maximum stats
