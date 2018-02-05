import logging
import sys

import click
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

from src import core
from src.core import config, build_command

logger = logging.getLogger('nepo')
logging.basicConfig()
logger.setLevel(logging.INFO)


class AllGroup(DYMMixin, HelpColorsGroup, click.Group):  # pylint: disable=too-many-public-methods
    def __init__(self, name=None, commands=None, **attrs):
        super(AllGroup, self).__init__(name=name, commands=commands, **attrs)
        self.dynamic_commands = []
        for command in config.get_commands():
            self.add_command(cmd=command)
            self.dynamic_commands.append(command.name)

    def get_command(self, ctx, cmd_name):
        if cmd_name in self.dynamic_commands:
            with config.get() as configs:
                return build_command(cmd_name, configs[cmd_name]['url'])
        return super(AllGroup, self).get_command(ctx, cmd_name)


@click.group(
    cls=AllGroup,
    help_headers_color='yellow',
    help_options_color='green'
)
@click.version_option()
def entry_point():
    pass


@entry_point.command()
@click.argument('name', required=True)
@click.argument('url', required=True)
def register(name, url):
    """Add an url to the config."""
    with config.get() as configs:
        if name in configs:
            configs.pop(name, None)

        configs[name] = {'url': url}

    config.save(configs)


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

# codacy = lambda: core.open_url('https://codacy.com')
#
# cmd = click.Command('codacy', callback=codacy)
#
# entry_point.add_command(cmd)



            # entry_point.add_command(cmd)


# get_commands_from_config()

if __name__ == '__main__':
    sys.exit(entry_point())
