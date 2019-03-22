import sys
import click
import os

@click.command()
@click.option("--config", "-c", type=click.Path(exists=True))
def start():
    os.system("bash run.sh")

# TODO(@LEO_MOON): add function for stopping dream
@click.command()
def stop():
    pass


def main():
    print(sys.argv)
    if sys.argv[1] == 'start' and sys.argv[2] == "dream.ini":
        sys.argv.pop(1)
        start()
    elif sys.argv[1] == "stop":
        sys.argv.pop(1)
        stop()


if __name__ == '__main__':
    main()