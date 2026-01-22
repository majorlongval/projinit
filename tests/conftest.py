import pytest
import os
import shutil
import pathlib

@pytest.fixture
def tmp_cwd(tmp_path):
    """
    Fixture to run tests in a temporary directory.
    Yields the temporary directory path.
    """
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)
