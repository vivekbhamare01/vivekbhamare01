"""Fetch public GitHub contribution data using the GraphQL API."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "vivekbhamare01"
GRAPHQL_URL = "https://api.github.com/graphql"
QUERY = """
query ProfileContributions($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to, includePrivate: false) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""
LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


class ContributionFetchError(Exception):
    """Raised when GitHub returns an unusable contribution response."""


def _month_start(month: date, offset: int) -> date:
    month_index = month.year * 12 + month.month - 1 + offset
    return date(month_index // 12, month_index % 12 + 1, 1)


def _unavailable(message: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "available": False,
        "username": USERNAME,
        "fetchedAt": None,
        "periodStart": None,
        "periodEnd": None,
        "totalContributions": None,
        "months": [],
        "days": [],
        "message": message,
    }


def _fetch_calendar(token: str, start: date, end: date) -> dict[str, Any]:
    variables = {
        "login": USERNAME,
        "from": f"{start.isoformat()}T00:00:00Z",
        "to": f"{end.isoformat()}T23:59:59Z",
    }
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps({"query": QUERY, "variables": variables}).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "vivekbhamare01-profile-readme",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ContributionFetchError("GitHub returned an invalid response.")
    if payload.get("errors"):
        raise ContributionFetchError("GitHub GraphQL reported an error.")
    try:
        calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except (KeyError, TypeError) as error:
        raise ContributionFetchError("GitHub returned no contribution calendar.") from error
    if not isinstance(calendar, dict) or not isinstance(calendar.get("weeks"), list):
        raise ContributionFetchError("GitHub returned an invalid contribution calendar.")
    return calendar


def _build_data(calendar: dict[str, Any], start: date, end: date) -> dict[str, Any]:
    monthly_counts: defaultdict[str, int] = defaultdict(int)
    days: list[dict[str, Any]] = []
    for week in calendar["weeks"]:
        for entry in week.get("contributionDays", []):
            day = date.fromisoformat(entry["date"])
            if not start <= day <= end:
                continue
            count = int(entry["contributionCount"])
            level_name = entry["contributionLevel"]
            if level_name not in LEVELS:
                raise ContributionFetchError("GitHub returned an unknown contribution level.")
            days.append({
                "date": day.isoformat(),
                "contributions": count,
                "level": LEVELS[level_name],
            })
            monthly_counts[day.strftime("%Y-%m")] += count

    if len(days) != (end - start).days + 1:
        raise ContributionFetchError("GitHub returned an incomplete contribution calendar.")
    months: list[dict[str, Any]] = []
    for offset in range(12):
        month = _month_start(end.replace(day=1), offset - 11)
        key = month.strftime("%Y-%m")
        months.append({"month": key, "contributions": monthly_counts[key]})

    return {
        "schemaVersion": 1,
        "available": True,
        "username": USERNAME,
        "fetchedAt": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "periodStart": start.isoformat(),
        "periodEnd": end.isoformat(),
        "totalContributions": int(calendar["totalContributions"]),
        "months": months,
        "days": days,
        "message": None,
    }


def _write_data(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def main() -> int:
    output_path = ROOT / "data" / "contributions.json"
    token = os.environ.get("GH_TOKEN", "").strip()
    if not token:
        _write_data(
            output_path,
            _unavailable("Add GH_TOKEN as a repository Actions secret to enable contribution data."),
        )
        print("GH_TOKEN is not set; contribution cards will show the unavailable-data fallback.")
        return 0

    today = date.today()
    start = _month_start(today.replace(day=1), -11)
    try:
        calendar = _fetch_calendar(token, start, today)
        result = _build_data(calendar, start, today)
    except (
        ContributionFetchError,
        urllib.error.URLError,
        TimeoutError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        _write_data(
            output_path,
            _unavailable("GitHub contribution data could not be fetched right now."),
        )
        print(f"Contribution refresh failed ({type(error).__name__}); using the unavailable-data fallback.", file=sys.stderr)
        return 0

    _write_data(output_path, result)
    print(
        f"Fetched {result['totalContributions']} contributions "
        f"for {USERNAME} ({result['periodStart']} to {result['periodEnd']})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
