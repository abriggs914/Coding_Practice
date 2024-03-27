import sys
import tkinter

import settings
from begin_game_pop_up import SettingsPopUp
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


# Pygame tutorial from
# https://youtu.be/ECqUrT7IdqQ


class Game:
    def __init__(self):

        # self.window = tkinter.Tk()
    # self.window.geometry("690x500")

        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        # self.show_settings()
        #
        self.new_game()

    def show_settings(self):
        self.top_level_settings = SettingsPopUp(self)
        self.top_level_settings.protocol("WM_DELETE_WINDOW", self.closing_settings)
        # self.window.mainloop()
        self.top_level_settings.mainloop()

    def closing_settings(self, *args):
        tv_use_3d = self.top_level_settings.toggle_2d_or_3d.is_on.get()
        tv_use_mouse_control = self.top_level_settings.toggle_mouse_control.is_on.get()
        tv_plos = self.top_level_settings.toggle_player_line_of_sight.is_on.get()
        tv_textured_walls = self.top_level_settings.toggle_textured_walls.is_on.get()
        tv_npc_bfs = self.top_level_settings.toggle_npc_path.is_on.get()

        old = [
            settings.DRAW_TWO_D_GAME,
            settings.CONTROL_WITH_MOUSE,
            settings.DRAW_PLAYER_LINE_OF_SIGHT,
            settings.DRAW_TEXTURED_WALLS,
            settings.NPC_USES_BFS
        ]

        global DRAW_TWO_D_GAME, CONTROL_WITH_MOUSE, DRAW_PLAYER_LINE_OF_SIGHT, DRAW_TEXTURED_WALLS, NPC_USES_BFS
        DRAW_TWO_D_GAME = not tv_use_3d
        CONTROL_WITH_MOUSE = tv_use_mouse_control
        DRAW_PLAYER_LINE_OF_SIGHT = tv_plos
        DRAW_TEXTURED_WALLS = tv_textured_walls
        NPC_USES_BFS = tv_npc_bfs

        new = [
            settings.DRAW_TWO_D_GAME,
            settings.CONTROL_WITH_MOUSE,
            settings.DRAW_PLAYER_LINE_OF_SIGHT,
            settings.DRAW_TEXTURED_WALLS,
            settings.NPC_USES_BFS
        ]

        print(f"{settings.DRAW_TWO_D_GAME=}\n{old=}\n{new=}\n{list(map(type, old))=}\n{list(map(type, new))=}\n{old==new=}")

        self.top_level_settings.destroy()
        if old != new:
            self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps()= : .1f}")

    def draw(self):
        # print(f"DRAW!!  {settings.DRAW_TWO_D_GAME=}")
        if DRAW_TWO_D_GAME:
            print(f"DRAW 2D GAME!!  {settings.DRAW_TWO_D_GAME=}")
            self.screen.fill("black")
            self.map.draw()
            self.player.draw()
        else:
            print(f"DRAW 3D GAME!!  {settings.DRAW_TWO_D_GAME=}")
            self.object_renderer.draw()
            self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                self.pause_trigger = True
            self.player.single_fire_event(event)

        # while self.pause_trigger:dddss

    def run(self):
        self.running_trigger = True
        self.pause_trigger = True
        while True:
            if not pg.get_init():
                self.running_trigger = False
                return
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    Game().run()

