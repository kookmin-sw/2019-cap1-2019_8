import sys
from mydream.cli import cli

# TODO(@LEO_MOON) develop main
def main():

    cli.start()
    # if len(sys.argv) < 2:
    #     print("mydream [start | stop]")
    # elif sys.argv[1] == 'start':
    #     print("TEST")
    #     cli.start()
    # elif sys.argv[1] == "stop":
    #     sys.argv.pop(1)
    #     cli.stop()
    # pass
    
if __name__ == '__main__':
    main()
