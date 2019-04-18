import sys
import click
import os

from dreamav.__init__ import _ROOT

@click.command()
def start():
    os.system(f"uwsgi --ini {os.path.join(_ROOT, 'dream.ini')} --chdir {os.path.join(_ROOT, 'backends')}")

@click.command()
def stop():
    os.system("pkill dreamav")
    os.system("pkill uwsgi")




# if __name__ == '__main__':
#     main()