from __future__ import annotations

from .adapters import get_adapter
from .adapters.base import ShotRecipe
from .models import ReferenceBundle, Storyboard, StoryboardShot


def _resolve_frame(event_start: int, event_end: int, ratio: float) -> int:
    duration = event_end - event_start
    return event_start + round(duration * ratio)


def _build_shot_id(event_id: str, index: int, recipe: ShotRecipe) -> str:
    return f"{event_id}.{index:02d}.{recipe.name}"


def build_storyboard(bundle: ReferenceBundle) -> Storyboard:
    adapter = get_adapter(bundle.sport)
    shots: list[StoryboardShot] = []
    for event in bundle.events:
        recipes = adapter.recipes_for(event, bundle)
        for index, recipe in enumerate(recipes, start=1):
            start = _resolve_frame(event.start_frame, event.end_frame, recipe.start_ratio)
            end = _resolve_frame(event.start_frame, event.end_frame, recipe.end_ratio)
            end = max(start, min(end, event.end_frame))
            shots.append(
                StoryboardShot(
                    id=_build_shot_id(event.id, index, recipe),
                    event_id=event.id,
                    start_frame=start,
                    end_frame=end,
                    shot_type=recipe.shot_type,
                    treatment_level=recipe.treatment_level,
                    subjects=event.actor_ids + event.target_ids,
                    camera=recipe.camera,
                    motion=recipe.motion,
                    effects=recipe.effects,
                    purpose=recipe.purpose,
                )
            )
    return Storyboard(
        schema_version="0.1",
        project_id=bundle.project_id,
        sport=bundle.sport,
        source=bundle.source,
        anime_profile=bundle.anime_profile,
        shots=tuple(shots),
    )

