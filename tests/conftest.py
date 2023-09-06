"""
Basic configuration for tests.

With whole project set to dashboard-stats-template,
and package_name field set to scikit-surgery.
"""

import pytest


@pytest.fixture()
def project_config():
    """
    Pytest fixture for defining the project config.

    Returns
    -------
    dict
        dictionary with values for the cookiecutter template,
        as defined in the cookiecutter.json
    """
    return {
        "project_slug": "dashboard-stats-template",
        "package_name": "scikit-surgery",
    }
