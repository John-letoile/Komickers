import subprocess
import sys
from pathlib import Path
from typing import TextIO
from dataclasses import dataclass

from .extractor import extract_download_link


@dataclass
class Inventory:
    pulled: list[str]
    missed: list[str]
    urls_path: Path


def save_html_file(
    comic_name: str, comic_name_formatted: str, pull_list_path: Path
) -> Path | None:
    url: str = f"https://getcomics.org/marvel{comic_name_formatted}"
    tmp_html_dir: Path = pull_list_path / "comics_indexes"
    tmp_html_dir.mkdir(parents=True, exist_ok=True)

    file_path: Path = tmp_html_dir / f"{comic_name_formatted[1:-1]}.html"

    try:
        result: subprocess.CompletedProcess = subprocess.run(
            ["curl", "-fL", url], check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        print(f"Couldn't fetch the html file for {comic_name}")
        return None

    output = result.stdout
    file_path.write_bytes(output)
    print(f'Successfully saved "{comic_name}"')
    return file_path


def download_comics_uget(urls_file_path: Path, inbox_dir: Path) -> None:
    print("Downloading...\n")
    if sys.platform == "linux":
        subprocess.run(
            [
                "uget-gtk",
                "--quiet",
                f"--input-file={urls_file_path}",
                f"--folder={inbox_dir}",
            ],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    elif sys.platform == "win32":
        subprocess.run(
            [
                "uget",
                "--quiet",
                f"--input-file={urls_file_path}",
                f"--folder={inbox_dir}",
            ],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    else:
        raise RuntimeError(f"uGet is not supported for this platform: {sys.platform}")


def download_comics_wget2(urls_file_path: Path, inbox_dir: Path) -> None:
    print("Downloading...\n")
    subprocess.run(
        [
            f"cat{urls_file_path}",
            "|",
            "xargs",
            "-n3",
            "-P1",
            "wget2",
            "-q",
            "--force-progress",
            "--trust-server-names",
            "-P",
            inbox_dir,
        ],
        check=True,
    )


def download_comics_surgeDM(urls_file_path: Path, inbox_dir: Path) -> None:
    print("Downloading...\n")
    subprocess.run(
        ["surge", "--batch", urls_file_path, "--output", inbox_dir],
        check=True,
    )


def download_comics(urls_file_path: Path, inbox_dir: Path, method: str) -> None:
    try:
        if method.lower() == "uget":
            download_comics_uget(urls_file_path, inbox_dir)
        elif method.lower() == "wget2":
            download_comics_wget2(urls_file_path, inbox_dir)
        elif method.lower() == "surge":
            download_comics_surgeDM(urls_file_path, inbox_dir)
        else:
            raise ValueError("Please select one of the available download methods")

    except subprocess.CalledProcessError:
        print(f"Couldn't run the download manager: {method}")
    except RuntimeError as rte:
        print(rte)


def _log_missed_comics(missed_comics: list[str], missed_file: TextIO, comic: str):
    missed_comics.append(comic)
    missed_file.write(f"{comic}\n")
    print("\n-------------------------****-------------------------\n")


def extract_comics_from_file(
    pull_list_path: Path, pull_list: list[tuple[str, str]]
) -> Inventory | None:
    missed_comics: list[str] = []
    pulled_comics: list[str] = []

    extracted_urls_path = pull_list_path / "pulled_list.txt"
    missed_path = pull_list_path / "missed_list.txt"

    # clean up files before writing to them
    extracted_urls_path.write_text("")
    missed_path.write_text("")

    # open files once

    pulled_file = open(extracted_urls_path, "a")
    missed_file = open(missed_path, "a")
    try:
        print("Extracting download links...")
        print("\n-------------------------****-------------------------\n")

        for comic in pull_list:
            print(f'Trying to find "{comic[0]}"')
            try:
                comic_html_file = save_html_file(comic[0], comic[1], pull_list_path)

                if comic_html_file is None:
                    print(f"Couldn't find page for {comic[0]}")
                    _log_missed_comics(missed_comics, missed_file, comic[0])
                    continue

                print(f"Found page\nExtracting download link for {comic[0]}")

                extracted_comic_link = extract_download_link(comic_html_file)

                if extracted_comic_link is None:
                    print(f"Couldn't extract download link for {comic[0]}")
                    _log_missed_comics(missed_comics, missed_file, comic[0])
                    continue

                print(f"Successfully extracted download link for {comic[0]}")
                pulled_comics.append(comic[0])
                pulled_file.write(f"{extracted_comic_link}\n")
                print("\n-------------------------****-------------------------\n")

            except FileNotFoundError:
                print("The indicated file wasn't found")
                _log_missed_comics(missed_comics, missed_file, comic[0])

            except subprocess.CalledProcessError:
                print("There was a problem with the extraction of download links")
                _log_missed_comics(missed_comics, missed_file, comic[0])

    finally:
        pulled_file.close()
        missed_file.close()

    return Inventory(pulled_comics, missed_comics, extracted_urls_path)


def download_from_inventory(
    comics_inventory: Inventory, inbox_path: Path, method: str
) -> None:

    pulled_comics: list[str] = comics_inventory.pulled
    missed_comics: list[str] = comics_inventory.missed
    extracted_urls_path: Path = comics_inventory.urls_path

    print(extracted_urls_path)

    if len(pulled_comics) == 0:
        print("No comics were pulled. Aborting...")
        print("\n======================================================\n")
        return

    print("The following comics were pulled:")
    for i, comic in enumerate(pulled_comics, start=1):
        print(f"{i})", comic)

    if missed_comics:
        print("\nThe following comics were unavailable:")
        for i, comic in enumerate(missed_comics, start=1):
            print(f"{i})", comic)

    print("\n-------------------------****-------------------------\n")
    download_permission = input("would you like to download these comics [N/y]? ")
    if download_permission.lower() in {"y", "yes"}:
        inbox_path.mkdir(parents=True, exist_ok=True)
        download_comics(extracted_urls_path, inbox_path, method)

    else:
        print("Aborting...")
        print("\n======================================================\n")
        return

    print("Successfully downloaded comics")
    print("\n======================================================\n")
