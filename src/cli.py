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
    """Add an url to the list of commands."""
    command_manager = CommandManager()
    command_manager.add(name, {'url': url})


@entry_point.command()
@click.argument('name')
def deregister(name):
    """ Remove a command from the list of commands."""
    command_manager = CommandManager()
    if command_manager.safe_delete(name):
        click.echo("Removed {} from the list of commands".format(name))


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
