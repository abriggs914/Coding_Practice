from battleship_grid import *
from battleship_game import *
from test_suite import *
import copy


def testing_area():
    battleship = BattleshipGrid(2, 2)
    print("lines:\n\t", battleship.lines(1))
    # print("lines:\n\t", battleship.lines(1, 1))
    # print("lines:\n\t", battleship.lines(0, 1))
    print("lines:\n\t", battleship.lines(filter_unique=1))

    TS_lines = TestSuite("BattleshipGrid lines")
    TS_lines.set_func(lambda x, *args: len(x.lines(*args)))
    TS_lines.add_test("Test1 - Removing the Nones (all spaces except (1, 1))", [[battleship, True, False, None, False], 4])
    TS_lines.add_test("Test2 - Removing the hit space at (1, 1)", [[battleship, False, False, BattleshipGrid.SYM_HIT, False], 9])
    TS_lines.add_test("Test3 - Unique lines", [[battleship, False, False, None, True], 4])
    TS_lines.add_test("Test4 - Removing non-Nones. Same as filter_symbols by \"Hits\"", [[battleship, False, True, None, False], 9])

    TS_lines.execute()



def main():
    print("repl_main")
    # testing_area()

    battleship_player_1 = BattleshipPlayer("Player 1")
    battleship_player_2 = BattleshipPlayer("Player 2")
    battleship_players = [battleship_player_1, battleship_player_2]
    battleship_1 = Battleship("Battleship 2", cells=[(1,0), (2, 1), (3, 2)])
    battleship_2 = Battleship("Battleship 2", cells=[(0,2), (1, 2), (2, 2), (3, 2)])
    battleship_grid = BattleshipGrid(5, 11, rnd_shp_max_size=True)
    battleships = [battleship_1, battleship_2]
    battleship_game = BattleshipGame("Game 1", players=battleship_players, grid=battleship_grid, ships=battleships)

    print(battleship_game)
    # battleship2.gen_ship(number=2)
    # print(battleship2)

    battleship_game.grids[0].gen_ship(number=3)
    print(battleship_game.game_grid())

    print(battleship_game.get_player_2_grid())

    a = copy.copy(battleship_1)
    print("a", a),
    print(a.cells)
    print("CREATING B")
    b = copy.copy(battleship_grid)
    print("b", b),
    print(b.grid)
    # a.cells = [["hey"]]
    # b = copy.copy(battleship_1)
    # print("a", a)
    # print("b", b)
    # print("battleship1", battleship_1)
    # print("copy.copy(battleship1)", copy.copy(battleship_1))
    # print("battleship1", battleship_1)
    c = copy.copy(battleship_game.grids[0])
    print("c", c)
