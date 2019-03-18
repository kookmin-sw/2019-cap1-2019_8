import sys
import os

def run(config="dream.ini"):
    os.system(f"uwsgi --ini {config}")


if __name__ == '__main__':
    run()
