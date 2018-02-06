#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import click

from src.command_manager import CommandManager
from src import manifest
from src import core
from src import groups

logger = logging.getLogger(manifest.name)
logging.basicConfig()
logger.setLevel(logging.INFO)


@click.group(
    cls=groups.AllGroup,
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
