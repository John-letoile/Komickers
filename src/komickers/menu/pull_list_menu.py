from pathlib import Path
import logging

from socket import gaierror
import httplib2

from komickers.core.downloader import (
    Inventory,
    extract_comics_from_file,
    download_from_inventory,
)
from komickers.core.extractor import extract_names
from komickers.mail_reader.reader import read_emails
from komickers.exceptions import (
    AuthenticationError,
    EmailError,
    ExtractionError,
    DownloaderError,
)

logger = logging.getLogger(__name__)


def pull_list_menu(config: dict) -> None:
    print("\n=================== PULL LIST MENU ===================\n")
    tmp_path: Path = Path(config["directories"]["tmp_dir"])
    tmp_path.mkdir(parents=True, exist_ok=True)

    pull_list_path: Path | None = None
    pulled: bool = False
    while not pulled:
        try:
            print(
                "Please select your preferred method of logging in:\ng) Google API\ni) IMAP\n"
            )
            login_method: str = input("your selection: ")
            pull_list_path: Path | None = read_emails(config, login_method)
            pulled = True

        except AuthenticationError as ae:
            print(f"\nAuthentication failed: {ae}")
            print("\n======================================================\n")
            return

        except EmailError as ee:
            print(f"Email error: {ee}")
            print("\n======================================================\n")
            return

        except ValueError:
            print(
                "\n.===============================."
                "\n||Please select a correct option||"
                "\n^===============================^\n"
            )

        except ImportError as ie:
            print(ie)

    if pull_list_path is None:
        print("Couldn't determine the path of the pull list. Aborting...")
        print("\n======================================================\n")
        return

    index_path: Path = pull_list_path / "index.html"
    inbox_path: Path = Path(config["download"]["downloads_dir"])
    method: str = config["download"]["download_manager"]
    pull_list: list[tuple[str, str]] | None = extract_names(index_path)

    if pull_list is None:
        print("Couldn't extract comic names. Aborting...")
        print("\n======================================================\n")
        return

    inventory: Inventory | None = extract_comics_from_file(pull_list_path, pull_list)

    if inventory is None:
        print("An error occured while extracting download links...")
        print("\n======================================================\n")
        return

    try:
        download_from_inventory(inventory, inbox_path, method)
    except DownloaderError as de:
        print(de)
        print("\n======================================================\n")
