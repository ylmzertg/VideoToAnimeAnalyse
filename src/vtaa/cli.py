from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .errors import VTAAError
from .planner import build_storyboard
from .preview import write_storyboard_html
from .probe import probe_video
from .project_io import load_reference_bundle, write_json


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vtaa",
        description="Reference-guided multi-sport 2D anime planning engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a reference bundle")
    validate.add_argument("input", type=Path)

    plan = subparsers.add_parser("plan", help="Create a storyboard JSON")
    plan.add_argument("input", type=Path)
    plan.add_argument("-o", "--output", type=Path, required=True)

    preview = subparsers.add_parser("preview", help="Create a visual HTML storyboard")
    preview.add_argument("input", type=Path)
    preview.add_argument("-o", "--output", type=Path, required=True)

    probe = subparsers.add_parser("probe", help="Create a reference template from a video")
    probe.add_argument("video", type=Path)
    probe.add_argument("--sport", default="football")
    probe.add_argument("--project-id")
    probe.add_argument("-o", "--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            bundle = load_reference_bundle(args.input)
            print(
                f"Valid reference bundle: {bundle.project_id} · {bundle.sport} · "
                f"{len(bundle.entities)} entities · {len(bundle.events)} events"
            )
            return 0
        if args.command == "plan":
            storyboard = build_storyboard(load_reference_bundle(args.input))
            output = write_json(args.output, storyboard.to_dict())
            print(f"Storyboard written: {output} ({len(storyboard.shots)} shots)")
            return 0
        if args.command == "preview":
            storyboard = build_storyboard(load_reference_bundle(args.input))
            output = write_storyboard_html(args.output, storyboard)
            print(f"Storyboard preview written: {output} ({len(storyboard.shots)} shots)")
            return 0
        if args.command == "probe":
            template = probe_video(args.video, args.sport, args.project_id)
            output = write_json(args.output, template)
            print(f"Reference template written: {output}")
            return 0
    except VTAAError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

