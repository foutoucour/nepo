import tempfile
import unittest
import os
import mock

from click.testing import CliRunner

import src.command_manager
from src import cli
from src import core


class Base(unittest.TestCase):

    def setUp(self):
        super(Base, self).setUp()
        self.runner = CliRunner()
        self.tmpfile = tempfile.mkstemp()[-1]
        self.command_manager = src.command_manager.CommandManager()
        self.mocks = []
        mock_config_file = mock.patch('src.core.get_config_file_path', autospec=True, return_value=self.tmpfile)
        self.mocks.append(mock_config_file)
        mock_config_file.start()
        core.generate_empty_config_file()

    def tearDown(self):
        os.remove(self.tmpfile)
        for mock_ in self.mocks:
            mock_.stop()


class TestRegister(Base):

    def setUp(self):
        super(TestRegister, self).setUp()
        self.command = cli.register
        self.url = 'https://www.python.org'
        self.command_name = 'python'

    def test_simple_registration(self):
        self.assertNotIn(
            self.command_name,
            [c_name for c_name in self.command_manager.commands],
            msg="The command {} has been found in {} ({}).".format(
                self.command_name,
                self.command_manager.commands,
                core.get_config_file_path()
            )
        )
        self.runner.invoke(self.command, [self.command_name, self.url])
        self.assertIn(
            self.command_name,
            [c for c in self.command_manager.commands],
            msg="The command {} has NOT been found in {} ({}).".format(
                self.command_name,
                self.command_manager.commands,
                core.get_config_file_path()
            )
        )


class TestGithub(Base):

    def setUp(self):
        super(TestGithub, self).setUp()
        self.command = cli.github
        self.url = 'https://github.com'

    @mock.patch('src.core.open_url')
    def test_no_argument(self, mock_open_url):
        """ Test the command without any of the optional arguments.

        :param mock.MagicMock mock_open_url: mock
        :return:
        """
        result = self.runner.invoke(self.command)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(1, mock_open_url.call_count)
        self.assertEqual(mock.call(self.url), mock_open_url.call_args)

    @mock.patch('click.launch')
    def test_user(self, mock_launch):
        """ Test with only one argument.

        :param mock.MagicMock mock_launch: mock
        """
        user = 'foutoucour'
        result = self.runner.invoke(self.command, [user])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(mock.call('{}/{}'.format(self.url, user)), mock_launch.call_args)

    @mock.patch('click.launch')
    def test_user_repo(self, mock_launch):
        """ Test with the all 2 arguments

        :param mock.MagicMock mock_launch: mock
        """
        user = 'foutoucour'
        repo = 'info'
        result = self.runner.invoke(self.command, [user, repo])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(mock.call('{}/{}/{}'.format(self.url, user, repo)), mock_launch.call_args)


class TestInbox(Base):
    def setUp(self):
        super(TestInbox, self).setUp()
        self.command = cli.register
        self.name = 'inbox'
        self.url = 'https://inbox.google.com'

    @mock.patch('src.core.open_url')
    def test_no_argument(self, mock_open_url):
        """ Test the command without any arguments.

        :param mock.MagicMock mock_open_url: mock
        """
        self.runner.invoke(self.command, [self.name, self.url])
        inbox = cli.AllGroup().get_command({}, 'inbox')
        result = self.runner.invoke(inbox)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(1, mock_open_url.call_count)
        self.assertEqual(mock.call(self.url), mock_open_url.call_args)
