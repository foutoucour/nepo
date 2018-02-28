import tempfile
import unittest
import os
import mock

from click.testing import CliRunner

import src.command_manager
import src.groups
from src import cli
from src import core


class Base(unittest.TestCase):

    def setUp(self):
        super(Base, self).setUp()
        self.tmpfile = tempfile.mkstemp()[-1]
        self.runner = CliRunner()
        self.mocks = []
        mock_config_file = mock.patch(
            'src.core.get_config_file_path',
            autospec=True,
            return_value=self.tmpfile
        )
        self.mocks.append(mock_config_file)
        mock_config_file.start()
        core.generate_empty_config_file()

        self.url = 'https://www.python.org'
        self.command_name = 'python'

        self.command_manager = src.command_manager.CommandManager()

    def tearDown(self):
        os.remove(self.tmpfile)
        for mock_ in self.mocks:
            mock_.stop()


class TestRegister(Base):
    """ Test suite for the command Register."""

    def test_simple_registration(self):
        self.assertIsNone(src.groups.AllGroup().get_command({}, self.command_name))
        self.runner.invoke(cli.register, [self.command_name, self.url])
        self.assertIsNotNone(src.groups.AllGroup().get_command({}, self.command_name))


class TestDeregister(Base):
    """ Test suite for the command deregister."""

    def test_simple_deregistration(self):
        self.runner.invoke(cli.register, [self.command_name, self.url])
        self.assertIsNotNone(src.groups.AllGroup().get_command({}, self.command_name))
        self.runner.invoke(cli.deregister, [self.command_name])
        self.assertIsNone(src.groups.AllGroup().get_command({}, self.command_name))


class TestGithub(Base):

    def setUp(self):
        super(TestGithub, self).setUp()
        self.command = cli.github
        self.url = 'https://github.com'

    @mock.patch('src.core.open_url')
    def test_no_argument(self, mock_open_url):
        """ Test the command without any of the optional arguments.

        :param mock.MagicMock mock_open_url: mock
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
        inbox = src.groups.AllGroup().get_command({}, 'inbox')
        result = self.runner.invoke(inbox)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(1, mock_open_url.call_count)
        self.assertEqual(mock.call(self.url), mock_open_url.call_args)
