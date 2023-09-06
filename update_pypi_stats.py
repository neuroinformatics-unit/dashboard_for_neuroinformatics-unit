"""
Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them.
"""

import os.path

import sksurgerystats.from_pypi as skspypi
from sksurgerystats.common import (
    get_packages,
    get_package_information,
    update_package_information,
)

if __name__ == "__main__":
    packages = get_packages()

    package_dictionaries = []
    for package in packages:
        package_dictionaries.append(skspypi.get_json_from_pypi(package))

    for index, dictionary in enumerate(package_dictionaries):
        package_name = dictionary.get("info").get("name")
        if package_name != packages[index]:
            print("Got package name mismatch: ", package_name, " != ", packages[index])
            continue
        (
            number_of_releases,
            first_release_date,
            last_release_date,
            last_release_name,
        ) = skspypi.get_release_information(dictionary)

        update_package_information(
            package_name,
            "Number of Releases",
            number_of_releases,
            overwrite=True,
        )

        update_package_information(
            package_name,
            "First Release Date",
            first_release_date,
            overwrite=True,
        )

        update_package_information(
            package_name,
            "Last Release Date",
            last_release_date,
            overwrite=True,
        )

        update_package_information(
            package_name,
            "Last Release Name",
            last_release_name,
            overwrite=True,
        )

        homepage = get_package_information(package_name, "home_page")
        pypi_homepage = dictionary.get("info").get("home_page", None)

        if pypi_homepage is not None and pypi_homepage != "":
            homepage = pypi_homepage

        if homepage is not None:
            update_package_information(
                package_name,
                "home_page",
                homepage,
                overwrite=True,
            )
