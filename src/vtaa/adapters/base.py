from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ..errors import ValidationError
from ..models import Event, ReferenceBundle


@dataclass(frozen=True)
class ShotRecipe:
    name: str
    start_ratio: float
    end_ratio: float
    shot_type: str
    treatment_level: int
    camera: str
    effects: tuple[str, ...]
    purpose: str
    motion: dict[str, Any]


class SportAdapter(Protocol):
    sport: str

    def recipes_for(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]: ...


def get_adapter(sport: str) -> SportAdapter:
    normalized = sport.strip().lower()
    if normalized == "football":
        from .football import FootballAdapter

        return FootballAdapter()
    raise ValidationError(
        f"No sport adapter registered for '{sport}'. Available adapters: football"
    )

