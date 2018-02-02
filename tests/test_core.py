import unittest
import mock

from src import core


class TestOpenUrl(unittest.TestCase):

    def setUp(self):
        super(TestOpenUrl, self).setUp()
        self.func = core.open_url

    @mock.patch('click.launch')
    def test_run(self, mock_launch):
        """

        :param mock.MagicMock mock_launch: mock
        """
        self.func('https://github.com')
        self.assertEqual(1, mock_launch.call_count)
