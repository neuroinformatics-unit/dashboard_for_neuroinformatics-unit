"""
Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them.
"""

import os.path
from datetime import datetime

from sksurgerystats.common import (
    get_package_information,
    get_packages,
    check_available_badges,
)
from sksurgerystats.html import WriteCellWithLinkedImage, adjustHeaders

if __name__ == "__main__":
    head = ""

    with open("html/dashboard.html.in.head") as filein:
        head = filein.read()
        metric_dictionary = {
            "created_date": "Total Weeks Up",
            "last_update_date": "Latest Update",
            "ci_badge": "CI Status",
            "docs_badge": "Docs",
            "coverage_badge": "Coverage",
            "pepy_downloads_badge": "Downloads with Mirror",
            "lines_of_code": "Lines of Code",
            "stars": "Stars",
            "forks": "Forks",
            "watchers": "Watchers",
            "contributors": "Contributors",
            "syntek_package_health_badge": "Package Health",
            "codeclimate_badge": "Maintainability",
        }
        available_metrics = [
            "Total Weeks Up",
            "Latest Update",
            "Lines of Code",
            "Stars",
            "Forks",
            "Watchers",
            "Contributors",
        ]
        available_badges = check_available_badges()
        available_metrics.extend(
            [
                metric_dictionary[available_badges[i]]
                for i in range(len(available_badges))
            ]
        )
        head = adjustHeaders(head, available_metrics)

    tail = ""
    with open("html/dashboard.html.in.tail") as filein:
        tail = filein.read()

    with open("html/dashboard.html", "w") as fileout:
        fileout.write(head)

        all_packages = os.listdir("libraries/")
        packages = get_packages(sort_key="Created Date")

        for count, package in enumerate(packages):
            first_release = get_package_information(package, "Created Date")
            last_update_date = get_package_information(package, "Last Update")
            lines_of_code = get_package_information(package, "loc")
            stars = get_package_information(package, "GitHub Stars")
            forks = get_package_information(package, "GitHub Forks")
            watchers = get_package_information(package, "GitHub Watchers")
            contributors = get_package_information(package, "GitHub Contributors")
            homepage = get_package_information(package, "home_page")
            if homepage is None:
                homepage = "Not Found"

            badges_dictionary = dict()
            for badge in available_badges:
                badge_link = badge.replace("badge", "target")
                badges_dictionary[badge] = [
                    get_package_information(package, badge),
                    get_package_information(package, badge_link),
                ]

            fileout.write("  <tr>\n")

            short_homepage = homepage
            host_logo = "None"
            logo_spacer = ""
            try:
                short_homepage = homepage.split("/")[2]
                host_logo = short_homepage.split(".")[0]
                if host_logo == "weisslab":
                    host_logo = "gitlab"
            except:
                logo_spacer = ".%20%20%20"
                pass

            package_badge = str(
                "https://img.shields.io/badge/"
                + logo_spacer
                + str(count)
                + "-"
                + package.replace("-", "&#8209")
                + "-orange?style=flat&logo="
                + host_logo,
            )
            WriteCellWithLinkedImage(
                fileout,
                package_badge,
                homepage,
                "Library Homepage",
            )

            weeks_up = 0
            try:
                time_up = datetime.now() - datetime.fromisoformat(str(first_release))
                weeks_up = int(time_up.days / 7)
            except ValueError:
                pass

            weeks_up_badge = None
            weeks_up_target = None
            if weeks_up > 0:
                weeks_up_badge = str(
                    "https://img.shields.io/badge/Weeks%20Up-"
                    + str(weeks_up)
                    + "-green?style=flat",
                )
                weeks_up_target = str(homepage + "/releases")

            WriteCellWithLinkedImage(
                fileout,
                weeks_up_badge,
                weeks_up_target,
                "Total Weeks Up",
            )

            last_update_badge = None
            last_update_target = None
            if last_update_date != "n/a":
                last_update_badge = str(
                    "https://img.shields.io/badge/Last%20Commit-"
                    + str(last_update_date).split("T")[0].replace("-", "%20")
                    + "-green?style=flat",
                )
                last_update_target = str(homepage + "/commits/master")

            WriteCellWithLinkedImage(
                fileout,
                last_update_badge,
                last_update_target,
                "Last Update",
            )

            loc_badge = None
            loc_link = str("loc/" + package + ".html")
            if lines_of_code is not None:
                loc_badge = str(
                    "https://img.shields.io/badge/LOC-"
                    + str(lines_of_code)
                    + "-blue?style=flat",
                )

            WriteCellWithLinkedImage(fileout, loc_badge, loc_link, "Lines of Code")

            github_user = get_package_information(package, "GitHub User")
            stars_badge = None
            forks_badge = None
            watchers_badge = None
            contrib_badge = None
            if github_user is not None:
                stars_badge = str(
                    "https://img.shields.io/github/stars/"
                    + github_user
                    + "/"
                    + package
                    + "?style=social",
                )
                forks_badge = str(
                    "https://img.shields.io/github/forks/"
                    + github_user
                    + "/"
                    + package
                    + "?style=social",
                )
                watchers_badge = str(
                    "https://img.shields.io/github/watchers/"
                    + github_user
                    + "/"
                    + package
                    + "?style=social",
                )
                contrib_badge = str(
                    "https://img.shields.io/badge/contrib-"
                    + str(contributors)
                    + "-lightgrey?style=social&logo=github",
                )

            WriteCellWithLinkedImage(
                fileout,
                stars_badge,
                str(homepage + "/stargazers"),
                "GitHub Stars",
            )

            WriteCellWithLinkedImage(
                fileout,
                forks_badge,
                str(homepage + "/forks"),
                "GitHub Forks",
            )

            WriteCellWithLinkedImage(
                fileout,
                watchers_badge,
                str(homepage + "/watchers"),
                "GitHub Watchers",
            )

            WriteCellWithLinkedImage(
                fileout,
                contrib_badge,
                str(homepage + "/graphs/contributors"),
                "GitHub Contributors",
            )

            # write the badges to the HTMLs
            for badge in badges_dictionary:
                description = metric_dictionary[badge]
                WriteCellWithLinkedImage(
                    fileout, badges_dictionary[badge][0],
                    badges_dictionary[badge][1], description
                )


            fileout.write("  </tr>\n")

        fileout.write(tail)

    head = ""
    with open("html/excluded.html.in.head") as filein:
        head = filein.read()

    tail = ""
    with open("html/excluded.html.in.tail") as filein:
        tail = filein.read()

    with open("html/exclusions.html", "w") as fileout:
        fileout.write(head)

        excluded_packages = get_packages(
            sort_key=None,
            path="libraries/exclusions/",
            exclusions_path="not a path",
        )

        for new_count, package in enumerate(excluded_packages):
            homepage = get_package_information(package, "home_page")
            if homepage is None:
                homepage = "Not Found"

            fileout.write("  <tr>\n")

            short_homepage = homepage
            host_logo = "None"
            logo_spacer = ""
            try:
                short_homepage = homepage.split("/")[2]
                host_logo = short_homepage.split(".")[0]
                if host_logo == "weisslab":
                    host_logo = "gitlab"
            except:
                logo_spacer = ".%20%20%20"
                pass

            package_badge = str(
                "https://img.shields.io/badge/"
                + logo_spacer
                + str(count + new_count + 1)
                + "-"
                + package.replace("-", "&#8209")
                + "-orange?style=flat&logo="
                + host_logo,
            )
            WriteCellWithLinkedImage(
                fileout,
                package_badge,
                homepage,
                "Library Homepage",
            )

            reason = get_package_information(
                package,
                "obsolete",
                path="libraries/exclusions/",
            )
            fileout.write("    <td>\n")
            fileout.write("      <p>" + str(reason) + "</p>\n")
            fileout.write("    </td>\n")

            fileout.write("  </tr>\n")

        fileout.write(tail)
