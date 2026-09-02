import logging
import argparse
from sys import stdout
from pathlib import Path

from komickers.exceptions import ConfigError

from .config import load_config
from .menu.config_menu import config_menu
from .menu.download_menu import download_menu
from .menu.pull_list_menu import pull_list_menu


def main():
    # Arguement Parser
    parser = argparse.ArgumentParser(
        description="Komickers - comic download automation"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug output"
    )
    args = parser.parse_args()

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Handler 1: Console (only shows INFO and above, respects user's -v flag)
    console_handler = logging.StreamHandler(stdout)
    console_handler.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    console_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Handler 2: Log File (always writes everything, even DEBUG)
    log_path = Path(__file__).resolve().parents[2] / "logs/komickers.log"
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Load Config File
    try:
        config: dict = load_config()
    except ConfigError as ce:
        print(ce)
        return

    print("""
         ██ ▄█▀ ▒█████   ███▄ ▄███▓ ██▓ ▄████▄   ██ ▄█▀▓█████  ██▀███    ██████ 
         ██▄█▒ ▒██▒  ██▒▓██▒▀█▀ ██▒▓██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒▒██    ▒ 
        ▓███▄░ ▒██░  ██▒▓██    ▓██░▒██▒▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒░ ▓██▄   
        ▓██ █▄ ▒██   ██░▒██    ▒██ ░██░▒▓█▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄    ▒   ██▒
        ▒██▒ █▄░ ████▓▒░▒██▒   ░██▒░██░▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒▒██████▒▒
        ▒ ▒▒ ▓▒░ ▒░▒░▒░ ░ ▒░   ░  ░░▓  ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
        ░ ░▒ ▒░  ░ ▒ ▒░ ░  ░      ░ ▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░ ░▒  ░ ░
        ░ ░░ ░ ░ ░ ░ ▒  ░      ░    ▒ ░░        ░ ░░ ░    ░     ░░   ░ ░  ░  ░  
        ░  ░       ░ ░         ░    ░  ░ ░      ░  ░      ░  ░   ░           ░  
                               ░                                        
        """)

    print(
        "Welcome to Komickers, True Believer!\nYour hub for getting your comics, fast and easy.\n"
    )

    while True:
        print(
            "c) Change Config\np) Pull latest pull list\nd) Download pull list\nq) Quit\n"
        )
        menu_selection = input("please select a menu: ")
        match menu_selection:
            case "c":
                config_menu()
                try:
                    config = load_config()
                except ConfigError as ce:
                    print(ce)
            case "p":
                pull_list_menu(config)
            case "d":
                download_menu(config)
            case "q":
                break
            case _:
                print(
                    "\n=============================="
                    "\n|Please select a correct menu|"
                    "\n==============================\n"
                )

    print("Aborting...")
