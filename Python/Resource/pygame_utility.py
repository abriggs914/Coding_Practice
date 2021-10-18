from utility import *
from colour_utility import *

#	General Utility functions for pygame applications
#	Version...........1.25
#	Date........2021-10-18
#	Author....Avery Briggs


# BLACK = (0, 0, 0)  # black
# WHITE = (255, 255, 255)  # white
# DARK_GRAY = (50, 50, 50)  # dark gray
# LIGHT_GRAY = (175, 175, 175)  # light gray
# RED = (255, 0, 0)  # red
# GREEN = (0, 255, 0)  # green
# BLUE = (0, 0, 255)  # blue


NORTH = 4
NORTH_EAST = 5
EAST = 6
SOUTH_EAST = 7
SOUTH = 0
SOUTH_WEST = 1
WEST = 2
NORTH_WEST = 3

DIRECTIONS = {
    "N": {
        "dir": "north",
        "i": -1,
        "j": 0,
        "x": 0,
        "y": -1,
        "opp": "S",
        "bounce": "S",
        "mirror_x": "S",
        "mirror_y": "N"
    },
    "NE": {
        "dir": "north-east",
        "i": -1,
        "j": -1,
        "x": 1,
        "y": -1,
        "opp": "SW",
        "bounce": "NW",
        "mirror_x": "SE",
        "mirror_y": "NW"
    },
    "E": {
        "dir": "east",
        "i": 0,
        "j": -1,
        "x": 1,
        "y": 0,
        "opp": "W",
        "bounce": "W",
        "mirror_x": "E",
        "mirror_y": "W"
    },
    "SE": {
        "dir": "south-east",
        "i": 1,
        "j": -1,
        "x": 1,
        "y": 1,
        "opp": "NW",
        "bounce": "SW",
        "mirror_x": "NE",
        "mirror_y": "SW"
    },
    "S": {
        "dir": "south",
        "i": 1,
        "j": 0,
        "x": 0,
        "y": 1,
        "opp": "N",
        "bounce": "N",
        "mirror_x": "N",
        "mirror_y": "S"
    },
    "SW": {
        "dir": "south-west",
        "i": 1,
        "j": 1,
        "x": -1,
        "y": 1,
        "opp": "NE",
        "bounce": "SE",
        "mirror_x": "NW",
        "mirror_y": "SE"
    },
    "W": {
        "dir": "west",
        "i": 0,
        "j": 1,
        "x": -1,
        "y": 0,
        "opp": "E",
        "bounce": "E",
        "mirror_x": "W",
        "mirror_y": "E"
    },
    "NW": {
        "dir": "north-west",
        "i": -1,
        "j": 1,
        "x": -1,
        "y": -1,
        "opp": "SE",
        "bounce": "NE",
        "mirror_x": "SW",
        "mirror_y": "NE"
    }
}


# Create and return text surface and rect for blitting
def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Ensure that a text will fit into a given pygame.Rect object.
# Adjusts the message using new line characters to fit width-wise.
def wrap_text(msg, r, font):
    txt = ""
    for c in msg:
        txt += c
        text = txt.split("\n")
        txt_w, txt_h = font.size(text[-1])
        if txt_w >= r.width * 0.9:
            txt += "\n"
    return txt


# Writes text to the display.
def write_text(game, display, r, msg, font, bg_c=None, tx_c=BLACK, wrap=True):
    if isinstance(r, Rect2):
        r = game.Rect(*r)
    if not msg or msg is None:
        msg = "--"
    if wrap:
        msg = wrap_text(msg, r, font)
    lines = msg.split("\n")
    x, y, w, h = r
    to_blit = []
    length = max(2, len(lines))
    for i, line in enumerate(lines):
        text_surf, text_rect = text_objects(line, font, tx_c)
        width, height = font.size(line)
        text_rect.center = ((x + (w / 2)), (((i * height) + y) + (h / length)))
        to_blit.append((text_surf, text_rect))

    if bg_c is not None:
        # print("rect:", r)
        # print("rect:", type(r))
        game.draw.rect(display, bg_c, r)
    display.blits(to_blit)


class Widget:

    def __init__(self, game, display, rect):
        self.game = game
        self.display = display
        if isinstance(rect, Rect2):
            rect = game.Rect(*rect.tupl)
        self.rect = rect
        self.rect_obj = Rect2(rect.x, rect.y, rect.width, rect.height)

    def resize(self, rect):
        if isinstance(rect, Rect2):
            rect = self.game.Rect(*rect.tupl)
        self.rect = rect
        self.rect_obj = Rect2(rect.x, rect.y, rect.width, rect.height)

    def move(self, rect):
        if isinstance(rect, Rect2):
            rect = self.game.Rect(*rect.tupl)
        self.rect = rect
        self.rect_obj = Rect2(rect.x, rect.y, rect.width, rect.height)

    def draw(self):
        print("Nothing to draw")


# class RadioGroup(Widget):
#
#     def __init__(self, game, display, max_selections=None):
#         super().__init__(game, display)
#         self.max_selections = 1 if max_selections is None else max_selections
#         self.radio_buttons = []
#         self.selected = Queue(self.max_selections)
#
#     def __repr__(self):
#         return "<RadioGroup (" + str(len(self.radio_buttons)) + " buttons, " + str(self.selected.qsize()) + " / " + str(self.max_selections) + " selected)>"
#
#     def get_selected_buttons(self):
#         # TODO: this can probably be done more efficiently with a simple list
#         buttons = [self.selected.get() for i in range(self.selected.qsize())]
#         self.selected = Queue(self.max_selections)
#         for b in buttons:
#             self.selected.put(b)
#         return buttons
#
#     def set_max_selections(self, n):
#         self.max_selections = clamp(1, n, len(self.radio_buttons))
#         new_queue = Queue(self.max_selections)
#         buttons = self.get_selected_buttons()
#         for i, b in enumerate(buttons):
#             if i < self.max_selections:
#                 new_queue.put(b)
#             if i < len(buttons) and new_queue.full():
#                 button = new_queue.get()
#                 button.set_selected(False)
#         self.selected = new_queue
#
#     def add_buttons(self, *radio_buttons):
#         for button in radio_buttons:
#             self.radio_buttons.append(button)
#
#             # Button listener
#             buttonr(self.game, self.display, "", button.bounds, None, None, None, self.set_selected, [button])
#
#     def set_selected(self, radio_button):
#         print("click:",self.selected.qsize())
#         if radio_button not in self.get_selected_buttons():
#             if self.selected.full():
#                 b = self.selected.get()
#                 b.set_selected(False)
#             self.selected.put(radio_button)
#             radio_button.set_selected(True)
#
#     def clear_all_selected(self):
#         buttons = self.get_selected_buttons()
#         for b in buttons:
#             b.set_selected(False)
#         self.selected = Queue(self.max_selections)


class Label(Widget):

    def __init__(self, game, display, rect, init_txt="", font=None, c=WHITE, txc=BLACK, bc=BLACK, fs=16, bs=1,
                 border_style=None, font_sel=None, c_sel=WHITE, txc_sel=BLACK, bc_sel=BLACK, fs_sel=16, bs_sel=1,
                 border_style_sel=None, wrap_text=True):
        super().__init__(game, display, rect)
        # print("rect:", rect)
        # print("rect:", type(rect))
        self.font = font if font is not None else game.font.Font(None, 16)
        self.font_size = fs
        self.colour = c
        self.text_colour = txc
        self.border_colour = bc
        self.border_size = bs
        self.border_style = border_style
        self.text_str = init_txt
        self.wrap_text = wrap_text
        self.sel_font = font_sel if font_sel is not None else game.font.Font(None, 16)
        self.sel_colour = c_sel
        self.sel_text_colour = txc_sel
        self.sel_border_colour = bc_sel
        self.sel_font_size = fs_sel
        self.sel_border_size = bs_sel
        self.sel_border_style = border_style_sel

        self.is_selected = False

    def __repr__(self):
        return "<Label txt=\"" + self.text_str + "\">"

    def move(self, r):
        super().move(r)

    def resize(self, r, is_horizontal=True):
        super().resize(r)

    def draw(self):
        display = self.display
        game = self.game
        rect = self.rect
        bs = self.border_size
        trect = game.Rect(rect.x + bs, rect.y + bs, rect.width - (bs * 2), rect.height - (bs * 2))
        if self.is_selected:
            write_text(game, display, trect, self.text_str, self.sel_font, bg_c=self.sel_colour,
                       tx_c=self.sel_text_colour, wrap=self.wrap_text)
        else:
            write_text(game, display, trect, self.text_str, self.font, bg_c=self.colour, tx_c=self.text_colour,
                       wrap=self.wrap_text)


