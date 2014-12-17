import shutil
import stat
import tempfile
import unittest

from pathlib import Path

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import make_readonly, validate_normalised
from inselect.lib.rect import Rect

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


class TestValidateNormalised(unittest.TestCase):
    def test_validate_normalised(self):
        validate_normalised([Rect(0,0,1,1)])
        self.assertRaises(InselectError, validate_normalised, [(-0.1, 0,    1,   1)])
        self.assertRaises(InselectError, validate_normalised, [( 0,  -0.1,  1,   1)])
        self.assertRaises(InselectError, validate_normalised, [( 0,   0,    1.1, 1)])
        self.assertRaises(InselectError, validate_normalised, [( 0,   0,    1,   1.1)])


if __name__=='__main__':
    unittest.main()
