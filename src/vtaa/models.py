from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .errors import ValidationError


SUPPORTED_SCHEMA_VERSION = "0.1"
SUPPORTED_COORDINATE_SPACES = {"image_normalized"}


def _required(data: dict[str, Any], key: str, expected_type: type) -> Any:
    if key not in data:
        raise ValidationError(f"Missing required field: {key}")
    value = data[key]
    if not isinstance(value, expected_type):
        raise ValidationError(
            f"Field '{key}' must be {expected_type.__name__}, got {type(value).__name__}"
        )
    return value


def _positive_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValidationError(f"Field '{field_name}' must be a positive number")
    return float(value)


def _frame(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValidationError(f"Field '{field_name}' must be a non-negative integer")
    return value


@dataclass(frozen=True)
class SourceClip:
    path: str
    fps: float
    width: int
    height: int
    frame_count: int

    @property
    def duration_seconds(self) -> float:
        return self.frame_count / self.fps

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SourceClip:
        path = _required(data, "path", str).strip()
        if not path:
            raise ValidationError("Field 'source.path' cannot be empty")
        fps = _positive_number(data.get("fps"), "source.fps")
        width = _frame(data.get("width"), "source.width")
        height = _frame(data.get("height"), "source.height")
        frame_count = _frame(data.get("frame_count"), "source.frame_count")
        if width == 0 or height == 0 or frame_count == 0:
            raise ValidationError("Source width, height and frame_count must be greater than zero")
        return cls(path=path, fps=fps, width=width, height=height, frame_count=frame_count)


@dataclass(frozen=True)
class Entity:
    id: str
    kind: str
    team: str | None = None
    display_name: str | None = None
    color: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Entity:
        entity_id = _required(data, "id", str).strip()
        kind = _required(data, "kind", str).strip()
        if not entity_id or not kind:
            raise ValidationError("Entity id and kind cannot be empty")
        return cls(
            id=entity_id,
            kind=kind,
            team=data.get("team"),
            display_name=data.get("display_name"),
            color=data.get("color"),
        )


@dataclass(frozen=True)
class TrackPoint:
    frame: int
    x: float
    y: float
    confidence: float = 1.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TrackPoint:
        frame = _frame(data.get("frame"), "track.points[].frame")
        x = data.get("x")
        y = data.get("y")
        confidence = data.get("confidence", 1.0)
        for value, name in ((x, "x"), (y, "y"), (confidence, "confidence")):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValidationError(f"Track point {name} must be numeric")
        if not 0 <= float(x) <= 1 or not 0 <= float(y) <= 1:
            raise ValidationError("Normalized track coordinates must be between 0 and 1")
        if not 0 <= float(confidence) <= 1:
            raise ValidationError("Track confidence must be between 0 and 1")
        return cls(frame=frame, x=float(x), y=float(y), confidence=float(confidence))


@dataclass(frozen=True)
class Track:
    entity_id: str
    coordinate_space: str
    points: tuple[TrackPoint, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Track:
        entity_id = _required(data, "entity_id", str)
        coordinate_space = data.get("coordinate_space", "image_normalized")
        if coordinate_space not in SUPPORTED_COORDINATE_SPACES:
            raise ValidationError(f"Unsupported coordinate space: {coordinate_space}")
        raw_points = _required(data, "points", list)
        points = tuple(TrackPoint.from_dict(point) for point in raw_points)
        if not points:
            raise ValidationError(f"Track '{entity_id}' must contain at least one point")
        frames = [point.frame for point in points]
        if frames != sorted(frames) or len(frames) != len(set(frames)):
            raise ValidationError(f"Track '{entity_id}' frames must be strictly increasing")
        return cls(entity_id=entity_id, coordinate_space=coordinate_space, points=points)


@dataclass(frozen=True)
class Event:
    id: str
    type: str
    start_frame: int
    impact_frame: int
    end_frame: int
    actor_ids: tuple[str, ...]
    target_ids: tuple[str, ...] = ()
    confidence: float = 1.0
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        event_id = _required(data, "id", str).strip()
        event_type = _required(data, "type", str).strip().lower()
        start = _frame(data.get("start_frame"), "event.start_frame")
        impact = _frame(data.get("impact_frame"), "event.impact_frame")
        end = _frame(data.get("end_frame"), "event.end_frame")
        if not start <= impact <= end:
            raise ValidationError(
                f"Event '{event_id}' must satisfy start_frame <= impact_frame <= end_frame"
            )
        actor_ids = tuple(_required(data, "actor_ids", list))
        target_ids = tuple(data.get("target_ids", []))
        if not actor_ids or not all(isinstance(item, str) and item for item in actor_ids):
            raise ValidationError(f"Event '{event_id}' must have at least one string actor_id")
        if not all(isinstance(item, str) and item for item in target_ids):
            raise ValidationError(f"Event '{event_id}' target_ids must be strings")
        confidence = data.get("confidence", 1.0)
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise ValidationError(f"Event '{event_id}' confidence must be numeric")
        if not 0 <= float(confidence) <= 1:
            raise ValidationError(f"Event '{event_id}' confidence must be between 0 and 1")
        attributes = data.get("attributes", {})
        if not isinstance(attributes, dict):
            raise ValidationError(f"Event '{event_id}' attributes must be an object")
        return cls(
            id=event_id,
            type=event_type,
            start_frame=start,
            impact_frame=impact,
            end_frame=end,
            actor_ids=actor_ids,
            target_ids=target_ids,
            confidence=float(confidence),
            attributes=attributes,
        )


@dataclass(frozen=True)
class AnimeProfile:
    visual_language: str = "original_clean_cel_anime"
    output_fps: int = 24
    drawing_fps: int = 12
    jump_multiplier: float = 6.0
    speed_multiplier: float = 3.0
    impact_multiplier: float = 4.0
    aspect_ratio: str = "16:9"

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> AnimeProfile:
        data = data or {}
        profile = cls(
            visual_language=str(data.get("visual_language", cls.visual_language)).strip(),
            output_fps=int(data.get("output_fps", cls.output_fps)),
            drawing_fps=int(data.get("drawing_fps", cls.drawing_fps)),
            jump_multiplier=float(data.get("jump_multiplier", cls.jump_multiplier)),
            speed_multiplier=float(data.get("speed_multiplier", cls.speed_multiplier)),
            impact_multiplier=float(data.get("impact_multiplier", cls.impact_multiplier)),
            aspect_ratio=str(data.get("aspect_ratio", cls.aspect_ratio)),
        )
        if profile.output_fps <= 0 or profile.drawing_fps <= 0:
            raise ValidationError("Anime output_fps and drawing_fps must be positive")
        if profile.drawing_fps > profile.output_fps:
            raise ValidationError("Anime drawing_fps cannot exceed output_fps")
        if min(profile.jump_multiplier, profile.speed_multiplier, profile.impact_multiplier) <= 0:
            raise ValidationError("Anime exaggeration multipliers must be positive")
        if profile.aspect_ratio != "16:9":
            raise ValidationError("V0.1 supports only the 16:9 output aspect ratio")
        return profile


@dataclass(frozen=True)
class ReferenceBundle:
    schema_version: str
    project_id: str
    sport: str
    source: SourceClip
    entities: tuple[Entity, ...]
    tracks: tuple[Track, ...]
    events: tuple[Event, ...]
    anime_profile: AnimeProfile

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReferenceBundle:
        schema_version = _required(data, "schema_version", str)
        if schema_version != SUPPORTED_SCHEMA_VERSION:
            raise ValidationError(
                f"Unsupported schema_version '{schema_version}'; expected {SUPPORTED_SCHEMA_VERSION}"
            )
        project_id = _required(data, "project_id", str).strip()
        sport = _required(data, "sport", str).strip().lower()
        if not project_id or not sport:
            raise ValidationError("project_id and sport cannot be empty")
        source_data = _required(data, "source", dict)
        entities_data = _required(data, "entities", list)
        tracks_data = _required(data, "tracks", list)
        events_data = _required(data, "events", list)
        source = SourceClip.from_dict(source_data)
        entities = tuple(Entity.from_dict(item) for item in entities_data)
        tracks = tuple(Track.from_dict(item) for item in tracks_data)
        events = tuple(Event.from_dict(item) for item in events_data)
        entity_ids = [entity.id for entity in entities]
        if len(entity_ids) != len(set(entity_ids)):
            raise ValidationError("Entity IDs must be unique")
        known_ids = set(entity_ids)
        for track in tracks:
            if track.entity_id not in known_ids:
                raise ValidationError(f"Track references unknown entity '{track.entity_id}'")
            if track.points[-1].frame >= source.frame_count:
                raise ValidationError(f"Track '{track.entity_id}' exceeds source frame_count")
        event_ids = [event.id for event in events]
        if len(event_ids) != len(set(event_ids)):
            raise ValidationError("Event IDs must be unique")
        for event in events:
            unknown = (set(event.actor_ids) | set(event.target_ids)) - known_ids
            if unknown:
                raise ValidationError(
                    f"Event '{event.id}' references unknown entities: {sorted(unknown)}"
                )
            if event.end_frame >= source.frame_count:
                raise ValidationError(f"Event '{event.id}' exceeds source frame_count")
        return cls(
            schema_version=schema_version,
            project_id=project_id,
            sport=sport,
            source=source,
            entities=entities,
            tracks=tracks,
            events=events,
            anime_profile=AnimeProfile.from_dict(data.get("anime_profile")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StoryboardShot:
    id: str
    event_id: str
    start_frame: int
    end_frame: int
    shot_type: str
    treatment_level: int
    subjects: tuple[str, ...]
    camera: str
    motion: dict[str, Any]
    effects: tuple[str, ...]
    purpose: str


@dataclass(frozen=True)
class Storyboard:
    schema_version: str
    project_id: str
    sport: str
    source: SourceClip
    anime_profile: AnimeProfile
    shots: tuple[StoryboardShot, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

