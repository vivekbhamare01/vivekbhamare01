"""Generate the SVG cards used by the GitHub profile README."""

from __future__ import annotations

import json
import os
import textwrap
from datetime import date
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PAPER = "#F5F1E8"
INK = "#222222"
BLUE = "#2563EB"
RED = "#E85D5D"
YELLOW = "#EAB308"
MUTED = "#69665F"

TECH_CARDS = (
    {
        "filename": "build.svg",
        "title": "BUILD",
        "subtitle": "LANGUAGES & WEB",
        "accent": BLUE,
        "items": ("Java", "Python", "C", "PHP", "HTML", "CSS", "JavaScript"),
    },
    {
        "filename": "data.svg",
        "title": "DATA",
        "subtitle": "DATA TOOLKIT",
        "accent": RED,
        "items": (
            "SQL",
            "MySQL",
            "MongoDB",
            "Power BI",
            "Excel",
            "Python",
            "Pandas",
            "NumPy",
            "Matplotlib",
            "R",
            "Tableau",
        ),
    },
    {
        "filename": "learn.svg",
        "title": "LEARN",
        "subtitle": "CURRENTLY LEARNING",
        "accent": YELLOW,
        "items": (
            "Data Science",
            "Machine Learning",
            "Artificial Intelligence",
            "Deep Learning",
            "Data Structures & Algorithms",
            "Statistics",
            "Git",
            "GitHub",
            "Docker",
            "REST API",
        ),
    },
)


def _text(x: int, y: int, value: str, *, size: int = 16, fill: str = INK,
          weight: int | str = 400, class_name: str = "") -> str:
    css_class = f' class="{class_name}"' if class_name else ""
    return (
        f'<text x="{x}" y="{y}" font-family="Inter, ui-sans-serif, '
        f'system-ui, sans-serif" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}"{css_class}>{escape(value)}</text>'
    )


def _document(title: str, description: str, width: int, height: int,
              content: str, static_mode: bool) -> str:
    animation_rules = textwrap.dedent(
        """
        .enter { animation: rise .75s cubic-bezier(.2,.7,.2,1) both; }
        .enter-2 { animation-delay: .12s; }
        .enter-3 { animation-delay: .24s; }
        .drift { animation: drift 5s ease-in-out infinite alternate; }
        .orbit { transform-box: fill-box; transform-origin: center; animation: orbit 16s linear infinite; }
        @keyframes rise {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes drift {
            from { transform: translateY(-4px); }
            to { transform: translateY(5px); }
        }
        @keyframes orbit { to { transform: rotate(360deg); } }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation: none !important; }
        }
        """
        if not static_mode
        else """
        .enter, .enter-2, .enter-3, .drift, .orbit { animation: none !important; }
        """
    ).strip()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
  <title id="title">{escape(title)}</title>
  <desc id="description">{escape(description)}</desc>
  <style>
    text {{ text-rendering: geometricPrecision; }}
{animation_rules}
</style>
{content}
</svg>
"""


def _card_base(width: int, height: int, accent: str, label: str) -> str:
    return f"""
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="22" fill="{PAPER}" stroke="#D8D2C5" stroke-width="1.5"/>
  <path d="M24 24h34" stroke="{accent}" stroke-width="4" stroke-linecap="round"/>
  <circle cx="{width - 38}" cy="38" r="13" fill="none" stroke="{accent}" stroke-width="1.5" opacity=".65" class="orbit"/>
  <circle cx="{width - 38}" cy="38" r="3" fill="{accent}" class="drift"/>
  {_text(24, height - 19, label.upper(), size=10, fill=MUTED, weight=600)}
