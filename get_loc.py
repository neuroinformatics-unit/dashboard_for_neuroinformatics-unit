"""
Searches for packages on pypi with SciKit-Surgery in the name, then
gets some statistics for them.
"""
import os.path
import shutil
import subprocess
import sys
from github import Github, GithubException

from sksurgerystats.common import (
    get_package_information,
    get_packages,
    update_package_information,
)
from sksurgerystats.from_github import (
    get_last_commit,
    get_loc,
    get_token,
)
from sksurgerystats.html import load_cache_file, make_html_file, write_to_js_file

if __name__ == "__main__":
    temp_dir = os.path.join(os.getcwd(), "temp")
    if len(sys.argv) == 2:
        temp_dir = sys.argv[1]

    packages = get_packages()

    token = None
    token = get_token()

    # cleanup of temp directory if script couldn't complete the last time it was run
    shutil.rmtree(temp_dir, ignore_errors=True)

    for package in packages:
        try:
            homepage = get_package_information(package, "home_page")
        except:
            continue

        print("Counting lines of ", package)

        cache_file = str("libraries/lines_of_code/" + package + ".js")
        html_file = str("loc/" + package + ".html")
        if not os.path.exists(cache_file):
            with open(cache_file, "w") as my_empty_loc_file:
                # now you have an empty file already
                pass
        git_hashes = load_cache_file(cache_file)
        last_hash = git_hashes if isinstance(git_hashes, str) else None

        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        if homepage is not None:
            last_commit = get_last_commit(homepage, token)
            if last_commit is None:
                continue
            if last_commit in git_hashes:
                print("No need to update ", package, " skipping")
                continue
            try:
                subprocess.run(["git", "clone", "--depth", "1", homepage, temp_dir])
                last_loc, last_hash = get_loc(
                    last_hash, temp_dir
                )  # we also return an updated last_hash if it was empty earlier
                update_package_information(package, "loc", last_loc, overwrite=True)
                write_to_js_file(last_hash, cache_file)
                make_html_file(package, cache_file)
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                print(package, "  is not available")
                shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print(package, " has no homepage")
