"""
Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them
"""

import os.path
import urllib.request
import requests
import subprocess
import json
import re
from datetime import datetime

# packages = os.system('./pypi-simple-search scikit-surgery')


def check_available_badges(path="libraries/", inclusion_policy=0.5):
    """ """
    filename = str(path + "available_badges.json")
    available_badges = []
    checked_badges = []
    with open(filename, "r") as filein:
        try:
            available_badges = json.load(filein)
        except json.JSONDecodeError:
            available_badges = {}

    for badge in available_badges.keys():
        if badge != "total":
            badge_availability = available_badges[badge] / available_badges["total"]
            if badge_availability >= inclusion_policy:
                checked_badges.append(badge)

    return checked_badges


def get_list_of_packages(all_packages, path="libraries/"):
    """
    For the given list, filter for the actual list of available packages with:
    1. check the package in libraries path exists
    2. doesn't end with txt
    3. doesn't have whitespaces
    4. doesn't start with .
    5. excludes available_badges.json

    """
    packages = []
    for package in all_packages:
        if (
            not os.path.isdir(path + package)
            and not package.endswith(".txt")
            and not re.search(r"\s", package)
            and not package.startswith(".")
            and not package == 'available_badges.json'
        ):
            packages.append(package)
    return packages


def add_packages(packages, path="libraries/"):
    """
    Searches through path directory for marker files
    for each package in list, creates file if not already present
    """
    for package in packages:
        filename = str("libraries/" + package)
        if not os.path.isfile(filename):
            print("Found new package ", package)
            with open(filename, "w"):
                pass


def add_github_package(github_rep, path="libraries/"):
    """
    Searches through path directory for marker files
    for the package, creates file if not already present
    and writes home_page entry
    """
    filename = str("libraries/" + github_rep.name)
    if not os.path.isfile(filename):
        print("Found new package ", github_rep.full_name)
        with open(filename, "w") as fileout:
            configuration = {"home_page": github_rep.html_url}
            json.dump(configuration, fileout)


def update_package_information(package, key, entry, overwrite=False, path="libraries/"):
    """
    adds key and entry to a dictionary for the given package.
    If overwrite is false it will not overwrite existing
    entries
    """
    filename = str("libraries/" + package)
    configuration = None
    with open(filename, "r") as filein:
        try:
            configuration = json.load(filein)
        except json.JSONDecodeError:
            configuration = {}

    if configuration.get(key, None) is None:
        configuration[key] = entry
    else:
        if overwrite:
            configuration[key] = entry

    with open(filename, "w") as fileout:
        configuration = json.dump(configuration, fileout, default=str)


def get_package_information(package, key, path="libraries/"):
    """
    returns a key value for a given package, returns None
    if key not present
    """
    filename = str(path + package)
    configuration = None
    with open(filename, "r") as filein:
        try:
            configuration = json.load(filein)
        except json.JSONDecodeError:
            configuration = {}

    return configuration.get(key, None)


def get_packages(
    sort_key=None, path="libraries/", exclusions_path="libraries/exclusions/"
):
    """
    returns a list of of packages, and optionally sorts by
    the sort key
    """
    all_packages = [f for f in os.listdir(path) if not f.startswith('.')] 
    packages = get_list_of_packages(all_packages)

    if sort_key is None:
        return packages

    package_dictionaries = []
    for package in packages:
        sort_key_return = get_package_information(package, sort_key, path)
        if sort_key_return == None:
            print(
                "Not able to fetch necessary information on package "
                + package
                + ", omitting from dashboard."
            )
        else:
            package_dictionaries.append(
                {
                    "package": package,
                    "sort key": get_package_information(package, sort_key, path),
                }
            )
    # now that Created Date is the sort key, we need to convert it to str() to use in key. Also we set reverse to True so on top of the list
    # we get the package that is the latest created
    sorted_dicts = sorted(
        package_dictionaries, key=lambda k: str(k["sort key"]), reverse=True
    )

    packages = []
    for sorted_dict in sorted_dicts:
        packages.append(sorted_dict.get("package"))

    return packages


def update_badge_links(badge_name, link_with_placeholder):
    """
    Updates the badge information for all packages, ie if link for given package needs to be corrected, or a new badge needs to be added
    badge_name = name of badge, refer to get_badges.py for correct naming, ex. pepy_downloads_target
    link_with_placeholder = html link for the given badge, use a placeholder "packagename" str
    instead of the library's name in given path, ex. 'https://pepy.tech/packagename?branch=master'
    """
    all_packages = os.listdir("libraries/")
    packages = get_list_of_packages(all_packages)

    for package in packages:
        print("Updating badge " + badge_name + "for ", package)
        badge = get_package_information(package, badge_name)
        homepage = get_package_information(package, "home_page")

        badge = link_with_placeholder.replace("packagename", package)
        req = requests.get(badge)
        if req.status_code == 200:
            update_package_information(package, badge_name, badge, overwrite=True)
