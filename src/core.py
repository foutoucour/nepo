import json
import os
from contextlib import contextmanager

import click
import crayons


def open_url(url):
    click.echo("Opening {}.".format(crayons.white(url, bold=True)))
    click.launch(url)


class Config(object):
    def __init__(self):
        self.__configs = None

    def save(self, configs):
        with self.__get_file('w') as config_file:
            json.dump(configs, config_file)

        self.__configs = None

    @contextmanager
    def get(self):
        if self.__configs is None:
            with self.__get_file() as config_file:
                self.__configs = json.load(config_file)
        yield self.__configs

    @contextmanager
    def __get_file(self, mode='r'):
        home = os.path.expanduser("~")
        path = os.path.realpath('{}/.commands.json'.format(home))

        if not os.path.exists(path):
            with open(path, 'w') as datafile:
                json.dump({}, datafile)

        with open(path, mode) as datafile:
            yield datafile

    def get_commands(self):
        with self.get() as commands:
            for command, details in commands.items():
                yield build_command(command, details['url'])


config = Config()


def build_command(name, url):
    return click.Command(
        name,
        callback=lambda: open_url(url),
        help='Open {}'.format(url)
    )
