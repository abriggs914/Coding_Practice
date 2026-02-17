# render/pygame_view.py
import pygame
from render.colors import congestion_to_color
from utils.geometry import point_at_s

class PygameView:
    def __init__(self, cfg: dict):
        pygame.init()
        self.ppm = cfg["view"].get("pixels_per_meter", 6)
        self.w, self.h = 1200, 800
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Traffic Sim")
        self.font = pygame.font.SysFont("consolas", 18)
        self.show_overlays = bool(cfg["view"].get("show_overlays", True))

        # world origin -> screen center
        self.cx, self.cy = self.w // 2, self.h // 2

    def world_to_screen(self, x, y):
        # y positive down in screen; you can flip if you prefer
        sx = self.cx + int(x * self.ppm)
        sy = self.cy + int(y * self.ppm)
        return sx, sy

    def draw(self, world):
        self.screen.fill((18, 18, 22))

        # intersection box (visual only)
        p1 = self.world_to_screen(-10, -10)
        p2 = self.world_to_screen(10, 10)
        rect = pygame.Rect(min(p1[0], p2[0]), min(p1[1], p2[1]),
                           abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
        pygame.draw.rect(self.screen, (45, 45, 55), rect, border_radius=6)

        # lanes
        for lane_id, lane in world.network.lanes.items():
            stats = world.metrics.lane_stats.get(lane_id)
            cong = stats.congestion_0_1 if stats else 0.0
            col = congestion_to_color(cong)

            pts = [self.world_to_screen(x, y) for (x, y) in lane.centerline]
            width_px = max(2, int(lane.width_m * self.ppm))
            pygame.draw.lines(self.screen, col, False, pts, width_px)

            if self.show_overlays and lane.stopline_s is not None:
                # draw stopline as small tick mark
                x, y = point_at_s(lane.centerline, lane.stopline_s)
                sx, sy = self.world_to_screen(x, y)
                pygame.draw.circle(self.screen, (255, 255, 255), (sx, sy), 4)

        # vehicles (simple circles for now)
        for v in world.vehicles:
            lane = world.network.lane(v.lane_id)
            x, y = point_at_s(lane.centerline, v.s_m)
            sx, sy = self.world_to_screen(x, y)
            pygame.draw.circle(self.screen, (220, 220, 230), (sx, sy), 5)

        # HUD metrics
        self.draw_hud(world)

        pygame.display.flip()

    def draw_hud(self, world):
        y = 10
        lines = [
            f"t={world.t_s:6.1f}s   vehicles={len(world.vehicles)}",
        ]
        if world.controller:
            phase = world.controller.current_phase().name
            lines.append(f"signal={phase}  state={world.controller.state}")

        for ln in lines:
            surf = self.font.render(ln, True, (220, 220, 220))
            self.screen.blit(surf, (10, y))
            y += 20
