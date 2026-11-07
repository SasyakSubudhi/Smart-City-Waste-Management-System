"""Feature 1 - Smart bin management (owner: Sasyak Subudhi)."""

from dataclasses import dataclass

VALID_TYPES = ("general", "recyclable", "organic")


@dataclass
class Bin:
    bin_id: str
    location: str
    capacity_litres: int
    waste_type: str = "general"
    fill_level: int = 0  # percent, 0-100

    def __post_init__(self):
        if not self.bin_id:
            raise ValueError("bin_id must not be empty")
        if self.capacity_litres <= 0:
            raise ValueError("capacity must be positive")
        if self.waste_type not in VALID_TYPES:
            raise ValueError(f"waste_type must be one of {VALID_TYPES}")
        self.update_fill_level(self.fill_level)

    def update_fill_level(self, level: int) -> None:
        """Set the sensor reading. Must be between 0 and 100 percent."""
        if level < 0 or level > 100:
            raise ValueError("fill level must be between 0 and 100")
        self.fill_level = level

    def empty(self) -> None:
        self.fill_level = 0

    @property
    def status(self) -> str:
        if self.fill_level >= 90:
            return "FULL"
        if self.fill_level >= 70:
            return "NEARLY_FULL"
        return "OK"


class BinRegistry:
    """Keeps track of every bin in the city."""

    def __init__(self):
        self._bins = {}

    def add(self, b: Bin) -> None:
        if b.bin_id in self._bins:
            raise ValueError(f"bin {b.bin_id} already registered")
        self._bins[b.bin_id] = b

    def get(self, bin_id: str) -> Bin:
        if bin_id not in self._bins:
            raise KeyError(f"bin {bin_id} not found")
        return self._bins[bin_id]

    def remove(self, bin_id: str) -> None:
        self.get(bin_id)  # raises KeyError if missing
        del self._bins[bin_id]

    def all(self) -> list:
        return list(self._bins.values())

    def by_status(self, status: str) -> list:
        return [b for b in self._bins.values() if b.status == status]
