import copy
from pathlib import Path

import tomlkit


def _default_config() -> dict:
    project_root = Path(__file__).resolve().parents[2]
    return {
        "directories": {
            "tmp_dir": str(project_root / ".tmp"),
            "credentials_dir": str(project_root / "credentials"),
            "token_dir": str(project_root / "token"),
        },
        "download": {
            "downloads_dir": str(project_root / "inbox"),
            "download_manager": "surge",
        },
        "email": {
            "scopes": ["https://mail.google.com/"],
            "email_address": "",
            "provider": "noreply@leagueofcomicgeeks.com",
            "app_password": "",
        },
    }


def _deep_merge(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> dict:
    path = Path(__file__).resolve().parents[2] / ".config/komickers.toml"
    if not path.exists():
        return _default_config()

    with open(path, "r", encoding="utf-8") as f:
        data = tomlkit.load(f)

    return _deep_merge(_default_config(), data)


def save_config(config: dict) -> None:
    path = Path(__file__).resolve().parents[2] / ".config/komickers.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        tomlkit.dump(config, f)


def update_config(**kwargs) -> None:
    config = load_config()
    default_config = _default_config()

    valid_keys = {
        "tmp_dir": ("directories", "tmp_dir"),
        "credentials_dir": ("directories", "credentials_dir"),
        "token_dir": ("directories", "token_dir"),
        "downloads_dir": ("download", "downloads_dir"),
        "download_manager": ("download", "download_manager"),
        "scopes": ("email", "scopes"),
        "email_address": ("email", "email_address"),
        "provider": ("email", "provider"),
        "app_password": ("email", "app_password"),
    }

    for key, value in kwargs.items():
        if key in valid_keys:
            section, subkey = valid_keys[key]
            config[section][subkey] = (
                default_config[section][subkey] if value == "" else value
            )
        else:
            raise KeyError(f"Invalid configuration key: {key}")

    save_config(config)
