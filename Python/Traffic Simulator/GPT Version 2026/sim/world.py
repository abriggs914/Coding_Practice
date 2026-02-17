# sim/world.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
import math

from sim.network import RoadNetwork
from sim.vehicles import Vehicle, VehicleModel
from sim.signals import TrafficLightController
from sim.metrics import LiveMetrics, clamp01, congestion_score
from sim.vehicles import idm_accel


@dataclass
class RouteChoice:
    p: float
    route: List[str]


@dataclass
class Spawner:
    lane_id: str
    arrival_rate_vps: float
    route: Optional[List[str]] = None
    choices: Optional[List[RouteChoice]] = None

    def try_spawn(self, dt: float, rng: random.Random) -> bool:
        p_arr = 1.0 - math.exp(-self.arrival_rate_vps * dt)
        return rng.random() < p_arr

    def pick_route(self, rng: random.Random) -> List[str]:
        if self.choices:
            r = rng.random()
            cum = 0.0
            for ch in self.choices:
                cum += ch.p
                if r <= cum:
                    return ch.route.copy()
            return self.choices[-1].route.copy()  # fallback
        if self.route:
            return self.route.copy()
        raise ValueError(f"Spawner {self.lane_id} has no route or choices.")


@dataclass
class World:
    network: RoadNetwork
    controller: Optional[TrafficLightController]
    spawners: List[Spawner]
    vehicles: List[Vehicle] = field(default_factory=list)
    t_s: float = 0.0
    next_vehicle_id: int = 1
    rng: random.Random = field(default_factory=random.Random)
    metrics: LiveMetrics = field(default_factory=LiveMetrics)

    def step(self, dt: float):
        self.t_s += dt

        # 1) signals
        if self.controller:
            self.controller.step(dt)

        # 2) spawn
        for sp in self.spawners:
            if sp.try_spawn(dt, self.rng) and self.can_spawn_in_lane(sp.lane_id):
                route = sp.pick_route(self.rng)
                self.spawn_vehicle(sp.lane_id, route)

        # 3) vehicle update (MVP: very simple logic)
        # You will replace this with IDM + proper leader finding.
        self.update_vehicles(dt)

        # 4) metrics
        self.update_metrics()

    def spawn_vehicle(self, lane_id: str, route: List[str]):
        v = Vehicle(
            id=self.next_vehicle_id,
            lane_id=lane_id,
            s_m=0.0,
            speed_mps=0.0,
            model=VehicleModel(),
            route=route.copy(),
            spawned_time_s=self.t_s
        )
        self.next_vehicle_id += 1
        self.vehicles.append(v)

    # def update_vehicles(self, dt: float):
    #     # Very simple placeholder movement:
    #     # - accelerate toward desired speed
    #     # - stop at stopline if movement is red
    #     for v in self.vehicles:
    #         lane = self.network.lane(v.lane_id)
    #         desired = min(v.model.desired_speed_mps, lane.speed_limit_mps)
    #
    #         # stop for red if lane has stopline and movement is not green
    #         target_speed = desired
    #         if self.controller and lane.stopline_s is not None:
    #             # movement key convention: you can store it on lane later; MVP hardcoded
    #             # Example: lane "N_in_through" maps to movement "NS_through"
    #             movement = "NS_through" if "N_in" in v.lane_id or "S_in" in v.lane_id else "EW_through"
    #             if not self.controller.movement_is_green(movement):
    #                 # if approaching stopline, force slowdown to stop
    #                 dist_to_stop = lane.stopline_s - v.s_m
    #                 if dist_to_stop <= 20.0:  # braking zone
    #                     target_speed = 0.0
    #
    #         # accelerate/brake toward target_speed (placeholder)
    #         if v.speed_mps < target_speed:
    #             v.speed_mps = min(target_speed, v.speed_mps + v.model.max_accel_mps2 * dt)
    #         else:
    #             v.speed_mps = max(target_speed, v.speed_mps - v.model.comfortable_decel_mps2 * dt)
    #
    #         v.s_m += v.speed_mps * dt
    #
    #         # lane end -> transition to next lane in route
    #         lane_len = lane.length_m
    #         if v.s_m >= lane_len:
    #             v.s_m -= lane_len
    #             v.route_index += 1
    #             if v.route_index < len(v.route):
    #                 v.lane_id = v.route[v.route_index]
    #             else:
    #                 v.finished_time_s = self.t_s
    #
    #     # remove completed
    #     self.vehicles = [v for v in self.vehicles if v.finished_time_s is None]

    def update_vehicles(self, dt: float):
        lane_order = self.build_lane_order()

        # Precompute leader for each vehicle (vehicle ahead in same lane)
        leader_of: dict[int, Vehicle | None] = {}
        for lane_id, ordered in lane_order.items():
            for i, v in enumerate(ordered):
                leader_of[v.id] = ordered[i + 1] if i + 1 < len(ordered) else None

        # --- compute accelerations first (don’t update positions yet) ---
        accel_cmd: dict[int, float] = {}

        for v in self.vehicles:
            lane = self.network.lane(v.lane_id)
            model = v.model

            # desired speed is min(vehicle desire, speed limit)
            v0 = min(model.desired_speed_mps, lane.speed_limit_mps)

            # determine physical leader (if any)
            lead = leader_of[v.id]

            # default: leader very far away
            gap = 1e9
            lead_speed = v0

            if lead is not None:
                # net gap: leader rear bumper minus ego front bumper
                lead_len = lead.model.length_m
                gap = (lead.s_m - v.s_m) - lead_len
                lead_speed = lead.speed_mps

            # --- Stopline virtual leader when RED ---
            if self.controller and lane.stopline_s is not None and lane.movement_key:
                if self.controller.lane_is_controlled_by(v.lane_id):
                    is_green = self.controller.movement_is_green(lane.movement_key)
                    if not is_green:
                        # virtual stopped vehicle at stopline
                        stop_gap = (lane.stopline_s - v.s_m)  # no length since it's a stopline
                        # only matters if ahead
                        if stop_gap >= 0.0:
                            gap = min(gap, stop_gap)
                            lead_speed = 0.0

            dv = v.speed_mps - lead_speed

            a = idm_accel(
                v=v.speed_mps,
                v0=v0,
                gap=gap,
                dv=dv,
                a=model.max_accel_mps2,
                b=model.comfortable_decel_mps2,
                s0=model.min_gap_m,
                T=model.time_headway_s,
                delta=model.delta
            )

            # clamp insane values (helps stability)
            a = max(-6.0, min(3.0, a))
            accel_cmd[v.id] = a

        # --- integrate speed + position ---
        for v in self.vehicles:
            a = accel_cmd[v.id]
            v.speed_mps = max(0.0, v.speed_mps + a * dt)
            v.s_m += v.speed_mps * dt

            lane = self.network.lane(v.lane_id)
            lane_len = lane.length_m

            # end-of-lane transition (same as before)
            if v.s_m >= lane_len:
                v.s_m -= lane_len
                v.route_index += 1
                if v.route_index < len(v.route):
                    v.lane_id = v.route[v.route_index]
                else:
                    v.finished_time_s = self.t_s

        # remove completed vehicles
        self.vehicles = [v for v in self.vehicles if v.finished_time_s is None]

    def update_metrics(self):
        # lane stats
        for lane_id, lane in self.network.lanes.items():
            self.metrics.ensure_lane(lane_id)
            stats = self.metrics.lane_stats[lane_id]

            vehs = [v for v in self.vehicles if v.lane_id == lane_id]
            stats.vehicle_count = len(vehs)
            stats.mean_speed_mps = sum(v.speed_mps for v in vehs) / len(vehs) if vehs else 0.0

            length_km = max(lane.length_m / 1000.0, 1e-6)
            stats.density_vpkm = stats.vehicle_count / length_km

            # queue: count vehicles near stopline moving slowly
            queue = 0
            if lane.stopline_s is not None:
                for v in vehs:
                    if (lane.stopline_s - v.s_m) < 15.0 and v.speed_mps < 1.0:
                        queue += 1
            stats.queue_count = queue
            queue_ratio = (queue / stats.vehicle_count) if stats.vehicle_count else 0.0

            mean_speed_ratio = (stats.mean_speed_mps / lane.speed_limit_mps) if lane.speed_limit_mps > 0 else 0.0
            stats.congestion_0_1 = congestion_score(stats.density_vpkm, mean_speed_ratio, queue_ratio)

    def build_lane_order(self) -> dict[str, list[Vehicle]]:
        lane_map: dict[str, list[Vehicle]] = {}
        for v in self.vehicles:
            lane_map.setdefault(v.lane_id, []).append(v)

        # sort by position along the lane (s increasing)
        for lane_id in lane_map:
            lane_map[lane_id].sort(key=lambda x: x.s_m)
        return lane_map

    def can_spawn_in_lane(self, lane_id: str, min_clearance_m: float = 8.0) -> bool:
        # if any vehicle is too close to the start, don't spawn
        for v in self.vehicles:
            if v.lane_id == lane_id and v.s_m < min_clearance_m:
                return False
        return True
