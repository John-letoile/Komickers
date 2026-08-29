from __future__ import annotations

from base64 import urlsafe_b64decode
from pathlib import Path
from typing import Any

from .utils import save_pull_list


def build_gmail_service(creds: Any) -> Any:
    try:
        from googleapiclient.discovery import build
    except ImportError as e:
        raise ImportError(
            "The 'google' optional dependencies are required to read Google emails"
        ) from e

    return build("gmail", "v1", credentials=creds)


def _search_latest_google(service: Any, query: str) -> dict | None:
    result: dict = service.users().messages().list(userId="me", q=query).execute()
    messages: list[dict] = list(result.get("messages", []))

    while "nextPageToken" in result:
        result = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=result["nextPageToken"])
            .execute()
        )
        messages.extend(result.get("messages", []))

    return messages[0] if messages else None


def _gmail_html(payload: dict) -> str | None:
    """Depth-first search of the MIME tree for the first text/html body."""
    data = (payload.get("body") or {}).get("data")

    if data and payload.get("mimeType") == "text/html":
        # Gmail strips base64 padding; restore it before decoding.
        padded = data + "=" * (-len(data) % 4)
        return urlsafe_b64decode(padded).decode("utf-8", errors="replace")

    for part in payload.get("parts") or []:
        html = _gmail_html(part)
        if html is not None:
            return html

    return None


def read_emails(creds: Any, tmp_path: Path) -> Path | None:
    try:
        from google.auth.exceptions import RefreshError
        from googleapiclient.errors import HttpError
    except ImportError as e:
        raise ImportError(
            "The 'google' optional dependencies are required to read Google emails"
        ) from e

    try:
        service = build_gmail_service(creds)

        latest = _search_latest_google(
            service,
            'from:noreply@leagueofcomicgeeks.com subject:"Your Comic Pull List for"',
        )
        if latest is None:
            print("No emails found.")
            return None

        msg: dict = (
            service.users()
            .messages()
            .get(userId="me", id=latest["id"], format="full")
            .execute()
        )

        subject = ""
        for header in msg.get("payload", {}).get("headers", []):
            if header.get("name", "").lower() == "subject":
                subject = header.get("value", "")
                break

        html_body = _gmail_html(msg.get("payload", {}))
        if html_body is None:
            print("Email does not contain an HTML body")
            return None

        return save_pull_list(tmp_path, subject, html_body)

    except RefreshError:
        print("Token expired/revoked — delete token/token.pickle and re-authenticate.")
    except HttpError as e:
        print(f"Gmail API error: {e.status_code} {e.reason}")
