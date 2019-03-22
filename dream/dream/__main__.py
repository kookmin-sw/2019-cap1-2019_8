import sys
import os


def run():
    from .cli import cli

    cli.main()


if __name__ == '__main__':
    run()
