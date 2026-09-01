import unittest
from pathlib import Path

from vtaa.planner import build_storyboard
from vtaa.project_io import load_reference_bundle


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "football_shot.reference.json"


class StoryboardPlannerTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_reference_bundle(EXAMPLE)
        self.storyboard = build_storyboard(self.bundle)

    def test_shot_event_creates_five_planned_shots(self):
        self.assertEqual(len(self.storyboard.shots), 5)
        self.assertEqual(
            [shot.treatment_level for shot in self.storyboard.shots],
            [1, 3, 3, 3, 2],
        )

    def test_fantasy_motion_and_verified_outcome_are_both_present(self):
        launch = next(shot for shot in self.storyboard.shots if shot.shot_type == "dynamic_full_body")
        outcome = next(shot for shot in self.storyboard.shots if shot.shot_type == "outcome_tracking")
        self.assertEqual(launch.motion["jump_multiplier"], 7.0)
        self.assertTrue(outcome.motion["preserve_reference_outcome"])

    def test_all_shots_remain_inside_event_range(self):
        event = self.bundle.events[0]
        for shot in self.storyboard.shots:
            self.assertGreaterEqual(shot.start_frame, event.start_frame)
            self.assertLessEqual(shot.end_frame, event.end_frame)
            self.assertLessEqual(shot.start_frame, shot.end_frame)


if __name__ == "__main__":
    unittest.main()

