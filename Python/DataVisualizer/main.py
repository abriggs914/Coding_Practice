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
        self.entities = []
        self.date_range = None, None

        self.invalid = True
        with open(file_name, 'r') as f:
            if file_name.endswith('.json'):
                try:
                    json_dat = json.load(f)
                    for k_date, v_ekv in json_dat.items():
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
                            if k_ent not in self.entities:
                                self.entities.append(k_ent)
                            if k_ent in self.data[date_k_date]['Raw']:
                                raise ValueError(f"Key \'{k_ent}\' already has an entry for date: \'{date_k_date}\'")
                            self.data[date_k_date]['Raw'].update({k_ent: v})
                            self.data[date_k_date]['Ordered'].append((k_ent, v, random_color()))
                            self.data[date_k_date]['Ordered'].sort(key=lambda tup: tup[1])
                except KeyError as ke:
                    print(f'Invalid json format. KeyError:', ke)
                except ValueError as ve:
                    print(f'Invalid json format. ValueError:', ve)
                else:
                    self.invalid = False

        self.dates.sort()
        self.entities.sort()

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

    def date_keys(self):
        for date in self.dates:
            yield date

    def next_key(self, date_key):
        if date_key not in self.data:
            raise KeyError(f"\'{date_key}\' key not found in dataset.")
        idx = self.dates.index(date_key)
        if idx != len(self.dates) - 1:
            return self.dates[idx + 1]

    def __repr__(self):
        if not self.is_valid():
            return f"< **INVALID** DataSet>"
        return f"<DataSet: Records: {len(self)}, over DateRange: {self.date_range}>"


class DataSetViewer:

    def __init__(self, file_name, frames_per_point=10, time_per_point=1000, name="Untitled Dataset", mode='daily'):
        self.name = name
        self.frames_per_point = frames_per_point
        self.time_per_point = time_per_point
        self.dataset = DataSet(file_name, mode=mode)
        if not self.dataset.is_valid():
            raise ValueError(f"This dataset cannot be viewed \'{self.dataset.file_name}\'")
        self.dataset_date_keys = self.dataset.date_keys()
        self.current_key = self.next_date_key()
        self.current_frame = -1
        self.current_frame = self.next_frame()
        print(f"keys? :{self.current_key}")

    # def frames_list(self):
    #     for i in range(self.frames_per_point):
    #         yield i

    def move_next_frame(self):
        self.current_frame = self.next_frame()

    def move_next_date_key(self):
        self.current_key = self.next_date_key()

    def next_frame(self):
        return (self.current_frame + 1) % self.frames_per_point

    def next_date_key(self):
        return self.dataset_date_keys.__next__()

    def compute_move_distance(self, top_n_lst, rect, reverse, ys):
        frame_n = self.current_frame + 1
        next_key = self.dataset.next_key(self.current_key)
        top_n = len(top_n_lst)
        if next_key is None:
            pass
        next_top_n = self.dataset.top_n(top_n, date_key=next_key, reverse=reverse)
        next_ents = [tup[0] for tup in next_top_n]
        # print(f"top_n:{top_n_lst}, next:{next_top_n}")
        y_diffs = []

        for i, pair in enumerate(top_n_lst):
            n_idx = None
            if pair[0] not in next_ents:
                # go to bottom:
                ogy = ys[i]
                nwy = rect.bottom
            else:
                ogy = ys[i]
                n_idx = next_ents.index(pair[0])
                nwy = ys[n_idx]
            print(f"ogy:{ogy}, ony:{nwy}, place_change=o={i}->n:{n_idx}")
            diff = nwy - ogy
            p = frame_n / self.frames_per_point
            # print(f"diff:{diff}, p: {p}")
            diff *= p
            y_diffs.append(diff)
        # print(f"RESULT: {y_diffs}")
        return y_diffs

    def draw(self, window, top_num=5, reverse=False):
        date_key = self.current_key
        rect = window.get_rect()
        top_n = self.dataset.top_n(top_num, date_key, reverse=reverse)

        # title
        text_surface = FONT_DEFAULT.render(self.window_name(), True, GREEN_4, GRAY_27)
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.y = 10
        window.blit(text_surface, text_rect)

        # date_key
        text_surface = FONT_DEFAULT.render(f"Today: {self.current_key}", True, GREEN_4, GRAY_27)
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.y = text_rect.bottom + 10
        window.blit(text_surface, text_rect)

        # backdrop
        marg = 15
        rem_h = rect.height - text_rect.bottom
        d_rect = pygame.Rect(marg, text_rect.bottom + marg, rect.width - (2 * marg), rem_h - (2 * marg))
        pygame.draw.rect(window, SNOW_3, d_rect)

        h = (((d_rect.h * 0.8) - (2 * marg)) / len(top_n)) * 0.9
        # print(f"h:{h}, dr:{d_rect}")
        ys = [d_rect.y + ((h + marg) * i) + (h / 2) for i in range(len(top_n))]

        # place labels
        for i in range(top_num):
            text_surface = FONT_DEFAULT.render(f"{i}", True, GREEN_4, GRAY_27)
            text_rect = text_surface.get_rect()
            text_rect.x = d_rect.x + marg
            # text_rect.y = d_rect.y + ((i + 0.5) * (h + (2 * marg)))
            text_rect.y = ys[i] + (h / 2) - marg
            window.blit(text_surface, text_rect)

        move_distances = self.compute_move_distance(top_n, d_rect, reverse, ys)
        print(f"md: {move_distances}")
        for i, yydt in enumerate(zip(ys, move_distances, top_n)):
            y, yd, ent = yydt
            colour = ent[2]
            pygame.draw.rect(window, colour, pygame.Rect(text_rect.right + marg, y + yd, 200, h))
        # self.current_frame = self.next_frame()



    def window_name(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<DataSetViewer name={self.name}>"


if __name__ == "__main__":
    ds1 = DataSetViewer("dataset_001.json",frames_per_point=100)
    print(ds1.dataset)
    print(f'top_(3): {ds1.dataset.top_n(3, ds1.dataset.date_range[0], 1)}')
    print(f'top_(8): {ds1.dataset.top_n(8, ds1.dataset.date_range[0])}')

    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 10

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
        ds1.draw(WINDOW, top_num=4)
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
