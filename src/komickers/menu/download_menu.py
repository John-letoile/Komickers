from pathlib import Path


from komickers.core.extractor import formatter
from komickers.core.downloader import extract_comics_from_file, download_from_inventory


def download_menu(config: dict) -> None:
    print("\n==================== DOWNLOAD MENU ===================\n")
    print(
        "Please provide a text file containing the download links of the comics to be downloaded."
    )
    pull_list_path: Path = Path(input("\nthe path to the text file: "))
    year: str = input("the year for this pull list: ")
    index_dir: Path = Path(input("the directory to save the index files to: "))

    if not pull_list_path.exists():
        print("The provided path doesn't exist. Aborting...")
        print("\n======================================================\n")
        return

    with open(pull_list_path, "r", encoding="utf-8") as f:
        names: list[str] = [line.rstrip() for line in f if line.strip()]

    pull_list: list[tuple[str, str]] = [(name, formatter(year, name)) for name in names]
    inbox_path = Path(config["download"]["downloads_dir"])
    method = config["download"]["download_manager"]
    inventory: tuple[list[str], list[str], Path] | None = extract_comics_from_file(
        index_dir, pull_list
    )

    if inventory is None:
        print("An error occured while extracting download links...")
        print("\n======================================================\n")
        return

    download_from_inventory(inventory, inbox_path, method)
