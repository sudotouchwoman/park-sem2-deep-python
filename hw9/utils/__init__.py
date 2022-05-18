from typing import Dict, Optional, TextIO, Any
from os import getenv
import sys
import logging


class LogManager:
    """
    Loging Manager. Wraps logging routines and configuration
    holds all loggers in a dict for easy access

    Can configure root logger to write logs
    to a file or to the terminal
    """
    LEVEL = getenv("LOGGING_LEVEL", "DEBUG")
    DATE_FORMATTING: str = "%D # %H:%M:%S"
    FILE_FORMATTING: str = (
        "[%(asctime)s]::[%(levelname)s]::[%(name)s]::%(message)s"
    )
    STREAM_FORMATTING: str = (
        "[%(asctime)s]::[%(levelname)s]::[%(name)s] - %(message)s"
    )

    def __init__(self, base_file: str = "log.log") -> None:
        self.logfile = base_file
        self._loggers: Dict[str, logging.Logger] = {}
        self.root = logging.getLogger()
        self.root.setLevel(getattr(logging, self.LEVEL))

    def default_logger(self, name: str) -> logging.Logger:
        return self.get_logger(name, None, "DEBUG")

    def get_logger(
        self,
        name: Optional[str],
        file: Optional[str] = None,
        level: str = None,
    ) -> logging.Logger:
        """
        Return a logger instance

        :param name - logger name, str (optional). If None, root logger
        will be returned
        :param file - File path to write logs to (optional)

        :rtype logging,Logger. logger instance
        """
        level = self.LEVEL if level is None else level
        if name is None:
            return self.root
        if name not in self._loggers:
            self.__make_logger(name, file, level)
        return self._loggers[name]

    def __make_logger(
        self, name: str, file: Optional[str], level: str
    ) -> None:
        # create new logger instance and store in loggers
        # set the specified logging level and add
        # file handler if required
        log = logging.getLogger(name=name)
        log.setLevel(getattr(logging, level.upper()))

        if log.hasHandlers():
            self.root.warning(f"logger for {name} already has handlers")

        logfile = file if file else self.logfile
        self.root.debug(msg=f"Adding handler for {name} for {logfile}")

        handler = logging.FileHandler(filename=logfile, encoding="utf-8")
        formatter = logging.Formatter(
            self.FILE_FORMATTING, self.DATE_FORMATTING
        )

        handler.setFormatter(formatter)
        log.addHandler(handler)

        self._loggers[name] = log

    def configure(self, **kwds: Dict[str, Any]) -> None:
        """
        Pass keyword-args to logging.basicConfig

        :param **kwds: Dict[str, Any] - keywords to be passed

        :rtype None
        """
        logging.basicConfig(**kwds)

    def stream_logs(self, stream: TextIO = sys.stdout) -> None:
        """
        Adds StreamHandler to the root logger

        :param stream: TextIO - stream to bind to the logger

        :rtype None
        """
        formatter = logging.Formatter(
            self.STREAM_FORMATTING, self.DATE_FORMATTING
        )
        handler = logging.StreamHandler(stream=stream)
        handler.setFormatter(formatter)
        self.root.addHandler(handler)


LOG_MANAGER = LogManager()
