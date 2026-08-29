import email
import imaplib
from email import policy
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from komickers.mail_reader.utils import save_pull_list

FetchedEmail = tuple[str, str]  # (subject, html_body)


def _extract_html(msg: EmailMessage) -> str | None:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                return str(part.get_content())
    elif msg.get_content_type() == "text/html":
        return str(msg.get_content())
    return None


def _fetch_latest_imap(mail: imaplib.IMAP4_SSL, provider: str) -> FetchedEmail | None:
    status, data = mail.search(
        None, f'(FROM "{provider}" SUBJECT "Your Comic Pull List for")'
    )
    if status != "OK" or not data[0]:
        return None

    # Message IDs come back in ascending order; the last one is newest.
    message_id = data[0].split()[-1]

    status, data = mail.fetch(message_id, "(RFC822)")
    if status != "OK":
        raise imaplib.IMAP4.error("Failed to fetch email")

    msg = email.message_from_bytes(data[0][1], policy=policy.default)
    subject = str(msg["Subject"] or "")

    html_body = _extract_html(msg)
    if html_body is None:
        return

    return subject, html_body


def read_emails_app_password(
    email_address: str, app_password: str, provider: str, tmp_path: Path
) -> Path | None:
    with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
        try:
            mail.login(email_address, app_password)
        except imaplib.IMAP4.error as e:
            print(f"IMAP authentication failed for {email_address}: {e}")
            return

        try:
            mail.select("INBOX")
        except imaplib.IMAP4.error as e:
            print(f"Couldn't open INBOX: {e}")
            return

        fetched = _fetch_latest_imap(mail, provider)

    if fetched is None:
        print("No matching emails found.")
        return None

    return save_pull_list(tmp_path, *fetched)


def read_emails_oauth(
    email_address: str, provider: str, tmp_path: Path, creds: Any
) -> Path | None:
    auth_string = f"user={email_address}\x01auth=Bearer {creds.token}\x01"
    first_call = True

    def xoauth2(_challenge: bytes) -> bytes:
        nonlocal first_call
        if first_call:
            first_call = False
            return auth_string.encode()
        return b""

    with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
        try:
            mail.authenticate("XOAUTH2", xoauth2)
        except imaplib.IMAP4.error as e:
            print(f"IMAP OAuth failed for {email_address}: {e}")
            return None

        try:
            mail.select("INBOX")
        except imaplib.IMAP4.error as e:
            print(f"Couldn't open INBOX: {e}")
            return None

        # Search for messages from the sender whose subject contains the phrase
        fetched = _fetch_latest_imap(mail, provider)

    if fetched is None:
        print("No matching emails found.")
        return None

    return save_pull_list(tmp_path, *fetched)
