from __future__ import annotations

from ..models import Event, ReferenceBundle
from .base import ShotRecipe


class FootballAdapter:
    sport = "football"

    def recipes_for(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]:
        handlers = {
            "shot": self._shot,
            "pass": self._pass,
            "dribble": self._dribble,
            "save": self._save,
        }
        return handlers.get(event.type, self._generic)(event, bundle)

    def _shot(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]:
        profile = bundle.anime_profile
        return (
            ShotRecipe(
                "establish",
                0.00,
                0.24,
                "wide_reference",
                1,
                "follow_source_camera",
                ("clean_cel_background", "subtle_telestration"),
                "Preserve the real tactical setup before exaggeration.",
                {},
            ),
            ShotRecipe(
                "anticipation",
                0.20,
                0.43,
                "hero_close_up",
                3,
                "fast_push_in",
                ("eye_highlight", "wind_lines", "background_drop"),
                "Signal the actor's decision and build anticipation.",
                {"speed_multiplier": profile.speed_multiplier},
            ),
            ShotRecipe(
                "launch",
                0.39,
                0.65,
                "dynamic_full_body",
                3,
                "vertical_tracking",
                ("speed_lines", "grass_particles", "energy_gather"),
                "Turn the real preparation motion into an impossible athletic action.",
                {
                    "jump_multiplier": profile.jump_multiplier,
                    "speed_multiplier": profile.speed_multiplier,
                },
            ),
            ShotRecipe(
                "impact",
                0.61,
                0.79,
                "impact_insert",
                3,
                "impact_shake_then_hold",
                ("impact_frame", "white_flash", "ball_energy_trail", "shockwave"),
                "Emphasize contact while preserving the real ball destination.",
                {"impact_multiplier": profile.impact_multiplier, "hold_frames": 2},
            ),
            ShotRecipe(
                "outcome",
                0.76,
                1.00,
                "outcome_tracking",
                2,
                "track_ball_then_reveal",
                ("energy_decay", "result_accent"),
                "Return to the verified event outcome and prepare analysis overlay.",
                {"preserve_reference_outcome": True},
            ),
        )

    def _pass(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]:
        profile = bundle.anime_profile
        return (
            ShotRecipe(
                "read",
                0.00,
                0.28,
                "tactical_wide",
                1,
                "source_pan",
                ("passing_lane_hint",),
                "Show the real passing context.",
                {},
            ),
            ShotRecipe(
                "decision",
                0.23,
                0.48,
                "actor_medium",
                2,
                "push_to_actor",
                ("focus_vignette", "eye_line"),
                "Clarify the passer's decision.",
                {"speed_multiplier": profile.speed_multiplier},
            ),
            ShotRecipe(
                "flight",
                0.43,
                0.80,
                "ball_trajectory",
                2,
                "track_ball",
                ("ball_trail", "speed_lines"),
                "Stylize but preserve the measured ball path.",
                {"preserve_reference_trajectory": True},
            ),
            ShotRecipe(
                "receive",
                0.76,
                1.00,
                "receiver_reveal",
                2,
                "reveal_target",
                ("reception_accent",),
                "Land on the verified receiver or outcome.",
                {"preserve_reference_outcome": True},
            ),
        )

    def _dribble(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]:
        profile = bundle.anime_profile
        return (
            ShotRecipe(
                "setup",
                0.00,
                0.24,
                "duel_wide",
                1,
                "source_camera",
                ("duel_focus",),
                "Establish attacker and defender positions.",
                {},
            ),
            ShotRecipe(
                "feint",
                0.20,
                0.49,
                "feet_insert",
                3,
                "snap_pan",
                ("afterimage", "grass_particles"),
                "Exaggerate the directional fake.",
                {"speed_multiplier": profile.speed_multiplier},
            ),
            ShotRecipe(
                "burst",
                0.45,
                0.80,
                "runner_profile",
                3,
                "speed_tracking",
                ("speed_tunnel", "multiple_afterimages"),
                "Create the fantasy acceleration beat.",
                {"speed_multiplier": profile.speed_multiplier},
            ),
            ShotRecipe(
                "exit",
                0.76,
                1.00,
                "wide_resolution",
                2,
                "ease_to_source",
                ("speed_decay",),
                "Reconnect the fantasy beat to the real next action.",
                {"preserve_reference_outcome": True},
            ),
        )

    def _save(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]:
        profile = bundle.anime_profile
        return (
            ShotRecipe(
                "threat",
                0.00,
                0.27,
                "goal_wide",
                1,
                "source_camera",
                ("goal_target",),
                "Establish the verified shot threat.",
                {},
            ),
            ShotRecipe(
                "keeper_read",
                0.22,
                0.48,
                "keeper_close_up",
                3,
                "fast_push_in",
                ("eye_highlight", "time_slow"),
                "Show the goalkeeper reading the trajectory.",
                {},
            ),
            ShotRecipe(
                "dive",
                0.43,
                0.79,
                "keeper_full_body",
                3,
                "arc_tracking",
                ("air_streak", "glove_energy", "impact_frame"),
                "Exaggerate reach without changing the save result.",
                {
                    "jump_multiplier": profile.jump_multiplier,
                    "impact_multiplier": profile.impact_multiplier,
                },
            ),
            ShotRecipe(
                "resolution",
                0.75,
                1.00,
                "save_resolution",
                2,
                "settle_and_reveal",
                ("shockwave_decay", "result_accent"),
                "Preserve the verified save and transition to analysis.",
                {"preserve_reference_outcome": True},
            ),
        )

    def _generic(self, event: Event, bundle: ReferenceBundle) -> tuple[ShotRecipe, ...]:
        return (
            ShotRecipe(
                "context",
                0.00,
                0.34,
                "wide_reference",
                1,
                "follow_source_camera",
                ("clean_cel_background",),
                "Preserve event context.",
                {},
            ),
            ShotRecipe(
                "action",
                0.28,
                0.76,
                "dynamic_action",
                2,
                "track_primary_actor",
                ("speed_lines",),
                "Stylize the primary action.",
                {"speed_multiplier": bundle.anime_profile.speed_multiplier},
            ),
            ShotRecipe(
                "result",
                0.71,
                1.00,
                "wide_resolution",
                1,
                "return_to_source",
                ("result_accent",),
                "Preserve the verified outcome.",
                {"preserve_reference_outcome": True},
            ),
        )

