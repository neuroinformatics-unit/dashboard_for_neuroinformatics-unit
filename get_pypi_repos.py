"""
Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them.
"""

import sksurgerystats.from_pypi as skspypi
from sksurgerystats.common import add_packages

if __name__ == "__main__":
    new_packages = skspypi.find_new_pypi_packages(
        "neuroinformatics-unit"
    )
    add_packages(new_packages)
