#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import click
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

from src.command_manager import CommandManager
from src import manifest
from src import core

logger = logging.getLogger(manifest.name)
logging.basicConfig()
logger.setLevel(logging.INFO)


class AllGroup(DYMMixin, HelpColorsGroup, click.Group):  # pylint: disable=too-many-public-methods
    def __init__(self, name=None, commands=None, **attrs):
        """ Overcharge the init of the instance to add the commands coming from the file.
        """
        super(AllGroup, self).__init__(name=name, commands=commands, **attrs)
        self.command_manager = CommandManager()
        self.dynamic_commands = []

        for command in self.command_manager.build_commands():
            self.add_command(cmd=command)
            self.dynamic_commands.append(command.name)

    def get_command(self, ctx, cmd_name):
        """ Overcharge the method to handle the special case of the dynamic commands."""
        # The dynamic commands use a lambda as callback. This lambda should be set at the trigger time.
        # If we use the command stored in the self.commands of the instance, the callback will have stored
        # the latest lambda built. That mean all the dynamic commands will open the same url, the latest
        # registered.
        if cmd_name in self.dynamic_commands:
            return core.build_command(cmd_name, self.command_manager.commands[cmd_name]['url'])
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
@click.argument('name')
@click.argument('url')
def register(name, url):
    """Add an url to the config."""
    command_manager = CommandManager()
    commands = command_manager.commands
    if name in commands:
        commands.pop(name, None)

    commands[name] = {'url': url}

    command_manager.save(commands)


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
