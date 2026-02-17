# sim/config.py
import json
from sim.network import RoadNetwork, Lane, LaneId
from sim.signals import Phase, SignalPlan, TrafficLightController
from sim.world import Spawner, World, RouteChoice
from utils.geometry import polyline_length

def load_world_from_json(path: str) -> tuple[World, dict]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    rn = RoadNetwork()
    for l in cfg["network"]["lanes"]:
        lane = Lane(
            id=LaneId(l["id"]),
            name=l.get("name", l["id"]),
            centerline=[tuple(p) for p in l["centerline"]],
            width_m=float(l["width_m"]),
            speed_limit_mps=float(l["speed_limit_mps"]),
            allowed_movements=list(l.get("allowed_movements", [])),
            connects_to=[LaneId(x) for x in l.get("connects_to", [])],
            stopline_s=l.get("stopline_s"),
            movement_key=l.get("movement_key")   # <-- ADD
        )
        lane.length_m = polyline_length(lane.centerline)
        rn.lanes[l["id"]] = lane

    controller = None
    if "signals" in cfg:
        phases = []
        for p in cfg["signals"]["plan"]["phases"]:
            phases.append(
                Phase(
                    name=p["name"],
                    green_movements=set(p["green_movements"]),
                    duration_s=float(p["duration_s"]),
                    yellow_s=float(p.get("yellow_s", 3.0)),
                    all_red_s=float(p.get("all_red_s", 1.0)),
                )
            )
        plan = SignalPlan(phases=phases, start_phase_index=int(cfg["signals"]["plan"].get("start_phase_index", 0)))
        controller = TrafficLightController(
            plan=plan,
            movement_to_lanes=cfg["signals"]["movement_to_lanes"],
        )
        controller.reset()

    spawners = []
    for s in cfg["demand"]["spawners"]:
        choices = None
        if "choices" in s:
            choices = [RouteChoice(p=float(ch["p"]), route=list(ch["route"])) for ch in s["choices"]]
        spawners.append(Spawner(
            lane_id=s["lane_id"],
            arrival_rate_vps=float(s["arrival_rate_vps"]),
            route=s.get("route"),
            choices=choices
        ))

    world = World(network=rn, controller=controller, spawners=spawners)
    seed = int(cfg["sim"].get("seed", 0))
    world.rng.seed(seed)
    return world, cfg
