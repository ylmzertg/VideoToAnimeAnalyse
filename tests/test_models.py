import copy
import json
import unittest
from pathlib import Path

from vtaa.errors import ValidationError
from vtaa.models import ReferenceBundle


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "football_shot.reference.json"


class ReferenceBundleTests(unittest.TestCase):
    def load_data(self):
        return json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_bundle_is_valid(self):
        bundle = ReferenceBundle.from_dict(self.load_data())
        self.assertEqual(bundle.sport, "football")
        self.assertEqual(len(bundle.entities), 3)
        self.assertEqual(bundle.events[0].type, "shot")
        self.assertAlmostEqual(bundle.source.duration_seconds, 9.0)

    def test_unknown_event_entity_is_rejected(self):
        data = copy.deepcopy(self.load_data())
        data["events"][0]["actor_ids"] = ["missing_player"]
        with self.assertRaisesRegex(ValidationError, "unknown entities"):
            ReferenceBundle.from_dict(data)

    def test_invalid_event_timing_is_rejected(self):
        data = copy.deepcopy(self.load_data())
        data["events"][0]["impact_frame"] = 200
        with self.assertRaisesRegex(ValidationError, "start_frame <= impact_frame <= end_frame"):
            ReferenceBundle.from_dict(data)

    def test_out_of_range_track_point_is_rejected(self):
        data = copy.deepcopy(self.load_data())
        data["tracks"][0]["points"][0]["x"] = 1.2
        with self.assertRaisesRegex(ValidationError, "between 0 and 1"):
            ReferenceBundle.from_dict(data)


if __name__ == "__main__":
    unittest.main()

