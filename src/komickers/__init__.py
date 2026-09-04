import logging

from .main import main

__author__ = "Arshia Shaygan"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


__all__ = ["main"]
