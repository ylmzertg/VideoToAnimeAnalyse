import tempfile
import unittest
from pathlib import Path

from vtaa.cli import main


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "football_shot.reference.json"


class CLITests(unittest.TestCase):
    def test_validate_command(self):
        self.assertEqual(main(["validate", str(EXAMPLE)]), 0)

    def test_plan_and_preview_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            storyboard_path = output_dir / "storyboard.json"
            preview_path = output_dir / "storyboard.html"
            self.assertEqual(main(["plan", str(EXAMPLE), "-o", str(storyboard_path)]), 0)
            self.assertEqual(main(["preview", str(EXAMPLE), "-o", str(preview_path)]), 0)
            self.assertTrue(storyboard_path.exists())
            html_text = preview_path.read_text(encoding="utf-8")
            self.assertIn("Anime Storyboard", html_text)
            self.assertIn("dynamic_full_body", html_text)


if __name__ == "__main__":
    unittest.main()

