import click
import crayons

def open_url(url):
    click.echo("Opening {}.".format(crayons.white(url, bold=True)))
    click.launch(url)
