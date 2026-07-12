#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "publications.json"
INDEX_PATH = ROOT / "index.html"
CV_PATH = ROOT / "cv.qmd"


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


def render_cv(data: dict[str, list[dict[str, str]]]) -> None:
    lines = [
        "---",
        "title: Kazushige Matsuda",
        "format:",
        "  pdf:",
        "    documentclass: article",
        "    geometry: margin=1in",
        "    fontsize: 11pt",
        "execute:",
        "  echo: false",
        "---",
        "",
        "Associate Professor, Keio University  ",
        "Email: kazu.matsuda@keio.jp",
        "",
        "## Education",
        "",
        "- Ph.D., Princeton University, 2019",
        "",
        "## Research Interests",
        "",
        "Macroeconomics, labor economics, and the economics of higher education.",
        "",
        "## Working Papers",
        "",
    ]

    for item in data["working_papers"]:
        lines.append(f"- {qmd_link(item)} ({item['year']})")
        if item.get("authors"):
            lines.append(f"  {item['authors']}")

    lines.extend(["", "## Publications", ""])
    for item in data["publications"]:
        venue = f", *{item['venue']}*" if item.get("venue") else ""
        lines.append(f"- {qmd_link(item)} ({item['year']}){venue}")
        if item.get("authors"):
            lines.append(f"  {item['authors']}")

    lines.extend(["", "## Research in Progress", ""])
    for item in data["in_progress"]:
        lines.append(f"- {item['title']}")
        if item.get("authors"):
            lines.append(f"  {item['authors']}")

    CV_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    render_index(data)
    render_cv(data)


if __name__ == "__main__":
    main()
