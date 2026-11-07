"""Capacity-aware collection planning for FR-5, FR-6 and FR-7.

Routes are priority lists, not geographic shortest paths: the SRS supplies
location labels but no coordinates or travel-distance model.
"""

from dataclasses import dataclass
from .bins import BinRegistry


@dataclass(frozen=True)
class Truck:
    truck_id: str
    capacity_bins: int

    def __post_init__(self):
        if not isinstance(self.truck_id, str) or not self.truck_id.strip():
            raise ValueError("truck_id must be a nonempty string")
        if type(self.capacity_bins) is not int or self.capacity_bins <= 0:
            raise ValueError("capacity_bins must be a positive integer")


@dataclass
class Route:
    truck: Truck
    bin_ids: tuple[str, ...]
    completed: bool = False


@dataclass(frozen=True)
class RoutingPlan:
    routes: tuple[Route, ...]
    unassigned_bin_ids: tuple[str, ...]


def plan_routes(registry: BinRegistry, trucks, threshold: int = 70) -> RoutingPlan:
    """Plan one trip per truck, fullest first; ties use bin ID.

    Truck input order determines which truck is filled first. Planning never
    changes sensor readings. The returned backlog preserves priority order.
    """
    if type(threshold) is not int or not 0 <= threshold <= 100:
        raise ValueError("threshold must be an integer between 0 and 100")
    fleet = list(trucks)
    if any(not isinstance(truck, Truck) for truck in fleet):
        raise ValueError("fleet entries must be Truck objects")
    if len({truck.truck_id for truck in fleet}) != len(fleet):
        raise ValueError("truck IDs must be unique")
    due = sorted((b for b in registry.all() if b.fill_level >= threshold),
                 key=lambda b: (-b.fill_level, b.bin_id))
    routes = []
    offset = 0
    for truck in fleet:
        assigned = due[offset:offset + truck.capacity_bins]
        if assigned:
            routes.append(Route(truck, tuple(b.bin_id for b in assigned)))
        offset += len(assigned)
    return RoutingPlan(tuple(routes), tuple(b.bin_id for b in due[offset:]))


def complete_route(route: Route, registry: BinRegistry) -> None:
    """Empty every bin on a route once; missing bins cause no partial update.

    The caller confirms the actual truck trip has finished. This in-memory
    application does not dispatch vehicles or authenticate operators.
    """
    if route.completed:
        raise ValueError("route is already completed")
    if not route.bin_ids or len(route.bin_ids) > route.truck.capacity_bins:
        raise ValueError("route must contain bins within truck capacity")
    if len(set(route.bin_ids)) != len(route.bin_ids):
        raise ValueError("route cannot contain duplicate bin IDs")
    bins = [registry.get(bin_id) for bin_id in route.bin_ids]
    for b in bins:
        b.empty()
    route.completed = True
