import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
import urllib.error

from scripts import fetch_contributions
from scripts.fetch_contributions import _build_data


class FetchContributionsTests(unittest.TestCase):
    def test_builds_real_daily_and_monthly_totals(self) -> None:
        calendar = {
            "totalContributions": 5,
            "weeks": [
                {
                    "contributionDays": [
                        {
                            "date": "2025-11-30",
                            "contributionCount": 2,
                            "contributionLevel": "SECOND_QUARTILE",
                        },
                        {
                            "date": "2025-12-01",
                            "contributionCount": 3,
                            "contributionLevel": "THIRD_QUARTILE",
                        },
                    ],
                },
            ],
        }

        result = _build_data(calendar, date(2025, 11, 30), date(2025, 12, 1))

        self.assertTrue(result["available"])
        self.assertEqual(result["totalContributions"], 5)
        self.assertEqual(len(result["months"]), 12)
        self.assertEqual(
            result["months"][-2:],
            [
                {"month": "2025-11", "contributions": 2},
                {"month": "2025-12", "contributions": 3},
            ],
        )
        self.assertEqual([entry["level"] for entry in result["days"]], [2, 3])

    def test_api_failure_writes_a_graceful_unavailable_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = io.StringIO()
            with (
                patch.object(fetch_contributions, "ROOT", root),
                patch.dict("os.environ", {"GH_TOKEN": "test-token"}),
                patch.object(
                    fetch_contributions,
                    "_fetch_calendar",
                    side_effect=urllib.error.URLError("offline"),
                ),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(output),
            ):
                result = fetch_contributions.main()

            payload = json.loads((root / "data" / "contributions.json").read_text(encoding="utf-8"))
            self.assertEqual(result, 0)
            self.assertFalse(payload["available"])
            self.assertIsNone(payload["totalContributions"])
            self.assertNotIn("test-token", output.getvalue())


if __name__ == "__main__":
    unittest.main()
