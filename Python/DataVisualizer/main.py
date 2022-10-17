import os
import json
import csv

from colour_utility import *
from utility import *
import pygame


def gen_race_test_data():
    dates = [random_date(start_year=2000, end_year=2025) for i in range(20)]
    entities = ["A", "B", "C", "D", "E", "F", "G"]
    # generate 1 race times for each entity
    race = lambda _: dict(zip(entities, [weighted_choice([i / 100 for i in range(100)]) for j in
                                         range(len(entities))]))
    # generate a race for each date
    return dict(zip(dates, [race(i) for i in range(len(dates))]))


class DataSet:

    def __init__(self, file_name, mode='daily'):
        self.file_name = file_name
        self.formats = {'daily': "%Y-%m-%d", 'monthly': "%Y-%m", 'annually': "%Y"}
        if mode not in self.formats:
            mode = "daily"
        self.strp_format = self.formats[mode]

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"Cannot find data set file \'{file_name}\'")
        self.data = {}
        self.dates = []
        self.entities = {}
        self.date_range = None, None
        self.data_range = None, None

        self.invalid = True
        entities_passed = False
        with open(file_name, 'r') as f:
            if file_name.endswith('.json'):
                try:
                    json_dat = json.load(f)
                    for i, k_date_v_ekv in enumerate(json_dat.items()):
                        k_date, v_ekv = k_date_v_ekv
                        # Check for 'ENTITIES' KEY
                        if k_date == "ENTITIES":
                            if i == 0:
                                entities_passed = True
                                for k_ent, ent_dat in v_ekv.items():
                                    c_1 = ent_dat["colour"] if ent_dat["colour"].startswith("#") else eval(ent_dat["colour"])
                                    c_2 = ent_dat["border_colour"] if "border_colour" in ent_dat and ent_dat["border_colour"].startswith("#") else eval(ent_dat["border_colour"] if "border_colour" in ent_dat else ent_dat["colour"])
                                    c_3 = ent_dat["font_colour"] if "font_colour" in ent_dat and ent_dat["font_colour"].startswith("#") else eval(ent_dat["font_colour"] if "font_colour" in ent_dat else "BLACK")
                                    c_4 = ent_dat["font_back_colour"] if "font_back_colour" in ent_dat and ent_dat["font_back_colour"].startswith("#") else eval(ent_dat["font_back_colour"] if "font_back_colour" in ent_dat else "WHITE")
                                    self.entities.update({k_ent: {
                                        "name": ent_dat["name"],
                                        "colour": c_1,
                                        "border_colour": c_2,
                                        "font_colour": c_3,
                                        "font_back_colour": c_4,
                                        "image_path": ent_dat["image_path"],
                                        "image": pygame.image.load(ent_dat["image_path"]) if ent_dat["image_path"] is not None else None
                                    }})
                                    # self.data[date_k_date]['Ordered'].append((k_ent, v, self.entities[k_ent]['colour']))
                                    # self.data[date_k_date]['Ordered'].sort(key=lambda tup: tup[1])
                                continue
                            else:
                                raise json.JSONDecodeError("Key \'ENTITIES\' must be the first entry in the json data.", self.file_name, 0)
                        date_k_date = dt.datetime.strptime(k_date, self.strp_format)
                        if self.date_range[0] is None:
                            self.date_range = date_k_date, date_k_date
                        elif date_k_date < self.date_range[0]:
                            self.date_range = date_k_date, self.date_range[1]
                        elif self.date_range[0] < date_k_date:
                            self.date_range = self.date_range[0], date_k_date
                        if date_k_date not in self.data:
                            self.data[date_k_date] = {'Raw': {}, 'Ordered': []}
                        self.dates.append(date_k_date)
                        for k_ent, v in v_ekv.items():
                            if self.data_range[0] is None:
                                self.data_range = v, v
                            elif v < self.data_range[0]:
                                self.data_range = v, self.data_range[1]
                            elif self.data_range[1] < v:
                                self.data_range = self.data_range[0], v
                            self.data[date_k_date]["drange_overall"] = self.data_range[0], self.data_range[1]

                            if entities_passed:
                                if k_ent not in self.entities:
                                    raise ValueError(f"Key \'{k_ent}\' not found in \'ENTITIES\' on date: \'{date_k_date}\'")
                            else:
                                self.entities.update({k_ent: {
                                    "name": "UNNAMED",
                                    "colour": eval("BLACK"),
                                    "border_colour": eval("BLACK"),
                                    "font_colour": eval("BLACK"),
                                    "font_back_colour": eval("WHITE"),
                                    "image_path": None,
                                    "image":  None
                                }})
                            # if k_ent in self.data[date_k_date]['Raw']:
                            self.data[date_k_date]['Raw'].update({k_ent: v})
                            # if not entities_passed:
                            self.data[date_k_date]['Ordered'].append((k_ent, v, (self.entities[k_ent]['colour'], self.entities[k_ent]['border_colour'], self.entities[k_ent]['font_colour'], self.entities[k_ent]['font_back_colour'])))
                            self.data[date_k_date]['Ordered'].sort(key=lambda tup: tup[1])
                    # if entities_passed:
                    #     for date_k_date in self.dates:
                    #         self.data[date_k_date]['Ordered'].append((k_ent, self.data[date_k_date]['Raw'][], self.entities[k_ent]['colour']))
                    #         self.data[date_k_date]['Ordered'].sort(key=lambda tup: tup[1])
                except KeyError as ke:
                    print(f'Invalid json format. KeyError:', ke)
                except json.JSONDecodeError as de:
                    print(f'Invalid json format. JSONDecodeError:', de)
                except ValueError as ve:
                    print(f'Invalid json format. ValueError:', ve)
                else:
                    self.invalid = False

        self.dates.sort()
        print(dict_print(self.entities, n="Entities"))
        print(dict_print(self.data, n="Data"))

    def __len__(self):
        return len(self.data)

    def is_valid(self):
        return not self.invalid

    def top_n(self, n, date_key, reverse=False):
        top_n = None
        try:
            data = self.data[date_key]
            top_n = data['Ordered'][:n]
            if reverse:
                top_n = data['Ordered'][-n:]
                top_n.reverse()
        except KeyError as ke:
            print("KeyError", ke)
        finally:
            return top_n

    def n_data_points(self, date_key):
        if date_key not in self.data:
            raise KeyError(f"\'{date_key}\' key not found in dataset.")
        return len(self.data[date_key]['Raw'])

    def date_keys(self):
        for date in self.dates:
            yield date

    def next_key(self, date_key):
        if date_key not in self.data:
            raise KeyError(f"\'{date_key}\' key not found in dataset.")
        idx = self.dates.index(date_key)
        if idx != len(self.dates) - 1:
            return self.dates[idx + 1]

    def f_data_range(self, date_key, lbound=None, reverse=False, overall=None):
        if overall not in [None, "All", "To Now"]:
            overall = "All"
        if overall == "All":
            # return the calculated overall data_range. Keeps all values from all keys in the right position as "time" passes
            return self.data_range
        elif overall == "To Now":
            return self.data[date_key]["drange_overall"]
        else:
            data_range = None, None
            if self.data[date_key]['Ordered']:
                data_range = self.data[date_key]['Ordered'][0][1], self.data[date_key]['Ordered'][-1][1]
            if data_range[0] is not None and (data_range[0] > data_range[1] or reverse and data_range[0] < data_range[1]):
                data_range[0], data_range = data_range[1], data_range[0]
            if lbound is not None:
                # use this to ensure that all bars have a non-zero width
                if lbound < data_range[0]:
                    data_range = lbound, data_range[1]
            return data_range

    def get_image(self, ent_key):
        if ent_key not in self.entities:
            raise KeyError(f"\'{ent_key}\' key not found in dataset entities.")
        return self.entities[ent_key]["image"]

    def get_colours(self, ent_key):
        if ent_key not in self.entities:
            raise KeyError(f"\'{ent_key}\' key not found in dataset entities.")
        return {
            "colour": self.entities[ent_key]["colour"],
            "border_colour": self.entities[ent_key]["border_colour"],
            "font_colour": self.entities[ent_key]["font_colour"],
            "font_back_colour": self.entities[ent_key]["font_back_colour"]
        }

    def __repr__(self):
        if not self.is_valid():
            return f"< **INVALID** DataSet>"
        return f"<DataSet: Records: {len(self)}, over DateRange: {self.date_range}>"


