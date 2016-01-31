import tempfile
import unittest

from pathlib import Path

from inselect.lib.utils import make_readonly, rmtree_readonly, is_writable


class TestFileReadWrite(unittest.TestCase):
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


class TestRMTreeReadOnly(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
