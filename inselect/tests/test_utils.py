import shutil
import stat
import tempfile
import unittest

from pathlib import Path

from inselect.lib.utils import make_readonly

class TestMakeReadOnly(unittest.TestCase):
    def test_makereadonly_file(self):
        f = tempfile.NamedTemporaryFile()
        path = Path(f.name)
        self.assertTrue(stat.S_IWUSR & path.stat()[stat.ST_MODE])
        make_readonly(path)
        self.assertFalse(stat.S_IWUSR & path.stat()[stat.ST_MODE])

    def test_makereadonly_dir(self):
        temp = tempfile.mkdtemp()
        try:
            path = Path(temp)
            self.assertTrue(stat.S_IWUSR & path.stat()[stat.ST_MODE])
            make_readonly(temp)
            self.assertFalse(stat.S_IWUSR & path.stat()[stat.ST_MODE])
        finally:
             shutil.rmtree(temp)


if __name__=='__main__':
    unittest.main()
