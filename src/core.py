#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from contextlib import contextmanager

import click
import crayons


def open_url(url):
    click.echo("Opening {}.".format(crayons.white(url, bold=True)))
    click.launch(url)


def get_config_file_path():
    home = os.path.expanduser("~")
    return os.path.realpath('{}/.commands.json'.format(home))


@contextmanager
def get_config_file(mode='r'):
    """ Return the file storing the commands.

    :param str mode: the mode the file with be opened with. Default: r
    :return: the file object.
    :rtype: file
    """
    path = get_config_file_path()
    if not os.path.exists(path):
        generate_empty_config_file()

    with open(path, mode) as datafile:
        yield datafile


def generate_empty_config_file():
    """ Reset the config file."""
    with open(get_config_file_path(), 'w') as datafile:
        json.dump({}, datafile)


def build_command(name, url):
    """ Build a click command according the arguments.

    :param str name: label that the user will use to trigger the command.
    :param str url: the url that will be opened.
    :rtype: click.Command
    """
    return click.Command(
        name,
        callback=lambda: open_url(url),
        help='Open {}'.format(url)
    )
