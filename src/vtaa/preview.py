from __future__ import annotations

import html
import json
from pathlib import Path

from .models import Storyboard


def _shot_card(storyboard: Storyboard, index: int) -> str:
    shot = storyboard.shots[index]
    fps = storyboard.source.fps
    start_seconds = shot.start_frame / fps
    end_seconds = shot.end_frame / fps
    effects = "".join(f"<li>{html.escape(effect)}</li>" for effect in shot.effects)
    motion = html.escape(json.dumps(shot.motion, ensure_ascii=False, indent=2))
    subjects = ", ".join(html.escape(item) for item in shot.subjects)
    return f"""
    <article class="shot level-{shot.treatment_level}">
      <div class="shot-index">{index + 1:02d}</div>
      <div class="shot-main">
        <div class="shot-header">
          <h2>{html.escape(shot.shot_type)}</h2>
          <span class="level">Level {shot.treatment_level}</span>
        </div>
        <p class="time">Frames {shot.start_frame}–{shot.end_frame} · {start_seconds:.2f}s–{end_seconds:.2f}s</p>
        <p>{html.escape(shot.purpose)}</p>
        <div class="grid">
          <div><strong>Event</strong><br>{html.escape(shot.event_id)}</div>
          <div><strong>Subjects</strong><br>{subjects}</div>
          <div><strong>Camera</strong><br>{html.escape(shot.camera)}</div>
        </div>
        <details><summary>Effects and motion</summary><ul>{effects}</ul><pre>{motion}</pre></details>
      </div>
    </article>
    """


def render_storyboard_html(storyboard: Storyboard) -> str:
    cards = "\n".join(_shot_card(storyboard, index) for index in range(len(storyboard.shots)))
    title = html.escape(storyboard.project_id)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Anime Storyboard</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, system-ui, sans-serif; }}
    body {{ margin: 0; background: #0b1020; color: #e8edf8; }}
    header {{ padding: 42px max(24px, 8vw); background: linear-gradient(135deg,#111936,#132849); }}
    header h1 {{ margin: 0 0 8px; font-size: clamp(28px,5vw,54px); }}
    header p {{ color: #aebbd2; margin: 6px 0; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 64px; }}
    .shot {{ display: grid; grid-template-columns: 64px 1fr; gap: 18px; margin: 18px 0; padding: 20px;
      background: #121a2d; border: 1px solid #293550; border-left: 5px solid #4d7cff; border-radius: 14px; }}
    .level-2 {{ border-left-color: #16c79a; }} .level-3 {{ border-left-color: #ff5f6d; }}
    .shot-index {{ font-size: 30px; font-weight: 800; color: #65789d; }}
    .shot-header {{ display: flex; align-items: center; justify-content: space-between; gap: 15px; }}
    h2 {{ margin: 0; text-transform: capitalize; }}
    .level {{ padding: 5px 10px; border-radius: 999px; background: #202c45; white-space: nowrap; }}
    .time {{ color: #8fa3c7; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; margin: 18px 0; }}
    .grid div {{ background: #0c1425; padding: 12px; border-radius: 8px; }}
    details {{ color: #b8c6de; }} pre {{ overflow: auto; background: #080d18; padding: 12px; border-radius: 8px; }}
    @media (max-width: 680px) {{ .shot {{ grid-template-columns: 1fr; }} .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p>{html.escape(storyboard.sport.title())} · {len(storyboard.shots)} planned shots · {storyboard.anime_profile.visual_language}</p>
    <p>Source: {storyboard.source.width}×{storyboard.source.height} @ {storyboard.source.fps:g} FPS</p>
  </header>
  <main>{cards}</main>
</body>
</html>
"""


def write_storyboard_html(path: str | Path, storyboard: Storyboard) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_storyboard_html(storyboard), encoding="utf-8")
    return output_path

