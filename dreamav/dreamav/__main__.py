import sys

from dreamav.cli import cli


def main():
    if sys.argv[1] == 'start':
        sys.argv.pop(1)
        cli.start()
    elif sys.argv[1] == "stop":
        sys.argv.pop(1)
        cli.stop()
    elif sys.argv[1] == "submit":
        sys.argv.pop(1)
        cli.submit()
    elif sys.argv[1] == "scan":
        sys.argv.pop(1)
        cli.scan()

    
if __name__ == '__main__':
    main()
