import sys
import click
import os

@click.command()
def start():
    os.system("bash run.sh")

@click.command()
def stop():
    os.system("pkill UWSGI")




# if __name__ == '__main__':
#     main()