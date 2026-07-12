#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "publications.json"
INDEX_PATH = ROOT / "index.html"
CV_PATH = ROOT / "cv.qmd"

CV_EMPLOYMENT = [
    ("2023-present", "Associate Professor, Keio University"),
    ("2021-2023", "Tenure-Track Associate Professor, Graduate School of Economics, Kobe University"),
    ("2019-2021", "Assistant Professor, Graduate School of Economics, Hitotsubashi University"),
]

CV_VISITING_POSITIONS = [
    ("2024", "Visiting Fellow, European University Institute"),
]

CV_EDUCATION = [
    ("2019", "Ph.D. Economics, Princeton University (advisor: Richard Rogerson)"),
    ("2013", "M.A. Economics, University of Tokyo"),
    ("2011", "B.A. Economics, University of Tokyo"),
]

CV_CONFERENCE_PRESENTATIONS = [
    "Society for Economic Dynamics 2022",
    "Seventh Annual CIGS End of Year Macroeconomics Conference 2022",
    "European Winter Meetings of the Econometric Society 2022",
    "European Winter Meetings of the Econometric Society, Winter School 2020",
    "15th Annual Conference Warsaw International Economic Meeting 2020",
    "CIGS Conference on Macroeconomic Theory and Policy 2019",
]

CV_REFEREEING_SERVICES = [
    "American Economic Journal: Macroeconomics",
    "Review of Economic Dynamics",
    "International Economic Review",
    "The B.E. Journal of Macroeconomics",
    "Journal of the Japanese and International Economies",
    "Japanese Economic Review",
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def article(item: dict[str, str]) -> str:
    title = esc(item["title"])
    url = esc(item.get("url", "#"))
    year = esc(item.get("year", ""))
    venue = item.get("venue")
    authors = item.get("authors")

    meta = year
    if venue:
        meta = f"{year}, <em>{esc(venue)}</em>"

    lines = [
        '          <article class="publication">',
        "            <h3>",
        f'              <a href="{url}" target="_blank" rel="noreferrer">{title}</a>',
        "            </h3>",
    ]
    if meta:
        lines.append(f'            <p class="pub-meta">{meta}</p>')
    if authors:
        lines.append(f"            <p>{esc(authors)}</p>")
    lines.append("          </article>")
    return "\n".join(lines)


def in_progress_article(item: dict[str, str]) -> str:
    lines = [
        '          <article class="publication">',
        f"            <h3>{esc(item['title'])}</h3>",
    ]
    if item.get("authors"):
        lines.append(f"            <p>{esc(item['authors'])}</p>")
    lines.append("          </article>")
    return "\n".join(lines)


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    start_index = text.index(start) + len(start)
    end_index = text.index(end, start_index)
    end_line_start = text.rfind("\n", 0, end_index) + 1
    end_indent = text[end_line_start:end_index]
    return text[:start_index] + "\n" + replacement + "\n" + end_indent + text[end_index:]


def render_index(data: dict[str, list[dict[str, str]]]) -> None:
    index = INDEX_PATH.read_text()
    working = "\n\n".join(article(item) for item in data["working_papers"])
    publications = "\n\n".join(article(item) for item in data["publications"])
    in_progress = "\n\n".join(in_progress_article(item) for item in data["in_progress"])

    index = replace_between(index, "<!-- working-papers:start -->", "<!-- working-papers:end -->", working)
    index = replace_between(index, "<!-- publications:start -->", "<!-- publications:end -->", publications)
    index = replace_between(index, "<!-- in-progress:start -->", "<!-- in-progress:end -->", in_progress)
    INDEX_PATH.write_text(index)


def qmd_link(item: dict[str, str]) -> str:
    title = item["title"]
    url = item.get("url")
    if url:
        return f"[{title}]({url})"
    return title


def qmd_entry(item: dict[str, str], include_year: bool = True) -> list[str]:
    year = f" ({item['year']})" if include_year and item.get("year") else ""
    venue = f", *{item['venue']}*" if item.get("venue") else ""
    lines = [f"- {qmd_link(item)}{year}{venue}"]
    if item.get("authors"):
        lines.append(f"  {item['authors']}")
    return lines


def render_cv(data: dict[str, list[dict[str, str]]]) -> None:
    lines = [
        "---",
        "title: KAZUSHIGE MATSUDA",
        "format:",
        "  pdf:",
        "    documentclass: article",
        "    geometry: margin=1in",
        "    fontsize: 11pt",
        "execute:",
        "  echo: false",
        "---",
        "",
        "Keio University, 2-15-45 Mita Minato-ku, Tokyo, Japan 108-8345  ",
        "Web page: https://kmatsuda723.github.io/  ",
        "Email: kazu.matsuda@keio.jp",
        "",
        "## Employment",
        "",
    ]

    for year, description in CV_EMPLOYMENT:
        lines.append(f"- {year}: {description}")

    lines.extend(["", "## Visiting Positions", ""])
    for year, description in CV_VISITING_POSITIONS:
        lines.append(f"- {year}: {description}")

    lines.extend(["", "## Education", ""])
    for year, description in CV_EDUCATION:
        lines.append(f"- {year}: {description}")

    lines.extend([
        "",
        "## Published Journal Articles",
        "",
    ])

    for item in data["publications"]:
        cv_item = dict(item)
        if item.get("cv_venue"):
            cv_item["venue"] = item["cv_venue"]
        lines.extend(qmd_entry(cv_item))

    lines.extend([
        "",
        "## Working Papers",
        "",
    ])

    for item in [*data["working_papers"], *data["in_progress"]]:
        lines.extend(qmd_entry(item, include_year=False))

    lines.extend(["", "## Conference Presentations", ""])
    lines.append(", ".join(CV_CONFERENCE_PRESENTATIONS))

    lines.extend(["", "## Refereeing Services", ""])
    lines.append(", ".join(CV_REFEREEING_SERVICES))

    CV_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    render_index(data)
    render_cv(data)


if __name__ == "__main__":
    main()
