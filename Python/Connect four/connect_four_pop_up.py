# game initializer pop-up for connect 4 game
# June 2020

from time import sleep
from tkinter import *
from connect_four import player_color_options, validate_int, CONNECT_X, MAX_CONNECT

#################################################
##		 		 Design vars		           ##
#################################################
HEIGHT_SPACE = 25
WIDTH_SPACE = 300
WIDTH = 700
HEIGHT = 650

valid_text_color = "#26b52b"

error_text_color = "#fa0c0c"
error_message = "Please enter a value."

SU_welcome_message = "Welcome to connect 4!"
SU_welcome_text_color = "#0e822d" # dark green
SU_welcome_font = "none 20 bold"

SU_player_name_message = "Please enter your name:"
SU_player_name_text_color = "#ffea05" # golden yellow
SU_player_name_font = "none 12 bold"

SU_player_color_selection_message = "Which color would you like to play as?"
SU_player_color_text_color = "#121fdb" # blue
SU_player_color_font = "none 12 bold"

SU_n_rows_message = "How many rows would you like?"
SU_n_rows_text_color = "#12dbd4" # cyan
SU_n_rows_font = "none 12 bold"

SU_n_cols_message = "How many columns would you like?"
SU_n_cols_text_color = "#db1212" # red
SU_n_cols_font = "none 12 bold"

SU_connect_x_message = "Traditionally the game is the first to connect 4,\nhowever you may choose to connect as many as you wish:"
SU_connect_x_text_color = "#b612db" # purple
SU_connect_x_font = "none 12 bold"

SU_first_player_message_1 = "Who will go first?"
SU_first_player_message_2 = "You will go first"
SU_first_player_message_3 = "You will go second"
SU_first_player_message_4 = "Randomly decided"
SU_first_player_text_color_1 = "#00bf03" # green
SU_first_player_text_color_2 = "#ffa600" # orange
SU_first_player_text_color_3 = "#3c3cb0" # blue
SU_first_player_text_color_4 = "#bf0000" # red
SU_first_player_font = "none 12 bold"

submit_button_text = "submit"
submit_button_text_color = "black"
submit_button_color = "#939694"
submit_button_font = "none 12 bold"

radiobutton_font = "none 12 bold"

#################################################
## 				Input vars					   ##
#################################################
window = None
name_entry = None
name_entry_var = None
color_entry = None
color_entry_var = None
rows_entry = None
rows_entry_var = None
cols_entry = None
cols_entry_var = None
x_entry = None
x_entry_var = None
first_player_entry = None
first_player_entry_var = None

color_option_1 = 1
color_option_2 = 2

first_player_option_1 = 1
first_player_option_2 = 2
first_player_option_3 = 3

game_info = {}
#################################################

def gather_info():
	main()
	return game_info

def get_error_message():
	return str(error_message)

def submit_button_clicked():
	global game_info
	name = name_entry_var.get()
	color = color_entry_var.get()
	rows = rows_entry_var.get()
	cols = cols_entry_var.get()
	connect_x = x_entry_var.get()
	first_player = first_player_entry_var.get()
	
	valid = True
	
	# expects at minimum a single character
	if not name:
		name_entry.config(fg=error_text_color)
		name_entry_var.set(error_message)
		valid = False
	else:
		name = name.title()
		name_entry.config(fg=valid_text_color)
		name_entry_var.set(name)
		
	# needs to be 1 or 2
	if color == 0:
		valid = False
		
	# needs to be an int value and within range
	if not rows or not rows.isdigit():
		rows_entry.config(fg=error_text_color)
		rows_entry_var.set(error_message)
		valid = False
	else:
		rows = validate_int(rows, CONNECT_X, range(CONNECT_X, MAX_CONNECT))
		rows_entry.config(fg=valid_text_color)
		rows_entry_var.set(rows)
		
	# needs to be an int value and within range
	if not cols or not cols.isdigit():
		cols_entry.config(fg=error_text_color)
		cols_entry_var.set(error_message)
		valid = False
	else:
		cols = validate_int(cols, CONNECT_X, range(CONNECT_X, MAX_CONNECT))
		cols_entry.config(fg=valid_text_color)
		cols_entry_var.set(cols)
		
	# needs to be an int value and within range
	if not connect_x or not connect_x.isdigit():
		x_entry.config(fg=error_text_color)
		x_entry_var.set(error_message)
		valid = False
	elif str(rows).isdigit() and str(cols).isdigit():
		connect_max = min(int(rows), int(cols))
		connect_x = validate_int(connect_x, CONNECT_X, range(2, connect_max + 1))
		x_entry.config(fg=valid_text_color)
		x_entry_var.set(connect_x)
		
	if first_player == 0:
		valid = False
	else:
		player_options = ["player", "bot", "random"]
		idx = first_player - 1
		first_player = player_options[idx]
		
	## logic checks
	if connect_x > min(rows, cols):
		valid = False
		
	if valid:
		print("Valid")
		game_info["name"] = name
		game_info["color"] = player_color_options[color - 1]
		game_info["rows"] = rows
		game_info["cols"] = cols
		game_info["connect_x"] = connect_x
		game_info["first_player"] = first_player
		print("name", name, "color", color, "rows", rows, "cols", cols, "connect_x", connect_x, "first_player", first_player)
		sleep(1)
		window.destroy()
	else:
		print("Not valid")

def get_dimensions():
	dimens = "%dx%d+%d+%d" % (WIDTH, HEIGHT, WIDTH_SPACE, HEIGHT_SPACE)
	return dimens