# TODO allow TextBox to overwrite the inc and dec functions. ex inc on a phone number should produce phone#n => phone#n + 1.
# TODO allow TextBox to center text
class TextBox(Widget):

    def __init__(self, game, display, rect, ic=GRAY_69, ac=WHITE, f=None, fc=BLACK, text='', min_width=20,
                 numeric=False, char_limit=None, n_limit=None, bs=1, border_style=None, draw_clear_btn=True,
                 editable=True, locked=False, iaction=None, daction=None, iargs=None, dargs=None, text_align=None,
                 fs=16):
        super().__init__(game, display, rect)
        self.ic = ic
        self.ac = ac
        self.font_size = fs
        self.f = f if f is not None else game.font.Font(None, self.font_size)
        self.fc = fc
        self.colour = ic
        self.text = text
        print("game:", game)
        print("f:", f)
        self.txt_surface = self.f.render(self.text, True, self.colour)
        self.active = False
        self.min_width = min_width
        self.numeric = numeric
        self.char_limit = None
        self.reset_char_limit()
        # max_chars = char_limit = rect.width / self.f.size(" ")[0]
        # if not char_limit:
        #     char_limit = max_chars
        # char_limit = min(max_chars, char_limit)
        # self.char_limit = char_limit
        if not n_limit or not isinstance(n_limit, range):
            print("adjust n_limit")
            if isinstance(n_limit, int):
                n_limit = range(2, n_limit)
            else:
                n_limit = range(5)
        n_start = 1
        n_stop = max(2, min(10, n_limit.stop))
        self.n_limit = range(min(n_start, n_stop), max(n_start, n_stop), 1)
        self.border_size = bs
        self.border_style = border_style
        self.draw_clear_btn = draw_clear_btn
        self.editable = editable
        self.locked = locked
        self.iaction = iaction if iaction is not None else self.increment
        self.daction = daction if daction is not None else self.decrement
        self.iargs = iargs
        self.dargs = dargs

        if str(text_align).lower() not in ["None", "left", "center", "right"]:
            text_align = None
        if text_align is not None:
            text_align = text_align.lower()
        self.text_align = text_align

    def __repr__(self):
        return "<TextBox txt=\"" + self.text_str + "\">"

    def count_n(self):
        txt = self.text
        nums = [s.strip() for s in txt.split(",") if isnumber(s.strip())]
        return len(nums)

    def handle_event(self, event):
        if not self.locked and self.editable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    # if self.active:

                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.colour = self.ac if self.active else self.ic
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        print("new_text:", self.text)
                        # if self.text.isdigit():
                        # 	DATA["input_dims"] = int(self.text)
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        txt = event.unicode
                        cn = self.count_n()
                        if len(self.text) < self.char_limit and ((cn in self.n_limit) or (cn < self.n_limit.start)):
                            if self.numeric:
                                if isnumber(str(txt)) or (len(self.text) == 0 and str(txt) == "-"):
                                    self.text += txt
                                    # DATA["input_dims"] = int(self.text)
                            else:
                                self.text += txt
                                # DATA["input_dims"] = self.text

                    # Re-render the text.
                    if self.text:
                        self.txt_surface = self.f.render(self.text, True, self.fc)

    def increment(self, *args, **kwargs):
        try:
            self.text = str(int(self.text) + 1)
        except ValueError:
            self.text = str(self.text) + "1"

    def decrement(self, *args, **kwargs):
        try:
            self.text = str(int(self.text) - 1)
        except ValueError:
            self.text = str(self.text)[:len(str(self.text)) - 1]

    def move(self, r):
        super().move(r)
        self.reset_char_limit()

    def resize(self, r):
        super().resize(r)
        self.reset_char_limit()

    def reset_char_limit(self):
        max_chars = char_limit = self.rect.width / self.f.size(" ")[0]
        if not char_limit:
            char_limit = max_chars
        char_limit = min(max_chars, char_limit)
        self.char_limit = char_limit

    def set_text(self, txt):
        self.text = txt

    def get_text(self):
        return self.text

    def clear(self):
        print("clearing textbox: <{}>".format(self.text))
        self.set_text("")

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.min_width, self.txt_surface.get_width() + 10)
        self.rect.width = width

    def draw(self):
        display = self.display
        game = self.game
        rect = self.rect
        bs = self.border_size
        trect = game.Rect(rect.x + bs, rect.y + bs, rect.width - (bs * 2), rect.height - (bs * 2))
        txt = str(self.text)
        # TODO fix this
        # if self.text_align == "center":
        #     txt = pad_centre(txt, )
        # elif self.text_align == "right":
        self.txt_surface = self.f.render(txt, True, self.colour)

        text_rect = self.txt_surface.get_rect(center=self.rect.center)

        # Blit the text.
        display.blit(self.txt_surface, text_rect)
        # display.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(display, self.colour, self.rect, 2)
        # draw_button("X", self.rect.right + 10, self.rect.y, 20, 20, self.ic, self.ac, self.colour, self.f, self.fc, self.clear)
        xrect = Rect2(rect.x + 5, rect.y + (rect.height * 0.075), rect.width, rect.height).translated(rect.width,
                                                                                                      0).scaled(0.15,
                                                                                                                0.85)
        irect = xrect.scaled(0.45, 0.45).translated(0, 0)
        drect = xrect.scaled(0.45, 0.45).translated(0, irect.height + (xrect.height * 0.1))
        if self.numeric:
            if self.locked:
                iaction = None
                iargs = [], {}
                daction = None
                dargs = [], {}
            else:
                iaction = self.iaction
                iargs = self.iargs
                daction = self.daction
                dargs = self.dargs
            ibutton = Button(game, display, "+", irect, WHITE, WHITE, None, font_size=self.font_size, action=iaction,
                             args=iargs)
            dbutton = Button(game, display, "-", drect, WHITE, WHITE, None, font_size=self.font_size, action=daction,
                             args=dargs)
            dbutton.enable_toggle()
            ibutton.enable_toggle()
            ibutton.draw()
            dbutton.draw()

            xrect = xrect.translated(irect.width + 5, 0)
        if self.draw_clear_btn:
            # xrect = Rect(rect.x + 5, rect.y + (rect.height * 0.075), rect.width, rect.height).translated(rect.width, 0).scaled(0.15, 0.85)
            action = None if self.locked else self.clear
            button = Button(game, display, "X", xrect, WHITE, WHITE, None, action=action, font_size=self.font_size)
            button.enable_toggle()
            button.draw()


# class TextBox(Widget):
#
#     def __init__(self, game, display, rect, init_txt="", font=None, c=WHITE, txc=BLACK, bc=BLACK, fs=16, bs=1, border_style=None, font_sel=None, c_sel=WHITE, txc_sel=BLACK, bc_sel=BLACK, fs_sel=16, bs_sel=1, border_style_sel=None, wrap_text=True):
#         super().__init__(game, display)
#         if isinstance(rect, Rect):
#             rect = game.Rect(*rect)
#         # print("rect:", rect)
#         # print("rect:", type(rect))
#         self.rect = rect
#         self.font = font if font is not None else game.font.Font(None, 16)
#         self.fs = fs
#         self.colour = c
#         self.text_colour = txc
#         self.border_colour = bc
#         self.border_size = bs
#         self.border_style = border_style
#         self.text_str = init_txt
#         self.wrap_text = wrap_text
#         self.sel_font = font_sel if font_sel is not None else game.font.Font(None, 16)
#         self.sel_colour = c_sel
#         self.sel_text_colour = txc_sel
#         self.sel_border_colour = bc_sel
#         self.sel_font_size = fs_sel
#         self.sel_border_size = bs_sel
#         self.sel_border_style = border_style_sel
#
#         self.is_selected = False
#
#     def __repr__(self):
#         return "<TextBox txt=\"" + self.text_str + "\">"
#
#     def click_selection(self):
#         print("Clicked TextBox: sel status:", self.is_selected)
#         self.is_selected = not self.is_selected
#
#     def move(self, r):
#         pass
#
#     def resize(self, r, is_horizontal=True):
#         pass
#
#     def draw(self):
#         display = self.display
#         game = self.game
#         rect = self.rect
#         bs = self.border_size
#         trect = game.Rect(rect.x + bs, rect.y + bs, rect.width - (bs * 2), rect.height - (bs * 2))
#         button = Button(game, display, "", *rect, WHITE, WHITE, None, action=self.click_selection)
#         button.enable_toggle()
#         button.draw()
#         if self.is_selected:
#             write_text(game, display, trect, self.text_str, self.sel_font, bg_c=self.sel_colour, tx_c=self.sel_text_colour, wrap=self.wrap_text)
#         else:
#             write_text(game, display, trect, self.text_str, self.font, bg_c=self.colour, tx_c=self.text_colour, wrap=self.wrap_text)


