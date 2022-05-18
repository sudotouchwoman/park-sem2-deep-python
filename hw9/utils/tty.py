from enum import Enum

import click

from .LRU import LRUCache
from . import LOG_MANAGER


class Command(str, Enum):
    ADD = "--add"
    ADD_S = "-a"
    GET = "--get"
    GET_S = "-g"
    PRINT = "--print"
    PRINT_S = "-p"
    DROP = "--new"
    DROP_S = "-n"
    EXIT = "exit"


CAPACITY = 10
USAGE = f"""
LRUCache demo

{Command.ADD}, {Command.ADD_S}: ADD new key-value pair to the cache
{Command.GET}, {Command.GET_S}: GET key from cache
{Command.PRINT}, {Command.PRINT_S}: PRINT the state of the cache
{Command.DROP}, {Command.DROP_S}: DROP current cache and create a new one
{Command.EXIT} to EXIT program
"""


class TTYWorker:
    cache: LRUCache

    def __init__(self, capacity: int = CAPACITY) -> None:
        self.log = LOG_MANAGER.default_logger(__name__)
        self.cache = LRUCache(capacity=capacity)
        click.secho(USAGE, fg="green")

    def run(self) -> None:
        while True:
            self.log.debug("Waiting for command")
            command: str = click.prompt(">>> Enter command", type=str)
            self.log.debug(msg=f"Recieved command: {command}")

            if command in (Command.ADD, Command.ADD_S):
                key, value = click.prompt(
                    ">>> Enter key-value pair separated by '='", type=str
                ).split("=")
                self.cache[key] = value
                continue

            if command in (Command.GET, Command.GET_S):
                key = click.prompt(">>> Enter key to lookup", type=str)
                value = self.cache[key]
                color = "red" if value is None else "yellow"
                click.secho(f"{value}", fg=color)
                continue

            if command in (Command.PRINT, Command.PRINT_S):
                click.secho(self.cache, fg="yellow")
                continue

            if command in (Command.DROP, Command.DROP_S):
                capacity = click.prompt(
                    ">>> Enter new cache capacity", type=int, default=CAPACITY
                )
                self.cache = LRUCache(capacity=capacity)
                continue

            if command == Command.EXIT:
                click.secho("Exiting...", fg="green")
                break
