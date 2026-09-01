# VideoToAnimeAnalyse

Reference-guided, multi-sport 2D anime re-animation engine.

The project does **not** attempt to apply an anime filter to every pixel of a full broadcast. It takes short highlight clips as motion and event references, converts their analysis into a stable interchange format, and plans an original 2D limited-animation reconstruction.

## Product goal

```text
CapCut highlight clips
        -> sport analysis / reference extraction
        -> normalized event bundle
        -> anime storyboard and motion exaggeration
        -> 2D scene rendering
        -> effects, telestration, narration and final 16:9 video
```

The real event order and outcome are preserved. Presentation may be exaggerated with impossible jumps, extreme speed, impact frames, energy trails, freeze frames and dramatic camera language.

## Current milestone: Foundation V0.1

The initial implementation provides:

- A versioned JSON contract for clips, entities, tracks, events and anime direction.
- Strict validation of references, frame ranges and normalized coordinates.
- A sport-adapter registry.
- A football adapter for `shot`, `pass`, `dribble` and `save` events.
- Automatic three-level limited-animation storyboard planning.
- A browser-viewable HTML storyboard preview.
- Optional `ffprobe` based clip metadata extraction.
- A working CLI and standard-library test suite.

Actual frame rendering, character rigs and effects compositing are later milestones. See [docs/analyse.md](docs/analyse.md) and [docs/architecture.md](docs/architecture.md).

## Working with Codex

For the permanent GitHub connection, Codex Cloud environment setup, required reading order, daily development workflow and troubleshooting steps, see [isAkis.md](isAkis.md).

## Requirements

- Python 3.10+
- FFmpeg/`ffprobe` only for the `probe` command
- No GPU dependency for the current milestone

## Setup

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install -e .
```

## Quick start

Validate the included football reference bundle:

```bash
python -m vtaa validate examples/football_shot.reference.json
```

Create an anime storyboard plan:

```bash
python -m vtaa plan examples/football_shot.reference.json -o build/football_shot.storyboard.json
```

Create a visual HTML preview:

```bash
python -m vtaa preview examples/football_shot.reference.json -o build/football_shot.storyboard.html
```

Create an empty analysis template from a CapCut-exported clip:

```bash
python -m vtaa probe input/my_highlight.mp4 --sport football -o build/my_highlight.reference.json
```

The template is then populated by a sport analyzer such as FootballAnalysisAI or, during development, by a manually prepared test fixture.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Repository structure

```text
src/vtaa/
  adapters/       Sport-specific event-to-animation rules
  cli.py          Command-line interface
  models.py       Versioned reference and storyboard contracts
  planner.py      Shared storyboard planner
  preview.py      HTML storyboard preview
  probe.py        ffprobe integration
docs/             Permanent decisions, architecture and integration contract
examples/         Small text-only reference fixtures
tests/            Unit and CLI tests
```

## Licensing

No project license has been selected yet. Third-party models and assets must be reviewed independently before commercial use.