"""


def _hero(static_mode: bool) -> str:
    content = f"""
  <rect x="1" y="1" width="1198" height="398" rx="26" fill="{PAPER}" stroke="#D8D2C5" stroke-width="1.5"/>
  <path d="M54 52h44" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>
  <g class="enter">
    {_text(58, 112, "HELLO, I'M", size=19, fill=BLUE, weight=700)}
  </g>
  <g class="enter enter-2">
    <text x="54" y="202" font-family="Georgia, 'Times New Roman', serif" font-size="76" font-weight="700" letter-spacing="-2" fill="{INK}">VIVEK BHAMARE</text>
  </g>
  <g class="enter enter-3">
    {_text(58, 250, "BCA Student  /  Aspiring Data Scientist", size=20, fill=INK, weight=500)}
    {_text(58, 289, "Interested in software development & data analytics.", size=16, fill=MUTED)}
    {_text(58, 345, "MAHARASHTRA, INDIA", size=11, fill=MUTED, weight=600)}
  </g>
  <g transform="translate(900 198)">
    <circle r="106" fill="none" stroke="#D8D2C5" stroke-width="1"/>
    <circle r="78" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="3 9" opacity=".62" class="orbit"/>
    <circle r="50" fill="{BLUE}" opacity=".08"/>
    <path d="M-50 0h100M0-50v100" stroke="#D8D2C5" stroke-width="1"/>
    <circle cx="-106" cy="-34" r="7" fill="{RED}" class="drift"/>
    <circle cx="69" cy="-78" r="6" fill="{YELLOW}" class="drift"/>
    <circle cx="82" cy="69" r="5" fill="{BLUE}" class="drift"/>
    <circle r="13" fill="{BLUE}" opacity=".88"/>
    <circle cx="-28" cy="25" r="8" fill="{RED}" opacity=".9"/>
    <circle cx="30" cy="-24" r="6" fill="{YELLOW}"/>
  </g>
  <path d="M54 370h1090" stroke="#D8D2C5" stroke-width="1"/>
  <text x="1144" y="390" text-anchor="end" font-family="ui-monospace, monospace" font-size="10" fill="{MUTED}">01 / PROFILE</text>