class DataSetViewer:

    def __init__(self, file_name, frames_per_point=10, time_per_point=1000, name="Untitled Dataset", mode='daily', min_width=10, value_fmt="int", bw=3, marg=15):
        self.valid_fmts = ["int", "float1", "float2", "float1", "float2", "float3", "float4", "float5", "float6", "float7", "float8", "float9", "float0"]
        if value_fmt not in self.valid_fmts:
            raise ValueError(f"value_fmt parameter: \"{value_fmt}\" not recognized.")
        self.name = name
        self.frames_per_point = frames_per_point  # number of frames between data points
        self.time_per_point = time_per_point  # calculated using fps to ensure frames_per_point is shown in the timeframe
        self.value_fmt = value_fmt
        self.marg = marg  # margin
        self.bw = bw  # border width
        self.dataset = DataSet(file_name, mode=mode)
        if not self.dataset.is_valid():
            raise ValueError(f"This dataset cannot be viewed '{self.dataset.file_name}'")
        if not 0 <= min_width < 500:
            raise ValueError(f"Parameter 'min_width' must be a number between 0 < x <= 100. This represents the proportion of the bar that must be shown")
        self.min_width = min_width  # minimum width in pixels, of each bar
        self.dataset_date_keys = self.dataset.date_keys()  # generator to retrieve date keys for this dataset
        self.used_keys = []  # list to track visited date keys
        self.current_key = self.next_date_key()  # the current key for this dataset.data
        # self.current_data_range = self.dataset.data_range(self.current_key, lbound=self.dataset.data_range(self.current_key)[0] - 1)
        self.current_data_range = self.dataset.f_data_range(self.current_key, overall="All")  # store the max and min values in this dataset.

        self.image_dims = None, None
        self.current_frame = -1
        self.current_frame = self.next_frame()
        # print(f"keys? :{self.current_key}")

    # def frames_list(self):
    #     for i in range(self.frames_per_point):
    #         yield i

    def move_next_frame(self):
        self.current_frame = self.next_frame()

    def move_next_date_key(self):
        self.used_keys.append(self.current_key)
        try:
            self.current_key = self.next_date_key()
        except StopIteration:
            print("CAUGHT")
            raise ValueError("Run again?")

    def next_frame(self):
        return (self.current_frame + 1) % self.frames_per_point

    def next_date_key(self):
        return self.dataset_date_keys.__next__()

    def formatter(self, value):
        try:
            if self.value_fmt == self.valid_fmts[0]:
                # int
                return int(value)
            else:
                n = int(self.value_fmt[-1])
                if n == 0:
                    n = 10
                return f"%.{n}f" % value
        except ValueError as ve:
            raise ValueError(f"could not format value: \"{value}\" of type: \"{type(value)}\" to \"{self.value_fmt}\"")

    def compute_move_distance(self, top_n_lst, rect, reverse, ys):
        frame_n = self.current_frame + 1
        pf = frame_n / self.frames_per_point
        next_key = self.dataset.next_key(self.current_key)
        print("")
        drange = self.current_data_range
        top_n = len(top_n_lst)
        next_ents = []
        next_top_n = []
        if next_key:
            next_top_n = self.dataset.top_n(top_n, date_key=next_key, reverse=reverse)
            next_ents = [tup[0] for tup in next_top_n]
        else:
            print(f"len(dataset): {len(self.dataset)}, used_keys: {self.used_keys}")
        top_n_lst_ents = [tnl[0] for tnl in top_n_lst]
        from_bottom = [(i, ent[1], ent[0]) for i, ent in enumerate(next_top_n) if ent[0] not in top_n_lst_ents]
        print(f"top_n_lst: {[tnl[0] for tnl in top_n_lst]}")
        print(f"next_ents: {next_ents}")
        print(f"from_bottom: {from_bottom}")

            # for c_key, c_v, c_c in top_n_lst:
        # for c_key, c_v, c_c in top_n_lst:
        #     # print(f"ckey: {c_key} not in next_ents")
        #     if c_key not in next_ents:
        #         print(f"ckey: {c_key} not in next_ents")
        # print(f"top_n:{top_n_lst}, next:{next_top_n}")
        y_diffs = []
        x_diffs = []
        v_diffs = []

        tw = rect.w
        TTLS = {}
        for i, pair in enumerate(top_n_lst):
            v1 = self.dataset.data[self.current_key]['Raw'][pair[0]]  # the value
            if next_key is None:
                p = abs(v1 - drange[0]) / abs(drange[1] - drange[0])
                x_diff = rect.w - (p * tw)
                v2 = v1  # next value
                vd = (v2 - v1)
                vx = vd * pf
                vx += v1
                v_diffs.append(vx)
                vx = (rect.w - self.min_width) * (abs(vx - drange[0]) / abs(drange[1] - drange[0]))
                vx += self.min_width
                x_diffs.append(vx)
                y_diffs.append(0)
                print("LAST")
                continue
            n_idx = None
            fbie = [(fbi, fbv, fbe) for fbi, fbv, fbe in from_bottom if fbi == i]
            print(f"FBIE: {fbie}")
            if fbie:
                # raise ValueError(f"Raising e: {fbie[0]} from the bottom to {i}")

                # v_diffs.append(drange[0])
                # x_diffs.append(((fbie[0][1] - drange[0]) * pf) + drange[0])
                # y_diffs.append((rect.bottom - ys[i]) * pf)
                # continue
                pass
                # raise ValueError(f"Raising e: {fbie[0][1]} from the bottom to {i}")
            if pair[0] not in next_ents:
                # go to bottom:
                ogy = ys[i]
                nwy = rect.bottom
            else:
                ogy = ys[i]
                n_idx = next_ents.index(pair[0])
                nwy = ys[n_idx]

            y_diff = nwy - ogy
            y_diff *= pf
            y_diffs.append(y_diff)

            v2 = self.dataset.data[next_key]['Raw'][pair[0]]  # next value
            vd = (v2 - v1)
            vx = vd * pf
            vx += v1
            v_diffs.append(vx)
            vx = (rect.w - self.min_width) * (abs(vx - drange[0]) / abs(drange[1] - drange[0]))
            vx += self.min_width
            x_diffs.append(vx)

            # TTLS.update({i: {"pair": pair, "CK": self.current_key, "v1->v2": f"({v1}->{v2})", "vd": vd, "vx": vx, "fn / fpp": f"({frame_n} / {self.frames_per_point})", "pf": pf, "W": rect.w}})


        # print(dict_print(TTLS))
        # print(f"RESULT 1: {y_diffs}")
        # print(f"RESULT 2: {x_diffs}")
        # print(f"RESULT 3: {v_diffs}")
        return x_diffs, y_diffs, v_diffs, from_bottom

    def draw(self, window, top_num=None, reverse=False):
        frame_n = self.current_frame + 1
        pf = frame_n / self.frames_per_point
        bw = self.bw
        marg = self.marg
        date_key = self.current_key
        n_points = top_num
        nps = self.dataset.n_data_points(date_key)
        if top_num is None:
            n_points = nps
            if n_points > 5:
                n_points = 5
        top_num = clamp(0, n_points, nps)
        # print(f"top_n: {top_num}")
        rect = window.get_rect()
        top_n = self.dataset.top_n(top_num, date_key, reverse=reverse)
        drange = self.current_data_range
        # if reverse and drange[0] < drange[1]:
        #     self.current_data_range = self.current_data_range[1], self.current_data_range[0]
        # elif not reverse and drange[1] < drange[0]:
        #     self.current_data_range = self.current_data_range[1], self.current_data_range[0]

        # title
        text_surface = FONT_DEFAULT.render(self.window_name(), True, GREEN_4, GRAY_27)
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.y = 10
        window.blit(text_surface, text_rect)

        # date_key
        text_surface = FONT_DEFAULT.render(f"Today: {self.current_key.strftime(self.dataset.strp_format)}", True, GREEN_4, GRAY_27)
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.y = text_rect.bottom + 10
        window.blit(text_surface, text_rect)

        # backdrop
        rem_h = rect.height - text_rect.bottom
        d_rect = pygame.Rect(marg, text_rect.bottom + marg, rect.width - (2 * marg), rem_h - (2 * marg))
        pygame.draw.rect(window, SNOW_3, d_rect)

        h = (((d_rect.h * 0.8) - (2 * marg)) / len(top_n)) * 0.9
        bw = clamp(0, bw, h - (2 * bw))
        hx = int(h - (2 * bw))
        if self.image_dims[0] is None or self.image_dims[1] != hx:
            self.image_dims = hx, hx
            for ent, ent_dat in self.dataset.entities.items():
                if ent_dat["image"] is not None:
                    # raise ValueError(f"hx: {hx}")
                    ent_dat["image"] = pygame.transform.scale(ent_dat["image"], (hx, hx))
        # print(f"h:{h}, dr:{d_rect}")
        ys = [d_rect.y + ((h + marg) * i) + (h / 2) for i in range(len(top_n))]
        # xs =

        # place labels
        for i in range(top_num):
            text_surface = FONT_DEFAULT.render(f"{i+1}", True, GREEN_4, GRAY_27)
            text_rect = text_surface.get_rect()
            text_rect.x = d_rect.x + marg
            # text_rect.y = d_rect.y + ((i + 0.5) * (h + (2 * marg)))
            text_rect.y = ys[i] + (h / 2) - marg
            window.blit(text_surface, text_rect)

        left_most = text_rect.right + marg
        bar_rect = pygame.Rect(d_rect)
        bar_rect.x += left_most
        bar_rect.w -= left_most
        pygame.draw.rect(window, SNOW_4, bar_rect)
        *move_distances, from_bottom = self.compute_move_distance(top_n, bar_rect, reverse, ys)

        # print(f"md: {move_distances}")
        # print("data_range:", drange)
        # print("\n\t" + "\n\t".join(list(map(str, [ys, move_distances[0], move_distances[1], top_n]))))
        # print(f"lens({len(ys)}, {len(move_distances[0])}, {len(move_distances[1])}, {len(top_n)})")

        # print(f"lens({ys}, {move_distances[0]}, {move_distances[1]}, {top_n})")
        # drange = drange[0], drange[1] + self.min_width
        drange = drange[0], drange[1]
        for i, yxdydvdt in enumerate(zip(ys, *move_distances, top_n)):
            y, xd, yd, vd, ent = yxdydvdt
            ent, v, colours = ent
            colour, border_colour, font_colour, font_back_colour = colours
            p = (v - drange[0]) / (drange[1] - drange[0])
            w = xd

            # print(f"\t{v=}, {drange=}, {p=}, f= {v - drange[0]} / {drange[1] - drange[0]}: {p=}")
            # print(f"\tRESULT: {pygame.Rect(bar_rect.x, y + yd, w, h)}")
            # print(f"\t{w=}, {left_most=}, {p=}, {bar_rect.w=}, {v=}, {drange=}, numer={abs(v - drange[0])} / denom={abs(drange[1] - drange[0])}, Rw={bar_rect.w - left_most}, {p * (bar_rect.w - left_most)}, {xd=}, {yd=}")

            # w = (1 * (d_rect.w - left_most)) + xd
            # pygame.draw.rect(window, border_colour, pygame.Rect(left_most, y + yd, w, h))
            # pygame.draw.rect(window, colour, pygame.Rect(left_most + bw, y + yd + bw, w - (2 * bw), h - (2 * bw)))
            # w =
            final_bar_rect = pygame.Rect(bar_rect.x, y + yd, w, h)
            pygame.draw.rect(window, border_colour, final_bar_rect)
            pygame.draw.rect(window, colour, pygame.Rect(bar_rect.x + bw, y + yd + bw, w - (2 * bw), h - (2 * bw)))
            text_surface = FONT_DEFAULT.render(f"{ent}: {self.formatter(vd)}", True, font_colour, font_back_colour)
            name_rect = text_surface.get_rect()
            name_rect.x = w + left_most - name_rect.w - (marg / 2)
            # print(f"name: {ent} name_rect: {name_rect}")
            # name_rect.centery = y + yd + marg  # top of the bar
            name_rect.centery = final_bar_rect.centery  # center of the bar
            # print(f"ENT: {ent}, t: {type(ent)}")
            image = self.dataset.get_image(ent)
            if ent is not None and image is not None:
                name_rect.x -= hx
                window.blit(image, pygame.Rect(bar_rect.x - (hx + 10) + bw, y + yd + bw, w, h).topright)
            window.blit(text_surface, name_rect)

        # # self.current_frame = self.next_frame()
        # next_key = self.dataset.next_key(self.current_key)
        # print("")
        # drange = self.current_data_range
        # # top_n = len(top_n_lst)
        # next_ents = []
        # next_top_n = []
        # if next_key:
        #     next_top_n = self.dataset.top_n(top_n, date_key=next_key, reverse=reverse)
        #     next_ents = [tup[0] for tup in next_top_n]
        # else:
        #     print(f"len(dataset): {len(self.dataset)}, used_keys: {self.used_keys}")
        if from_bottom:
            for place, value, ent_name in from_bottom:
                v1 = 2
                vd = ((v1 - value) * pf) + v1
                w = 300
                colour, border_colour, font_colour, font_back_colour = list(self.dataset.get_colours(ent_name).values())

                hd = (bar_rect.h - ys[place]) * pf
                hd = ys[place-1] + ((bar_rect.h - ys[place]) * (1 - pf))
                final_bar_rect = pygame.Rect(bar_rect.x, bar_rect.y + hd, w, h)
                pygame.draw.rect(window, border_colour, final_bar_rect)
                pygame.draw.rect(window, colour, pygame.Rect(bar_rect.x + bw, bar_rect.y + hd + bw, w - (2 * bw), h - (2 * bw)))
                text_surface = FONT_DEFAULT.render(f"{ent_name}: {self.formatter(vd)}", True, font_colour, font_back_colour)
                name_rect = text_surface.get_rect()
                name_rect.x = w + left_most - name_rect.w - (marg / 2)
                # print(f"name: {ent} name_rect: {name_rect}")
                # name_rect.centery = y + yd + marg  # top of the bar
                name_rect.centery = final_bar_rect.centery  # center of the bar
                # print(f"ENT: {ent}, t: {type(ent)}")
                image = self.dataset.get_image(ent_name)
                if ent_name is not None:
                    name_rect.x -= hx
                    window.blit(image, pygame.Rect(bar_rect.x - (hx + 10) + bw, bar_rect.y + hd + bw, w, h).topright)
                window.blit(text_surface, name_rect)



    def window_name(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<DataSetViewer name={self.name}>"


if __name__ == "__main__":
    # ds1 = DataSetViewer("dataset_001.json", frames_per_point=50, min_width=0)
    FPP = 100
    FPS = 10
    TPP = FPP / FPS
    # ds1 = DataSetViewer("dataset_004.json", frames_per_point=25, min_width=100, value_fmt="float3")
    ds1 = DataSetViewer("dataset_nhl_team_wins.json", mode="annually", name="Stanley Cup Winners 1927-2022", frames_per_point=15, min_width=300, value_fmt="int")
    # ds1 = DataSetViewer("dataset_nhl_team_losses.json", mode="annually", name="Stanley Cup Runner-Ups 1927-2022", frames_per_point=15, min_width=300, value_fmt="int")
    # ds1 = DataSetViewer("dataset_nhl_team_apperances.json", mode="annually", name="Stanley Cup Appearances 1927-2022", frames_per_point=15, min_width=300, value_fmt="int")
    # print(ds1.dataset)
    # print(f'top_(3): {ds1.dataset.top_n(3, ds1.dataset.date_range[0], 1)}')
    # print(f'top_(8): {ds1.dataset.top_n(8, ds1.dataset.date_range[0])}')

    pygame.init()
    WIDTH, HEIGHT = 1600, 950
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

    while running:
        CLOCK.tick(FPS)
        last_frame = ds1.current_frame
        ds1.move_next_frame()
        new_frame = ds1.current_frame
        if new_frame < last_frame:
            ds1.move_next_date_key()

        # reset window
        WINDOW.fill(BLACK)

        # begin drawing
        ds1.draw(WINDOW, top_num=15, reverse=True)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # update the display
        pygame.display.update()

    pygame.quit()
#
# # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
# # text_rect = text_surface.get_rect()
# # text_rect.center = WINDOW.get_rect().center
# # WINDOW.blit(text_surface, text_rect)
