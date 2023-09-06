"""
Get package information

Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them.

"""
import contextlib
import os.path

import requests
from requests.exceptions import SSLError
import json

from sksurgerystats.common import (
    get_packages,
    get_package_information,
    update_package_information,
)

if __name__ == "__main__":
    packages = get_packages()

    badges = {
        "total": 0,
        "ci_badge": 0,
        "coverage_badge": 0,
        "docs_badge": 0,
        "codeclimate_badge": 0,
        "pepy_downloads_badge": 0,
        "syntek_package_health_badge": 0,
    }

    for package in packages:
        print("Getting badges for ", package)
        ci_badge = get_package_information(package, "ci_badge")
        ci_target = get_package_information(package, "ci_target")
        coverage_badge = get_package_information(package, "coverage_badge")
        coverage_target = get_package_information(package, "coverage_target")
        docs_badge = get_package_information(package, "docs_badge")
        docs_target = get_package_information(package, "docs_target")
        codeclimate_badge = get_package_information(package, "codeclimate_badge")
        codeclimate_target = get_package_information(package, "codeclimate_target")
        pepy_downloads_badge = get_package_information(package, "pepy_downloads_badge")
        pepy_downloads_target = get_package_information(
            package,
            "pepy_downloads_target",
        )
        syntek_package_health_badge = get_package_information(
            package,
            "syntek_package_health_badge",
        )
        syntek_package_health_target = get_package_information(
            package,
            "syntek_package_health_target",
        )

        homepage = get_package_information(package, "home_page")
        if homepage is not None:
            project_name = homepage
            split_name = project_name.split("/")
            badges["total"] += 1
            with contextlib.suppress(IndexError):
                project_name = split_name[-2] + "/" + split_name[-1]

            if ci_badge is None:
                ci_badge = str(
                    homepage + "/workflows/.github/workflows/ci.yml/badge.svg",
                )
            if ci_target is None:
                ci_target = str(homepage + "/actions")

            if coverage_badge is None:
                coverage_badge = str(
                    "https://coveralls.io/repos/github/"
                    + project_name
                    + "/badge.svg?branch=master&service=github",
                )
            if coverage_target is None:
                coverage_target = str(
                    "https://coveralls.io/github/" + project_name + "?branch=master",
                )

            if docs_badge is None:
                docs_badge = str(
                    "https://readthedocs.org/projects/"
                    + package
                    + "/badge/?version=latest",
                )
            if docs_target is None:
                docs_target = str(
                    "https://" + package + ".readthedocs.io/en/latest/?badge=latest",
                )

            if codeclimate_badge is None:
                # doesn't seem a straight forward way here
                pass
            if codeclimate_target is None:
                codeclimate_target = str(
                    "https://codeclimate.com/github/" + project_name,
                )

            if pepy_downloads_badge is None:
                pepy_downloads_badge = str("https://static.pepy.tech/badge/" + package)
            # always update this
            if pepy_downloads_target is None:
                pepy_downloads_target = str(
                    "https://pepy.tech/projects/" + package)

            if syntek_package_health_badge is None:
                syntek_package_health_badge = str(
                    "https://snyk.io/advisor/python/" + package + "/badge.svg",
                )
            if syntek_package_health_target is None:
                syntek_package_health_target = str(
                    "https://snyk.io/advisor/python/" + package,
                )

        # check and update ci
        if ci_badge is not None:
            req = requests.get(ci_badge)
            if req.status_code == 200:
                badges["ci_badge"] = badges["ci_badge"] + 1
                update_package_information(
                    package,
                    "ci_badge",
                    ci_badge,
                    overwrite=True,
                )

        if ci_target is not None:
            req = requests.get(ci_target)
            if req.status_code == 200:
                update_package_information(
                    package,
                    "ci_target",
                    ci_target,
                    overwrite=True,
                )

        # cheek and update coverage
        if coverage_badge is not None:
            req = requests.get(coverage_badge)
            if req.status_code == 200:
                badges["coverage_badge"] = badges["coverage_badge"] + 1
                update_package_information(
                    package,
                    "coverage_badge",
                    coverage_badge,
                    overwrite=True,
                )

        if coverage_target is not None:
            req = requests.get(coverage_target)
            if req.status_code == 200:
                update_package_information(
                    package,
                    "coverage_target",
                    coverage_target,
                    overwrite=True,
                )

        if docs_badge is not None:
            try:
                try:
                    req = requests.get(docs_badge)
                except:
                    req = requests.get(docs_badge, verify=False)
                    # This conditional protects against some of the certificate errors we got with especially excluded libraries
            except SSLError as e:
                print("SSL version or cipher mismatch error occurred:", e)
                # Handle the error or continue with other operations
                pass

            if req.status_code == 200:
                badges["docs_badge"] += 1
                update_package_information(
                    package,
                    "docs_badge",
                    docs_badge,
                    overwrite=False,
                )

        # This conditional protects against some of the certificate errors we got with especially excluded libraries
        if docs_target is not None:
            try:
                try:
                    req = requests.get(docs_target)
                except:
                    req = requests.get(docs_target, verify=False)
            except SSLError as e:
                print("SSL version or cipher mismatch error occurred:", e)
                # Handle the error or continue with other operations
                pass
            if req.status_code == 200:
                update_package_information(
                    package,
                    "docs_target",
                    docs_target,
                    overwrite=True,
                )

        # check and update codeclimate
        if codeclimate_badge is not None:
            req = requests.get(codeclimate_badge)
            if req.status_code == 200:
                badges["codeclimate_badge"] += 1
                update_package_information(
                    package,
                    "codeclimate_badge",
                    codeclimate_badge,
                    overwrite=True,
                )

        if codeclimate_target is not None:
            req = requests.get(codeclimate_target)
            if req.status_code == 200:
                update_package_information(
                    package,
                    "codeclimate_target",
                    codeclimate_target,
                    overwrite=True,
                )

        # check and update pepy_downloads
        if pepy_downloads_badge is not None:
            req = requests.get(pepy_downloads_badge)
            if req.status_code == 200:
                badges["pepy_downloads_badge"] += 1
                update_package_information(
                    package,
                    "pepy_downloads_badge",
                    pepy_downloads_badge,
                    overwrite=True,
                )

        if pepy_downloads_target is not None:
            req = requests.get(pepy_downloads_target)
            if req.status_code == 200:
                update_package_information(
                    package,
                    "pepy_downloads_target",
                    pepy_downloads_target,
                    overwrite=True,
                )

        # check and update syntek_package_health
        if syntek_package_health_badge is not None:
            req = requests.get(syntek_package_health_badge)
            if req.status_code == 200:
                badges["syntek_package_health_badge"] += 1
                update_package_information(
                    package,
                    "syntek_package_health_badge",
                    syntek_package_health_badge,
                    overwrite=True,
                )

        if syntek_package_health_target is not None:
            req = requests.get(syntek_package_health_target)
            if req.status_code == 200:
                update_package_information(
                    package,
                    "syntek_package_health_target",
                    syntek_package_health_target,
                    overwrite=True,
                )

    with open("libraries/available_badges.json", "w") as fileout:
        json.dump(badges, fileout, default=str)
