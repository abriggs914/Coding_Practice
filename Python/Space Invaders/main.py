from customtkinter_utility import *


class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.w_can_gb, self.h_can_gb = 400, 400
        
        self.canvas_game_board = ctk.CTkCanvas(
            self,
			width=self.w_can_gb,
			height=self.h_can_gb
        )
        
        self.lvl = 1
		
        self.y_ground = 400
        self.w_ship, self.h_ship = 60, 40
        self.hh_ship = 8
        self.ms_ship = 6
        self.w_bullet = 4
        self.h_bullet = 8
        self.ms_bullet = 12
        self.ms_anim = 120
        self.ms_loop = 60
        
        self.tag_ship = self.canvas_game_board.create_rectangle(
            ((self.w_can_gb - self.w_ship) / 2),
            self.y_ground - (self.h_ship + self.hh_ship),
			((self.w_can_gb + self.w_ship) / 2),
			self.y_ground - self.hh_ship
        )
        
        self.keys_pressed = list()
        self.bullets = list()
        
        self.enemies = list()
        
        self.bind("<KeyPress>", self.key_down)
        self.bind("<KeyRelease>", self.key_up)
        #self.bind("<Left>", self.move_left)
        #self.bind("<Right>", self.move_right)
        #self.bind("<Up>", self.shoot)
        
        self.gen_enemies(new_game=True)
        
        self.grid_widgets()
        
        self.af_id_animate = self.after(self.ms_anim, self.animate)
        self.af_id_loop = self.after(self.ms_loop, self.loop)
        
    def gen_enemies(self, new_game: bool = True):
        if new_game:
            self.enemies.clear()
        lvl = self.lvl
        
        # 2 x 8 (R x C)
        n_rows, n_cols = 2, 8
        w_enemy, h_enemy = 20, 10
        
        if 4 <= lvl <= 6:
            # 4 rows of enemies, 4 x 8 (R x C)
            n_rows, n_cols = 4, 8
            w_enemy, h_enemy = 15, 8
        else:
            pass
         
        x0, y0 = 20, 20
        w_btwn_enemy, h_btwn_enemy = 10, 20
        for i in range(n_rows):
            for j in range(n_cols):
                self.enemies.append(
                    self.canvas_game_board.create_rectangle(
                        x0 + (j * w_enemy) + (max(0, (j - 1)) * w_btwn_enemy),
                        y0 + (i * h_enemy) + (max(0, (i - 1)) * h_btwn_enemy),
                        x0 + ((j + 1) * (w_enemy + w_btwn_enemy)),
                        y0 + ((i + 1) * (h_enemy + h_btwn_enemy)),
                        fill="#126633"
                    )
                )
            
        
    def grid_widgets(self):
        self.rowconfigure(0, weight=100)
        self.columnconfigure(0, weight=100)
        self.canvas_game_board.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        
    def key_up(self, event):
        key = event.keysym
        #if self.keys_pressed:
        #    print(f"{self.keys_pressed=}")
        #print(f"{key=}")
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        
    def key_down(self, event):
        key = event.keysym
        # print(f"{key=}")
        
        if key in ("Left", "Right", "Up"):
            if key not in self.keys_pressed:
                self.keys_pressed.append(key)
    
    def loop(self, *args):
        #if self.keys_pressed:
        #    print(f"{self.keys_pressed=}")
        for key in self.keys_pressed:
            if key == "Left":
                self.move_left(None)
            elif key == "Right":
                self.move_right(None)
            elif key == "Up":
                self.shoot(None)
            else:
                pass
        self.af_id_loop = self.after(self.ms_loop, self.loop)
            
        
    def animate(self, *args):
        to_rem = list()
        for bullet in self.bullets:
            bbox_b = self.canvas_game_board.bbox(bullet)
            bd = float(self.canvas_game_board.itemcget(bullet, "width"))
            bbox_b = [
                bbox_b[0] + bd,
                bbox_b[1] + bd,
                bbox_b[2] - bd,
                bbox_b[3] - bd
            ]
            w = bbox_b[2] - bbox_b[0]
            h = bbox_b[3] - bbox_b[1]
            cx = bbox_b[0] + (w / 2)
            cy = (bbox_b[1] + (h / 2)) - self.ms_bullet
            new_bbox = [
                cx,
                cy - (self.h_bullet / 2),
                cx,
                cy + (self.h_bullet / 2),
            ]
            #print(f"{new_bbox=}, {cx=}, {cy=}, {w=}, {h=}, {bd=}")
            if new_bbox[3] < 0:
                to_rem.append(bullet)
            self.canvas_game_board.coords(bullet, *new_bbox)
        for bullet in to_rem:
            self.bullets.remove(bullet)
        self.af_id_animate = self.after(self.ms_anim, self.animate)
        
        
    def shoot(self, event):
        bbox = self.canvas_game_board.bbox(self.tag_ship)
        bd = float(self.canvas_game_board.itemcget(self.tag_ship, "width"))
        bbox = [
            bbox[0] + bd,
            bbox[1] + bd,
            bbox[2] - bd,
            bbox[3] - bd
        ]
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        cx = bbox[0] + (w / 2)
        cy = bbox[1] + (h / 2)
        self.bullets.append(
            self.canvas_game_board.create_line(
                cx,
                cy - (self.h_bullet / 2),
                cx,
                cy + (self.h_bullet / 2)
            )
        )
		
    def move_left(self, event):
        #print(f"move_left {event}")
        bbox = self.canvas_game_board.bbox(self.tag_ship)
        bd = float(self.canvas_game_board.itemcget(self.tag_ship, "width"))
        bbox = [
            bbox[0] + bd,
            bbox[1] + bd,
            bbox[2] - bd,
            bbox[3] - bd
        ]
        new_bbox = [
            clamp(0, bbox[0] - self.ms_ship, self.w_can_gb - self.w_ship),
            bbox[1],
            clamp(self.w_ship, bbox[2] - self.ms_ship, self.w_can_gb),
            bbox[3]
        ]
        self.canvas_game_board.coords(self.tag_ship, *new_bbox)
        
		
    def move_right(self, event):
        #print(f"move_right {event}")
        bbox = self.canvas_game_board.bbox(self.tag_ship)
        bd = float(self.canvas_game_board.itemcget(self.tag_ship, "width"))
        bbox = [
            bbox[0] + bd,
            bbox[1] + bd,
            bbox[2] - bd,
            bbox[3] - bd
        ]
        new_bbox = [
            clamp(0, bbox[0] + self.ms_ship, self.w_can_gb - self.w_ship),
            bbox[1],
            clamp(self.w_ship, bbox[2] + self.ms_ship, self.w_can_gb),
            bbox[3]
        ]
        self.canvas_game_board.coords(self.tag_ship, *new_bbox)
	


if __name__ == "__main__":
	
	app = App()
	app.mainloop()
	