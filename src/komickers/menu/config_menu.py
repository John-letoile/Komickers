from komickers.config import update_config


def config_menu():
    print("\n================= CONFIGURATION MENU =================\n")
    print(
        "Please give your preference for each of these fields (for extra configuration, checkout the TOML file in .config)"
    )
    print("Any blank fields will be filled with their respective default values:\n")

    tmp_dir = input("Temp Files Directory: ")
    downloads_dir = input("Downloads Directory: ")
    download_manager = input("Download Manager (surge, uget, wget2): ")
    email_address = input("Email Address: ")

    update_config(
        tmp_dir=tmp_dir,
        downloads_dir=downloads_dir,
        download_manager=download_manager,
        email_address=email_address,
    )

    print("\nSuccessfully updated config file")
    print("======================================================\n")
