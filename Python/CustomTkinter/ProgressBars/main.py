from customtkinter_utility import *
import datetime

from utility import percent, money


class Row(ctk.CTkFrame):

    def __init__(
            self,
            master: Any,
            name: str,
            monthly: float,
            day0: Optional[datetime.datetime] = None,
            day1: Optional[datetime.datetime] = None,
            auto_grid: bool = True,
            days_per_month: float = ((365 * 4) + 1) / (4 * 12),
            **kwargs
    ):
        super().__init__(master, **kwargs)

        # self.day0: datetime.datetime = day0 if isinstance(day0, datetime.datetime) else (datetime.datetime.now() + datetime.timedelta(days=365.25))
        # self.day1: datetime.datetime = day1
        self.name: str = name
        self.monthly: float = monthly
        self.day0: datetime.datetime = day0
        self.day1: datetime.datetime = day1
        self.mode: str = "determinate" if isinstance(self.day1, datetime.datetime) else "continuous"
        self.auto_grid: bool = auto_grid
        self.days_per_month: float = days_per_month

        self.total_month_diff: float = ((datetime.datetime.now() if (self.mode == "continuous") else self.day1) - self.day0).days / self.days_per_month
        self.total_dollars: float = self.monthly * self.total_month_diff

        self.n_cols = 4
        self.columnconfigure(0, weight=int(100/self.n_cols))
        self.columnconfigure(1, weight=int(100/self.n_cols))
        self.columnconfigure(2, weight=int(100/self.n_cols))
        self.columnconfigure(3, weight=int(100/self.n_cols))

        self.var_progress: ctk.DoubleVar = ctk.DoubleVar(self, value=0)

        self.lbl_progress_name = label_factory(
            self,
            tv_label=self.name
        )
        self.lbl_progress_percent = label_factory(
            self,
            tv_label=f"{percent(self.var_progress.get())}"
        )
        self.lbl_progress_money = label_factory(
            self,
            tv_label=f"{money(self.monthly * 0, int_only=True)}"
        )
        self.progress_bar = ctk.CTkProgressBar(
            self,
            mode="determinate",
            variable=self.var_progress
        )

        if self.auto_grid:
            self.grid_widgets()

    def grid_widgets(self, grid: bool = True):
        if grid:
            self.grid()
            self.lbl_progress_name[1].grid(row=0, column=0, rowspan=1, columnspan=1)
            self.lbl_progress_percent[1].grid(row=0, column=1, rowspan=1, columnspan=1)
            self.lbl_progress_money[1].grid(row=0, column=2, rowspan=1, columnspan=1)
            self.progress_bar.grid(row=0, column=3, rowspan=1, columnspan=1)
        else:
            self.grid_forget()
            self.lbl_progress_name[1].grid_forget()
            self.lbl_progress_percent[1].grid_forget()
            self.lbl_progress_money[1].grid_forget()
            self.progress_bar.grid_forget()

    def month_diff(self, date: datetime.datetime, from_day0: bool = True) -> float:
        return (date - (self.day1 if not from_day0 else self.day0)).days / self.days_per_month

    def set_progress(self, value: datetime.datetime | float):

        if self.mode == "continuous":
            self.day1 = datetime.datetime.now()
            self.total_month_diff = (self.day1 - self.day0).days / self.days_per_month
            self.total_dollars = self.monthly * self.total_month_diff

        print(f"{self.name=}, {self.monthly=}, {self.total_month_diff=}, {self.total_dollars=}")

        if isinstance(value, datetime.datetime):
            month_progress = self.month_diff(value) / self.total_month_diff
        else:
            month_progress = value

        self.var_progress.set(month_progress)
        self.lbl_progress_percent[0].set(percent(month_progress))
        self.lbl_progress_money[0].set(money(month_progress * self.total_dollars, int_only=True))

    def reset(self):
        self.var_progress.set(0)
        self.lbl_progress_percent[0].set(percent(self.var_progress.get()))
        self.lbl_progress_money[0].set(money(self.monthly * 0, int_only=True))


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frame_rows: ctk.CTkFrame = ctk.CTkFrame(self)
        self.rows = {
            "sl": Row(
                self.frame_rows,
                name="Student Loans:",
                monthly=600,
                day0=datetime.datetime(2021, 4, 1),
                day1=datetime.datetime(2029, 4, 30)
            ),
            "cp": Row(
                self.frame_rows,
                name="Honda Payments:",
                monthly=366.69*2,
                day0=datetime.datetime(2023, 11, 3),
                day1=datetime.datetime(2029, 10, 15)
            )
        }
        self.today = datetime.datetime(2021, 1, 1)
        self.today_og = self.today
        self.end_day = datetime.datetime.now() + datetime.timedelta(days=1)

        self.days_per_sec = 1

        self.var_today = ctk.StringVar(self, value=f"{self.today:%Y-%m-%d}")
        self.var_slider_speed = ctk.IntVar(self, value=1)

        self.frame_today = ctk.CTkFrame(self)
        self.lbl_today = label_factory(
            self.frame_today,
            tv_label=self.var_today
        )
        self.frame_controls = ctk.CTkFrame(self)
        self.btn_start = button_factory(
            self.frame_controls,
            tv_btn="start",
            command=self.click_start
        )
        self.slider_speed = ctk.CTkSlider(
            self.frame_controls,
            variable=self.var_slider_speed,
            number_of_steps=10,
            from_=1,
            to=10,
            command=self.update_slider_speed
        )

        # self
        self.frame_today.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.frame_controls.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.frame_rows.grid(row=2, column=0, rowspan=1, columnspan=1)

        # self.frame_today
        self.lbl_today[1].grid(row=0, column=0, rowspan=1, columnspan=1)

        # self.frame_controls
        self.btn_start[1].grid(row=0, column=0, rowspan=1, columnspan=1)
        self.slider_speed.grid(row=1, column=0, rowspan=1, columnspan=1)

    def click_start(self):
        # print(f"click_start", end="")
        speed = self.var_slider_speed.get()
        day_p_sec = self.days_per_sec
        anim_speed = day_p_sec * speed
        # print(f" {anim_speed=}")
        self.today = self.today_og
        self.var_today.set(f"{self.today:%Y-%m-%d}")
        self.btn_start[1].configure(state=ctk.DISABLED)
        self.slider_speed.configure(state=ctk.DISABLED)

        for k, row in self.rows.items():
            row.reset()

        self.after(1000, self.animate)

    def update_slider_speed(self, *args):
        # print(f"update_slider_speed", end="")
        # speed = self.var_slider_speed.get()
        # print(f" mode={speed}")
        pass

    def animate(self):

        if self.today < self.end_day:
            speed = self.var_slider_speed.get()
            day_p_sec = self.days_per_sec
            anim_speed = day_p_sec * speed

            for k, row in self.rows.items():
                if self.today >= row.day0:
                    row.set_progress(self.today)

            self.today += datetime.timedelta(days=anim_speed)
            self.var_today.set(f"{self.today:%Y-%m-%d}")
            self.after(1000, self.animate)
        else:
            self.btn_start[1].configure(state=ctk.NORMAL)
            self.slider_speed.configure(state=ctk.NORMAL)



        # if self.today < self.end_day:
        #     speed = self.var_slider_speed.get()
        #     day_p_sec = self.days_per_sec
        #     anim_speed = day_p_sec * speed
        #     if self.today >= self.day0_sl:
        #         month_diff_sl = (self.today - self.day0_sl).days / 30
        #         total_month_diff_sl = (self.day1_sl - self.day0_sl).days / 30
        #         total_dollar_diff_sl = total_month_diff_sl * self.payment_monthly_sl
        #         month_progress_sl = month_diff_sl / total_month_diff_sl
        #         self.var_pb_sl.set(month_progress_sl)
        #         self.lbl_pn_sl[0].set(percent(month_progress_sl))
        #         self.lbl_pd_sl[0].set(money(month_progress_sl * total_dollar_diff_sl, int_only=True))
        #     if self.today >= self.day0_cp:
        #         month_diff_cp = (self.today - self.day0_cp).days / 30
        #         total_month_diff_cp = (self.day1_cp - self.day0_cp).days / 30
        #         total_dollar_diff_cp = total_month_diff_cp * self.payment_monthly_cp
        #         month_progress_cp = month_diff_cp / total_month_diff_cp
        #         self.lbl_pn_cp[0].set(percent(month_progress_cp))
        #         self.lbl_pd_cp[0].set(money(month_progress_cp * total_dollar_diff_cp, int_only=True))
        #         self.var_pb_cp.set(month_progress_cp)
        #
        #     self.today += datetime.timedelta(days=anim_speed)
        #     self.var_today.set(f"{self.today:%Y-%m-%d}")
        #     self.after(1000, self.animate)
        # else:
        #     self.btn_start[1].configure(state=ctk.NORMAL)
        #     self.slider_speed.configure(state=ctk.NORMAL)


