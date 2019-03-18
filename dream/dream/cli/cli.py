import os
import sys
import click

from dream.__main__ import run

@click.command()
@click.option("--config", "-c", type=click.Path(exists=True))
def start(config):
    run(config)


@click.command()
def stop():
    os.system("pkill python3")


def main():
    print(sys.argv)
    if sys.argv[1] == 'start':
        sys.argv.pop(1)
        start()
    elif sys.argv[1] == "stop":
        sys.argv.pop(1)
        stop()


if __name__ == '__main__':
    main()