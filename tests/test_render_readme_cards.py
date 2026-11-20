import json
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from scripts.render_readme_cards import render_all


class RenderReadmeCardsTests(unittest.TestCase):
    def test_generates_all_six_valid_static_cards_without_contribution_data(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "data").mkdir()
            (root / "data" / "contributions.json").write_text(
                json.dumps({"available": False, "months": [], "days": []}),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"STATIC": "1"}):
                generated = render_all(root=root)

            self.assertEqual(
                {path.name for path in generated},
                {
                    "hero.svg",
                    "build.svg",
                    "data.svg",
                    "learn.svg",
                    "activity.svg",
                    "heatmap.svg",
                },
            )
            for path in generated:
                root_svg = ET.parse(path).getroot()
                self.assertEqual(root_svg.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertIn("animation: none", path.read_text(encoding="utf-8"))

            card_text = {
                path.name: " ".join(ET.parse(path).getroot().itertext())
                for path in generated
            }
            required_items = {
                "hero.svg": (
                    "HELLO, I'M",
                    "VIVEK BHAMARE",
                    "BCA Student",
                    "Interested in software development & data analytics.",
                ),
                "build.svg": ("Java", "Python", "C", "PHP", "HTML", "CSS", "JavaScript"),
                "data.svg": (
                    "SQL", "MySQL", "MongoDB", "Power BI", "Excel", "Python",
                    "Pandas", "NumPy", "Matplotlib", "R", "Tableau",
                ),
                "learn.svg": (
                    "Data Science", "Machine Learning", "Artificial Intelligence",
                    "Deep Learning", "Data Structures & Algorithms", "Statistics",
                    "Git", "GitHub", "Docker", "REST API",
                ),
            }
            for filename, items in required_items.items():
                with self.subTest(filename=filename):
                    for item in items:
                        self.assertIn(item, card_text[filename])

            activity = (root / "cards" / "activity.svg").read_text(encoding="utf-8")
            self.assertIn("No placeholder or estimated statistics are shown.", activity)
            learn = (root / "cards" / "learn.svg").read_text(encoding="utf-8")
            self.assertIn("NOT EXPERTISE", learn)

    def test_animated_mode_includes_reduced_motion_support(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "data").mkdir()
            (root / "data" / "contributions.json").write_text(
                json.dumps({"available": False, "months": [], "days": []}),
                encoding="utf-8",
            )

            render_all(root=root, static_mode=False)

            hero = (root / "cards" / "hero.svg").read_text(encoding="utf-8")
            self.assertIn("@media (prefers-reduced-motion: reduce)", hero)
            self.assertIn("@keyframes rise", hero)


if __name__ == "__main__":
    unittest.main()
