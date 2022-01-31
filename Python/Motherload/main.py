from vehicle import *
from pygame_utility import *


def main_loop():
    app = PygameApplication("Name Goes Here!", 750, 500)
    game = app.get_game()
    display = app.display

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here

        event_queue = app.run()
        for event in event_queue:
            # handle events
            pass

    app.clock.tick(30)


if __name__ == '__main__':
    t1 = Vehicle(1, "Tank", None, GREEN)
    grid_data_template = [
            "width",
            "height",
            "ground_level",
            "shop_pos",
            "fuel_station_pos",
            "spawn_pos",
            "gem_data"
    ]
    main_loop()

# tank
# - drill
# - hull
# - storage
# - propeller
# - fuel tank
# grid
# gems
# shop
# fuel
# fuel station

