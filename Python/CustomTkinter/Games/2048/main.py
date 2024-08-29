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
		self.canvas_game_board.itemconfigure(self.tag_rect_summary, state=ctk.HIDDEN)
		self.canvas_game_board.itemconfigure(self.tag_text_summary_0, state=ctk.HIDDEN)
		
		self.lvl = 1
		
		self.y_ground = 400
		self.w_ship, self.h_ship = 60, 40
		self.hh_ship = 8
		self.ms_ship = 6
		self.w_bullet = 4
		self.h_bullet = 8
		self.ms_bullet = 12
		self.ms_anim = 120
		self.ms_loop = 300
		
		self.bbox_ship_og = (
			(self.w_can_gb - self.w_ship) / 2,
			self.y_ground - (self.h_ship + self.hh_ship),
			((self.w_can_gb + self.w_ship) / 2),
			self.y_ground - self.hh_ship
		)
		self.tag_ship = self.canvas_game_board.create_rectangle(
			*self.bbox_ship_og,
			fill=self.colour_ship.hex_code
		)
		
		self.keys_pressed = list()
		self.n_cycles = 0
		
		self.n_new_tiles_per_move = 2
		self.options_new_val = [2, 4]
		self.n_rows, self.n_cols = 10, 10
		self.positions = dict()
		self.empty_positions = list()
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
				
		print(f"{len(self.positions)=}")
		print(f"{len(self.empty_positions)=}")
				
		
		"""
		self.bullets = list()
		self.s_shooting = 3
		
		
		self.enemies = list()
		self.ms_enemy = 5
		self.n_enemy_rows = 8
		self.n_enemy_cols = 12
		self.enemy_data = dict()
		
		self.gc = grid_cells(
			self.w_can_gb,
			self.n_enemy_cols,
			self.h_can_gb,
			self.n_enemy_rows,
			x_pad=10,
			y_pad=10
		)
		print(f"{len(self.gc)=}")
		print(f"{len(self.gc[0])=}")
		"""
		
		self.bind("<KeyPress>", self.key_down)
		self.bind("<KeyRelease>", self.key_up)
		#self.bind("<Left>", self.move_left)
		#self.bind("<Right>", self.move_right)
		#self.bind("<Up>", self.shoot)
		
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
		
	def gen_enemies(self):
		
		self.clear_board()
		self.enemies.clear()
		self.enemy_data.clear()
		
		lvl = self.lvl
		
		# 1 x 8 (R x C) 4 enemies
		#	 * * * *	
		n_rows, n_cols = 1, 8
		w_enemy, h_enemy = 20, 10
		hp_enemy = 4
		to_del = list()
		to_del += [(0, 0), (0, 1), (0, 6), (0, 7)]
		
		if lvl == 2:
			# 1 x 8 (R x C) 8 enemies
			# * * * * * * * *
			to_del.clear()
		elif lvl == 3:
			# 2 rows of enemies, 2 x 8 (R x C) 12 enemies
			# * * * * * * * *
			#	 * * * *
			to_del.clear()
			n_rows = 2
			to_del += [(1, 0), (1, 1), (1, 6), (1, 7)]
		elif 4 <= lvl <= 6:
			# 4 rows of enemies, 4 x 8 (R x C) 32 enemies
			to_del.clear()
			n_rows, n_cols = 4, 8
			w_enemy, h_enemy = 15, 8
			hp_enemy = 5
		else:
			pass
			
		# del self.enemy_data[bullet]
		
		"""
		x0, y0 = 20, 20
		w_btwn_enemy, h_btwn_enemy = 10, 20
		for i in range(n_rows):
			for j in range(n_cols):
				self.enemies.append(
					self.canvas_game_board.create_rectangle(
						x0 + (j * w_enemy) + ((j + 0.5) * w_btwn_enemy),
						y0 + (i * h_enemy) + ((i + 0.5) * h_btwn_enemy),
						x0 + ((j + 1) * (w_enemy + w_btwn_enemy)),
						y0 + ((i + 1) * (h_enemy + h_btwn_enemy)),
						fill="#126633"
					)
					
					#self.canvas_game_board.create_rectangle(
					#	x0 + (j * w_enemy) + (max(0, (j - 1)) * w_btwn_enemy),
					#	y0 + (i * h_enemy) + (max(0, (i - 1)) * h_btwn_enemy),
					#	x0 + ((j + 1) * (w_enemy + w_btwn_enemy)),
					#	y0 + ((i + 1) * (h_enemy + h_btwn_enemy)),
					#	fill="#126633"
					#)
				)
			self.enemy_data[(i * n_cols) + j] = {
				"hp": hp_enemy,
				"row": self.n_enemy_rows - i,
				"col": j
			}
		
		"""
		
		for i, row in enumerate(self.gc):
			for j, bbox in enumerate(row):
				if (i < n_rows) and (j < n_cols):
					self.enemies.append(
						self.canvas_game_board.create_rectangle(
							*bbox,
							fill=self.colour_enemy_hp_full.hex_code
						)
					)
				self.enemy_data[(i * n_cols) + j] = {
					"hp": hp_enemy,
					"row": i,
					"col": j,
					"hit_colours": [
						gradient(
							i,
							hp_enemy,
							self.colour_enemy_hp_full,
							self.colour_enemy_hp_empty,
							rgb=False
						)
						for i in range(hp_enemy + 1)
					]
				}
		
		self.enemy_data["n_cols"] = n_cols
		self.enemy_data["n_rows"] = n_rows
		self.enemy_data["w_enemy"] = w_enemy
		self.enemy_data["h_enemy"] = h_enemy
		self.enemy_data["max_hp_enemy"] = hp_enemy
		
		#print(f"{lvl=}")
		#print(f"{n_rows=}")
		#print(f"{n_cols=}")
		#print(f"{to_del=}")
		to_rem = list()
		for i, j in to_del:
			enemy = self.enemies[(i * n_cols) + j]
			self.canvas_game_board.delete(enemy)
			to_rem.append(enemy)
		for enemy in to_rem:
			self.enemies.remove(enemy)
			
		
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
		#if self.keys_pressed:
		#	print(f"{self.keys_pressed=}")
		#print(f"{key=}")
		if key in self.keys_pressed:
			self.keys_pressed.remove(key)
		
	def key_down(self, event):
		key = event.keysym
		state = event.state
		#print(f"{event=}")
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
		#if self.keys_pressed:
		#	print(f"{self.keys_pressed=}")
		keep_going = True
		if self.game_state == STATE.PLAY:
			for key in self.keys_pressed:
				if key == "Left":
					self.move_left(None)
					self.gen_new_positions()
				elif key == "Right":
					self.move_right(None)
					self.gen_new_positions()
				elif key == "Up":
					self.move_up(None)
					self.gen_new_positions()
				elif key == "Down":
					self.move_down(None)
					self.gen_new_positions()
				elif key == "p":
					self.click_pause()
				else:
					pass
				
			#has_enemies = any(self.enemies)
			#
			#if not has_enemies:
			#	# no more enemies left, end game
			#	self.end_game(1)
			#	
			# print(f"{self.enemies=}, {has_enemies=}")
			#if has_enemies and ((self.n_cycles % self.ms_enemy) == 0):
			#	
			#	keep_going = None
			#	min_row, max_row, min_col, max_col = None, None, None, None
			#	n_rows, n_cols = self.enemy_data["n_rows"], self.enemy_data["n_cols"]
			#	for i, enemy in enumerate(self.enemies):
			#		if enemy is None:
			#			continue
			#		r, c = divmod(i, n_cols)
			#		enemy_data = self.enemy_data[(r * n_cols) + c]
			#		e_r, e_c = enemy_data["row"], enemy_data["col"]
			#		
			#		if min_row is None:
			#			min_row = e_r
			#		else:
			#			if e_r < min_row:
			#				min_row = e_r
			#		if max_row is None:
			#			max_row = e_r
			#		else:
			#			if e_r > max_row:
			#				max_row = e_r
			#		if min_col is None:
			#			min_col = e_c
			#		else:
			#			if e_c < min_col:
			#				min_col = e_c
			#		if max_col is None:
			#		   max_col = e_c
			#		else:
			#			if e_c > max_col:
			#				max_col = e_c
			#		
			#	direction_x = self.enemy_data.get("direction_x", 1)  # default move right
			#	direction_y = self.enemy_data.get("direction_y", 0)  # default same row
			#	
			#	if (direction_y == 1) and ((min_col != 0) or (max_col != (self.n_enemy_cols - 1))):
			#		# not at an end, can't move down
			#		direction_x = 1
			#		direction_y = 0
			#		
			#	if max_col == (self.n_enemy_cols - 1):
			#		# go left
			#	   # print(f"GO Left!")
			#		direction_x = -1
			#	elif (min_col == 0) and (self.enemy_data.get("direction_x", 1) == -1):
			#		# move down
			#		# print(f"GO Down!")
			#		direction_x = 0
			#		direction_y = 1
			#	
			#	self.enemy_data["direction_x"] = direction_x
			#	self.enemy_data["direction_y"] = direction_y
			#	
			#	bbox_s = self.canvas_game_board.bbox(self.tag_ship)
			#	d = 0
			#	for i, enemy in enumerate(self.enemies[::-1]):
			#		if enemy is None:
			#			continue
			#		i = len(self.enemies) - (i + 1)
			#		r, c = divmod(i, n_cols)
			#		enemy_data = self.enemy_data[(r * n_cols) + c]
			#		e_r, e_c = enemy_data["row"], enemy_data["col"]
			#		n_r, n_c = e_r + direction_y, e_c + direction_x
			#		self.enemy_data[(r * n_cols) + c].update({
			#			"row": n_r,
			#			"col": n_c
			#		})
			#		# print(f"{i=}, {e_r=}, {e_c=}, {direction_x=}, {direction_y=}, {min_row=}, {max_row=}, {min_col=}, {max_col=}, ner={self.n_enemy_rows}, nec={self.n_enemy_cols}")
			#		bbox = None
			#		if n_r >= self.n_enemy_rows:
			#			# out of range veritcally, end game
			#			self.end_game(-2)
			#			keep_going = False
			#		else:
			#			bbox = self.gc[n_r][n_c]
			#			if bbox[3] >= bbox_s[1]:
			#				# enemy hit ship, end game
			#				d = bbox[3] - bbox_s[1]
			#				self.end_game(-1)
			#				keep_going = False
			#		
			#		if bbox:
			#			bbox = [
			#				bbox[0],
			#				bbox[1] - d,
			#				bbox[2],
			#				bbox[3] - d
			#			]
			#				
			#		if keep_going is not False:					
			#			self.canvas_game_board.coords(
			#				enemy,
			#				*bbox
			#			)
			#			keep_going = True
			#		elif bbox:
			#			self.canvas_game_board.coords(
			#				enemy,
			#				*bbox
			#			)
			
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
		#print(f"{self.n_cycles=}, {keep_going=}")
			
		if keep_going:
			self.n_cycles += 1
			self.af_id_loop = self.after(self.ms_loop, self.loop)
			
		
	def animate(self, *args):
		pass
		#if self.game_state == STATE.PLAY:
		#	to_rem = list()
		#	n_rows, n_cols = self.enemy_data["n_rows"], self.enemy_data["n_cols"]
		#	max_hp = self.enemy_data["max_hp_enemy"]
		#	for bullet in self.bullets:
		#		bbox_b = self.canvas_game_board.bbox(bullet)
		#		bd = float(self.canvas_game_board.itemcget(bullet, "width"))
		#		bbox_b = [
		#			bbox_b[0] + bd,
		#			bbox_b[1] + bd,
		#			bbox_b[2] - bd,
		#			bbox_b[3] - bd
		#		]
		#		w = bbox_b[2] - bbox_b[0]
		#		h = bbox_b[3] - bbox_b[1]
		#		cx = bbox_b[0] + (w / 2)
		#		cy = (bbox_b[1] + (h / 2)) - self.ms_bullet
		#		new_bbox = [
		#			cx,
		#			cy - (self.h_bullet / 2),
		#			cx,
		#			cy + (self.h_bullet / 2),
		#		]
		#		#print(f"{new_bbox=}, {cx=}, {cy=}, {w=}, {h=}, {bd=}")
		#		if new_bbox[3] < 0:
		#			to_rem.append(bullet)
		#		self.canvas_game_board.coords(bullet, *new_bbox)
		#		
		#	for i, enemy in enumerate(self.enemies[::-1]):
		#		if enemy is None:
		#			continue
		#		i = len(self.enemies) - (i + 1)
		#		r, c = divmod(i, n_cols)
		#		idx = (r * n_cols) + c
		#		enemy_data = self.enemy_data[idx]
		#		e_r, e_c = enemy_data["row"], enemy_data["col"]
		#		bbox_e = self.canvas_game_board.bbox(enemy)
		#		for j, bullet in enumerate(self.bullets):
		#			bbox_b = self.canvas_game_board.bbox(bullet)
		#			if ((bbox_e[0] <= bbox_b[0] <= bbox_e[2]) or (bbox_e[0] <= bbox_b[2] <= bbox_e[2])) and ((bbox_e[1] <= bbox_b[1] <= bbox_e[3]) or (bbox_e[1] <= bbox_b[3] <= bbox_e[3])):
		#				# hit enemy with bullet
		#				self.enemy_data[idx]["hp"] -= 1
		#				print(f"{i}: hp: {self.enemy_data[idx]['hp']}")
		#				self.canvas_game_board.itemconfigure(
		#					enemy,
		#					fill=enemy_data["hit_colours"][max_hp - self.enemy_data[idx]["hp"]]
		#				)
		#				
		#				if self.enemy_data[idx]["hp"] <= 0:
		#					# enemy is dead:
		#					print(f"Enemy {i} is dead")
		#					self.canvas_game_board.delete(enemy)
		#					self.enemies[i] = None
		#				#else:
		#				#	print(f"")
		#				if bullet not in to_rem:
		#					to_rem.append(bullet)
		#			
		#			if self.enemy_data[idx]['hp'] <= 0:
		#				break
		#		
		#		
		#	for bullet in to_rem:
		#		self.bullets.remove(bullet)
		#		self.canvas_game_board.delete(bullet)
		#self.af_id_animate = self.after(self.ms_anim, self.animate)
		
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
		#self.n_cycles = 0
		#self.gen_enemies()
		
		self.gen_new_positions()
		
		self.game_state = STATE.PLAY
		self.af_id_animate = self.after(self.ms_anim, self.animate)
		self.af_id_loop = self.after(self.ms_loop, self.loop)
		
	def clear_board(self):
		pass
		#for tag in self.enemies + self.bullets:
		#	self.canvas_game_board.delete(tag)
		#self.enemies.clear()
		#self.bullets.clear()
		
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
		
		#if self.af_id_loop is not None:
		#	self.after_cancel(self.af_id_loop)
		#	
		#if self.af_id_animate is not None:
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
		for i in range(1, self.n_rows):
			for j in range(self.n_cols):
				
				data = self.positions[i][j]
				# print(f"{data=}")
				val = data["val"]
				if val is None:
					continue
					
				idx = j + (i * self.n_cols)
				tile = data["tile"]
				text = data["text"]
				val_u = self.positions[i - 1][j]["val"]
				
				if val == val_u:
					# combine
					new_val = val * 2
				elif val_u is None:
					# shift
					new_val = val
				else:
					# do not set the top neighbour cell, or clear this cell as they cannot be combined or shifted.
					continue
								
				self.set_cell(i - 1, j, new_val)
				self.clear_cell(i, j)
		
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
	