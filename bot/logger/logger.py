from dataclasses import dataclass
import logging

from colorlog import ColoredFormatter


@dataclass
class LoggerConfig:
    debug: bool
    file_path: str


class ConditionalColoredFormatter(ColoredFormatter):
    """Custom formatter for adding a file path"""

    def format(self, record):
        if record.levelno >= logging.WARNING:
            extra_info = f"\t[File: {record.filename}:{record.lineno}]"
            record.msg += extra_info

        return super().format(record)


def get_logger(name: str, cfg: LoggerConfig) -> logging.Logger:
    """Get the configured logger.

    Args:
        name (str): The name of the logger
        level (int): Logging level. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: The configured logger
    """

    level = logging.DEBUG if cfg.debug else logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check that handlers are not added more than once
    if not logger.hasHandlers():
        console_formatter = ConditionalColoredFormatter(
            "%(blue)s%(asctime)s\t%(log_color)s[%(levelname)-8s]%(reset)s\t%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=level)
        console_handler.setFormatter(console_formatter)

        logger.addHandler(console_handler)

        # Configuring the log file
        if cfg.file_path:
            file_formatter = logging.Formatter(
                "%(asctime)s    [%(levelname)-8s]    %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            file_handler = logging.FileHandler(cfg.file_path, encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(file_formatter)

            logger.addHandler(file_handler)

    return logger


__all__ = ["get_logger"]