class RadioGroup(Widget):

    def __init__(self, game, display, max_selections=None):
        super().__init__(game, display, None)
        self.max_selections = 1 if max_selections is None else max_selections
        self.radio_buttons = []
        self.selected = []
        self.keep_grouped = True

    def __repr__(self):
        return "<RadioGroup (" + str(len(self.radio_buttons)) + " buttons, " + str(len(self.selected)) + " / " + str(
            self.max_selections) + " selected)>"

    def set_max_selections(self, n):
        n = clamp(1, n, len(self.radio_buttons))
        self.max_selections = n
        if n < len(self.selected):
            unselect = self.selected[len(self.selected) - n:]
            for button in unselect:
                button.set_selected(False)

    def add_buttons(self, *radio_buttons):
        for button in radio_buttons:
            self.radio_buttons.append(button)
        # sort list for resizing purposes, don't want any overlap.
        self.sort_buttons()

    # sort the list of buttons by increasing x coordinates
    def sort_buttons(self):
        print("BEFORE radio buttons", self.radio_buttons)
        self.radio_buttons.sort(key=lambda rb: rb.bounds.x)
        print("AFTER radio buttons", self.radio_buttons)

    def set_selected(self, radio_button):
        if radio_button not in self.selected:
            if len(self.selected) == self.max_selections:
                b = self.selected.pop(0)
                b.set_selected(False)
            self.selected.append(radio_button)
            radio_button.set_selected(True)

    def clear_all_selected(self):
        for b in self.selected:
            b.set_selected(False)
        self.selected = []

    def set_keep_grouped(self, g):
        self.keep_grouped = g

    def move(self, r):
        if len(self.radio_buttons) > 0:
            first_bounds = self.radio_buttons[0].bounds
            diff_bounds = r.x - first_bounds.x, r.y - first_bounds.y
            for button in self.radio_buttons:
                new_r = self.game.Rect(diff_bounds[0] + button.bounds.x, diff_bounds[1] + button.bounds.y,
                                       button.bounds.width, button.bounds.height)
                button.move(new_r)

    def resize(self, r, is_horizontal=True):
        if len(self.radio_buttons) > 0:
            first_bounds = self.radio_buttons[0].bounds
            diff_bounds = r.width - first_bounds.width, r.height - first_bounds.height
            # print("first_bounds:", first_bounds)
            # print("first_bounds:", first_bounds)
            # print("r_bounds:", r)
            # print("diff_bounds:", diff_bounds)
            nb = len(self.radio_buttons)
            w = r.width / nb if is_horizontal else r.width
            h = r.height / nb if not is_horizontal else r.height
            for i, button in enumerate(self.radio_buttons):
                # new_r = self.game.Rect(button.bounds.x, button.bounds.y, diff_bounds[0] + button.bounds.width,
                #                        diff_bounds[1] + button.bounds.height)
                new_r = self.game.Rect(button.bounds.x, button.bounds.y, w, h)
                if i < len(self.radio_buttons) - 1:
                    next_bounds = self.radio_buttons[i + 1].bounds
                    x_diff = abs(new_r.right - next_bounds.x) if is_horizontal else 0
                    y_diff = abs(new_r.bottom - next_bounds.y) if not is_horizontal else 0
                    if new_r.colliderect(next_bounds):
                        # x_diff = new_r.right - next_bounds.x if is_horizontal else 0
                        # y_diff = new_r.bottom - next_bounds.y if not is_horizontal else 0
                        next_bounds = self.game.Rect(next_bounds.x + x_diff, next_bounds.y + y_diff, next_bounds.width,
                                                     next_bounds.height)
                        self.radio_buttons[i + 1].move(next_bounds)
                        print("next_bounds:", next_bounds)
                    elif self.keep_grouped:
                        # x_diff = next_bounds.x - new_r.right if is_horizontal else 0
                        # y_diff = next_bounds.y - new_r.bottom if not is_horizontal else 0
                        next_bounds = self.game.Rect(next_bounds.x - x_diff, next_bounds.y - y_diff, next_bounds.width,
                                                     next_bounds.height)
                        self.radio_buttons[i + 1].move(next_bounds)
                        print("next_bounds:", next_bounds)

                button.resize(new_r)

    def draw(self):
        for button in self.radio_buttons:
            b = buttonr(self.game, self.display, "", button.bounds, None, None, None, self.set_selected, [button])
            b.draw()
            button.draw()


class RadioButton(Widget):

    # Create a RadioButton, used to act as a selection switch between multiple options.
    # Must be accompanied by a RadioGroup in order to interact with the widget, otherwise
    # only shows the set selection state of the button.
    def __init__(self, game, display, rect, msg, font=None, c=None, sc=None, txc=None, bgc=None):
        super().__init__(game, display, rect)
        self.bounds = self.rect
        self.radius = None
        self.set_radius(self.calc_radius())
        self.msg = msg

        self.font = font if font is not None else game.font.Font(None, 16)
        self.c = c
        self.sc = sc if sc is not None else darken(c, 0.6)
        self.txc = txc if txc is not None else BLACK
        self.bgc = bgc  # can be None, will have no background
        self.div_c = BLACK
        self.div_w = 3
        self.draw_border = bgc is not None
        self.is_selected = False
        # normal color
        # selected color
        # 2 circles, outer button, and inner depressed button
        # label text color
        # label background color
        # label font
        # label message

    def __repr__(self):
        return "RadioButton<(" + self.msg + ") " + str(self.bounds) + ">"

    def calc_radius(self):
        bounds = self.bounds
        return (min(bounds.height, bounds.width) * 0.6) / 2

    def move(self, r):
        self.bounds = self.game.Rect(r.x, r.y, self.bounds.width, self.bounds.height)

    def resize(self, r):
        self.bounds = self.game.Rect(self.bounds.x, self.bounds.y, r.width, r.height)
        self.set_radius(self.calc_radius())

    def set_radius(self, r):
        self.radius = round(r)

    def set_label(self, msg):
        self.msg = msg

    def set_font(self, f):
        self.font = f

    def set_button_color(self, c):
        self.c = c

    def set_selected_color(self, c):
        self.sc = c

    def set_text_color(self, c):
        self.txc = c

    def set_background_color(self, c):
        self.bgc = c

    def set_border_color(self, c):
        self.div_c = c

    def set_border_width(self, w):
        self.div_w = w

    def set_draw_border(self, t):
        self.draw_border = t

    def set_selected(self, t):
        self.is_selected = t

    def toggle(self):
        self.is_selected = not self.is_selected

    def draw(self):
        if self.bgc is not None:
            # draw background
            self.game.draw.rect(self.display, self.bgc, self.bounds)

        # draw border lines
        if self.draw_border:
            self.game.draw.line(self.display, self.div_c, self.bounds.topleft, self.bounds.topright, self.div_w)
            self.game.draw.line(self.display, self.div_c, self.bounds.topleft, self.bounds.bottomleft, self.div_w)
            self.game.draw.line(self.display, self.div_c, self.bounds.topright, self.bounds.bottomright, self.div_w)
            self.game.draw.line(self.display, self.div_c, self.bounds.bottomleft, self.bounds.bottomright, self.div_w)

        # draw circle
        c_x, c_y = self.bounds.centerx, self.bounds.bottom - self.radius - self.div_w
        self.game.draw.circle(self.display, self.c, (c_x, c_y), self.radius, self.div_w)

        if self.is_selected:
            self.game.draw.circle(self.display, self.sc, (c_x, c_y), round(self.radius * 0.5))

        # draw label
        title_rect = self.game.Rect(self.bounds.left + self.div_w, self.bounds.top + self.div_w,
                                    self.bounds.width - (2 * self.div_w),
                                    self.bounds.height - (2 * (self.radius + self.div_w)))
        write_text(self.game, self.display, title_rect, self.msg, self.font, self.bgc, wrap=True)


# display a button and listen for it to be clicked.
# shorter signature, but requires a pygame.Rect object for sizing.
# game      -   pygame object
# display   -   display created by pygame
# msg 		- 	button text
# r			-	pygame rect shape
# ic		-	button color
# ac		-	button color when hovering
# font      -   font style
# action	-	function to be called on click
def buttonr(game, display, msg, r, ic, ac, font, action=None, args=None):
    return Button(game, display, msg, r, ic, ac, font, action, args)


class Button(Widget):

    def __init__(self, game, display, msg, rect, ic=GRAY_69, ac=None, font=None, font_size=16, action=None, args=None,
                 text_colour=BLACK):
        super().__init__(game, display, rect)
        self.msg = msg
        self.ic = ic
        self.ac = ac if ac is not None else brighten(ic, 0.15)
        self.font = font if font is not None else game.font.Font(None, font_size)
        self.action = action
        if args is not None:
            if not isinstance(args, list) or not isinstance(args, tuple):
                args = [args]
        self.args = args
        self.resize(rect)

        self.draw_rect = ic is not None  # if ic is None, no background square is drawn
        self.draw_hover = ac is not None  # if ac is None, no hover square is drawn

        self.scrollable = False
        self.scroll_up_func = None
        self.scroll_up_args = None
        self.scroll_down_func = None
        self.scroll_down_args = None

        self.toggleable = False
        self.toggle_val = False
        self.text_colour = text_colour

    def move(self, r):
        super().move(r)

    def resize(self, r):
        super().resize(r)

    def enable_toggle(self):
        self.toggleable = True

    def disable_toggle(self):
        self.toggleable = False

    def toggle(self):
        self.toggle_val = not self.toggle_val

    # add scrolling functionality to a button.
    # up_func       -   function to execute on scroll up
    # up_args       -   arguments to pass to scroll up function
    # down_func     -   function to execute on scroll down
    # down_args     -   arguments to pass to scroll down function
    def enable_scrollable(self, up_func, up_args, down_func, down_args):
        self.scrollable = True
        self.scroll_up_func = up_func
        self.scroll_up_args = up_args
        self.scroll_down_func = down_func
        self.scroll_down_args = down_args

    def disable_scrollable(self):
        self.scrollable = False
        self.scroll_up_func = None
        self.scroll_up_args = None
        self.scroll_down_func = None
        self.scroll_down_args = None

    def draw(self):
        mouse = self.game.mouse.get_pos()
        click = self.game.mouse.get_pressed()

        # mouse in button bounds
        if self.rect.collidepoint(mouse):
            if self.draw_rect:
                self.game.draw.rect(self.display, self.ac, self.rect)
            # left click
            if click[0] == 1:
                if self.action is not None:
                    if self.args is None:
                        self.action()
                    else:
                        self.action(*self.args)
                # check toggling
                if self.toggleable:
                    self.toggle()
                    self.game.event.wait()
            # check scrolling
            elif self.scrollable:
                event = self.game.event.poll()
                if event.type == self.game.locals.MOUSEBUTTONDOWN or event.type == self.game.locals.MOUSEBUTTONUP:
                    # scroll up
                    if event.button == 4:
                        self.scroll_up_func(*self.scroll_up_args)
                    # scroll down
                    elif event.button == 5:
                        self.scroll_down_func(*self.scroll_down_args)

        elif self.toggleable and self.toggle_val:
            if self.draw_hover:
                self.game.draw.rect(self.display, self.ac, self.rect)
        elif self.draw_rect:
            self.game.draw.rect(self.display, self.ic, self.rect)

        # print("toggleable:", self.toggleable, "toggle_val:", self.toggle_val)

        # draw button label
        self.font.set_bold(True)
        text_surf, text_rect = text_objects(self.msg, self.font, self.text_colour)
        text_rect.center = ((self.rect.x + (self.rect.width / 2)), (self.rect.y + (self.rect.height / 2)))
        self.display.blit(text_surf, text_rect)


