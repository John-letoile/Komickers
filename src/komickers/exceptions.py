class KomickersError(Exception):
    """Base exception for all komickers errors."""


class EmailError(KomickersError):
    """Failed to read or authenticate with email"""


class AuthenticationError(EmailError):
    """Invalid authentication or expired token"""


class InboxError(EmailError):
    """Failed to read inbox"""


class NoPullListError(EmailError):
    """No pull list email found in inbox"""


class ExtractionError(KomickersError):
    """Failed to extract comic names or download links"""


class DownloaderError(KomickersError):
    """Download manager failed or was unavailable"""


class ConfigError(KomickersError):
    """Invalid or misconfigured configuration"""
