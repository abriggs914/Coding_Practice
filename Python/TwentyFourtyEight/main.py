import random as rand
from test_suite import *
from G2048 import *


def play_game(gen_moves=True, start_grid=None):
	if start_grid:
		game = G2048(init_spaces=start_grid)
	else:
		game = G2048()
		game.gen_random_tile()
		game.gen_random_tile()

	game.play()
		
	
def move_tests():
	move_test_grid = [[2, None, None, 2], [None, 2, None, None], [None, None, 2, None], [2, 2, 2, 2]]
	moves_test_set = {
		"test_1, testing 1 move up": [
			[
				move_test_grid,
				"up"
			],
			[[4, 4, 4, 4], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_2, testing 1 move down": [
			[
				move_test_grid,
				"down"
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [4, 4, 4, 4]]
		],
		"test_3, testing 1 move left": [
			[
				move_test_grid,
				"left"
			],
			[[4, None, None, None], [2, None, None, None], [2, None, None, None], [4, 4, None, None]]
		],
		"test_4, testing 1 move right": [
			[
				move_test_grid,
				"right"
			],
			[[None, None, None, 4], [None, None, None, 2], [None, None, None, 2], [None, None, 4, 4]]
		],
		"test_5, should only make one push not 2": [
			[
				[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]],
				"right"
			],
			[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, None, 4, 4]]
		],
		"test_6, should only make one push not 2": [
			[
				[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]],
				"left"
			],
			[[2, None, None, None], [4, None, None, None], [2, 4, 2, None], [4, 4, None, None]]
		],
		"test_7, testing 2 moves, up then left": [
			[
				move_test_grid,
				[
					"up",
					"left"
				]
			],
			[[8, 8, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_8, testing 2 moves, up then right": [
			[
				move_test_grid,
				[
					"up",
					"right"
				]
			],
			[[None, None, 8, 8], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_9, testing 2 moves, up then up": [
			[
				move_test_grid,
				[
					"up",
					"up"
				]
			],
			[[4, 4, 4, 4], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_10, testing 2 moves, up then down": [
			[
				move_test_grid,
				[
					"up",
					"down"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [4, 4, 4, 4]]
		],
		"test_11, testing 2 moves, down then left": [
			[
				move_test_grid,
				[
					"down",
					"left"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [8, 8, None, None]]
		],
		"test_12, testing 2 moves, down then right": [
			[
				move_test_grid,
				[
					"down",
					"right"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, 8, 8]]
		],
		"test_13, testing 2 moves, down then up": [
			[
				move_test_grid,
				[
					"down",
					"up"
				]
			],
			[[4, 4, 4, 4], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_14, testing 2 moves, down then down": [
			[
				move_test_grid,
				[
					"down",
					"down"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [4, 4, 4, 4]]
		],
		"test_15, testing 2 moves, left then left": [
			[
				move_test_grid,
				[
					"left",
					"left"
				]
			],
			[[4, None, None, None], [2, None, None, None], [2, None, None, None], [8, None, None, None]]
		],
		"test_16, testing 2 moves, left then right": [
			[
				move_test_grid,
				[
					"left",
					"right"
				]
			],
			[[None, None, None, 4], [None, None, None, 2], [None, None, None, 2], [None, None, None, 8]]
		],
		"test_17, testing 2 moves, left then up": [
			[
				move_test_grid,
				[
					"left",
					"up"
				]
			],
			[[4, 4, None, None], [4, None, None, None], [4, None, None, None], [None, None, None, None]]
		],
		"test_18, testing 2 moves, left then down": [
			[
				move_test_grid,
				[
					"left",
					"down"
				]
			],
			[[None, None, None, None], [4, None, None, None], [4, None, None, None], [4, 4, None, None]]
		],
		"test_19, testing 2 moves, right then left": [
			[
				move_test_grid,
				[
					"right",
					"left"
				]
			],
			[[4, None, None, None], [2, None, None, None], [2, None, None, None], [8, None, None, None]]
		],
		"test_20, testing 2 moves, right then right": [
			[
				move_test_grid,
				[
					"right",
					"right"
				]
			],
			[[None, None, None, 4], [None, None, None, 2], [None, None, None, 2], [None, None, None, 8]]
		],
		"test_21, testing 2 moves, right then up": [
			[
				move_test_grid,
				[
					"right",
					"up"
				]
			],
			[[None, None, 4, 4], [None, None, None, 4], [None, None, None, 4], [None, None, None, None]]
		],
		"test_22, testing 2 moves, right then down": [
			[
				move_test_grid,
				[
					"right",
					"down"
				]
			],
			[[None, None, None, None], [None, None, None, 4], [None, None, None, 4], [None, None, 4, 4]]
		],
		"test_23, middle shift": [
			[
				[[4, 2, 2, 4], [2, 2, 2, 2], [8, 2, 2, 2], [8, 2, 4, 4]],
				[
					"left"
				]
			],
			[[4, 4, 4, None], [4, 4, None, None], [8, 4, 2, None], [8, 2, 8, None]]
		],
		"test_23 shift right.. again?": [
			[
				[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, 4, 8, 8]],
				"right"
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, 4, 16]]
		],
		"test_24 shift up on a partially full grid": [
			[
				[[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]],
				"up"
			],
			[[16, 2, 4, 8], [256, 32, 64, 128], [4096, 512, 1024, 2048], [None, 8192, 16384, 32768]]
		],
		"test_25 shift left on a partially full grid": [
			[
				[[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]],
				"left"
			],
			[[2, 4, 8, None], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]]
		]
	}

	valid_move_test_set = {
			"test_1 invalid shift right": [
				[
					[[None, None, None, 2], [None, None, None, 4], [None, None, 4, 8], [None, None, 16, 32]],
					"right"
				],
				False
			],
			"test_2 invalid shift up": [
				[
					[[None, None, None, 2], [None, None, None, None], [None, None, None, None], [None, None, None, None]],
					"up"
				],
				False
			],
			"test_3 valid shift up": [
				[
					[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, 2]],
					"up"
				],
				True
			],
			"test_4 shift left on a partially full grid": [
				[
					[[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]],
					"left"
				],
				True
			],
			"test_5 shift up on a partially full grid": [
				[
					[[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]],
					"up"
				],
				True
			],
			"test_6 shift right on a partially full grid": [
				[
					[[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]],
					"right"
				],
				False
			],
			"test_7 shift left on a partially full grid": [
				[
					[[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]],
					"down"
				],
				False
			]
		}
	
	playable_test_set = {
		"test_1 still playable": [
			[
				[[None, 4, 8, 2], [8, 16, 4, 8], [16, 32, 16, 8], [32, 64, 128, 512]]
			],
			True
		],
		"test_2 full grid, still playable": [
			[
				[[2, 4, 8, 2], [8, 16, 4, 8], [16, 32, 16, 8], [32, 64, 128, 512]]
			],
			True
		],
		"test_3 full grid, not playable": [
			[
				[[2, 4, 8, 2], [8, 16, 4, 32], [16, 32, 16, 8], [32, 64, 128, 512]]
			],
			False
		]
	}
	
	def test_move(set_places, move):
		game = G2048(init_spaces=set_places)
		if type(move) == list:
			for m in move:
				game.shift_grid(m)
		else:
			game.shift_grid(move)
		return game.grid

	def test_move_validity(set_places, move):
		game = G2048(init_spaces=set_places)
		return game.shift_grid(move)

	def test_still_playable(set_places):
		game = G2048(init_spaces=set_places)
		return game.playable()

		
	run_multiple_tests([
		(test_move, moves_test_set),
		(test_move_validity, valid_move_test_set),
		(test_still_playable, playable_test_set)
	])
		
if __name__ == "__main__":
	a = """
	game = G2048()
	# game.gen_random_tile()
	game.place(0, 3, 2)
	game.place(3, 3, 2)
	game.place(3, 1, 4)
	game.place(3, 2, 16)
	game.place(2, 1, 32)
	game.place(1, 2, 16)
	print(game)
	# game.shift_grid(game.shift_options["UP"])
	# game.shift_grid(game.shift_options["DOWN"])
	# game.shift_grid(game.shift_options["LEFT"])
	game.shift_grid(game.shift_options["RIGHT"])
	print(game)
	"""
	move_tests()
	# play_game()
	# play_game(start_grid=[[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12],[13, 14, 15, 16]])
	# play_game([[None, None, None, None], [2, None, None, None], [2, None, None, None], [4, 2, 4, 4]])
	# play_game(gen_moves=False, start_grid=[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]])
