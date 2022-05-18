import click

from utils import LOG_MANAGER
from utils.tty import TTYWorker


@click.command()
@click.option("-s", "--stream", is_flag=True, default=None)
def main(stream):
    if stream:
        LOG_MANAGER.stream_logs()

    TTYWorker().run()


if __name__ == "__main__":
    main(None)
