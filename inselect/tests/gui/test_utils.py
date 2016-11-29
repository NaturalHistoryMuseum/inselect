import platform
import unittest
import subprocess
import sys

from mock import patch

from inselect.gui.utils import reveal_path
from inselect.tests.utils import temp_directory_with_files


class TestUtils(unittest.TestCase):
    """Test GUI utils
    """
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch.object(subprocess, 'call', return_value=1)
    def test_reveal_path_windows(self, mock_subprocess):
        with temp_directory_with_files() as tempdir:
            path = tempdir / 'xyz'
            path.open('w')
            reveal_path(path)
            expected = "explorer.exe /select,{0}".format(path.resolve())
            mock_subprocess.assert_called_once_with(expected)

    @unittest.skipUnless('Darwin' == platform.system(), "requires OS X")
    @patch.object(subprocess, 'check_call')
    def test_reveal_path_os_x(self, mock_subprocess):
        with temp_directory_with_files() as tempdir:
            path = tempdir / 'xyz'
            path.open('w')
            reveal_path(path)
            expected = [
                '/usr/bin/osascript',
                '-e',
                u'tell application "Finder" to reveal POSIX file "{0}"'.format(str(path.resolve()))
            ]
            mock_subprocess.assert_any_call(expected)


if __name__ == '__main__':
    unittest.main()
