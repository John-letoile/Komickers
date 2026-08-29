from .config import load_config
from .menu.config_menu import config_menu
from .menu.download_menu import download_menu
from .menu.pull_list_menu import pull_list_menu


def main():
    config: dict = load_config()
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
                config = load_config()
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
