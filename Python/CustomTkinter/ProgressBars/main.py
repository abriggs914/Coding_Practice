from customtkinter_utility import *
import datetime

from utility import percent, money


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.day0_sl = datetime.datetime(2020, 4, 1)
        self.day1_sl = datetime.datetime(2030, 9, 30)
        self.payment_monthly_sl = 600
        self.day0_cp = datetime.datetime(2023, 11, 3)
        self.day1_cp = datetime.datetime(2030, 9, 30)
        self.payment_monthly_cp = 366.79 * 2
        self.today = datetime.datetime(2020, 1, 1)
        self.today_og = self.today
        self.end_day = datetime.datetime.now() + datetime.timedelta(days=1)

        self.days_per_sec = 1

        self.var_today = ctk.StringVar(self, value=f"{self.today:%Y-%m-%d}")
        self.var_slider_speed = ctk.IntVar(self, value=1)
        self.var_pb_sl = ctk.DoubleVar(self, value=0)
        self.var_pb_cp = ctk.DoubleVar(self, value=0)

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

        self.frame_sl = ctk.CTkFrame(self)
        self.frame_sl.columnconfigure(0, weight=int(100/4))
        self.frame_sl.columnconfigure(1, weight=int(100/4))
        self.frame_sl.columnconfigure(2, weight=int(100/4))
        self.frame_sl.columnconfigure(3, weight=int(100/4))
        self.lbl_pb_sl = label_factory(
            self.frame_sl,
            tv_label="Student Loans:"
        )
        self.lbl_pn_sl = label_factory(
            self.frame_sl,
            tv_label=f"{percent(self.var_pb_sl.get())}"
        )
        self.lbl_pd_sl = label_factory(
            self.frame_sl,
            tv_label=f"{money(self.payment_monthly_sl * 0, int_only=True)}"
        )
        self.pb_sl = ctk.CTkProgressBar(
            self.frame_sl,
            mode="determinate",
            variable=self.var_pb_sl
        )

        self.frame_cp = ctk.CTkFrame(self)
        self.frame_cp.columnconfigure(0, weight=int(100/4))
        self.frame_cp.columnconfigure(1, weight=int(100/4))
        self.frame_cp.columnconfigure(2, weight=int(100/4))
        self.frame_cp.columnconfigure(3, weight=int(100/4))
        self.lbl_pb_cp = label_factory(
            self.frame_cp,
            tv_label="Car Payments:"
        )
        self.lbl_pn_cp = label_factory(
            self.frame_cp,
            tv_label=f"{percent(self.var_pb_cp.get())}"
        )
        self.lbl_pd_cp = label_factory(
            self.frame_cp,
            tv_label=f"{money(self.payment_monthly_cp * 0, int_only=True)}"
        )
        self.pb_cp = ctk.CTkProgressBar(
            self.frame_cp,
            mode="determinate",
            variable=self.var_pb_cp
        )

        # self
        self.frame_today.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.frame_controls.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.frame_sl.grid(row=2, column=0, rowspan=1, columnspan=1)
        self.frame_cp.grid(row=3, column=0, rowspan=1, columnspan=1)

        # self.frame_today
        self.lbl_today[1].grid(row=0, column=0, rowspan=1, columnspan=1)

        # self.frame_controls
        self.btn_start[1].grid(row=0, column=0, rowspan=1, columnspan=1)
        self.slider_speed.grid(row=1, column=0, rowspan=1, columnspan=1)

        # self.frame_sl
        self.lbl_pb_sl[1].grid(row=0, column=0, rowspan=1, columnspan=1)
        self.lbl_pn_sl[1].grid(row=0, column=1, rowspan=1, columnspan=1)
        self.lbl_pd_sl[1].grid(row=0, column=2, rowspan=1, columnspan=1)
        self.pb_sl.grid(row=0, column=3, rowspan=1, columnspan=1)

        # self.frame_cp
        self.lbl_pb_cp[1].grid(row=0, column=0, rowspan=1, columnspan=1)
        self.lbl_pn_cp[1].grid(row=0, column=1, rowspan=1, columnspan=1)
        self.lbl_pd_cp[1].grid(row=0, column=2, rowspan=1, columnspan=1)
        self.pb_cp.grid(row=0, column=3, rowspan=1, columnspan=1)

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
        self.lbl_pd_sl[0].set(money(0, int_only=True))
        self.lbl_pd_cp[0].set(money(0, int_only=True))
        self.lbl_pn_sl[0].set(percent(0))
        self.lbl_pn_cp[0].set(percent(0))
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
            if self.today >= self.day0_sl:
                month_diff_sl = (self.today - self.day0_sl).days / 30
                total_month_diff_sl = (self.day1_sl - self.day0_sl).days / 30
                total_dollar_diff_sl = total_month_diff_sl * self.payment_monthly_sl
                month_progress_sl = month_diff_sl / total_month_diff_sl
                self.var_pb_sl.set(month_progress_sl)
                self.lbl_pn_sl[0].set(percent(month_progress_sl))
                self.lbl_pd_sl[0].set(money(month_progress_sl * total_dollar_diff_sl, int_only=True))
            if self.today >= self.day0_cp:
                month_diff_cp = (self.today - self.day0_cp).days / 30
                total_month_diff_cp = (self.day1_cp - self.day0_cp).days / 30
                total_dollar_diff_cp = total_month_diff_cp * self.payment_monthly_cp
                month_progress_cp = month_diff_cp / total_month_diff_cp
                self.lbl_pn_cp[0].set(percent(month_progress_cp))
                self.lbl_pd_cp[0].set(money(month_progress_cp * total_dollar_diff_cp, int_only=True))
                self.var_pb_cp.set(month_progress_cp)

            self.today += datetime.timedelta(days=anim_speed)
            self.var_today.set(f"{self.today:%Y-%m-%d}")
            self.after(1000, self.animate)
        else:
            self.btn_start[1].configure(state=ctk.NORMAL)
            self.slider_speed.configure(state=ctk.NORMAL)


if __name__ == "__main__":
    win = App()
    win.mainloop()
