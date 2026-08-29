import email
from pathlib import Path

from .reader_google import read_emails as _read_emails_google
from .reader_imap import read_emails_app_password as _read_emails_app_password
from .reader_imap import read_emails_oauth as _read_emails_oauth
from .utils import get_credentials


def read_emails(config: dict, login_method: str) -> Path | None:
    tmp_path = Path(config["directories"]["tmp_dir"])

    if login_method.lower() in {"g", "1"}:
        token_path = Path(config["directories"]["token_dir"])
        credentials_path = Path(config["directories"]["credentials_dir"])
        scopes: list[str] = config["email"]["scopes"]
        creds = get_credentials(token_path, credentials_path, scopes)
        return _read_emails_google(creds, tmp_path)

    elif login_method.lower() in {"i", "2"}:
        print(
            "\nPlease select one of the following ways to log into your account:\na) App Password\no) OAuth2\n"
        )
        auth_method = input("your selection: ")
        email_address = config["email"]["email_address"]
        provider = config["email"]["provider"]

        if auth_method.lower() in {"a", "1"}:
            app_password = config["email"]["app_password"]
            return _read_emails_app_password(
                email_address, app_password, provider, tmp_path
            )

        elif auth_method.lower() in {"o", "2"}:
            token_path = Path(config["directories"]["token_dir"])
            credentials_path = Path(config["directories"]["credentials_dir"])
            scopes: list[str] = config["email"]["scopes"]
            creds = get_credentials(token_path, credentials_path, scopes)
            return _read_emails_oauth(email_address, provider, tmp_path, creds)

        else:
            raise ValueError("Incorrect value picked")
    else:
        raise ValueError("Incorrect value picked")
