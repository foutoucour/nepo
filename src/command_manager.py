#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from src import core


class CommandManager(object):
    def __init__(self):
        self.__commands = None

    def save(self, commands):
        """Save the configs to the file.

        :param dict commands: mapping of command name and their details
        """
        with core.get_config_file('w') as config_file:
            json.dump(commands, config_file)

        self.__commands = None

    @property
    def commands(self):
        """Get the commands from the config file.

        :return: mapping of commands in it
        :rtype: dict
        """
        if not self.__commands:
            with core.get_config_file() as config_file:
                self.__commands = json.load(config_file)
        return self.__commands

    def build_commands(self):
        """ Return the list of commands stored in the file.

        :return: generator of click commands.
        :rtype: generator
        """
        for command, details in self.commands.items():
            yield core.build_command(command, details['url'])
