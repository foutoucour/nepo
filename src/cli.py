import logging
import sys

import click
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

from src import core

logger = logging.getLogger('voodoo')
logging.basicConfig()
logger.setLevel(logging.INFO)


class AllGroup(DYMMixin, HelpColorsGroup, click.Group):  # pylint: disable=too-many-public-methods
    pass


@click.group(
    cls=AllGroup,
    help_headers_color='yellow',
    help_options_color='green'
)
@click.version_option()
def entry_point():
    pass


@entry_point.command()
@click.argument('user', required=False)
@click.argument('repo', required=False)
def github(user='', repo=''):
    url = 'https://github.com'
    if user:
        url = '/'.join([url, user])
        if repo:
            url = '/'.join([url, repo])
    core.open_url(url)


@entry_point.command()
def inbox():
    core.open_url("https://inbox.google.com")


if __name__ == '__main__':
    sys.exit(entry_point())