class ButtonBar(Widget):

    # display a bar of buttons and listen for them to be clicked.
    # game          -   pygame object
    # display       -   display created by pygame
    # x			    -	bar x
    # y			    -	bar y
    # w			    -	bar width
    # h			    -	bar height
    # font          -   button font style
    # bg            -   bar background color
    # proportion    -   proportion of the total bar to consume
    # is_horizontal -   whether the bar is horizontal or vertical
    def __init__(self, game, display, rect, font=None, bg=WHITE, proportion=1, is_horizontal=True, font_size=16):
        super().__init__(game, display, rect)
        self.font = font if font is not None else game.font.Font(None, 16)
        self.bg = bg
        self.proportion = proportion
        self.is_horizontal = is_horizontal
        self.font_size = font_size

        self.buttons = {}

    # No need to move buttons within bar, since their placement is calculated in the draw function.
    def move(self, r):
        super().move(r)

    # No need to resize buttons within bar, since their placement is calculated in the draw function.
    def resize(self, r):
        super().resize(r)

    # Using information, add a button to the bar.
    # msg       -   button name
    # ic        -   button color
    # ac        -   button color when hovering
    # action    -   function to be executed on click
    # args      -   tuple of function args
    # ex: self.add_button("Click Me", RED, brighten(RED, 0.15), eval, "print(\"Hey!\")")
    def add_button(self, msg, ic, ac, action=None, args=None):
        button = {msg: (ic, ac, action, args)}
        self.buttons.update(button)

    def draw(self):
        nb = len(self.buttons)  # number buttons
        wp = (self.rect.width * self.proportion)  # width proportional
        hp = (self.rect.height * self.proportion)  # height proportional
        xd = self.rect.width - wp  # difference between total width and proportional width
        yd = self.rect.height - hp  # difference between total height and proportional height
        xi = self.rect.x + (xd / 2)  # starting x
        yi = self.rect.y + (yd / 2)  # starting y
        if self.is_horizontal:
            wi = wp / max(1, nb)  # single button width
            hi = hp
        else:
            wi = wp
            hi = hp / max(1, nb)  # single button height
        # wi = wp / max(1, (nb if self.is_horizontal else wp))  # single button width
        # hi = hp / max(1, (nb if self.is_horizontal else hp))  # single button height

        # draw background
        self.game.draw.rect(self.display, self.bg, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

        # create and draw buttons
        for b, info in self.buttons.items():
            # button = Button(self.game, self.display, b, xi, yi, wi, hi, *info[:2], self.font, *info[2:])
            button = Button(self.game, self.display, b, Rect2(xi, yi, wi, hi), *info[:2], self.font, self.font_size,
                            *info[2:])
            button.enable_toggle()
            button.draw()
            if self.is_horizontal:
                xi += (xd / (nb + 1)) + wi
            else:
                yi += (yd / (nb + 1)) + hi


class ScrollBar(Widget):

    def __init__(self, game, display, x, y, w, h, bar_proportion, button_c, bar_background_c, bar_c, contents,
                 content_c, is_vertical=True):
        super().__init__(game, display, Rect2(x, y, w, h))
        self.bar_proportion = bar_proportion
        self.button_c = button_c
        self.bar_background_c = bar_background_c
        self.bar_c = bar_c
        self.contents = [contents] if not isinstance(contents, list) else contents
        self.content_c = content_c
        self.is_vertical = is_vertical

        self.bar_bounds = None
        self.content_bounds = None
        self.widget_bounds = None
        self.set_bounds(x, y, w, h)
        self.bar_val = 0  # 0-100 based on the position of the scroll bar

    def set_bounds(self, x, y, w, h):
        # TODO: adjust content sizes somehow
        if self.is_vertical:
            self.bar_bounds = self.game.Rect(x, y, w * self.bar_proportion, h)
            self.content_bounds = self.game.Rect(x + self.bar_bounds.width, y, w - self.bar_bounds.width, h)
        else:
            self.bar_bounds = self.game.Rect(x, y, w, h * self.bar_proportion)
            self.content_bounds = self.game.Rect(x, y + self.bar_bounds.height, w, h - self.bar_bounds.height)

        self.widget_bounds = self.content_bounds.union(self.bar_bounds)
        self.rect = self.widget_bounds

    def move(self, r):
        self.set_bounds(r.x, r.y, r.width, r.height)

    def resize(self, r):
        self.set_bounds(r.x, r.y, r.width, r.height)

    # Draw an arrow in 1 of 8 directions, denoted by the orientations above.
    # r     -   pygame.Rect object for sizing
    # p     -   float between 0 and 1 for border size around the arrow within the square (0 - 1)
    # o     -   orientation of the arrow using one of the orientations above (0 - 8)
    # c     -   line color of the arrow
    # w     -   line width of the arrow (w >= 1)
    def draw_arrow(self, r, p, o, c, w):
        # p1 - tip
        # p2 - first wing
        # p3 - second wing
        p1x = r.center[0]
        p1y = r.center[1] + (r.height * p)
        p2x = r.center[0] - (r.width * p)
        p2y = r.center[1] - (r.height * p)
        p3x = r.center[0] + (r.width * p)
        p3y = r.center[1] - (r.height * p)
        points = [rotate_point(*r.center, *pt, o * 45) for pt in [(p2x, p2y), (p1x, p1y), (p3x, p3y)]]

        self.game.draw.lines(self.display, c, False, points, w)
        return points

    def get_scroll_pos(self):
        return self.bar_val

    def set_scroll_pos(self, val):
        self.bar_val = val

    def increment_bar_pos(self, n=1):
        if n > 0:
            if self.bar_val < 100:
                self.bar_val += 1
                self.increment_bar_pos(n - 1)

    def decrement_bar_pos(self, n=1):
        if n > 0:
            if self.bar_val > 0:
                self.bar_val -= 1
                self.decrement_bar_pos(n - 1)

    # Using the bar_val attribute, determine where the scroll bar should be positioned on the background.
    def decode_bar_pos(self):
        # TODO: width and height attributes are hardcoded, need to represent the height and width of the contents
        bounds = self.bar_bounds
        if self.is_vertical:
            width = bounds.width * 0.8
            height = 75
            x = bounds.x + (bounds.width * 0.1)
            y = bounds.y + (bounds.height * 0.1) + ((self.bar_val / 100) * ((bounds.height * 0.8) - height))
        else:
            width = 10
            height = bounds.height * 0.8
            y = bounds.y + (bounds.height * 0.1)
            x = bounds.x + (bounds.width * 0.1) + ((self.bar_val / 100) * ((bounds.width * 0.8) - width))

        # print("bar_pos:", self.game.Rect(x, y, width, height))
        return x, y, width, height

    # Using either x or y mouse coordinates, return the position of the top of the scroll bar.
    # Ensures the bar will be encapsulated within the bounds of the scroll area.
    def encode_bar_pos(self, pos):
        bounds = self.bar_bounds
        if self.is_vertical:
            val = min(1, (max(0, pos - bounds.top)) / ((bounds.bottom - bounds.top) * 0.8)) * 100
        else:
            val = min(1, (max(0, pos - bounds.left)) / ((bounds.right - bounds.left) * 0.8)) * 100
        return val

    # Called when the bar is clicked and dragged.
    # Updates the scroll bar's bar_val attribute.
    def move_bar(self):
        mouse_pos = self.game.mouse.get_pos()
        bounds = self.bar_bounds  # self.game.Rect(self.x, self.y, self.w, self.h)
        if bounds.collidepoint(mouse_pos):
            if self.is_vertical:
                button_space = bounds.height * 0.1
                y = mouse_pos[1] - button_space
                val = self.encode_bar_pos(y)
            else:
                button_space = bounds.width * 0.1
                x = mouse_pos[0] - button_space
                val = self.encode_bar_pos(x)
            self.set_scroll_pos(val)

    # content can be nested widgets, strings, pictures..
    def add_contents(self, content):
        self.contents.append(content)
        # TODO needs work, will be nested widgets or generic texts

    def draw(self):
        background = self.bar_bounds  # self.game.Rect(self.x, self.y, self.w, self.h)
        if self.is_vertical:
            space = background.height * 0.1
            bar_background = self.game.Rect(background.x, (background.y + space), background.width,
                                            (background.height - (2 * space)))
            scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
                                    self.bar_background_c, font=None, action=self.move_bar)
            scroll_percent = round((background.height - (2 * space)) * 0.02)
            increment_button_rect = self.game.Rect(background.left, background.top, background.width, space)
            decrement_button_rect = self.game.Rect(background.left, background.bottom - space, background.width, space)
            increment_button_arrow = NORTH
            decrement_button_arrow = SOUTH

            bar_rect = self.game.Rect(*self.decode_bar_pos())
        else:
            space = background.width * 0.1
            bar_background = self.game.Rect(background.x + space, background.y, (background.width - (2 * space)),
                                            background.height)
            scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
                                    self.bar_background_c, font=None, action=self.move_bar)
            scroll_percent = round((background.width - (2 * space)) * 0.02)
            increment_button_rect = self.game.Rect(background.left, background.top, space, background.height)
            decrement_button_rect = self.game.Rect(background.right - space, background.top, space, background.height)
            increment_button_arrow = WEST
            decrement_button_arrow = EAST
            bar_rect = self.game.Rect(*self.decode_bar_pos())

        # enable mouse scrolling for entire widget
        widget_button = buttonr(self.game, self.display, "", self.widget_bounds, self.bar_background_c,
                                self.bar_background_c, font=None, action=None)
        widget_button.enable_scrollable(self.decrement_bar_pos, [scroll_percent], self.increment_bar_pos,
                                        [scroll_percent])
        widget_button.draw()

        # draw scroll background
        scroll_button.draw()

        # draw increment, decrement buttons
        increment_button = Button(self.game, self.display, "", increment_button_rect, self.button_c, self.button_c,
                                  font=None,
                                  action=self.decrement_bar_pos)
        decrement_button = Button(self.game, self.display, "", decrement_button_rect, self.button_c, self.button_c,
                                  font=None, action=self.increment_bar_pos)
        increment_button.draw()
        decrement_button.draw()

        # draw increment, decrement arrows
        self.draw_arrow(increment_button_rect, 0.2, increment_button_arrow, BLACK, 3)
        self.draw_arrow(decrement_button_rect, 0.2, decrement_button_arrow, BLACK, 3)

        # draw bar
        self.game.draw.rect(self.display, self.bar_c, bar_rect)

        # draw content background
        self.game.draw.rect(self.display, self.content_c, self.content_bounds)

    # def draw(self):
    #     background = self.game.Rect(self.x, self.y, self.w, self.h)
    #     if self.is_vertical:
    #         space = background.height * 0.1
    #         bar_background = self.game.Rect(self.x, (self.y + space), self.w, (self.h - (2 * space)))
    #         scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
    #                                 self.bar_background_c, font=None, action=self.move_bar)
    #         scroll_percent = round((self.h - (2 * space)) * 0.02)
    #         scroll_button.enable_scrollable(self.decrement_bar_pos, [scroll_percent], self.increment_bar_pos, [scroll_percent])
    #         scroll_button.draw()
    #         top_button_rect = self.game.Rect(background.left, background.top, background.width, space)
    #         bottom_button_rect = self.game.Rect(background.left, background.bottom - space, background.width, space)
    #         top_button = Button(self.game, self.display, "", *top_button_rect, self.button_c, self.button_c, font=None,
    #                             action=self.decrement_bar_pos)
    #         bottom_button = Button(self.game, self.display, "", *bottom_button_rect, self.button_c, self.button_c,
    #                                font=None, action=self.increment_bar_pos)
    #         top_button.draw()
    #         bottom_button.draw()
    #         # self.game.draw.rect(self.display, self.button_c, top_button_rect)
    #         # self.game.draw.rect(self.display, self.button_c, bottom_button_rect)
    #         # down arrow - left side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (bottom_button_rect.left + (bottom_button_rect.width * 0.2)),
    #                                 (bottom_button_rect.top + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 bottom_button_rect.center[0],
    #                                 (bottom_button_rect.center[1] + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # down arrow - right side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (bottom_button_rect.right - (bottom_button_rect.width * 0.2)),
    #                                 (bottom_button_rect.top + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 bottom_button_rect.center[0],
    #                                 (bottom_button_rect.center[1] + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # up arrow - left side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (top_button_rect.left + (top_button_rect.width * 0.2)),
    #                                 (top_button_rect.bottom - (top_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 top_button_rect.center[0],
    #                                 (top_button_rect.center[1] - (top_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # up arrow - right side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (top_button_rect.right - (top_button_rect.width * 0.2)),
    #                                 (top_button_rect.bottom - (top_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 top_button_rect.center[0],
    #                                 (top_button_rect.center[1] - (top_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         bar_rect = self.game.Rect(*self.decode_bar_pos())
    #     else:
    #         space = background.width * 0.1
    #         bar_background = self.game.Rect(self.x + space, self.y, (self.w - (2 * space)), self.h)
    #         scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
    #                                 self.bar_background_c, font=None, action=self.move_bar)
    #         scroll_percent = round((self.w - (2 * space)) * 0.02)
    #         scroll_button.enable_scrollable(self.decrement_bar_pos, [scroll_percent], self.increment_bar_pos, [scroll_percent])
    #         scroll_button.draw()
    #         left_button_rect = self.game.Rect(background.left, background.top, space, background.height)
    #         right_button_rect = self.game.Rect(background.right - space, background.top, space, background.height)
    #         left_button = Button(self.game, self.display, "", *left_button_rect, self.button_c, self.button_c,
    #                              font=None,
    #                              action=self.decrement_bar_pos)
    #         right_button = Button(self.game, self.display, "", *right_button_rect, self.button_c, self.button_c,
    #                               font=None,
    #                               action=self.increment_bar_pos)
    #         left_button.draw()
    #         right_button.draw()
    #
    #         # self.game.draw.rect(self.display, self.button_c, left_button_rect)
    #         # self.game.draw.rect(self.display, self.button_c, right_button_rect)
    #         # right arrow - top side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (right_button_rect.left + (right_button_rect.width * 0.2)),
    #                                 (right_button_rect.top + (right_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 (right_button_rect.center[0] + (right_button_rect.width * 0.2)),
    #                                 right_button_rect.center[1]
    #                             ),
    #                             3)
    #         # right arrow - bottom side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (right_button_rect.center[0] + (right_button_rect.width * 0.2)),
    #                                 right_button_rect.center[1]
    #                             ),
    #                             (
    #                                 (right_button_rect.left + (right_button_rect.width * 0.2)),
    #                                 (right_button_rect.bottom - (right_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # left arrow - top side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (left_button_rect.right - (left_button_rect.width * 0.2)),
    #                                 (left_button_rect.top + (left_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 (left_button_rect.center[0] - (left_button_rect.width * 0.2)),
    #                                 left_button_rect.center[1]
    #                             ),
    #                             3)
    #         # left arrow - bottom side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (left_button_rect.right - (left_button_rect.width * 0.2)),
    #                                 (left_button_rect.bottom - (left_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 (left_button_rect.center[0] - (left_button_rect.width * 0.2)),
    #                                 left_button_rect.center[1]
    #                             ),
    #                             3)
    #         bar_rect = self.game.Rect(*self.decode_bar_pos())
    #     self.game.draw.rect(self.display, self.bar_c, bar_rect)


