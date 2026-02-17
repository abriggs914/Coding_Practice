# main.py
import pygame
from sim.config import load_world_from_json
from render.pygame_view import PygameView

def main():
    world, cfg = load_world_from_json("scenarios/four_way_mvp.json")
    view = PygameView(cfg)

    sim_dt = float(cfg["sim"]["dt"])
    duration_s = float(cfg["sim"].get("duration_s", 300))

    clock = pygame.time.Clock()
    accumulator = 0.0
    running = True
    paused = False

    while running and world.t_s < duration_s:
        dt_real = clock.tick(60) / 1000.0
        accumulator += dt_real

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_PERIOD:  # step one tick
                    if paused:
                        world.step(sim_dt)

        if not paused:
            while accumulator >= sim_dt:
                world.step(sim_dt)
                accumulator -= sim_dt

        view.draw(world)

    pygame.quit()

if __name__ == "__main__":
    main()
