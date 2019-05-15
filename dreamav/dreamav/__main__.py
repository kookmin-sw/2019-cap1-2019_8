import sys
import os

from dreamav.cli import cli


# TODO(@LEO_MOON) add start options
def main():
    print(sys.argv)
    if sys.argv[1] == 'start':
        sys.argv.pop(1)
        cli.start()
    elif sys.argv[1] == "stop":
        sys.argv.pop(1)
        cli.stop()
    elif sys.argv[1] == "submit":
        sys.argv.pop(1)
        cli.submit()

    
if __name__ == '__main__':
    main()
