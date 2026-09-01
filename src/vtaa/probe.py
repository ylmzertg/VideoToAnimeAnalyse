from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

from .errors import ProbeError
from .models import SUPPORTED_SCHEMA_VERSION


def _parse_rate(value: str | None) -> float:
    if not value or value == "0/0":
        raise ProbeError("ffprobe did not report a valid frame rate")
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ProbeError(f"Invalid frame rate returned by ffprobe: {value}") from exc


def probe_video(path: str | Path, sport: str, project_id: str | None = None) -> dict[str, Any]:
    video_path = Path(path)
    if not video_path.exists():
        raise ProbeError(f"Video file not found: {video_path}")
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,avg_frame_rate,nb_frames,duration:format=duration",
        "-of",
        "json",
        str(video_path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise ProbeError("ffprobe was not found. Install FFmpeg and add it to PATH.") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or "unknown ffprobe failure"
        raise ProbeError(f"Could not probe video: {detail}") from exc
    try:
        payload = json.loads(result.stdout)
        stream = payload["streams"][0]
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        raise ProbeError("ffprobe returned no readable video stream") from exc
    fps = _parse_rate(stream.get("avg_frame_rate"))
    duration_value = stream.get("duration") or payload.get("format", {}).get("duration")
    try:
        duration = float(duration_value)
    except (TypeError, ValueError) as exc:
        raise ProbeError("ffprobe did not report video duration") from exc
    raw_frame_count = stream.get("nb_frames")
    frame_count = int(raw_frame_count) if raw_frame_count not in (None, "N/A") else round(duration * fps)
    return {
        "schema_version": SUPPORTED_SCHEMA_VERSION,
        "project_id": project_id or video_path.stem,
        "sport": sport.strip().lower(),
        "source": {
            "path": str(video_path),
            "fps": fps,
            "width": int(stream["width"]),
            "height": int(stream["height"]),
            "frame_count": frame_count,
        },
        "entities": [],
        "tracks": [],
        "events": [],
        "anime_profile": {
            "visual_language": "original_clean_cel_anime",
            "output_fps": 24,
            "drawing_fps": 12,
            "jump_multiplier": 6.0,
            "speed_multiplier": 3.0,
            "impact_multiplier": 4.0,
            "aspect_ratio": "16:9",
        },
    }

