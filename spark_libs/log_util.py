"""Logging utility."""

import logging


def get_logger() -> logging.Logger:
    """Get logger."""
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )

    return logging.getLogger(__name__)
