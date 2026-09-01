import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
import re
import logging

from komickers.exceptions import ExtractionError

logger = logging.getLogger(__name__)
SPECIAL_CHARACTERS: tuple[str, ...] = ("#", "(", ")", "!", "?", ":")


def get_year(file_path: Path) -> str:
    return file_path.parent.name[:4]


def formatter(year: str, line: str) -> str:
    if "\u2013" in line:
        line = line.replace("\u2013", "-")
    no_space_line: str = line.replace(" ", "-")
    translated_line = no_space_line.translate(
        str.maketrans("", "", "".join(SPECIAL_CHARACTERS))
    )
    translated_line = re.sub(r"-{2,}", "-", translated_line.lower())
    return f"/{translated_line.lower()}-{year}/"


def extract_names(file_path: Path) -> list[tuple[str, str]] | None:
    list_of_comics: list[tuple[str, str]] = []
    year: str = get_year(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find the heading that identifies the Pull List section.
    heading = soup.find(
        lambda tag: (
            tag.name in {"h1", "h2", "h3"}
            and "Your Pull List" in tag.get_text(" ", strip=True)
        )
    )

    if heading is None:
        logger.error("No 'Pull List' section")
        raise ExtractionError(f"Failed to find 'Pull List' section in {file_path}")

    section = heading.find_parent("table")

    if section is None:
        logger.error("No 'Pull List' container")
        raise ExtractionError(f"Failed to find 'Pull List' container in {file_path}")

    for link in section.find_all("a", href=True):
        href = link["href"]
        if "/comic/" not in href:
            continue

        title = link.get("title")

        if title:
            list_of_comics.append((str(title), formatter(year, str(title))))

    return list_of_comics


def extract_download_link(file_path: Path) -> str | None:
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # case sensitive. change if website changes format
    anchor = soup.select_one('a[title="DOWNLOAD NOW"]')

    if anchor is None:
        logger.warning("No 'DOWNLOAD NOW' linkg found in %s", file_path)
        raise ExtractionError(f"No download link found in {file_path.name}")

    download_url: str | None = anchor.get("href")

    if not download_url:
        logger.warning("Download anchor has no 'href' in %s", file_path)
        raise ExtractionError(f"Download link has no URL in {file_path.name}")

    result: subprocess.CompletedProcess = subprocess.run(
        ["curl", "-I", download_url],
        capture_output=True,
        text=True,
        check=False,
    )

    # Get the output and error message (if any)
    output: list[str] = result.stdout.splitlines()
    error = result.stderr
    server_side_url: str | None = None

    # Check if it was successful
    if result.returncode == 0:
        for line in output:
            if line.lower().startswith("location: "):
                server_side_url = line.split(":", 1)[1].strip()

    else:
        print(error)
        return None

    if server_side_url is None:
        print("the server response didn't have a 'location' field")
        return None

    return server_side_url