"""
    return _document(
        "Vivek Bhamare — GitHub profile",
        "Animated introduction: BCA student and aspiring data scientist from Maharashtra, India.",
        1200,
        400,
        content,
        static_mode,
    )


def _technology_card(card: dict[str, Any], static_mode: bool) -> str:
    width, height = 480, 340
    footer = (
        "LEARNING IN PROGRESS - NOT EXPERTISE"
        if card["title"] == "LEARN"
        else "TOOLS & LANGUAGES"
    )
    content = _card_base(width, height, card["accent"], footer)
    content += _text(24, 76, card["title"], size=31, weight=700, class_name="enter")
    content += _text(24, 101, card["subtitle"], size=10, fill=MUTED, weight=600)
    items: tuple[str, ...] = card["items"]
    row_count = (len(items) + 1) // 2
    for index, item in enumerate(items):
        column, row = divmod(index, row_count)
        x = 26 + column * 222
        y = 142 + row * 30
        content += (
            f'<circle cx="{x}" cy="{y - 5}" r="3" fill="{card["accent"]}" opacity=".85"/>'
            + _text(x + 13, y, item, size=13, fill=INK, class_name="enter")
        )
    return _document(
        f'{card["title"]} — Vivek Bhamare',
        f'{card["subtitle"]}: {", ".join(items)}.',
        width,
        height,
        content,
        static_mode,
    )


def _load_contributions(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False, "months": [], "days": [], "totalContributions": None}
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict) or not isinstance(payload.get("available"), bool):
        raise ValueError(f"{path} must contain a JSON object with an 'available' boolean.")
    if payload["available"]:
        if not isinstance(payload.get("months"), list) or not isinstance(payload.get("days"), list):
            raise ValueError(f"{path} must contain 'months' and 'days' arrays when available.")
    return payload


def _activity(data: dict[str, Any], static_mode: bool) -> str:
    width, height = 960, 340
    content = _card_base(width, height, BLUE, "MONTHLY CONTRIBUTIONS")
    content += _text(26, 73, "ACTIVITY", size=26, weight=700, class_name="enter")
    if not data.get("available"):
        content += _text(26, 139, "GitHub contribution data is currently unavailable.", size=18, fill=INK)
        content += _text(26, 174, "Configure GH_TOKEN; the scheduled workflow will retry.", size=14, fill=MUTED)
        content += _text(26, 222, "No placeholder or estimated statistics are shown.", size=12, fill=MUTED)
        return _document(
            "Monthly GitHub contribution activity",
            "Real monthly contribution activity will appear after GitHub access is configured.",
            width,
            height,
            content,
            static_mode,
        )

    total = data.get("totalContributions")
    total_label = f"{total:,} contributions in the last 12 months" if isinstance(total, int) else "Contribution activity"
    content += _text(26, 101, total_label, size=13, fill=MUTED)
    months = data["months"]
    counts = [month["contributions"] for month in months]
    max_count = max(counts, default=0) or 1
    baseline = 263
    for index, month in enumerate(months[-12:]):
        x = 62 + index * 73
        bar_height = max(3, round(112 * month["contributions"] / max_count)) if month["contributions"] else 3
        content += f'<rect x="{x + 14}" y="{baseline - bar_height}" width="28" height="{bar_height}" rx="5" fill="{BLUE}" opacity=".78" class="enter"/>'
        content += _text(x + 28, baseline - bar_height - 9, str(month["contributions"]), size=10, fill=MUTED, class_name="enter")
        content += _text(x + 28, baseline + 21, month["month"][-3:], size=10, fill=MUTED)
    content += f'<path d="M48 {baseline}h864" stroke="#D8D2C5" stroke-width="1"/>'
    return _document(
        "Monthly GitHub contribution activity",
        f"Verified monthly contribution counts for the last 12 months. {total_label}.",
        width,
        height,
        content,
        static_mode,
    )


def _heatmap(data: dict[str, Any], static_mode: bool) -> str:
    width, height = 1080, 220
    content = _card_base(width, height, RED, "CONTRIBUTION CALENDAR")
    content += _text(26, 73, "A YEAR IN CONTRIBUTIONS", size=25, weight=700, class_name="enter")
    if not data.get("available"):
        content += _text(26, 127, "The contribution calendar is currently unavailable.", size=14, fill=MUTED)
        content += _text(26, 156, "No activity is invented or estimated.", size=12, fill=MUTED)
        return _document(
            "GitHub contribution calendar",
            "The contribution calendar is unavailable until GitHub access is configured.",
            width,
            height,
            content,
            static_mode,
        )

    days_by_date: dict[date, dict[str, Any]] = {}
    for entry in data["days"]:
        day = date.fromisoformat(entry["date"])
        days_by_date[day] = entry
    if not days_by_date:
        content += _text(26, 127, "No contribution days were returned for this period.", size=14, fill=MUTED)
    else:
        first_day = min(days_by_date)
        first_sunday = date.fromordinal(first_day.toordinal() - (first_day.weekday() + 1) % 7)
        grid_x, grid_y, cell, gap = 141, 91, 11, 4
        month_labels: set[str] = set()
        for day, entry in days_by_date.items():
            week = (day - first_sunday).days // 7
            weekday = (day.weekday() + 1) % 7
            x = grid_x + week * (cell + gap)
            y = grid_y + weekday * (cell + gap)
            month_key = day.strftime("%Y-%m")
            if day.day <= 7 and month_key not in month_labels:
                content += _text(x, 83, day.strftime("%b"), size=9, fill=MUTED)
                month_labels.add(month_key)
            level = max(0, min(4, int(entry.get("level", 0))))
            colors = ("#E4DFD4", "#F8B5AD", "#F28B80", RED, "#A92F2F")
            content += (
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
                f'fill="{colors[level]}" aria-label="{day.isoformat()}: '
                f'{int(entry.get("contributions", 0))} contributions"/>'
            )
    content += _text(141, 202, "LESS", size=9, fill=MUTED)
    for index, color in enumerate(("#E4DFD4", "#F8B5AD", "#F28B80", RED, "#A92F2F")):
        content += f'<rect x="{177 + index * 17}" y="192" width="11" height="11" rx="2" fill="{color}"/>'
    content += _text(270, 202, "MORE", size=9, fill=MUTED)
    total = data.get("totalContributions")
    if isinstance(total, int):
        content += _text(1054, 73, f"{total:,} total", size=11, fill=MUTED, weight=600)
    return _document(
        "GitHub contribution calendar",
        "Daily GitHub contributions over the last 12 months, represented by activity intensity.",
        width,
        height,
        content,
        static_mode,
    )


def render_all(*, root: Path = ROOT, static_mode: bool | None = None) -> list[Path]:
    """Generate every card under root/cards and return the generated paths."""
    if static_mode is None:
        static_mode = os.environ.get("STATIC") == "1"
    cards_dir = root / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    contributions = _load_contributions(root / "data" / "contributions.json")
    documents = {
        "hero.svg": _hero(static_mode),
        "activity.svg": _activity(contributions, static_mode),
        "heatmap.svg": _heatmap(contributions, static_mode),
    }
    documents.update({
        card["filename"]: _technology_card(card, static_mode)
        for card in TECH_CARDS
    })
    generated: list[Path] = []
    for filename, svg in documents.items():
        path = cards_dir / filename
        path.write_text(svg, encoding="utf-8")
        generated.append(path)
    return generated


if __name__ == "__main__":
    files = render_all()
    mode = "static" if os.environ.get("STATIC") == "1" else "animated"
    print(f"Generated {len(files)} SVG cards ({mode} mode).")
