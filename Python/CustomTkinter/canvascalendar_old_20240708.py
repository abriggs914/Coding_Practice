
class CalendarCanvas_OLD(ctk.CTkCanvas):
    def __init__(
            self,
            master,
            year: int | None = datetime.datetime.now().year,
            show_weekdays: bool = True,
            months_per_row: int = 4,
            width: int = 600,
            height: int = 700,
            colour_background_canvas: Colour = Colour("#AEBEBE"),
            colour_foreground_canvas: Colour = Colour("#000000"),
            colour_background_owned_number_check: Colour = Colour("#2A4AFA"),
            colour_background_header_year: Colour = Colour("#627272"),
            colour_background_header_month: Colour = Colour("#7B8B8B"),
            colour_background_header_weekday: Colour = Colour("#94A4A4"),
            colour_background_canvas_selected: Colour = Colour("#081688"),
            colour_foreground_canvas_selected: Colour = Colour("#FFFFFF"),
            colour_scheme_month: dict[int: Colour] = None,
            colour_scheme_day: dict[tuple[int, int]: Colour] = None,
            hover_style: Literal[None, "darken", "brighten"] = "brighten",
            invalid_style: Literal[None, "darken", "brighten", "invisible"] = None,
            show_all_rows: bool = False,
            selectable: bool = False,
            *args, **kwargs
    ):
        super().__init__(master=master, *args, **kwargs)

        # colour_scheme_month overrides the default colours

        self.year: None | int = year
        self.show_weekdays = show_weekdays and bool(self.year)
        self.show_all_rows = show_all_rows
        self.selectable = selectable
        self.selected_date = ctk.Variable(self, value=None)
        self.months_per_row = clamp(3, months_per_row, 4)
        self.weeks_per_month = 6 + 1  # for the month label
        self.weeks_per_month += (1 if self.show_weekdays else 0)  # offset for weekday labels
        self.weeks_per_month -= (1 if self.year is None else 0)  # offset for weekday labels
        # self.n_rows: int = ((self.weeks_per_month + int(self.show_weekdays)) * (12 // self.months_per_row)) + 1
        self.n_rows: int = (self.weeks_per_month * (12 // self.months_per_row)) + int(self.show_weekdays)
        self.n_cols: int = 7 * self.months_per_row
        self.w_canvas: int = width
        self.h_canvas: int = height
        self.colour_background_canvas = colour_background_canvas
        self.colour_foreground_canvas = colour_foreground_canvas
        self.colour_background_owned_number_check = colour_background_owned_number_check
        self.colour_background_header_year = colour_background_header_year
        self.colour_background_header_month = colour_background_header_month
        self.colour_background_header_weekday = colour_background_header_weekday
        self.colour_background_canvas_selected = colour_background_canvas_selected
        self.colour_foreground_canvas_selected = colour_foreground_canvas_selected
        self.colour_scheme_month: dict[int: Colour] = self.validate_colour_scheme(colour_scheme_month) if colour_scheme_month is not None else dict()
        # self.colour_scheme_day: dict[tuple[int, int]: Colour] = self.validate_colour_scheme(colour_scheme_day) if colour_scheme_day is not None else dict()
        self.colour_scheme_day: dict[tuple[int, int]: Colour] = colour_scheme_day if colour_scheme_day is not None else dict()
        self.hover_style = hover_style
        self.invalid_style = invalid_style
        self.v_cell_ids_hovered = ctk.Variable(self, value=None)
        self.v_cell_ids_selected = ctk.Variable(self, value=None)
        self.max_days_per_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.configure(
            width=self.w_canvas,
            height=self.h_canvas,
            background=self.colour_background_canvas.hex_code
        )
        self.gc = grid_cells(
            t_width=self.w_canvas,
            n_cols=self.n_cols,
            t_height=self.h_canvas,
            n_rows=self.n_rows,
            # x_pad=4,
            # y_pad=4,
            r_type=list
        )
        self.dict_canvas_tags = dict()
        self.set_date_cells = set()
        self.dict_cell_to_cal_idx = dict()
        self.date_to_cell = dict()

        self.disabled_cells = set()

        ri = 1 if self.year is not None else 0

        for i, row in enumerate(self.gc):
            for j, coords in enumerate(row):
                n = ((i * self.n_cols) + j) + 1
                # if n == 100:
                #     # no #100
                #     break
                x0, y0, x1, y1 = coords
                # cal_idx = (j // 7) + (i // 7)  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
                # cal_idx = (j // 7) + (i // (self.weeks_per_month + 1))  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
                # cal_idx = (j // 7) + (max(0, i - (1 + sum([bool(self.year), self.show_weekdays]))) // (
                #             self.weeks_per_month + 1))  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))

                # j//7
                # j = c_i // self.months_per_row
                # ri0 = ri + (j * self.weeks_per_month)
                # ci0 = (c_i % self.months_per_row) * 7
                # cal_idx =
                p_a = j // 7
                p_ba = (i - ri) // (self.weeks_per_month + self.show_weekdays)
                p_bb = p_ba * self.months_per_row
                cal_idx = p_a + p_bb
                self.dict_cell_to_cal_idx[(i, j)] = cal_idx

                cs = self.colour_scheme_month.get(cal_idx, {})
                col_wd = cs.get("colour_background_canvas", self.colour_background_canvas)
                col_wd_txt = cs.get("colour_foreground_canvas", col_wd.font_foreground_c())
                # print(f"{i=}, {j=}, {cal_idx=}, {p_a=}, {p_ba=}, {p_bb=}, col_wd={col_wd.hex_code}, col_wd_txt={col_wd_txt.hex_code}, {cs=}")
                tr = self.create_rectangle(
                    x0, y0, x1, y1, fill=col_wd.hex_code
                )
                tt = self.create_text(
                    x0 + ((x1 - x0) / 2), y0 + ((y1 - y0) / 2),
                    fill=col_wd_txt.hex_code,
                    text=f"{n}"
                )
                if self.selectable:
                    for tag in (tr, tt):
                        self.tag_bind(
                            tag,
                            "<Button-1>",
                            lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
                        )

                self.set_date_cells.add((i, j))
                self.dict_canvas_tags[(i, j)] = {
                    "rect": tr,
                    "text": tt
                }
                if (hs := self.hover_style) is not None:
                    for tag in (tr, tt):
                        self.tag_bind(tr, "<Motion>", lambda event, i_=i, j_=j, t_=tag: self.motion_cell(event, i_, j_, t_))

        self.dict_canvas_tags["header_year"] = {"rect": None, "text": None}
        self.dict_canvas_tags["header_month"] = {"rect": None, "text": None}
        self.dict_canvas_tags["header_weekday"] = {"rect": None, "text": None}

        if self.year is not None:
            # hide top row cells
            for j in range(self.n_cols):
            #     for tag_name in ("rect", "text"):
            #         self.itemconfigure(
            #             self.dict_canvas_tags[(0, j)][tag_name],
            #             state="hidden"
            #         )
                self.set_date_cells.discard((0, j))

            # create a new rectangle for the year label row
            bbox_year = (
                *self.gc[0][0][:2],
                *self.gc[0][-1][-2:]
            )
            w = bbox_year[2] - bbox_year[0]
            h = bbox_year[3] - bbox_year[1]
            self.dict_canvas_tags["header_year"].update({
                "rect": self.create_rectangle(
                    *bbox_year,
                    fill=self.colour_background_header_year.hex_code
                ),
                "text": self.create_text(
                    bbox_year[0] + (w / 2),
                    bbox_year[1] + (h / 2),
                    text=f"{self.year}",
                    fill=self.colour_background_header_year.font_foreground(rgb=False)
                )
            })

        # blank month row
        # for j in range(self.n_cols):
        #     self.set_date_cells.discard((ri, j))
        #     for tag_name in ("rect", "text"):
        #         self.itemconfigure(
        #             self.dict_canvas_tags[(ri, j)][tag_name],
        #             state="hidden"
        #         )
        self.dict_canvas_tags["header_month"] = list()
        print(f"gc={self.gc}")
        for c_i in range(12):
            j = c_i // self.months_per_row
            ri0 = ri + (j * self.weeks_per_month)
            ci0 = (c_i % self.months_per_row) * 7
            print(f"{c_i=}, {j=}, {ri0=}, {ci0=}")
            month_name = calendar.month_name[c_i + 1]
            bbox_month = (
                *self.gc[ri0][ci0][:2],
                *self.gc[ri0][ci0 + 7 - 1][-2:]
            )
            w = bbox_month[2] - bbox_month[0]
            h = bbox_month[3] - bbox_month[1]
            cs = self.colour_scheme_month.get(c_i, {})
            col_hm = cs.get("colour_background_header_month", self.colour_background_header_month)
            col_txt = cs.get("colour_foreground_header_month", col_hm.font_foreground_c())
            self.dict_canvas_tags[f"header_month"].append({
                "rect": self.create_rectangle(
                    *bbox_month,
                    fill=col_hm.hex_code
                ),
                "text": self.create_text(
                    bbox_month[0] + (w / 2),
                    bbox_month[1] + (h / 2),
                    text=f"{month_name}",
                    fill=col_txt.hex_code
                ),
                "weekdays": list()
            })
            print(f"{month_name[:3].upper()}: {bbox_month=}")

            col_hw = cs.get("colour_background_header_weekday", self.colour_background_header_weekday)
            if self.show_weekdays:
                ri0 += 1
                for k in range(self.n_cols):
                    self.itemconfigure(
                        self.dict_canvas_tags[(ri0, k)]["rect"],
                        fill=col_hw.hex_code
                    )
                    self.set_date_cells.discard((ri0, k))
        # print(f"{self.dict_canvas_tags['header_month']=}")

        self.time_after_motion = 3600
        self.id_after_motion = None

        self.calc_days()
        self.selected_date.trace_variable("w", self.update_selected_date)

    # def deselect_day(self, day_in: int | datetime.datetime = None, month_in: Optional[int] = None)
    def deselect_day(self):
        last_select: tuple[int, int] = self.v_cell_ids_selected.get()
        print(f"{last_select=}")
        if last_select:
            cal_idx_lh = self.dict_cell_to_cal_idx[last_select]
            cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
            col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
            col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
            self.itemconfigure(
                self.dict_canvas_tags[last_select]["rect"],
                fill=col_lh.hex_code
            )
            self.itemconfigure(
                self.dict_canvas_tags[last_select]["text"],
                fill=col_txt_lh.hex_code
            )

    def disable_day(self, day_in: int | datetime.datetime, month_in: Optional[int] = None):
        if isinstance(day_in, datetime.datetime):
            m_idx = day_in.month - 1
            d_idx = day_in.day
            if not (0 <= m_idx < 12):
                raise ValueError(f"Param 'month_in' must be between 1 and 12, representing the months of the year.")
            if not (1 <= d_idx <= self.max_days_per_month[m_idx]):
                raise ValueError(f"Param 'day_in' must be between 1 and {self.max_days_per_month[m_idx]}, since you supplied 'month_idx'={m_idx + 1}, the maximum number of days can only be {self.max_days_per_month[m_idx]} for {calendar.month_name[m_idx + 1]}.")

        else:
            m_idx, d_idx = month_in, day_in
        i, j = self.date_to_cell[(m_idx, d_idx)]

        # self.click_canvas(None, i, j)
        if (i, j) not in self.disabled_cells:
            self.disabled_cells.add((i, j))
            tr = self.dict_canvas_tags[(i, j)]["rect"]
            tt = self.dict_canvas_tags[(i, j)]["text"]
            cs = self.colour_scheme_month.get(m_idx, {})
            ds = self.colour_scheme_day.get((m_idx, d_idx), {})
            bg, fg = None, None
            if ds:
                bg = ds.get("colour_background_canvas")
                fg = ds.get("colour_foreground_canvas")
            if not bg:
                bg = cs.get("colour_background_canvas")
            if not fg:
                fg = cs.get("colour_foreground_canvas")
            if not bg:
                bg = self.colour_background_canvas.darkened(0.3)
            if not fg:
                fg = self.colour_foreground_canvas.darkened(0.3)

            # is_ = self.invalid_style[]
            self.itemconfigure(tt, fill=fg.hex_code)
            self.itemconfigure(tr, fill=bg.hex_code)


    def disable_date(self, date_in: datetime.datetime):
        if self.year is None:
            raise ValueError(f"Please use CalendarCanvas.disable_day when disabling a cell on a calendar with no specified year.")

        d1 = datetime.datetime(self.year, 1, 1)
        d2 = datetime.datetime(self.year, 12, 31, 23, 59, 59, 999999)
        if not (d1 <= date_in <= d2):
            raise ValueError(f"Param 'date_in' must be between {d1:%Y-%m-%d} and {d2:%Y-%m-%d} at end of day. Got {date_in:%x}")

        i, j = self.date_to_cell[date_in]

        if (i, j) not in self.disabled_cells:
            cal_idx = date_in.month - 1
            self.disabled_cells.add((i, j))

            tr = self.dict_canvas_tags[(i, j)]["rect"]
            tt = self.dict_canvas_tags[(i, j)]["text"]
            cs = self.colour_scheme_month.get(cal_idx, {})
            ds = self.colour_scheme_day.get((date_in.month, date_in.day), {})
            bg, fg = None, None
            if ds:
                bg = ds.get("colour_background_canvas")
                fg = ds.get("colour_foreground_canvas")
            if not bg:
                bg = cs.get("colour_background_canvas")
            if not fg:
                fg = cs.get("colour_foreground_canvas")
            if not bg:
                bg = self.colour_background_canvas.darkened(0.3)
            if not fg:
                fg = self.colour_foreground_canvas.darkened(0.3)

            # is_ = self.invalid_style[]
            self.itemconfigure(tt, fill=fg.hex_code)
            self.itemconfigure(tr, fill=bg.hex_code)

    def select_day(self, day_in: int | datetime.datetime, month_in: Optional[int] = None):
        if isinstance(day_in, datetime.datetime):
            m_idx = day_in.month - 1
            d_idx = day_in.day
            if not (0 <= m_idx < 12):
                raise ValueError(f"Param 'month_in' must be between 1 and 12, representing the months of the year.")
            if not (1 <= d_idx <= self.max_days_per_month[m_idx]):
                raise ValueError(f"Param 'day_in' must be between 1 and {self.max_days_per_month[m_idx]}, since you supplied 'month_idx'={m_idx + 1}, the maximum number of days can only be {self.max_days_per_month[m_idx]} for {calendar.month_name[m_idx + 1]}.")

        else:
            m_idx, d_idx = month_in, day_in
        i, j = self.date_to_cell[(m_idx, d_idx)]
        self.click_canvas(None, i, j)


    def select_date(self, date_in: datetime.datetime):
        if self.year is None:
            raise ValueError(f"Please use CalendarCanvas.select_day when selecting a cell on a calendar with no specified year.")

        d1 = datetime.datetime(self.year, 1, 1)
        d2 = datetime.datetime(self.year, 12, 31, 23, 59, 59, 999999)
        if not (d1 <= date_in <= d2):
            raise ValueError(f"Param 'date_in' must be between {d1:%Y-%m-%d} and {d2:%Y-%m-%d} at end of day. Got {date_in:%x}")

        i, j = self.date_to_cell[date_in]

        self.click_canvas(None, i, j)

    def validate_colour_scheme(self, colour_scheme_month) -> dict[int: Colour]:
        if not isinstance(colour_scheme_month, dict):
            raise ValueError(f"Param 'colour_scheme_month' must be an instance of a dictionary. Got '{type(colour_scheme_month)}'")

        valid_style_keys = {
            "colour_background_canvas": iscolour,
            "colour_background_owned_number_check": iscolour,
            "colour_background_header_month": iscolour,
            "colour_background_header_weekday": iscolour,

            "colour_foreground_canvas": iscolour,
            "colour_foreground_header_month": iscolour,

            "colour_background_canvas_selected": iscolour,
            "colour_foreground_canvas_selected": iscolour
        }

        result = {}

        for k, scheme_data in colour_scheme_month.items():
            if not isinstance(k, int):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer key. Got '{k}'")
            if not (0 <= k < 12):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer keys between 0 and 11. Got '{k}'")
            if not isinstance(scheme_data, dict):
                raise ValueError(f"Param 'scheme_data' must be an instance of a dict. Got '{scheme_data}'")
            result[k] = dict()
            for k_style, v in scheme_data.items():
                if k_style not in valid_style_keys:
                    raise ValueError(f"Style key '{k_style}' is not recognized. Must be an one of: {', '.join(valid_style_keys)}")
                try:
                    col = Colour(v)
                except Colour.ColourCreationError:
                    raise ValueError(f"Param 'colour_scheme_month' must only have Colour objects or equivalent as values. Got '{k}'")
                result[k][k_style] = col

        return result

    def calc_days(self):
        ri = 2 if self.year is not None else 1
        is_ = self.invalid_style
        if self.year is not None:
            # for i, data in enumerate(self.dict_canvas_tags["header_month"]):

            for cal_i in range(12):
                day_one = datetime.datetime(self.year, cal_i + 1, 1)
                wd_d1 = day_one.isoweekday() % 7
                j = cal_i // self.months_per_row
                cs = self.colour_scheme_month.get(cal_i, {})
                for wk_i in range(self.weeks_per_month - 1):
                    used_row = False
                    ri0 = ri + (j * self.weeks_per_month) + wk_i
                    for wkd_i in range(7):
                        ds = self.colour_scheme_day[(day_one.month, day_one.day)]
                        str_day = f"{day_one.day}"
                        ci0 = ((cal_i % self.months_per_row) * 7) + wkd_i
                        # print(f"{day_one:%Y-%m-%d}, {cal_i=}, {j=}, {ri0=}, {ci0=}, {wk_i=}, {wkd_i=}, {wd_d1=}", end="")
                        # month_name = calendar.month_name[cal_i + 1]
                        tag_txt = self.dict_canvas_tags[(ri0, ci0)]["text"]
                        tag_rect = self.dict_canvas_tags[(ri0, ci0)]["rect"]

                        s = ds if ds else cs  # TODO this won't work right

                        if self.show_weekdays and (wk_i == 0):
                            self.dict_canvas_tags["header_month"][cal_i]["weekdays"].append({
                                "rect": tag_rect,
                                "text": tag_txt
                            })
                            self.itemconfigure(
                                tag_rect,
                                fill=s.get("colour_background_header_weekday", self.colour_background_header_weekday).hex_code
                            )
                            self.itemconfigure(
                                tag_txt,
                                text=f"{calendar.day_abbr[(wkd_i - 1) % 7]}"[0],
                                fill=s.get("colour_foreground_header_weekday", self.colour_background_header_weekday.font_foreground_c()).hex_code
                            )
                            # self.set_date_cells.discard((ri0, ci0))
                            used_row = True
                            continue
                        if cal_i != (day_one.month - 1):
                            self.itemconfigure(tag_txt, state="hidden")
                            if is_ == "invisible":
                                self.itemconfigure(tag_rect, state="hidden")
                            # print(f" -A")
                            continue
                        if ((wk_i - (1 if self.show_weekdays else 0)) == 0) and (wd_d1 > 0):
                            wd_d1 -= 1
                            self.itemconfigure(tag_txt, state="hidden")
                            if is_ == "invisible":
                                self.itemconfigure(tag_rect, state="hidden")
                            # print(f" -B")
                            continue

                        self.itemconfigure(tag_txt, text=str_day)
                        self.date_to_cell[day_one] = (ri0, ci0)
                        txt = self.itemcget(tag_txt, "text")
                        day_one += datetime.timedelta(days=1)
                        used_row = True

                        # # bbox_month = (
                        # #     *self.gc[ri0][ci0][:2],
                        # #     *self.gc[ri0][ci0 + 7 - 1][-2:]
                        # # )
                        # # tag_txt = self.dict_canvas_tags["header_month"][cal_i]["text"]
                        # # txt = self.itemcget(tag_txt, "text")
                        # print(f" {txt=}")

                    if (not self.show_all_rows) and (not used_row):
                        for k in range(7):
                            self.itemconfigure(
                                self.dict_canvas_tags[(ri0, ((cal_i % self.months_per_row) * 7) + k)]["rect"],
                                state="hidden"
                            )
        else:
            sr = [0 for i in range(self.n_cols)]
            for i in range(1, self.n_rows):
                used_row = False
                for j in range(self.n_cols):
                    tag_txt = self.dict_canvas_tags[(i, j)]["text"]
                    tag_rect = self.dict_canvas_tags[(i, j)]["rect"]
                    wk_i = (i - 1) % (self.weeks_per_month + self.show_weekdays - 1)
                    cal_idx = self.dict_cell_to_cal_idx[((i - 1), j)]
                    cs = self.colour_scheme_month.get(cal_idx, {})
                    print(f"{i=}, {j=}, {wk_i=}, {cal_idx=}, sr={sum(sr)},", end="")
                    # if self.show_weekdays and (wk_i == 0):
                    #     self.itemconfigure(
                    #         tag_txt,
                    #         # text=f"{calendar.day_abbr[j // self.months_per_row]}"[0],
                    #         text=f"{calendar.day_abbr[(j - 1) % 7]}"[0],
                    #         fill=cs.get("colour_foreground_header_weekday",
                    #                     self.colour_background_header_weekday.font_foreground_c()).hex_code
                    #     )
                    #     used_row = True
                    #     print(f" -A")
                    #     sr[i] = 1
                    #     continue
                    # # elif wk_i == ()
                    # # if wk_idx == 0:
                    # #     break
                    # str_day = ((j % 7) + 1) + (((i - (sum(sr) + 1)) * self.n_cols) // self.months_per_row)
                    str_day = ((j % 7) + 1) + (((i - 1) * self.n_cols) // self.months_per_row)
                    str_day %= (self.weeks_per_month * 7)
                    if str_day > self.max_days_per_month[cal_idx]:
                        self.itemconfigure(tag_txt, state="hidden")
                        if is_ == "invisible":
                            self.itemconfigure(tag_rect, state="hidden")
                        print(f" End of Month")
                        continue
                    print(f" {str_day=}")
                    self.date_to_cell[(cal_idx, str_day)] = (i, j)
                    self.itemconfigure(tag_txt, text=str_day)
                    used_row = True
                    # day_one = datetime.datetime(self.year, cal_i + 1, 1)

                if (not self.show_all_rows) and (not used_row):
                    for k in range(7):
                        self.itemconfigure(
                            # self.dict_canvas_tags[(ri0, ((cal_i % self.months_per_row) * 7) + k)]["rect"],
                            self.dict_canvas_tags[(i, j)]["rect"],
                            state="hidden"
                        )

    def get_colour(self, i, j, key):
        ds = self.colour_scheme_day
        cs = self.colour_scheme_month
        is_ = self.invalid_style
        valid_style_keys = {
            "colour_background_canvas": iscolour,
            "colour_background_owned_number_check": iscolour,
            "colour_background_header_month": iscolour,
            "colour_background_header_weekday": iscolour,

            "colour_foreground_canvas": iscolour,
            "colour_foreground_header_month": iscolour,

            "colour_background_canvas_selected": iscolour,
            "colour_foreground_canvas_selected": iscolour
        }

        if key not in valid_style_keys:
            raise ValueError(f"Key '{key}' is not recognized as a valid colour key.")

        val = ds.get(key)
        if not val:
            val = cs.get(key)
        if not val:
            val = self.__getattribute__(key)

        return val

    # def get_cell_colour(self, n):
    #     # n is offset by 1
    #     if self.owned_numbers[n] > 0:
    #         if self.v_sw_show_heat_map.get():
    #             # return Colour(random_colour(name=True))
    #             return self.heat_map_colours[n]
    #         else:
    #             return self.colour_background_owned_number_check
    #     else:
    #         return self.colour_background_canvas
    def click_canvas(self, event, i, j):
        print(f"click_canvas {i=}, {j=}, {event=}", end="")
        if (i, j) in self.disabled_cells:
            return
        tr = self.dict_canvas_tags[(i, j)]["rect"]
        tt = self.dict_canvas_tags[(i, j)]["text"]
        cal_idx = self.dict_cell_to_cal_idx[(i, j)]
        text: str = self.itemcget(tt, "text")
        text_vis: str = self.itemcget(tt, "state") != "hidden"
        year = self.year if self.year is not None else datetime.datetime.now().year
        if text_vis and text.isdigit():
            print(f" {year=}, month={cal_idx+1}, day={int(text)}")
            # TODO highlight that this is now selected

            last_select: tuple[int, int] = self.v_cell_ids_selected.get()
            print(f"{last_select=}")
            if last_select:
                cal_idx_lh = self.dict_cell_to_cal_idx[last_select]
                ds = self.colour_scheme_day
                cs = self.colour_scheme_month
                bg = self.get_colour(i, j, "colour_background_canvas")
                cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
                col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
                col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
                self.itemconfigure(
                    self.dict_canvas_tags[last_select]["rect"],
                    fill=col_lh.hex_code
                )
                self.itemconfigure(
                    self.dict_canvas_tags[last_select]["text"],
                    fill=col_txt_lh.hex_code
                )

            self.v_cell_ids_selected.set((i, j))
            self.selected_date.set(datetime.datetime(year, cal_idx + 1, int(text)))

        print(f" SD={self.selected_date.get()}")
        # self.tb_canvas_click_data.delete("0.0", ctk.END)
        # n = ((i * self.n_cols) + j) + 1
        #
        # if not self.v_canvas_has_been_clicked.get():
        #     self.lbl_canvas_click_instruction.grid_forget()
        #     self.tb_canvas_click_data.grid(row=0, column=0, rowspan=1, columnspan=1)
        #     self.v_canvas_has_been_clicked.set(True)
        #
        # n = datetime.datetime(datetime.datetime.now().year, 1, 1) + datetime.timedelta(days=n-1)
        # print(f"{n=}")
        # df = self.ctk_.df.loc[(self.ctk_.df["DOB"].dt.month == n.month) & (self.ctk_.df["DOB"].dt.day == n.day)]
        # df = df.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        # text = ""
        # for k, row in df.iterrows():
        #     # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
        #     text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        # if df.shape[0] == 0:
        #     text = "No Data"
        # self.tb_canvas_click_data.insert("0.0", text)

    def motion_cell(self, event, i, j, t_):
        if self.id_after_motion is not None:
            self.after_cancel(self.id_after_motion)

        self.id_after_motion = self.after(self.time_after_motion, self.after_motion)

        if (i, j) in self.disabled_cells:
            return

        cal_idx = self.dict_cell_to_cal_idx[(i, j)]

        cs = self.colour_scheme_month.get(cal_idx, {})
        col = cs.get("colour_background_canvas", self.colour_background_canvas)
        col_txt = cs.get("colour_foreground_canvas", col.font_foreground_c())
        hs = self.hover_style
        is_ = self.invalid_style
        tr = self.dict_canvas_tags[(i, j)]["rect"]
        tt = self.dict_canvas_tags[(i, j)]["text"]
        last_hover = self.v_cell_ids_hovered.get()
        selected = self.v_cell_ids_selected.get()
        # print(f"LH={last_hover}, IJ={(i, j)=}, {col.hex_code=}, {col_txt.hex_code=}")

        if last_hover and (last_hover != selected):
            # cal_idx_lh = (last_hover[0] // 7) + (last_hover[1] // 7)  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
            cal_idx_lh = self.dict_cell_to_cal_idx[last_hover]
            cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
            col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
            col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
            self.itemconfigure(
                self.dict_canvas_tags[last_hover]["rect"],
                fill=col_lh.hex_code
            )
            self.itemconfigure(
                self.dict_canvas_tags[last_hover]["text"],
                fill=col_txt_lh.hex_code
            )

        # too slow
        # for r in range(self.n_rows):
        #     for c in range(self.n_cols):
        #         self.itemconfigure(
        #             self.dict_canvas_tags[(r, c)]["rect"],
        #             fill=col.hex_code
        #         )
        #         self.itemconfigure(
        #             self.dict_canvas_tags[(r, c)]["text"],
        #             fill=col_txt.hex_code
        #         )

        # print(f"{self.itemcget(tt, 'state')=}")
        text_vis = self.itemcget(tt, "state") != "hidden"
        if not text_vis:
            if is_ is None:
                # invalid cell (no visible date) and invalid_style is None
                return

            if ((i, j) in self.set_date_cells) and ((i, j) != selected):
                col_a = cs.get("colour_active_background_canvas")
                if col_a is None:
                    col_a = col.darkened(0.25) if is_ == "darken" else (col.brightened(0.25) if is_ == "brighten" else self.colour_background_canvas)
                # col_txt_a = cs.get("colour_active_foreground_canvas")
                # if col_txt_a is None:
                #     col_txt_a = (col.darkened(0.25) if is_ == "darken" else col.brightened(0.25)).font_foreground_c()
                    # col_txt_a = col_a.font_foreground_c()
                # print(f"{col_a.hex_code=}, {col_txt_a.hex_code=}")
                self.itemconfigure(
                    tr,
                    fill=col_a.hex_code
                )
                # self.itemconfigure(
                #     tt,
                #     fill=col_txt_a.hex_code
                # )
                self.v_cell_ids_hovered.set((i, j))
            return

        if hs is not None:
            if ((i, j) in self.set_date_cells) and ((i, j) != selected):
                col_a = cs.get("colour_active_background_canvas")
                if col_a is None:
                    col_a = col.darkened(0.25) if hs == "darken" else col.brightened(0.25)
                col_txt_a = cs.get("colour_active_foreground_canvas")
                if col_txt_a is None:
                    col_txt_a = (col.darkened(0.25) if hs == "darken" else col.brightened(0.25)).font_foreground_c()
                # print(f"{col_a.hex_code=}, {col_txt_a.hex_code=}")
                self.itemconfigure(
                    tr,
                    fill=col_a.hex_code
                )
                self.itemconfigure(
                    tt,
                    fill=col_txt_a.hex_code
                )
                self.v_cell_ids_hovered.set((i, j))

    def after_motion(self, *args):
        mx = self.winfo_pointerx()
        my = self.winfo_pointery()
        # bbox_canvas = self.bbox("all")
        # bbox_canvas = self.grid_bbox()
        # bbox_canvas = self.master.bbox(self)
        bbox_canvas = (self.winfo_rootx(), self.winfo_rooty(), self.winfo_width(), self.winfo_height())
        # print(f"{mx=}, {my=}, {bbox_canvas=}")
        self.id_after_motion = None

        if not ((bbox_canvas[0] <= mx <= bbox_canvas[2]) and (bbox_canvas[1] <= my <= bbox_canvas[3])):
            last_hover = self.v_cell_ids_hovered.get()
            selected = self.v_cell_ids_selected.get()
            # print(f"LH={last_hover}, IJ={(i, j)=}, {col.hex_code=}, {col_txt.hex_code=}")

            if last_hover and (last_hover != selected):
                # cal_idx_lh = (last_hover[0] // 7) + (last_hover[1] // 7)  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
                cal_idx_lh = self.dict_cell_to_cal_idx[last_hover]
                cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
                col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
                col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
                self.itemconfigure(
                    self.dict_canvas_tags[last_hover]["rect"],
                    fill=col_lh.hex_code
                )
                self.itemconfigure(
                    self.dict_canvas_tags[last_hover]["text"],
                    fill=col_txt_lh.hex_code
                )

    def update_selected_date(self, *args):
        print(f"update_selected_date")
        select: tuple[int, int] = self.v_cell_ids_selected.get()
        if select:
            cal_idx_lh = self.dict_cell_to_cal_idx[select]
            cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
            col_lh = cs_lh.get("colour_background_canvas_selected", self.colour_background_canvas_selected)
            col_txt_lh = cs_lh.get("colour_foreground_canvas_selected", self.colour_foreground_canvas_selected)
            self.itemconfigure(
                self.dict_canvas_tags[select]["rect"],
                fill=col_lh.hex_code
            )
            self.itemconfigure(
                self.dict_canvas_tags[select]["text"],
                fill=col_txt_lh.hex_code
            )
