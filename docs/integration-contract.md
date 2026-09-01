# Reference Bundle Integration Contract v0.1

The canonical example is `examples/football_shot.reference.json`.

## Coordinate spaces

V0.1 accepts track points in `image_normalized` coordinates:

- `(0, 0)` is the top-left of the source frame.
- `(1, 1)` is the bottom-right.
- Coordinates are independent of input resolution.

Future versions may add calibrated pitch/court/world coordinates without changing the normalized image track.

## Timing

All event and track timing is stored as integer source-frame indices. The clip FPS converts frames to seconds. This avoids drift caused by rounded timestamps.

Events must satisfy:

```text
0 <= start_frame <= impact_frame <= end_frame < source.frame_count
```

## Identity

Entity IDs are strings and must be unique within a bundle. Event actor/target references and track entity references must resolve to declared entities.

## Compatibility

- Producers must emit `schema_version: "0.1"`.
- Consumers must reject unsupported major/minor versions instead of guessing.
- New optional fields may be added in later compatible versions.
- Breaking coordinate, identity or timing semantics require a new schema version.

## FootballAnalysisAI export boundary

FootballAnalysisAI should eventually export:

- source metadata,
- tracked players, goalkeeper and ball,
- normalized image-space track points,
- detected/verified events,
- event actor and target IDs,
- confidence and sport-specific attributes,
- optional calibrated field coordinates and camera trajectory.

VideoToAnimeAnalyse must not require FootballAnalysisAI's internal class names or database layout.

