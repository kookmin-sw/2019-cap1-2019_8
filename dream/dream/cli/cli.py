import sys
import click

@click.command()
@click.option("--count", default=1)

def cli(count):
    click.echo("asd")

if __name__ == '__main__':
    print(sys.argv)
    if sys.argv[1] == 'start':
        sys.argv.pop(1)
        cli()