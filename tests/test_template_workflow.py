"""An example set of tests."""
import os

import sksurgerystats.from_pypi as skspypi


def test_library_exists(package_name):
    """Placeholder for checking whether the given library name is correct, ie pypi can find packages associated with this name."""
    assert skspypi.find_new_pypi_packages(package_name) is not None


def test_token_availability():
    """Test for checking if local github.token exists. This is not necessary in the case of only deploying through GH Actions + Secret PAT token saved in environments."""
    return os.path.exists("github.token")


def test_files_exists():
    """Maybe a test is necessary to check if html files exist or the update_dashboard.py can run."""
    assert True
