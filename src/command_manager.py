#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from src import core

def load_config_file():
    with core.get_config_file() as config_file:
        return json.load(config_file)


class CommandManager(object):
    def __init__(self):
        self.commands = load_config_file()

    def _save(self):
        """	Save the configs to the file."""
        with core.get_config_file('w') as config_file:
            json.dump(self.commands, config_file)

        # require the update of the commands for the next time.
        self.commands = load_config_file()

    def add(self, name, details):
        """ Add a command to the list."""
        self.commands[name] = details
        self._save()

    def safe_delete(self, name):
        """ Safe Remove a command to the list.

        :return: True if the name has been found and removed from the list. False otherwise.
        """
        if name in self.commands:
            self.commands.pop(name, None)
            self._save()
            return True

        return False

    def build_commands(self):
        """ Return the list of commands stored in the file.

        :return: generator of click commands.
        :rtype: generator
        """
        for command, details in self.commands.items():
            yield core.build_command(command, details['url'])
