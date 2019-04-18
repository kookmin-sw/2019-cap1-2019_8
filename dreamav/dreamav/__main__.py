import sys
import os

from dreamav.cli import cli


# TODO(@LEO_MOON) add start options
def main():
    # print(sys.argv)
    # cli.start()
    if len(sys.argv) < 2:
        print("dreamav [start | stop]")
    elif sys.argv[1] == 'start':
        sys.argv.pop(1)
        cli.start()
    elif sys.argv[1] == "stop":
        sys.argv.pop(1)
        cli.stop()
    pass
    
if __name__ == '__main__':
    main()
