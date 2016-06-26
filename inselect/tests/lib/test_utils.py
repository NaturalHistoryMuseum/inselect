import sys
import tempfile
import unittest

from datetime import datetime

from mock import patch
from pathlib import Path


try:
    import win32api
except ImportError:
    win32api = None


from inselect.lib.utils import (format_dt_display, is_writable, make_readonly,
                                rmtree_readonly)


class TestUtils(unittest.TestCase):
    def test_makereadonly_file(self):
        f = tempfile.NamedTemporaryFile()
        path = Path(f.name)
        self.assertTrue(is_writable(path))
        make_readonly(path)
        self.assertFalse(is_writable(path))

    def test_makereadonly_dir(self):
        temp = tempfile.mkdtemp()
        try:
            self.assertTrue(is_writable(temp))
            make_readonly(temp)
            self.assertFalse(is_writable(temp))
        finally:
            rmtree_readonly(temp)

    def test_rmtree_readonly(self):
        d = tempfile.mkdtemp()
        path = Path(d)
        try:
            (path / 'a file').open('w')
            (path / 'a directory').mkdir()
            (path / 'a directory' / 'another file').open('w')
            make_readonly(path)
            self.assertTrue(path.is_dir())
        finally:
            rmtree_readonly(path)
            self.assertFalse(path.is_dir())

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch.object(win32api, 'GetTimeFormat', return_value='01:01:01')
    @patch.object(win32api, 'GetDateFormat', return_value='Sonntag, 1. M\xe4rz 2015')
    def format_dt_display_windows(self, mock_get_time_format, mock_get_date_format):
        self.assertEqual(
            u'Sonntag, 1. M\xe4rz 2015', format_dt_display(datetime.now())
        )


if __name__ == '__main__':
    unittest.main()
