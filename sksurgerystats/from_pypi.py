"""
Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them
"""

import os.path
import urllib.request
import subprocess
import json
from datetime import datetime

# packages = os.system('./pypi-simple-search scikit-surgery')


def find_new_pypi_packages(searchname):
    """
    Searched for packages with names matching the searchname in PyPi
    """
    packages = subprocess.run(
        ["./pypi-simple-search", "-u", searchname], capture_output=True
    ).stdout
    package_list = packages.decode("utf-8").splitlines()
    package_list.remove("Updating cache of PyPi packages")
    return package_list


def get_release_information(package_dictionary):
    """
    Queries PyPi generated dictionary to get releases for
    each package
    returns the number of releases, first release date,
    last release date, last release name
    """
    if not package_dictionary.get("on_pypi", True):
        return "n/a", "n/a", "n/a", "n/a"

    releases = package_dictionary.get("releases")
    releases_list = list(package_dictionary.get("releases"))
    first_release_date = None
    last_release_date = None
    last_release_name = 'n/a'
    number_of_releases = len(releases_list)

    for release in releases_list:
        try:
            release_date_string = releases.get(release)[0].get("upload_time")
        except IndexError:
            #some releases have an empty list for release information
            #if so skip this iteration
            continue
        release_date = datetime.fromisoformat(release_date_string)
        if first_release_date is None:
            first_release_date = release_date
        if last_release_date is None:
            last_release_date = release_date

        if release_date < first_release_date:
            first_release_date = release_date
        if release_date > last_release_date:
            last_release_date = release_date
            last_release_name = release

    if first_release_date is not None:
        return (
            number_of_releases,
            first_release_date.isoformat(),
            last_release_date.isoformat(),
            last_release_name
        )

    return (
        number_of_releases,
        'n/a',
        'n/a',
        last_release_name
    )


def get_json_from_pypi(package):
    """
    gets data on the package from pypi
    if the project is not found on pypi returns a
    json a distionary with one entry
    on_pypi : False
    """
    print("Looking for ", package, " on pypi")
    url = str("https://pypi.org/pypi/" + package + "/json")
    data = str('{ "on_pypi" : false, "info" : {"name" : "' + package + '"}}')
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = response.read()
    except urllib.error.HTTPError:
        pass

    return json.loads(data)