def init_window():
	global window
	# create window
	window = Tk()
	# set title & background color
	window.title("Connect 4")
	window.configure(background="black")
	# set window size & position
	window.geometry(get_dimensions())
	# center all widgets and labels by asserting that column 0 consumes entire space
	window.columnconfigure(0, weight=1)
	return window
	
def game_set_up():
	global name_entry, color_entry, rows_entry, cols_entry, x_entry, name_entry_var, color_entry_var, rows_entry_var, cols_entry_var, x_entry_var, first_player_entry_var
	name_entry_var = StringVar()
	color_entry_var = IntVar()
	rows_entry_var = StringVar()
	cols_entry_var = StringVar()
	x_entry_var = StringVar()
	first_player_entry_var = IntVar()
	
	print("name_entry_var", name_entry_var, "color_entry_var", color_entry_var, "rows_entry_var", rows_entry_var, "cols_entry_var", cols_entry_var, "x_entry_var", x_entry_var)
	
	# Welcome message
	Label(
		window,
		text=SU_welcome_message,
		bg="black",
		fg=SU_welcome_text_color,
		font=SU_welcome_font,
		pady=10
	).grid(row=1, column=0, sticky=N)
	
	# Player name message
	Label(
		window,
		text=SU_player_name_message,
		bg="black",
		fg=SU_player_name_text_color,
		font=SU_player_name_font,
		pady=10
	).grid(row=4, column=0, sticky=N)
	
	name_entry = Entry(
		window,
		width=50,
		bg="white",
		fg="black",
		font=SU_player_name_font,
		textvariable=name_entry_var
	)
	name_entry.grid(row=5, column=0, sticky=N)
	
	# Color selection message
	Label(
		window,
		text=SU_player_color_selection_message,
		bg="black",
		fg=SU_player_color_text_color,
		font=SU_player_color_font,
		pady=10
	).grid(row=6, column=0, sticky=N)
	
	Radiobutton(
		window,
		text=player_color_options[0], # Red
		bg="black",
		fg=player_color_options[0].lower(),
		variable=color_entry_var,
		value=color_option_1,
		font=radiobutton_font,
		indicatoron = 0
	).grid(row=7, column=0, sticky=N)
	
	Radiobutton(
		window,
		text=player_color_options[1], # Yellow
		bg="black",
		fg=player_color_options[1].lower(),
		variable=color_entry_var,
		value=color_option_2,
		font=radiobutton_font,
		indicatoron = 0
	).grid(row=8, column=0, sticky=N)
	
	# N rows selection
	Label(
		window,
		text=SU_n_rows_message,
		bg="black",
		fg=SU_n_rows_text_color,
		font=SU_n_rows_font,
		pady=10
	).grid(row=9, column=0, sticky=N)
	
	rows_entry = Entry(
		window,
		width=50,
		bg="white",
		fg="black",
		font=SU_n_rows_font,
		textvariable=rows_entry_var
	)
	rows_entry.grid(row=10, column=0, sticky=N)
	
	# N cols selection
	Label(
		window,
		text=SU_n_cols_message,
		bg="black",
		fg=SU_n_cols_text_color,
		font=SU_n_cols_font,
		pady=10
	).grid(row=11, column=0, sticky=N)
	
	cols_entry = Entry(
		window,
		width=50,
		bg="white",
		fg="black",
		font=SU_n_cols_font,
		textvariable=cols_entry_var
	)
	cols_entry.grid(row=12, column=0, sticky=N)
	
	# Connect x message
	Label(
		window,
		text=SU_connect_x_message,
		bg="black",
		fg=SU_connect_x_text_color,
		font=SU_connect_x_font,
		pady=10
	).grid(row=13, column=0, sticky=N)
	
	x_entry = Entry(
		window,
		width=50,
		bg="white",
		fg="black",
		font=SU_connect_x_font,
		textvariable=x_entry_var
	)
	x_entry.grid(row=14, column=0, sticky=N)
	
	# First player message
	Label(
		window,
		text=SU_first_player_message_1,
		bg="black",
		fg=SU_first_player_text_color_1,
		font=SU_first_player_font,
		pady=10
	).grid(row=15, column=0, sticky=N)
	
	Radiobutton(
		window,
		text=SU_first_player_message_2,
		bg="black",
		fg=SU_first_player_text_color_2,
		font=SU_first_player_font,
		variable=first_player_entry_var,
		value=first_player_option_1,
		indicatoron = 0
	).grid(row=16, column=0, sticky=N)
	
	Radiobutton(
		window,
		text=SU_first_player_message_3,
		bg="black",
		fg=SU_first_player_text_color_3,
		font=SU_first_player_font,
		variable=first_player_entry_var,
		value=first_player_option_2,
		indicatoron = 0
	).grid(row=17, column=0, sticky=N)
	
	Radiobutton(
		window,
		text=SU_first_player_message_4,
		bg="black",
		fg=SU_first_player_text_color_4,
		font=SU_first_player_font,
		variable=first_player_entry_var,
		value=first_player_option_3,
		indicatoron = 0
	).grid(row=18, column=0, sticky=N)
	
	submit_button = Button(
		window,
		text=submit_button_text,
		command=submit_button_clicked,
		width=10,
		bg=submit_button_color,
		fg=submit_button_text_color,
		font=submit_button_font,
		pady=10
	).grid(row=19, column=0, sticky=N)
	

def main():
	global window
	window = init_window()
	game_set_up()
	window.mainloop()

if __name__ == "__main__":
	main()