import click

import utils


@click.command()
@click.option("-s", "--stream", is_flag=True, default=None)
def main(stream):
    utils.LOG_MANAGER.stream_logs() if stream else None

    from utils.tty import TTYWorker

    TTYWorker().run()


if __name__ == "__main__":
    main()
