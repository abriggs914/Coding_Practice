import pygame
from render.colors import congestion_to_color, random_rgb
from sim import world
from sim.vehicles import Vehicle
from sim.world import World
from utils.geometry import point_at_s, heading_at_end
import math


def heading_at_s(points, s: float) -> float:
    """Approximate heading along polyline at distance s."""
    # sample a tiny delta forward to estimate tangent
    s2 = s + 0.5
    x1, y1 = point_at_s(points, max(0.0, s))
    x2, y2 = point_at_s(points, max(0.0, s2))
    return math.atan2(y2 - y1, x2 - x1)


def draw_vehicle_selection_annotation(screen, world_to_screen, lane, vehicle: Vehicle, font: pygame.font.Font):
    s_m = vehicle.s_m
    x, y = point_at_s(lane.centerline, s_m)
    ang = heading_at_s(lane.centerline, s_m)
    sx, sy = world_to_screen(x, y)
    rect = pygame.rect.Rect(0, 0, 75, 24)
    rect.center = (sx + 40, sy - 40)

    pygame.draw.line(screen, (245, 245, 245), (sx, sy), rect.center, 3)
    pygame.draw.rect(screen, (255, 255, 255), rect)

    lines = [
        f"#{vehicle.id} {vehicle.speed_mps:.3f} mph",
        f"{vehicle.route}"
    ]


    for i, ln in enumerate(lines):
        surf = font.render(ln, True, (0, 0, 160))
        screen.blit(surf, (rect.left + 3, rect.top + (8 * (i + 0)) + 2))
        y += 20


def draw_vehicle_triangle(screen, world_to_screen, lane, s_m: float, size_px: int = 7, color: tuple = (220, 220, 230)):
    x, y = point_at_s(lane.centerline, s_m)
    ang = heading_at_s(lane.centerline, s_m)

    sx, sy = world_to_screen(x, y)

    # triangle points: tip forward, two rear corners
    tip = (sx + int(size_px * 1.6 * math.cos(ang)),
           sy + int(size_px * 1.6 * math.sin(ang)))

    rear_ang1 = ang + 2.5
    rear_ang2 = ang - 2.5
    rear1 = (sx + int(size_px * math.cos(rear_ang1)),
             sy + int(size_px * math.sin(rear_ang1)))
    rear2 = (sx + int(size_px * math.cos(rear_ang2)),
             sy + int(size_px * math.sin(rear_ang2)))

    return pygame.draw.polygon(screen, color, [tip, rear1, rear2])


def draw_stopline(screen, world_to_screen, lane, s_stop: float, half_len_m: float = 2.0, width_px: int = 3):
    """
    Draw a stopline centered at lane position s_stop, perpendicular to lane direction.
    half_len_m controls the half-length of the stop line in meters.
    """
    x, y = point_at_s(lane.centerline, s_stop)
    ang = heading_at_s(lane.centerline, s_stop)

    # perpendicular direction
    perp = ang + math.pi / 2.0

    x1 = x + half_len_m * math.cos(perp)
    y1 = y + half_len_m * math.sin(perp)
    x2 = x - half_len_m * math.cos(perp)
    y2 = y - half_len_m * math.sin(perp)

    p1 = world_to_screen(x1, y1)
    p2 = world_to_screen(x2, y2)

    pygame.draw.line(screen, (245, 245, 245), p1, p2, width_px)


class PygameView:
    def __init__(self, cfg: dict):
        pygame.init()
        self.ppm = cfg["view"].get("pixels_per_meter", 6)
        self.w, self.h = 1200, 800
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Traffic Sim")
        self.font = pygame.font.SysFont("consolas", 18)
        self.font_mini = pygame.font.SysFont("consolas", 10)
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

            mid = lane.length_m * 0.6
            x, y = point_at_s(lane.centerline, mid)
            ang = heading_at_end(lane.centerline)

            sx, sy = self.world_to_screen(x, y)
            L = 12  # pixels
            tip = (sx + int(L * math.cos(ang)), sy + int(L * math.sin(ang)))
            left = (sx + int(0.6 * L * math.cos(ang + 2.6)), sy + int(0.6 * L * math.sin(ang + 2.6)))
            right = (sx + int(0.6 * L * math.cos(ang - 2.6)), sy + int(0.6 * L * math.sin(ang - 2.6)))
            pygame.draw.polygon(self.screen, (220, 220, 220), [tip, left, right])

            if self.show_overlays and lane.stopline_s is not None:
                draw_stopline(self.screen, self.world_to_screen, lane, lane.stopline_s, half_len_m=2.2, width_px=3)

        # vehicles (simple circles for now)
        for v in world.vehicles:
            lane = world.network.lane(v.lane_id)
            v.rect = draw_vehicle_triangle(self.screen, self.world_to_screen, lane, v.s_m, size_px=6, color=v.color)
            if v in world.selected_vehicles:
                draw_vehicle_selection_annotation(self.screen, self.world_to_screen, lane, v, self.font_mini)

        # HUD metrics
        self.draw_hud(world)

        pygame.display.flip()

    def draw_hud(self, world: World):
        y = 10
        thru: int = world.next_vehicle_id - (len(world.vehicles) + 1)
        lines = [
            f"t={world.t_s:6.1f}s   CarsOnMap={len(world.vehicles)}   CarsThru={thru}"
        ]
        if world.vehicles:
            lines.append(f"CarsTotal={world.next_vehicle_id - 1}   Thru%={100 * thru / (world.next_vehicle_id - 1):.3f} %")
        if world.controller:
            phase = world.controller.current_phase().name
            lines.append(f"signal={phase}  state={world.controller.state}")

        for ln in lines:
            surf = self.font.render(ln, True, (220, 220, 220))
            self.screen.blit(surf, (10, y))
            y += 20

    def handle_event(self, event: pygame.event.Event, world: World):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            mods = pygame.key.get_mods()
            print(f"SC={mods & pygame.KMOD_SHIFT}, {mods=}, {pygame.K_LSHIFT=}, , {pygame.K_RSHIFT=}, {pygame.KMOD_SHIFT=}")
            sel_v_ids = world.selected_vehicles.copy()
            for vehicle in world.vehicles:
                # s_m = vehicle.s_m
                # lane = world.network.lane(vehicle.lane_id)
                # x, y = point_at_s(lane.centerline, s_m)
                # ang = heading_at_s(lane.centerline, s_m)
                rect: pygame.rect.Rect = vehicle.rect
                if rect is not None:
                    if rect.collidepoint(event.pos):
                        if mods & pygame.KMOD_SHIFT:
                            sel_v_ids.append(vehicle)
                        else:
                            sel_v_ids = [vehicle]
            world.select_vehicle(sel_v_ids)
