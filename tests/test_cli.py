import unittest

from click.testing import CliRunner
import mock

from src import cli


class TestGithub(unittest.TestCase):

    def setUp(self):
        super(TestGithub, self).setUp()
        self.runner = CliRunner()
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


class TestInbox(unittest.TestCase):
    def setUp(self):
        super(TestInbox, self).setUp()
        self.runner = CliRunner()
        self.command = cli.inbox
        self.url = 'https://inbox.google.com'

    @mock.patch('src.core.open_url')
    def test_no_argument(self, mock_open_url):
        """ Test the command without any arguments.

        :param mock.MagicMock mock_open_url: mock
        :return:
        """
        result = self.runner.invoke(self.command)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(1, mock_open_url.call_count)
        self.assertEqual(mock.call(self.url), mock_open_url.call_args)
