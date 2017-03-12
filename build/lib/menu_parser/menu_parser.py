import click

import read_image


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file_path", default='test.jpg', required=False)
def cli(file_path):
    read_image.main(file_path)
