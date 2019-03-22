import sys
import click

from __main__ import run

@click.command()
@click.option("--config", "-c", type=click.Path(exists=True))
def start(config):
    run(config)


# TODO(@LEO_MOON): add function for stopping dream-av-av
@click.command()
def stop():
    pass


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