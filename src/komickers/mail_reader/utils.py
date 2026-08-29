from __future__ import annotations

import pickle
from pathlib import Path
from datetime import datetime


def get_credentials(
    token_path: Path, credentials_path: Path, scopes: list[str]
) -> google.oauth2.credentials.Credentials | None:
    try:
        import google
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as e:
        raise ImportError(
            "The 'google' optional dependencies is required to use OAuth2"
        ) from e

    creds: google.oauth2.credentials.Credentials | None = None
    token_path.mkdir(parents=True, exist_ok=True)
    if (token_path / "token.pickle").exists():
        print("Reading token file...")
        with open(str(token_path / "token.pickle"), "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials outdated. Refreshing...")
            creds.refresh(Request())
        else:
            print("Credentials not available. Creating them...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path / "credentials.json"),
                scopes,
            )
            creds = flow.run_local_server(port=0)

        with open(str(token_path / "token.pickle"), "wb") as token:
            pickle.dump(creds, token)

    return creds


def parse_pull_list_date(text: str | None) -> str | None:
    if not text:
        return None

    prefix = "Your Comic Pull List for "
    if not text.startswith(prefix):
        return None

    try:
        date = datetime.strptime(text.removeprefix(prefix), "%B %d, %Y")
    except ValueError:
        return None

    return date.strftime("%Y-%m-%d")


def save_pull_list(tmp_path: Path, subject: str, html_body: str) -> Path | None:
    """Shared sink: the ONE place that touches the filesystem.

    Policy (identical for both backends):
      - Non pull-list subjects yield None ("not a pull list email").
      - If `<folder>/index.html` already exists, skip re-downloading.
      - Otherwise create the dated folder, write index.html, return it.
    """
    folder_name = parse_pull_list_date(subject)
    if folder_name is None:
        print("Not a pull list email...")
        return None

    email_path = tmp_path / folder_name

    if (email_path / "index.html").exists():
        print(f"The latest pull list's index file already exists: {email_path.name}")
        print("-------------------------****-------------------------")
        return email_path

    email_path.mkdir(parents=True, exist_ok=True)
    print("Pull List:", subject)

    with open(email_path / "index.html", "w", encoding="utf-8") as f:
        f.write(html_body)

    print(f"Saved to {email_path}")
    print("-------------------------****-------------------------")
    return email_path
