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
    running = True
    paused = False
    accumulator = 0.0

    while running:
        dt_real = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    accumulator = 0.0  # <-- critical: prevent catch-up jump
                elif event.key == pygame.K_PERIOD and paused:
                    world.step(sim_dt)

        if not paused:
            accumulator += dt_real
            while accumulator >= sim_dt:
                world.step(sim_dt)
                accumulator -= sim_dt

        running = running and (world.t_s < duration_s)

        view.draw(world)

    pygame.quit()

if __name__ == "__main__":
    main()