class TableRow(Widget):

    def __init__(self, game, display):
        super().__init__(game, display, None)

        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.bounds = None
        self.contents = []
        self.cols = len(self.contents)
        self.div_c = BLACK
        self.div_w = 3
        self.c = WHITE
        self.tx_c = BLACK
        self.font = game.font.Font(None, 16)

    def set_row_font(self, f):
        self.font = f

    def set_row_color(self, c):
        self.c = c

    def set_divider_color(self, c):
        self.div_c = c

    def set_divider_width(self, w):
        self.div_w = w

    def set_text_color(self, c):
        self.tx_c = c

    def update_bounds(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.bounds = self.game.Rect(x, y, w, h)

    # Insert either a single cell of data to the row, or a list of data points for the row of cells.
    def add_content(self, content):
        if isinstance(content, list):
            for c in content:
                self.contents.append(c)
        else:
            self.contents.append(content)
        self.cols = len(self.contents)

    # Get the cell data from row's contents at index col.
    def get_data(self, col):
        data = None
        if -1 < col < self.cols:
            data = self.contents[col]
        return data

    def move(self, r):
        self.update_bounds(r.x, r.y, self.width, self.height)

    def resize(self, r):
        self.update_bounds(self.x, self.y, r.width, r.height)

    def draw(self):
        bounds = self.bounds
        n_dividers = max(1, self.cols)
        divider_space = (bounds.width / n_dividers)
        xi = bounds.left
        for i in range(n_dividers + 1):
            if i < self.cols:
                cell_bounds = self.game.Rect(xi, bounds.y, divider_space, bounds.h)
                # cell_surface, cell_rect = text_objects(self.contents[i], self.font)
                write_text(self.game, self.display, cell_bounds, self.contents[i], self.font, self.c, self.tx_c)
                # center text within cell TODO : add option for gravity and orientation
                # cell_rect.center = (
                #     (cell_bounds.x + (cell_bounds.width / 2)), (cell_bounds.y + (cell_bounds.height / 2))
                # )
                # self.game.draw.rect(self.display, self.c, cell_bounds)
                # self.display.blit(cell_surface, cell_rect)

            self.game.draw.line(self.display, self.div_c, (xi, bounds.top), (xi, bounds.bottom), self.div_w)
            xi += divider_space


class Table(Widget):

    # Create a generic table with a title and header.
    def __init__(self, game, display, x, y, w, h, c, font, title, header):
        super().__init__(game, display, Rect2(x, y, w, h))
        self.c = c
        self.font = font if font is not None else game.font.Font(None, 16)
        self.title = title.title()
        self.header = header

        self.title_color = BLACK
        self.div_c = BLACK
        self.div_w = 3

        self.table_rows = []

        self.set_header(header)

    # Return a TableRow object from index r.
    def get_row(self, r):
        row = None
        if -1 < r < len(self.table_rows):
            row = self.table_rows[r]
        return row

    # Return a list of all column data using a header value.
    def get_col_data(self, c_name):
        h = list(map(str.lower, self.header))
        if c_name.lower() in h:
            idx = self.header.index(c_name)
            return self.get_col(idx)
        return []

    def get_col(self, c_index):
        return [row.contents[c_index] for row in self.table_rows if c_index < row.cols][1:]

    # Get the cell data from row r and col c.
    def get_data(self, r, c):
        row = self.get_row(r)
        if row is not None:
            return row.get_data(c)

    def set_title_color(self, c):
        self.title_color = c
        header_row = self.table_rows[0]
        header_row.set_row_color(self.c)
        header_row.set_text_color(self.title_color)

    def set_table_color(self, c):
        self.c = c

    def set_divider_color(self, c):
        self.div_c = c

    def set_divider_width(self, w):
        self.div_w = w

    def set_title(self, t):
        self.title = t

    def set_header(self, h):
        self.header = h
        header_row = TableRow(self.game, self.display)
        header_row.add_content(list(map(str.title, map(str, h))))
        if len(self.table_rows) > 0:
            self.table_rows = self.table_rows[1:]
        self.add_row(header_row, 0)

    def set_font(self, f):
        self.font = f

    def move(self, r):
        super().move(r)
        for row in self.table_rows:
            row.move(r)
        self.update_row_sizes()

    def resize(self, r):
        # def resize(self, r):
        #     self.width = r.width
        #     self.height = r.height
        #     self.bounds = self.game.Rect(self.x, self.y, self.width, self.height)
        #     self.update_row_sizes()
        #     th = r.height
        #     nr = len(self.table_rows)
        #     rh = round((th / nr) + self.div_w)
        #     y = 0
        #     for row in self.table_rows:
        #         row_r = self.game.Rect(self.x, y, self.width, rh)
        #         row.resize(row_r)
        #         y += rh
        super().resize(r)
        for row in self.table_rows:
            row.resize(r)
        self.update_row_sizes()

    # Append a TableRow object to the end of the list, or insert it at given index.
    def add_row(self, table_row, index=None):
        if not isinstance(table_row, TableRow):
            tr = TableRow(self.game, self.display)
            tr.add_content(list(map(str, table_row)))
            tr.set_divider_color(self.div_c)
            table_row = tr
        if index:
            self.table_rows.insert(index, table_row)
        else:
            self.table_rows.append(table_row)
        self.update_row_sizes()

    # When the table is re-sized or a row is added, need to update the sizes of all rows.
    def update_row_sizes(self):
        rows = len(self.table_rows)
        title_height = self.rect.height * 0.1
        space_left = self.rect.height - title_height
        row_height = space_left / max(1, rows)
        for i, row in enumerate(self.table_rows):
            x = self.rect.x
            y = self.rect.top + title_height + (row_height * i) + round((row.div_w * i) / 2)
            w = self.rect.width
            h = row_height
            new_bounds = self.game.Rect(x, y, w, h)
            row.update_bounds(*new_bounds)

    # Add a single TableRow, a list of TableRows, a dict of data, or a list of contents to make TableRows.
    # Using a dict, each key becomes a column, and their values become rows
    def add_rows(self, *table_rows):
        for row in table_rows:
            if isinstance(row, list):
                for el in row:
                    self.add_row(el)
            elif isinstance(row, dict):
                self.set_header(list(row.keys()))
                m = max([len(v) for v in row.values()])
                for i in range(m):
                    data = []
                    for k in row:
                        if len(row[k]) > i:
                            data.append(row[k][i])
                        else:
                            data.append("")
                    self.add_row(data)
            else:
                self.add_row(row)

    def clear_rows(self):
        self.table_rows = []
        self.update_row_sizes()

    def draw(self):
        # draw background
        self.game.draw.rect(self.display, self.c, self.rect)
        # draw border lines
        self.game.draw.line(self.display, self.div_c, self.rect.topleft, self.rect.topright, self.div_w)
        self.game.draw.line(self.display, self.div_c, self.rect.topleft, self.rect.bottomleft, self.div_w)
        self.game.draw.line(self.display, self.div_c, self.rect.topright, self.rect.bottomright, self.div_w)
        self.game.draw.line(self.display, self.div_c, self.rect.bottomleft, self.rect.bottomright, self.div_w)

        # draw title
        title_surface, title_rect = text_objects(self.title, self.font, self.title_color)
        title_rect.center = ((self.rect.x + (self.rect.width / 2)), (self.rect.y + (self.rect.height * 0.05)))
        self.display.blit(title_surface, title_rect)

        # draw each row
        for i, row in enumerate(self.table_rows):
            row.draw()
            bounds = row.bounds
            # draw top border
            if i == 0:
                self.game.draw.line(self.display, row.div_c, bounds.topleft, bounds.topright, row.div_w)
            # draw bottom border
            self.game.draw.line(self.display, row.div_c, bounds.bottomleft, bounds.bottomright, row.div_w)


class Box(Widget):

    def __init__(self, game, display, contents, r, p, bgc, is_horizontal=True):
        super().__init__(game, display, r)
        self.contents = [] if contents is None else contents
        self.proportion = p
        self.bgc = bgc
        self.is_horizontal = is_horizontal

    def add_contents(self, *contents):
        for content in contents:
            self.contents.append(content)

    def move(self, r):
        super().move(r)

    def resize(self, r):
        super().resize(r)

    def draw(self):
        nw = len(self.contents)  # number widgets
        wp = (self.rect.width * self.proportion)  # width proportional
        hp = (self.rect.height * self.proportion)  # height proportional
        xd = self.rect.width - wp  # difference between total width and proportional width
        yd = self.rect.height - hp  # difference between total height and proportional height
        xi = self.rect.x + (xd / 2)  # starting x
        yi = self.rect.y + (yd / 2)  # starting y
        wi = wp / max(1, nw) if self.is_horizontal else wp  # single widget width
        hi = hp / max(1, nw) if not self.is_horizontal else hp  # single widget height

        # draw background
        if self.bgc is not None:
            self.game.draw.rect(self.display, self.bgc, self.rect)

        # update bounds and draw widgets
        for i, widget in enumerate(self.contents):
            new_bounds = self.game.Rect(xi, yi, wi, hi)
            widget.move(new_bounds)
            if isinstance(widget, RadioGroup):
                widget.resize(new_bounds, self.is_horizontal)
            else:
                widget.resize(new_bounds)
            widget.draw()
            # button = Button(self.game, self.display, b, xi, yi, wi, hi, *info[:2], self.font, *info[2:])
            # button.draw()
            if self.is_horizontal:
                xi += (xd / (nw + 1)) + wi
            else:
                yi += (yd / (nw + 1)) + hi


class VBox(Box):

    # Create a vertical content box, which contains widgets.
    # All widget contents are sized to fit inside box bounds.
    def __init__(self, game, display, contents, r, p, bgc):
        super().__init__(game, display, contents, r, p, bgc, is_horizontal=False)


class HBox(Box):

    # Create a horizontal content box, which contains widgets.
    # All widget contents are sized to fit inside box bounds.
    def __init__(self, game, display, contents, r, p, bgc):
        super().__init__(game, display, contents, r, p, bgc, is_horizontal=True)


class Slider(Widget):

    def __init__(self, game, display, rect, min_val=0, max_val=1, n_ticks=10, slider_colour=BLACK,
                 slider_border_colour=BLACK, slider_radius=5, line_colour=BLACK, tick_colour=BLACK, stick_to_ticks=True,
                 start_val=None, labels=None, background_colour=GRAY_69, background_is_transparent=False,
                 slider_width=1, font=None, locked=False, lbl_format=lambda x: int(x)):
        super().__init__(game, display, rect)
        self.min_val = min_val
        self.max_val = max_val
        self.n_ticks = max(2, n_ticks)
        self.slider_colour = slider_colour
        self.slider_border_colour = slider_border_colour
        self.slider_radius = slider_radius
        self.line_colour = line_colour
        self.tick_colour = tick_colour
        self.stick_to_ticks = stick_to_ticks
        self.slider_val = start_val if start_val is not None else min_val
        self.labels = labels if labels is not None else []
        if not isinstance(self.labels, list) and not isinstance(self.labels, tuple):
            self.labels = [self.labels]
        self.background_colour = background_colour
        self.background_is_transparent = background_is_transparent
        self.slider_width = slider_width
        self.font = font if font is not None else game.font.Font(None, 16)
        self.slider_radius = slider_radius
        self.locked = locked
        self.lbl_format = lbl_format
        self.dragging = False
        self.tick_labels = []

    def get_val(self):
        return self.slider_val

    def get_slider_rect(self):
        return self.rect_obj.scaled(0.95, 0.5).translated(self.rect.width * 0.025, self.rect.height * 0.25)

    def gen_tick_labels(self, lst_in=None, reduce_lst=False, p=0.5, how="distributed"):
        if p == 0:
            return []
        diff = self.max_val - self.min_val
        step = diff // self.n_ticks - 1
        if lst_in is not None:
            lst = lst_in
        else:
            # lst = list(range(self.min_val, self.max_val, step))
            # lst = [round((((i + 1) / self.n_ticks) * diff) + self.min_val, 2) for i in range(self.min_val, self.max_val, step)]
            # lst = [round((i * step) + self.min_val, 2) for i in range(self.min_val, self.max_val, step)]
            lst = [round((i * step) + self.min_val, 2) for i in range(self.n_ticks)]
        if reduce_lst:
            lst = reduce(lst, p, how)
        if not lst:
            return []
        last = self.max_val - lst[-1]
        lst[-1] += last
        return lst

    def handle_event(self, event):
        if not self.locked:
            if event.type == self.game.MOUSEBUTTONDOWN:
                # val = self.slider_val
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    slider_rect = self.get_slider_rect()
                    x, y = event.pos
                    if slider_rect.collide_point(x, y):
                        # val = ((x / (self.max_val - self.min_val)) * slider_rect.width) + slider_rect.x
                        x -= (slider_rect.x - self.rect.x)
                        val = ((x / slider_rect.width) * (self.max_val - self.min_val)) + self.min_val - 1
                        print("a:", val)
                    else:
                        if self.rect.x <= x <= slider_rect.x:
                            val = 0
                            print("b:", val)
                        else:
                            val = self.max_val
                            print("c:", val)
                    if self.stick_to_ticks:
                        space = slider_rect.width / self.n_ticks
                        ticks = self.tick_labels
                        best_val = None, None
                        t = self.min_val
                        for t in ticks:
                            if best_val[0] is None or abs(val - t) < best_val[1]:
                                best_val = t, abs(val - t)
                            # print("val:", val, "t", t, "best_val:", best_val, "abs(val - t):", abs(val - t), "abs(best_val - t):", abs(best_val[1] - t))
                        val = best_val[0]
                    self.slider_val = clamp(self.min_val, val, self.max_val)
                    print("new val:", self.slider_val, "v", val)
                # Change the current color of the input box.
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    # val = self.slider_val
                    # If the user clicked on the input_box rect.
                    if self.rect.collidepoint(event.pos):
                        slider_rect = self.get_slider_rect()
                        x, y = event.pos
                        x -= (slider_rect.x - self.rect.x)
                        # if slider_rect.collide_point(x, y):
                        #     val = ((x / slider_rect.width) * (self.max_val - self.min_val)) + self.min_val - 1
                        # else:
                        val = ((x / slider_rect.width) * (self.max_val - self.min_val)) + self.min_val - 1
                        if self.stick_to_ticks:
                            ticks = [i for i in range(self.min_val, self.max_val + 1)]
                            best_val = None, None
                            t = self.min_val
                            for t in ticks:
                                if best_val[0] is None or abs(val - t) < best_val[1]:
                                    best_val = t, abs(val - t)
                                # print("val:", val, "t", t, "best_val:", best_val, "abs(val - t):", abs(val - t), "abs(best_val - t):", abs(best_val[1] - t))
                            val = best_val[0]
                        self.slider_val = clamp(self.min_val, val, self.max_val)
                        # print("new val:", self.slider_val, "v", val)
                    # Change the current color of the input box.
            elif event.type == self.game.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

    def draw(self):
        game = self.game
        display = self.display
        rect = self.rect
        if not self.background_is_transparent:
            game.draw.rect(display, self.background_colour, rect)
        slider_rect = self.get_slider_rect()
        line = Line(*slider_rect.center_left, *slider_rect.center_right)
        minor_tick_width = max(1, self.slider_width - 1)
        major_tick_width = max(1, self.slider_width)
        game.draw.line(display, self.slider_colour, *line, self.slider_width)
        diff = self.max_val - self.min_val
        og_lbls = self.gen_tick_labels()
        # og_lbls = [round((((i + 1) / self.n_ticks) * diff) + self.min_val, 2) for i in range(self.n_ticks - 1)]

        total_lbl_width = sum([self.font.size(str(lbl))[0] for lbl in og_lbls])
        # print("BEGIN TTL:", total_lbl_width)
        p = 1
        tick_labels = self.gen_tick_labels(og_lbls, True, p, how="distributed")
        while total_lbl_width > slider_rect.width:
            # print("P:", p, "w:", total_lbl_width)
            p -= 0.01
            tick_labels = self.gen_tick_labels(og_lbls, True, p, how="distributed")
            total_lbl_width = sum([self.font.size(str(lbl))[0] for lbl in tick_labels])

        self.tick_labels = tick_labels
        n_ticks = len(tick_labels) - 1
        space = slider_rect.width / n_ticks
        xc = slider_rect.x + space
        # print("og_lbls:", og_lbls, "\ntick_lbls:", tick_labels)
        for i, t in enumerate(range(n_ticks)):
            game.draw.line(display, self.slider_colour, (xc, line.y1 - 5), (xc, line.y1 + 5), minor_tick_width)
            # lbl = round((((i + 1) / self.n_ticks) * diff) + self.min_val, 2)
            lbl = og_lbls[i]
            if i < len(self.labels):
                lbl = self.labels[i]
            if self.lbl_format is not None:
                lbl = self.lbl_format(lbl)
            lbl = str(lbl)
            if self.background_is_transparent:
                write_text(game, display, Rect2(xc - 12, line.y1 - 30, 24, 24), lbl, self.font, self.background_colour,
                           self.tick_colour, False)
            else:
                write_text(game, display, Rect2(xc - 12, line.y1 - 30, 24, 24), lbl, self.font, None,
                           self.tick_colour, False)
            xc += space
        game.draw.line(display, self.slider_colour, (line.x1, line.y1 - 5), (line.x1, line.y1 + 5), major_tick_width)
        game.draw.line(display, self.slider_colour, (line.x2, line.y1 - 5), (line.x2, line.y1 + 5), major_tick_width)
        min_val = str(self.min_val)
        max_val = str(self.max_val)
        if self.lbl_format is not None:
            min_val = str(self.lbl_format(self.min_val))
            max_val = str(self.lbl_format(self.max_val))
        if self.background_is_transparent:
            write_text(game, display, Rect2(slider_rect.x - 12, line.y1 - 30, 24, 24), min_val, self.font,
                       self.background_colour, self.tick_colour, True)
            write_text(game, display, Rect2(slider_rect.right - 12, line.y1 - 30, 24, 24), max_val, self.font,
                       self.background_colour,
                       self.tick_colour, True)
        else:
            write_text(game, display, Rect2(slider_rect.x - 12, line.y1 - 30, 24, 24), min_val, self.font, None,
                       self.tick_colour, True)
            write_text(game, display, Rect2(slider_rect.right - 12, line.y1 - 30, 24, 24), max_val, self.font, None,
                       self.tick_colour, True)

        slider_x = (((self.slider_val - 1) / diff) * slider_rect.width) + slider_rect.x
        game.draw.circle(display, self.slider_border_colour, (slider_x, line.y1), self.slider_radius + 2)
        game.draw.circle(display, self.slider_colour, (slider_x, line.y1), self.slider_radius)


class MenuBar(Widget):

    # button_data must be tree structure of dict objects.
    # Leaves denoted by a function signature and args.
    # ex:
    #   {"file": {"open": open_file, "branch": {"leaf1": leaf1_func, "leaf2": leaf2_func}}}
    def __init__(self, game, display, x, y, w, h, button_data, bc, fs, bs, font, tile_height=15):
        super().__init__(game, display, Rect2(x, y, w, h))
        self.background_colour = bc
        self.font_size = fs
        self.border_style = bs
        self.font = font
        self.is_clicked = False

        self.button_data = self.validate_button_data(button_data)
        print(dict_print(self.button_data, "Parsed Button Data"))
        # self.state = list(self.button_data)
        self.state = list()

    def validate_button_data(self, button_data):
        def validate_tree(btn_data):
            print("btn_data:", btn_data)
            if isinstance(btn_data, dict):
                for k, v in btn_data.items():
                    print("k: t=\'{}\' [{}], v: t=\'{}\' [{}]".format(k, type(k), v, type(v)))
                    if isinstance(v, dict):
                        if validate_tree(v):
                            continue
                    elif isfunc(v) or isclassmethod(v):
                        continue
                    print("exit a")
                    return False
                return True
            print("exit b")
            return False
        return button_data if validate_tree(button_data) else {}


    # def draw(self):
    #     game = self.game
    #     display = self.display
    #     rect = self.rect
    #     game.draw.rect(display, self.background_colour, rect)
    #
    #     btns = self.button_data
    #
    #     n_drop_downs = len(btns)
    #     w_drop_down = rect.w / max(1, n_drop_downs)
    #     mouse = self.game.mouse.get_pos()
    #     click = self.game.mouse.get_pressed()
    #
    #     for i, key in enumerate(btns):
    #         dat = btns[key]
    #         write_text(game, display, game.Rect(rect.x + (i * w_drop_down), rect.y, w_drop_down, rect.h), key, game.font.Font(None, 16))
    #
    #     def rec_menu(last_rect, press_key, rem_btn_data, d=0):
    #         print("last_rect: {}\npress_key: {}\nrem_btn_data: {}".format(last_rect, press_key, rem_btn_data))
    #         dat = rem_btn_data[press_key]
    #         sub_data = []
    #         for i, k in enumerate(dat):
    #             print("DRAWING K: {}".format(k))
    #             v = dat[k]
    #             if d == 0:
    #                 new_rect = last_rect
    #             else:
    #                 new_rect = game.Rect(last_rect.x + last_rect.w, last_rect.y + (i * last_rect.h), last_rect.w,
    #                                  last_rect.h)
    #             game.draw.rect(display, self.background_colour, new_rect)
    #             write_text(game, display, new_rect, k, game.font.Font(None, 16))
    #             if new_rect.collidepoint(mouse):
    #                 # rec_menu(new_rect, k, v)
    #                 if isinstance(v, dict):
    #                     sub_data.append((new_rect, k, dat, d + 1))
    #                 else:
    #                     # leaf node
    #                     if click[0]:
    #                         print("evoke function: {}".format(v))
    #
    #         for sd in sub_data:
    #             rec_menu(*sd)
    #
    #     # print("click:", click, "mouse:", mouse)
    #     # rect_bg = rect
    #     handle = False
    #     if self.is_clicked or click[0]:
    #         # if rect not in self.state:
    #         #     self.state.append(rect)
    #         if rect.collidepoint(mouse):
    #             # print("mouse[0]: {}\nrect.x: {}\n(mouse[0] - rect.x): {}\nint((mouse[0] - rect.x) // w_drop_down): {}".format(mouse[0], rect.x, (mouse[0] - rect.x), int((mouse[0] - rect.x) // w_drop_down)))
    #             top_btn = int((mouse[0] - rect.x) // w_drop_down)
    #             print("{} clicked {}".format(top_btn, list(btns)[top_btn]))
    #             sub_data = btns[list(btns)[top_btn]]
    #             rect_bg = game.Rect(rect.x + (top_btn * w_drop_down), rect.y + rect.h, rect.w, rect.h * len(sub_data))
    #             game.draw.rect(display, self.background_colour, rect_bg)
    #             if self.is_clicked:
    #                 self.state.clear()
    #             if (rect_bg, list(btns)[top_btn], btns) not in self.state:
    #                 self.state.append((rect_bg, list(btns)[top_btn], btns))
    #             handle = True
    #
    #             rec_menu(rect_bg, list(btns)[top_btn], btns)
    #             # for dat in sub_data:
    #         # else:
    #         #     self.is_clicked = False
    #         if any(list(map(lambda x: x.collidepoint(mouse), [state[0] for state in self.state]))):
    #             print("rect_bg", self.state)
    #             # game.draw.rect(display, self.background_colour, rect_bg)
    #             for tpl in self.state:
    #                 r, k, v = tpl
    #                 game.draw.rect(display, self.background_colour, r)
    #                 rec_menu(*tpl)
    #             handle = True
    #
    #         # t = []
    #         # for r in self.state:
    #         #     if r.collidepoint(mouse):
    #         #         t.append(r)
    #         # self.state = t
    #
    #         if not handle:
    #             self.state.clear()
    #
    #     if not handle:
    #         self.is_clicked = False
    #     if click[0]:
    #         self.is_clicked = not self.is_clicked
    #         game.event.wait()
    #
    #     # rect_dd =

    def draw(self):
        game = self.game
        display = self.display
        rect = self.rect

        game.draw.rect(display, self.background_colour, rect)

        btns = self.button_data

        n_drop_downs = len(btns)
        w_drop_down = rect.w / max(1, n_drop_downs)
        mouse = self.game.mouse.get_pos()
        click = self.game.mouse.get_pressed()

        # instead of drawing the top and the the sides, draw each iteratively using the state path.

        for i, key in enumerate(btns):
            dat = btns[key]
            write_text(game, display, game.Rect(rect.x + (i * w_drop_down), rect.y, w_drop_down, rect.h), key, game.font.Font(None, 16))

        game.draw.line(display, RED, (rect.x, rect.y), (rect.x, rect.y + rect.h), 2)
        game.draw.line(display, RED, (rect.x, rect.y), (rect.x + rect.w, rect.y), 2)
        game.draw.line(display, RED, (rect.x + rect.w, rect.y), (rect.x + rect.w, rect.y + rect.h), 2)
        game.draw.line(display, RED, (rect.x, rect.y + rect.h), (rect.x + rect.w, rect.y + rect.h), 2)

        # print("click:", click, "mouse:", mouse)
        # rect_bg = rect
        handle = False
        if self.is_clicked or click[0]:
            # if rect not in self.state:
            #     self.state.append(rect)
            if rect.collidepoint(mouse):
                # print("mouse[0]: {}\nrect.x: {}\n(mouse[0] - rect.x): {}\nint((mouse[0] - rect.x) // w_drop_down): {}".format(mouse[0], rect.x, (mouse[0] - rect.x), int((mouse[0] - rect.x) // w_drop_down)))
                top_btn = int((mouse[0] - rect.x) // w_drop_down)
                print("{} clicked {}".format(top_btn, list(btns)[top_btn]))
                sub_data = btns[list(btns)[top_btn]]
                l = len(btns[list(btns)[top_btn]])
                l = len(sub_data)
                rect_bg = game.Rect(rect.x + (top_btn * w_drop_down), rect.y + rect.h, rect.w, rect.h * len(sub_data))
                # game.draw.rect(display, darken(self.background_colour, 1), rect_bg)
                if self.is_clicked:
                    self.state.clear()
                start_y = rect.y + rect.h
                if not self.state:
                    for i, k in enumerate(sub_data):
                        rect_btn = game.Rect(rect_bg.x, start_y + (i * rect.h), rect_bg.w, rect.h)
                        tpl = (rect_btn, k, sub_data[k])
                        if tpl not in self.state:
                            self.state.append(tpl)
                handle = True

            new_state = []
            for tpl in self.state:
                r, k, v = tpl
                game.draw.rect(display, self.background_colour, r)
                write_text(game, display, r, k, game.font.Font(None, 16))

                game.draw.line(display, RED, (r.x, r.y), (r.x, r.y + r.h), 2)
                game.draw.line(display, RED, (r.x, r.y), (r.x + r.w, r.y), 2)
                game.draw.line(display, RED, (r.x + r.w, r.y), (r.x + r.w, r.y + r.h), 2)
                game.draw.line(display, RED, (r.x, r.y + r.h), (r.x + r.w, r.y + r.h), 2)

                if r.collidepoint(mouse):
                    if not isfunc(v) and not isclassmethod(v):
                        # print("v:", v)
                        for j, kk in enumerate(v):
                            ntpl = (game.Rect(r.x + r.w, r.y + (j * r.h), r.w, rect.h), kk, v[kk])
                            if ntpl not in self.state:
                                new_state.append(ntpl)
                    else:
                        if click[0]:
                            v()
            self.state += new_state

            if any(list(map(lambda x: x.collidepoint(mouse), [state[0] for state in self.state]))):
                handle = True
            if not handle:
                self.state.clear()

        if not handle:
            self.is_clicked = False
        if click[0]:
            self.is_clicked = not self.is_clicked
            game.event.wait()

        # rect_dd =


# buttons & toggle buttons
# button bar
# scrollable bar TODO: allow a scroll bar on both the vertical and horizontal axes.
# Table rows & cols
# Radio Buttons and groups

# VBox & HBox
# clock
# text area
# text input
# image button
# hyperlink
# combobox
# slider
# menubar


if not is_imported("pygame"):
    import pygame


class PygameApplication:
    TOP_LEFT = 1
    TOP = 2
    TOP_CENTER = 3
    TOP_RIGHT = 4
    CENTER_LEFT = 5
    CENTER = 6
    CENTER_RIGHT = 7
    BOTTOM_LEFT = 8
    BOTTOM_CENTER = 9
    BOTTOM_RIGHT = 10

    def __init__(self, title, w, h, allow_kbd_ctrls=True, auto_init=True):
        global kbd
        self.title = title
        self.w = w
        self.h = h
        self.display = None
        self.is_playing = True
        self.allow_kbd_ctrls = allow_kbd_ctrls
        self.clock = pygame.time.Clock()
        self.background_colour = BLACK
        if allow_kbd_ctrls:
            if not is_imported("keyboard"):
                import keyboard as kbd

        if auto_init:
            self.init()

    def get_display(self):
        return self.display

    def get_game(self):
        return pygame

    def get_dims(self):
        return self.w, self.h

    def set_background_colour(self, bg_colour):
        self.display.fill(bg_colour)

    def colliderect_offset(self, r1, r2, offset=0, l=True, r=True):
        assert isinstance(r1, pygame.Rect)
        assert isinstance(r2, pygame.Rect)
        if l and r:
            return pygame.Rect(r1.left - offset, r1.top - offset, r1.width + (2 * offset),
                               r1.height + (2 * offset)).colliderect(
                pygame.Rect(r2.left - offset, r2.top - offset, r2.width + (2 * offset), r2.height + (2 * offset)))
        elif l:
            return pygame.Rect(r1.left - offset, r1.top - offset, r1.width + (2 * offset),
                               r1.height + (2 * offset)).colliderect(
                pygame.Rect(r2.left, r2.top, r2.width, r2.height))
        else:
            return pygame.Rect(r1.left, r1.top, r1.width,
                               r1.height).colliderect(pygame.Rect(r2.left, r2.top, r2.width, r2.height))

    def add_menubar(self, pos):
        if pos not in [
            self.TOP_LEFT,
            self.TOP,
            self.TOP_CENTER,
            self.TOP_RIGHT,
            self.CENTER_LEFT,
            self.CENTER,
            self.CENTER_RIGHT,
            self.BOTTOM_LEFT,
            self.BOTTOM_CENTER,
            self.BOTTOM_RIGHT
        ]:
            pos = self.TOP_LEFT

    def init(self):
        try:
            import pygame
            pygame.init()
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption(self.title)
        except ImportError:
            print("\nUnable to import pygame.\nPlease try again after installing.\n")

    def tick(self, t):
        self.clock.tick(t)

    def get_game_queue(self):
        return pygame.event.get()

    # Call this function iteratively.
    # Include any application specific UI / other code
    # within the instance of the child application.
    # Example:
    #
    #    def main_loop():
    #        app = PygameApplication("Create Custom WO Update Queries", 750, 500)
    #        game = app.get_game()
    #        display = app.display
    #
    #        while app.is_playing:
    #            display.fill(BLACK)
    #
    #            # draw widgets and objects here
    #
    #            event_queue = app.run()
    #            for event in event_queue:
    #
    #                # handle events
    #
    #                pass
    #
    #            app.clock.tick(30)
    #

    def run(self):
        if self.display is None:
            self.init()
        events = self.get_game_queue()
        kbd_q, kbd_w, kbd_ua, kbd_a, kbd_la, kbd_s, kbd_da, kbd_d, kbd_ra = False, False, False, False, False, False, False, False, False
        if self.allow_kbd_ctrls:
            kbd_w = kbd.is_pressed('w')
            kbd_ua = kbd.is_pressed('up')
            kbd_a = kbd.is_pressed('a')
            kbd_la = kbd.is_pressed('left')
            kbd_s = kbd.is_pressed('s')
            kbd_da = kbd.is_pressed('down')
            kbd_d = kbd.is_pressed('d')
            kbd_ra = kbd.is_pressed('right')
            str_dir_keys = ["kbd_w", "kbd_ua", "kbd_a", "kbd_la", "kbd_s", "kbd_da", "kbd_d", "kbd_ra"]
            dir_keys = [kbd_w, kbd_ua, kbd_a, kbd_la, kbd_s, kbd_da, kbd_d, kbd_ra]
            a_dir_keys = any(dir_keys)
            kbd_q = kbd.is_pressed('q')
        for i, event in enumerate(events):
            pos = pygame.mouse.get_pos()
            if kbd_q or event.type == pygame.QUIT:
                self.is_playing = False
            # if i != len(events) - 1:
            #     pygame.display.flip()
        pygame.display.flip()
        return events
