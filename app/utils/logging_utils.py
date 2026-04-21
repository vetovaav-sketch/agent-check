import logging


def setup_logging(level: str = "INFO", verbose: bool = False) -> None:
    log_level = "DEBUG" if verbose else level.upper()
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
