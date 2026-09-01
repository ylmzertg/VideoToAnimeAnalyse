from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ValidationError
from .models import ReferenceBundle


def read_json(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ValidationError(f"File not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {file_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"Root JSON value must be an object: {file_path}")
    return data


def load_reference_bundle(path: str | Path) -> ReferenceBundle:
    return ReferenceBundle.from_dict(read_json(path))


def write_json(path: str | Path, data: dict[str, Any]) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return file_path

