import enum

from customtkinter_utility import *
from tkinter_utility import *
from colour_utility import gradient


class STATE(enum.Enum):
    IDLE: int = 0
    PLAY: int = 1
    END: int = -1
    PAUSE: int = 2


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Space Invaders")

        self.colour_rect_summary = Colour("#9A9A9A")
        self.colour_text_summary = Colour("#000000")
        self.colour_ship = Colour("#652318")
        self.colour_enemy_hp_full = Colour("#126633")
        self.colour_enemy_hp_empty = Colour("#FF6633")

        self.w_can_gb, self.h_can_gb = 400, 400

        self.game_state = STATE.IDLE

        self.frame_controls = ctk.CTkFrame(self)
        self.btn_restart = button_factory(
            self.frame_controls,
            tv_btn="restart",
            command=self.click_restart
        )
        self.btn_pause = button_factory(
            self.frame_controls,
            tv_btn="pause",
            command=self.click_pause
        )

        self.canvas_game_board = ctk.CTkCanvas(
            self,
            width=self.w_can_gb,
            height=self.h_can_gb
        )

        self.tag_rect_summary = self.canvas_game_board.create_rectangle(
            self.w_can_gb / 2 - 50,
            self.h_can_gb / 2 - 40,
            self.w_can_gb / 2 + 50,
            self.h_can_gb / 2 + 40,
            fill=self.colour_rect_summary.hex_code
        )

        self.tag_text_summary_0 = self.canvas_game_board.create_text(
            self.w_can_gb / 2,
            self.h_can_gb / 2,
            fill=self.colour_text_summary.hex_code,
            font=("calibri", 14),
            text=""
        )

        self.ms_anim = 120
        self.ms_loop = 300
        self.n_new_tiles_per_move = 2
        self.options_new_val = [2, 4]
        self.n_rows, self.n_cols = 10, 10
        self.positions = dict()
        self.empty_positions = list()

        self.keys_pressed = list()
        self.n_cycles = 0

        self.af_id_loop = None
        self.af_id_animate = None

        self.gc = grid_cells(
            self.w_can_gb,
            self.n_cols,
            self.h_can_gb,
            self.n_rows
        )

        for i, row in enumerate(self.gc):
            self.positions[i] = dict()
            for j, bbox in enumerate(row):
                self.positions[i][j] = {
                    "tile":
                        self.canvas_game_board.create_rectangle(
                            *bbox
                        ),
                    "val": None,
                    "text":
                        self.canvas_game_board.create_text(
                            bbox[0] + ((bbox[2] - bbox[0]) / 2),
                            bbox[1] + ((bbox[3] - bbox[1]) / 2),
                            text="",
                            font=("Arial", 18)
                        )
                }
                self.empty_positions.append((i * self.n_cols) + j)

        self.bind("<KeyPress>", self.key_down)
        self.bind("<KeyRelease>", self.key_up)
        # self.bind("<Left>", self.move_left)
        # self.bind("<Right>", self.move_right)
        # self.bind("<Up>", self.shoot)

        self.grid_widgets()

        self.start_new_game()

    def click_pause(self):
        print(f"click_pause")
        if self.game_state == STATE.PAUSE:
            # resume
            self.game_state = STATE.PLAY
            self.btn_pause[0].set("pause")
        else:
            self.game_state = STATE.PAUSE
            self.btn_pause[0].set("resume")

    def click_restart(self):
        print(f"click_restart")
        self.end_game(0)
        self.start_new_game()

    def grid_widgets(self):
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=80)
        self.columnconfigure(0, weight=100)
        self.frame_controls.grid(row=0, column=0, sticky=ctk.NSEW)
        self.canvas_game_board.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)

        # frame_controls
        self.btn_restart[1].grid(row=0, column=0)
        self.btn_pause[1].grid(row=0, column=1)

    def key_up(self, event):
        key = event.keysym
        # if self.keys_pressed:
        #	print(f"{self.keys_pressed=}")
        # print(f"{key=}")
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def key_down(self, event):
        key = event.keysym
        state = event.state
        # print(f"{event=}")
        # print(f"{key=}, {state=}")

        if key in ("Left", "Right", "Up", "Down"):
            if key not in self.keys_pressed:
                self.keys_pressed.append(key)
        elif state == 12:
            # control held
            if key in ("p"):
                if key not in self.keys_pressed:
                    self.keys_pressed.append(key)
        else:
            if key in ("p"):
                if key not in self.keys_pressed:
                    self.keys_pressed.append(key)

    def loop(self, *args):
        # if self.keys_pressed:
        #	print(f"{self.keys_pressed=}")
        keep_going = True
        moved = False
        if self.game_state == STATE.PLAY:
            for key in self.keys_pressed:
                if key == "Left":
                    self.move_left(None)
                    moved = True
                # self.gen_new_positions()
                elif key == "Right":
                    self.move_right(None)
                    moved = True
                # self.gen_new_positions()
                elif key == "Up":
                    self.move_up(None)
                    moved = True
                # self.gen_new_positions()
                elif key == "Down":
                    self.move_down(None)
                    moved = True
                # self.gen_new_positions()
                elif key == "p":
                    self.click_pause()
                else:
                    pass
                    # else:
                    #     pass
                    #     # print(f"pass {key=}")
                    #     # pass
                if moved:
                    self.gen_new_positions()
        else:
            # loop non-move actions
            to_rem = list()
            for key in self.keys_pressed:
                if key == "p":
                    self.click_pause()
                    to_rem.append(key)
                else:
                    pass
            for key in to_rem:
                self.keys_pressed.remove(key)
        # print(f"{self.n_cycles=}, {keep_going=}")

        if keep_going:
            self.n_cycles += 1
            self.af_id_loop = self.after(self.ms_loop, self.loop)

    def gen_new_positions(self):

        def new_empty_position(n: int = 1):
            if len(self.empty_positions) < n:
                return None
            result = list()
            i = 0
            while i < n:
                chx = random.choice(self.empty_positions)
                if chx not in result:
                    self.empty_positions.remove(chx)
                    result.append(chx)
                    i += 1
            return result

        def new_value():
            return random.choice(self.options_new_val)

        new_positions = new_empty_position(self.n_new_tiles_per_move)
        print(f"{new_positions=}")
        if new_positions:
            for idx in new_positions:
                i = int(idx / self.n_cols)
                j = idx - (i * self.n_cols)
                tile = self.positions[i][j]["tile"]
                text = self.positions[i][j]["text"]
                val = self.positions[i][j]["val"]
                new_val = new_value()
                print(f"{new_val=}")

                self.positions[i][j]["val"] = new_val
                self.canvas_game_board.itemconfigure(
                    text,
                    text=str(new_val),
                    state=ctk.NORMAL
                )
        else:
            print(f"TODO QUIT HERE")
            pass

    def start_new_game(self):
        if getattr(self, "af_id_animate", None):
            self.after_cancel(self.af_id_animate)
        if getattr(self, "af_id_loop", None):
            self.after_cancel(self.af_id_loop)
        self.canvas_game_board.itemconfigure(self.tag_rect_summary, state=ctk.HIDDEN)
        self.canvas_game_board.itemconfigure(self.tag_text_summary_0, state=ctk.HIDDEN)
        # self.n_cycles = 0
        # self.gen_enemies()

        self.gen_new_positions()

        self.game_state = STATE.PLAY
        # self.af_id_animate = self.after(self.ms_anim, self.animate)
        self.af_id_loop = self.after(self.ms_loop, self.loop)

    def animate(self, *args):
        pass

    def clear_board(self):
        pass

    # for tag in self.enemies + self.bullets:
    #	self.canvas_game_board.delete(tag)
    # self.enemies.clear()
    # self.bullets.clear()

    def end_game(self, code):
        if self.game_state == STATE.END:
            return

        if code > 0:
            # win
            print(f"WIN {code=}")
            summary_text = "You Win!"

        elif code < 0:
            # lose
            print(f"LOSE {code=}")
            summary_text = "You Lose"
        else:
            # draw
            print(f"DRAW {code=}")
            summary_text = "DRAW"

        self.game_state = STATE.END

        self.canvas_game_board.itemconfigure(self.tag_rect_summary, state=ctk.NORMAL)
        self.canvas_game_board.itemconfigure(self.tag_text_summary_0, state=ctk.NORMAL)
        self.canvas_game_board.itemconfigure(self.tag_text_summary_0, text=summary_text)

    # if self.af_id_loop is not None:
    #	self.after_cancel(self.af_id_loop)
    #
    # if self.af_id_animate is not None:
    #	self.after_cancel(self.af_id_animate)

    def clear_cell(self, i: int, j: int):
        self.positions[i][j]["val"] = None
        self.canvas_game_board.itemconfigure(
            self.positions[i][j]["text"],
            text="",
            state=ctk.HIDDEN
        )
        self.empty_positions.append(j + (i * self.n_cols))

    def set_cell(self, i: int, j: int, val: int):
        print(f"{i=}, {j=}, {val=}")
        self.positions[i][j]["val"] = val
        self.canvas_game_board.itemconfigure(
            self.positions[i][j]["text"],
            text=str(val),
            state=ctk.NORMAL
        )

    def move_up(self, event):
        print(f"move_up {event}")
        # cols = list(range(self.n_cols))
        # rows = list(range(self.n_rows))
        # while cols:
        #     j = cols[0]

        for j in range(self.n_cols):
            for i in range(self.n_rows - 1, -1, -1):
                data = self.positions[i][j]
                val = data["val"]
                if val is None:
                    continue
                if i > 0:
                    k = -1
                    val_u = None
                    for k in range(i - 1, -1, -1):
                        data_u = self.positions[k][j]
                        val_u = data_u["val"]
                        if val_u is not None:
                            break
                    new_val = None
                    if k >= 0:
                        if val_u == val:
                            # combine
                            new_val = val * 2
                        else:
                            # move val at [i][j] to [k][j]
                            new_val = val

                        self.set_cell(k + 1, j, new_val)
                        self.clear_cell(i, j)
                    print(f"{j=}, {i=}, {k+1=}, {val=}, {val_u=}, {new_val=}")





        # for i in range(1, self.n_rows):
        #     for j in range(self.n_cols):
        #
        #         data = self.positions[i][j]
        #         # print(f"{data=}")
        #         val = data["val"]
        #         if val is None:
        #             continue
        #
        #         idx = j + (i * self.n_cols)
        #         tile = data["tile"]
        #         text = data["text"]
        #         val_u = self.positions[i - 1][j]["val"]
        #
        #         if val == val_u:
        #             # combine
        #             new_val = val * 2
        #         elif val_u is None:
        #             # shift
        #             new_val = val
        #         else:
        #             # do not set the top neighbour cell, or clear this cell as they cannot be combined or shifted.
        #             continue
        #
        #         self.set_cell(i - 1, j, new_val)
        #         self.clear_cell(i, j)
        # # print(f"move_up {event}")
        # # for i in range(1, self.n_rows):
        # #     for j in range(self.n_cols):
        # #
        # #         data = self.positions[i][j]
        # #         # print(f"{data=}")
        # #         val = data["val"]
        # #         if val is None:
        # #             continue
        # #
        # #         idx = j + (i * self.n_cols)
        # #         tile = data["tile"]
        # #         text = data["text"]
        # #         val_u = self.positions[i - 1][j]["val"]
        # #
        # #         if val == val_u:
        # #             # combine
        # #             new_val = val * 2
        # #         elif val_u is None:
        # #             # shift
        # #             new_val = val
        # #         else:
        # #             # do not set the top neighbour cell, or clear this cell as they cannot be combined or shifted.
        # #             continue
        # #
        # #         self.set_cell(i - 1, j, new_val)
        # #         self.clear_cell(i, j)

    def move_down(self, event):
        print(f"move_down {event}")
        for i in range(self.n_rows - 2, -1, -1):
            for j in range(self.n_cols):

                data = self.positions[i][j]
                # print(f"{data=}")
                val = data["val"]
                if val is None:
                    continue

                idx = j + (i * self.n_cols)
                tile = data["tile"]
                text = data["text"]
                val_d = self.positions[i + 1][j]["val"]

                if val == val_d:
                    # combine
                    new_val = val * 2
                elif val_d is None:
                    # shift
                    new_val = val
                else:
                    # do not set the right neighbour cell, or clear this cell as they cannot be combined or shifted.
                    continue

                self.set_cell(i + 1, j, new_val)
                self.clear_cell(i, j)

    def move_left(self, event):
        print(f"move_left {event}")
        for i in range(self.n_rows):
            for j in range(1, self.n_cols):

                data = self.positions[i][j]
                # print(f"{data=}")
                val = data["val"]
                if val is None:
                    continue

                idx = j + (i * self.n_cols)
                tile = data["tile"]
                text = data["text"]
                val_l = self.positions[i][j - 1]["val"]

                if val == val_l:
                    # combine
                    new_val = val * 2
                elif val_l is None:
                    # shift
                    new_val = val
                else:
                    # do not set the left neighbour cell, or clear this cell as they cannot be combined or shifted.
                    continue

                self.set_cell(i, j - 1, new_val)
                self.clear_cell(i, j)

    def move_right(self, event):
        print(f"move_right {event}")
        for i in range(self.n_rows):
            for j in range(self.n_cols - 2, -1, -1):

                data = self.positions[i][j]
                # print(f"{data=}")
                val = data["val"]
                if val is None:
                    continue

                idx = j + (i * self.n_cols)
                tile = data["tile"]
                text = data["text"]
                val_r = self.positions[i][j + 1]["val"]

                if val == val_r:
                    # combine
                    new_val = val * 2
                elif val_r is None:
                    # shift
                    new_val = val
                else:
                    # do not set the right neighbour cell, or clear this cell as they cannot be combined or shifted.
                    continue

                self.set_cell(i, j + 1, new_val)
                self.clear_cell(i, j)


if __name__ == "__main__":
    app = App()
    app.mainloop()
