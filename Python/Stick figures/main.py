
# Python program to animate ASCII art.
# Calculates the number of usable
# frames from input of a specific format
# seen in the source.py file.
# The escape character '\' gave me trouble
# until I converted the input strings to a raw
# format using the 'r' keyword.
# In my cmd window I needed to change the font
# from GOTHICMS to CONSOLAS in order to accurately
# show the backslash character, else it would print
# the yen symbol instead.
#
# ASCII art is courtesy of http://www.ascii-art.de/ascii/s/stickman.txt
#
# June 2020


from os import system
import numpy as np
from time import sleep
from source import *


# import re
# import codecs

# ESCAPE_SEQUENCE_RE = re.compile(r'''
    # ( \\U........      # 8-digit hex escapes
    # | \\u....          # 4-digit hex escapes
    # | \\x..            # 2-digit hex escapes
    # | \\[0-7]{1,3}     # Octal escapes
    # | \\N\{[^}]+\}     # Unicode characters by name
    # | \\[\\'"abfnrtv]  # Single-character escapes
    # )''', re.UNICODE | re.VERBOSE)

# def decode_escapes(s):
    # def decode_match(match):
        # return codecs.decode(match.group(0), 'unicode-escape')

    # return ESCAPE_SEQUENCE_RE.sub(decode_match, s)

def group_spaces(spaces):
	groups = []
	i = 0
	while i < len(spaces):
		start = spaces[i]
		while i + 1 < len(spaces) and spaces[i] + 1 == spaces[i + 1]:
			i += 1
		end = spaces[i]
		i += 1
		groups.append(range(start, end + 1))
	return groups
	
def group_frames(name, src, groups):
	keys = list(range(len(groups)))
	vals = ["" for i in range(len(groups))]
	frames = dict(zip(keys, vals))
	for n, group in enumerate(groups):
		start = group.start
		stop = group.stop
		# print("start", start, "stop", stop, "len(frames)", len(frames), "len(src)", len(src))
		for i in range(len(src)):
			if i == 0:
				frames[n] += "\n\n\n\n\t\t{0}\n\n\n\n\n\n\n".format(name)
			# print("i", i, "len(src[i])", len(src[i]))
			frames[n] += "\t\t" + "".join(src[i][start: stop])
			frames[n] += "\n" 
	return frames
	
def fill_in_spaces(max_len, space_groups):
	groups = []
	for i, group in enumerate(space_groups):
		start = group.stop
		if i < len(space_groups) - 1:
			stop = space_groups[i + 1].start
		else:
			stop = max_len
		groups.append(range(start, stop))
	return groups

def split_src_img(src):
	lines = src.split("\n")
	img_name = lines[1].strip()
	max_len = max([len(line) for line in lines[2:]])
	lines = [list(line.ljust(max_len, " ")) for line in lines[2:]]
	# print(np.array(lines), "\n\n")
	
	transpose = np.transpose(lines)
	spaces_idxs = [i for i in range(len(transpose)) if len("".join(transpose[i]).strip()) == 0]
	# print("\tspaces_idxs:\n", spaces_idxs)
	
	space_groups = group_spaces(spaces_idxs)
	groups = fill_in_spaces(max_len, space_groups)
	# print(space_groups)
	# print(groups)
	
	frames = group_frames(img_name, lines, groups)
	return img_name, frames
	
def animate(times, src_material, sleep_time=0.1):
	for i in range(times):
		for key, frame in src_material.items():
			system("cls")
			print(frame)
			sleep(sleep_time)
	
	
src_images_unparsed = [dancing_in_the_rain, weight_lifting, riding_bikes, gymnastics, cartwheel, flip, head_over_heals, tai_chi_1, tai_chi_2]
src_images_unparsed += [tai_chi_1, tai_chi_2, playing_tennis, wheelie, skateboarding]
src_images = {}

for img in src_images_unparsed:
	img_name, src_material = split_src_img(img)
	src_images[img_name] = src_material

border = "".join(["#" for i in range(50)])
for name, src_material in src_images.items():
	# print("\t\t{0}:\n".format(name))
	animate(5, src_material, 0.2)