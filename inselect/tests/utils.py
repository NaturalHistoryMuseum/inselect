import shutil
import tempfile

from contextlib import contextmanager
from pathlib import Path

from inselect.lib.utils import rmtree_readonly

@contextmanager
def temp_directory_with_files(*paths):
    """A context manager that creates a temporary directory and copies all
    paths to it. The temporary directory is unlinked when the context is exited.
    """
    temp = tempfile.mkdtemp()
    try:
        temp = Path(temp)
        for p in paths:
            shutil.copy(str(p), str(temp / Path(p).name))
        yield temp
    finally:
        rmtree_readonly(temp)
