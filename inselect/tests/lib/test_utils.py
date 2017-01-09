# -*- coding: utf8 -*-
import os
import sys
import tempfile
import unittest

from datetime import datetime

from mock import patch
from pathlib import Path


try:
    import pwd
except ImportError:
    pwd = None


try:
    import win32api
    import pywintypes
except ImportError:
    win32api = pywintypes = None


from inselect.lib.utils import (format_dt_display, is_writable, make_readonly,
                                rmtree_readonly, user_name)


class TestUtils(unittest.TestCase):
    MOCK_USERNAME = 'Alfred Schütz'

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
            (path / 'a file').touch()
            (path / 'a directory').mkdir()
            (path / 'a directory' / 'another file').touch()
            make_readonly(path)
            self.assertTrue(path.is_dir())
        finally:
            rmtree_readonly(path)
            self.assertFalse(path.is_dir())


    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch.object(win32api, 'GetTimeFormat', return_value='01:01:01')
    @patch.object(
        win32api, 'GetDateFormat',
        return_value='Sonntag, 1. M\xe4rz 2015'    # 'März' encoded as mbcs
    )
    def test_format_dt_display_windows(self, mock_get_time_format,
                                       mock_get_date_format):
        self.assertEqual(
            'Sonntag, 1. M\xe4rz 2015 01:01:01',
            format_dt_display(datetime.now())
        )

    @unittest.skipIf(sys.platform.startswith("win"), "requires Unix-like OS")
    def test_user_name_unix(self):
        # Unix-like OSes should be able to handle more 'exotic' characters,
        # such as Katakana
        username = 'ローレンス　ハドソン'
        class MockPWD(object):
            pw_gecos = username

        with patch.object(
                pwd, 'getpwuid', return_value=MockPWD()
            ) as mock_getpwuid:
            self.assertEqual(username, user_name())
            mock_getpwuid.assert_called_once_with(os.getuid())

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch.object(win32api, 'GetUserNameEx', return_value=MOCK_USERNAME)
    def test_user_name_windows_route1(self, mock_get_user_name_ex):
        "Get user name using GetUserNameEx"
        self.assertEqual(self.MOCK_USERNAME, user_name())
        self.assertEqual(1, mock_get_user_name_ex.call_count)

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch.object(win32api, 'GetUserName', return_value=MOCK_USERNAME)
    def test_user_name_windows_route2(self, mock_get_user_name):
        "Get user name using GetUserName"
        # Creating instance of pywintypes.error so this patch needs to be
        # within the function body
        with patch.object(
            win32api, 'GetUserNameEx', side_effect=pywintypes.error()
        ) as mock_get_user_name_ex:
            self.assertEqual(self.MOCK_USERNAME, user_name())
            mock_get_user_name_ex.assert_called_once_with(3)
            mock_get_user_name.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