# 202411042058
# class App(ctk.CTk):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.day0_sl = datetime.datetime(2020, 4, 1)
#         self.day1_sl = datetime.datetime(2030, 9, 30)
#         self.payment_monthly_sl = 600
#         self.day0_cp = datetime.datetime(2023, 11, 3)
#         self.day1_cp = datetime.datetime(2030, 9, 30)
#         self.payment_monthly_cp = 366.79 * 2
#         self.today = datetime.datetime(2020, 1, 1)
#         self.today_og = self.today
#         self.end_day = datetime.datetime.now() + datetime.timedelta(days=1)
#
#         self.days_per_sec = 1
#
#         self.var_today = ctk.StringVar(self, value=f"{self.today:%Y-%m-%d}")
#         self.var_slider_speed = ctk.IntVar(self, value=1)
#         self.var_pb_sl = ctk.DoubleVar(self, value=0)
#         self.var_pb_cp = ctk.DoubleVar(self, value=0)
#
#         self.frame_today = ctk.CTkFrame(self)
#         self.lbl_today = label_factory(
#             self.frame_today,
#             tv_label=self.var_today
#         )
#         self.frame_controls = ctk.CTkFrame(self)
#         self.btn_start = button_factory(
#             self.frame_controls,
#             tv_btn="start",
#             command=self.click_start
#         )
#         self.slider_speed = ctk.CTkSlider(
#             self.frame_controls,
#             variable=self.var_slider_speed,
#             number_of_steps=10,
#             from_=1,
#             to=10,
#             command=self.update_slider_speed
#         )
#
#         self.frame_sl = ctk.CTkFrame(self)
#         self.frame_sl.columnconfigure(0, weight=int(100/4))
#         self.frame_sl.columnconfigure(1, weight=int(100/4))
#         self.frame_sl.columnconfigure(2, weight=int(100/4))
#         self.frame_sl.columnconfigure(3, weight=int(100/4))
#         self.lbl_pb_sl = label_factory(
#             self.frame_sl,
#             tv_label="Student Loans:"
#         )
#         self.lbl_pn_sl = label_factory(
#             self.frame_sl,
#             tv_label=f"{percent(self.var_pb_sl.get())}"
#         )
#         self.lbl_pd_sl = label_factory(
#             self.frame_sl,
#             tv_label=f"{money(self.payment_monthly_sl * 0, int_only=True)}"
#         )
#         self.pb_sl = ctk.CTkProgressBar(
#             self.frame_sl,
#             mode="determinate",
#             variable=self.var_pb_sl
#         )
#
#         self.frame_cp = ctk.CTkFrame(self)
#         self.frame_cp.columnconfigure(0, weight=int(100/4))
#         self.frame_cp.columnconfigure(1, weight=int(100/4))
#         self.frame_cp.columnconfigure(2, weight=int(100/4))
#         self.frame_cp.columnconfigure(3, weight=int(100/4))
#         self.lbl_pb_cp = label_factory(
#             self.frame_cp,
#             tv_label="Car Payments:"
#         )
#         self.lbl_pn_cp = label_factory(
#             self.frame_cp,
#             tv_label=f"{percent(self.var_pb_cp.get())}"
#         )
#         self.lbl_pd_cp = label_factory(
#             self.frame_cp,
#             tv_label=f"{money(self.payment_monthly_cp * 0, int_only=True)}"
#         )
#         self.pb_cp = ctk.CTkProgressBar(
#             self.frame_cp,
#             mode="determinate",
#             variable=self.var_pb_cp
#         )
#
#         # self
#         self.frame_today.grid(row=0, column=0, rowspan=1, columnspan=1)
#         self.frame_controls.grid(row=1, column=0, rowspan=1, columnspan=1)
#         self.frame_sl.grid(row=2, column=0, rowspan=1, columnspan=1)
#         self.frame_cp.grid(row=3, column=0, rowspan=1, columnspan=1)
#
#         # self.frame_today
#         self.lbl_today[1].grid(row=0, column=0, rowspan=1, columnspan=1)
#
#         # self.frame_controls
#         self.btn_start[1].grid(row=0, column=0, rowspan=1, columnspan=1)
#         self.slider_speed.grid(row=1, column=0, rowspan=1, columnspan=1)
#
#         # self.frame_sl
#         self.lbl_pb_sl[1].grid(row=0, column=0, rowspan=1, columnspan=1)
#         self.lbl_pn_sl[1].grid(row=0, column=1, rowspan=1, columnspan=1)
#         self.lbl_pd_sl[1].grid(row=0, column=2, rowspan=1, columnspan=1)
#         self.pb_sl.grid(row=0, column=3, rowspan=1, columnspan=1)
#
#         # self.frame_cp
#         self.lbl_pb_cp[1].grid(row=0, column=0, rowspan=1, columnspan=1)
#         self.lbl_pn_cp[1].grid(row=0, column=1, rowspan=1, columnspan=1)
#         self.lbl_pd_cp[1].grid(row=0, column=2, rowspan=1, columnspan=1)
#         self.pb_cp.grid(row=0, column=3, rowspan=1, columnspan=1)
#
#     def click_start(self):
#         # print(f"click_start", end="")
#         speed = self.var_slider_speed.get()
#         day_p_sec = self.days_per_sec
#         anim_speed = day_p_sec * speed
#         # print(f" {anim_speed=}")
#         self.today = self.today_og
#         self.var_today.set(f"{self.today:%Y-%m-%d}")
#         self.btn_start[1].configure(state=ctk.DISABLED)
#         self.slider_speed.configure(state=ctk.DISABLED)
#         self.lbl_pd_sl[0].set(money(0, int_only=True))
#         self.lbl_pd_cp[0].set(money(0, int_only=True))
#         self.lbl_pn_sl[0].set(percent(0))
#         self.lbl_pn_cp[0].set(percent(0))
#         self.after(1000, self.animate)
#
#     def update_slider_speed(self, *args):
#         # print(f"update_slider_speed", end="")
#         # speed = self.var_slider_speed.get()
#         # print(f" mode={speed}")
#         pass
#
#     def animate(self):
#         if self.today < self.end_day:
#             speed = self.var_slider_speed.get()
#             day_p_sec = self.days_per_sec
#             anim_speed = day_p_sec * speed
#             if self.today >= self.day0_sl:
#                 month_diff_sl = (self.today - self.day0_sl).days / 30
#                 total_month_diff_sl = (self.day1_sl - self.day0_sl).days / 30
#                 total_dollar_diff_sl = total_month_diff_sl * self.payment_monthly_sl
#                 month_progress_sl = month_diff_sl / total_month_diff_sl
#                 self.var_pb_sl.set(month_progress_sl)
#                 self.lbl_pn_sl[0].set(percent(month_progress_sl))
#                 self.lbl_pd_sl[0].set(money(month_progress_sl * total_dollar_diff_sl, int_only=True))
#             if self.today >= self.day0_cp:
#                 month_diff_cp = (self.today - self.day0_cp).days / 30
#                 total_month_diff_cp = (self.day1_cp - self.day0_cp).days / 30
#                 total_dollar_diff_cp = total_month_diff_cp * self.payment_monthly_cp
#                 month_progress_cp = month_diff_cp / total_month_diff_cp
#                 self.lbl_pn_cp[0].set(percent(month_progress_cp))
#                 self.lbl_pd_cp[0].set(money(month_progress_cp * total_dollar_diff_cp, int_only=True))
#                 self.var_pb_cp.set(month_progress_cp)
#
#             self.today += datetime.timedelta(days=anim_speed)
#             self.var_today.set(f"{self.today:%Y-%m-%d}")
#             self.after(1000, self.animate)
#         else:
#             self.btn_start[1].configure(state=ctk.NORMAL)
#             self.slider_speed.configure(state=ctk.NORMAL)


if __name__ == "__main__":
    win = App()
    win.mainloop()
