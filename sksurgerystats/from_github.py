from github import Github, GithubException
import os
import subprocess
from github import Github, GithubException


def get_loc(githash, directory="./"):
    """Use git hash of the repository (already cloned in current_dir) to run `cloc` function which counts the lines of code.
    Total parses the cloc output to get the total lines of code and return that.
    """
    current_dir = os.getcwd()
    os.chdir(directory)
    if githash == None:
        githash = subprocess.run(
            ["git", "log", "-n 1", '--pretty=format:"%H"'],
            capture_output=True,
            text=True,
        ).stdout[1:-1]
    loc = subprocess.run(["cloc", githash, "--quiet"], capture_output=True).stdout

    total = 0
    try:
        total = loc.decode("utf-8").replace("-", "").split()[-1]
    except IndexError:
        pass

    os.chdir(current_dir)
    return total, githash


def get_last_commit(project_name, token=None):
    """Use github API to get information on a repository with the passed `project_name`
    and return the last_commit hash key from the default_branch of the repository
    """
    github = Github(token)
    split_name = project_name.split("/")
    try:
        project_name = split_name[-2] + "/" + split_name[-1]
    except IndexError:
        pass

    try:
        rep = github.get_repo(project_name)
    except:
        print("repository not found for " + project_name)
        return None
    try:
        default_branch = rep.get_branch(rep.default_branch)
        last_commit = default_branch.commit.sha[0:7]
    except:
        print("Default branch is empty")
        last_commit = None

    return last_commit


def get_token():
    """Get github personal access token. This function checks if the environment variable
    added as secret.ADMIN_TOKEN exists (ex. inside a GHA) or a local github.token
    file exists, and returns whichever token exists.
    """

    if os.environ.get("admin_token") is not None:
        token = os.environ.get("admin_token")
    else:
        with open("github.token", "r") as token_file:
            token = token_file.read()
            token = token.rstrip("\n")
    return token


def get_github_stats(project_name, token=None):
    """Get in formatation from github. project name can either be
    the github project name or the web address
    """
    rep = "not found"
    stars = 0
    watchers = 0
    forks = 0
    contributors = 0
    create_date = 0
    last_update_date = 0

    split_name = project_name.split("/")
    try:
        project_name = split_name[-2] + "/" + split_name[-1]
    except IndexError:
        pass

    github = Github(token)

    try:
        rep = github.get_repo(project_name)
    except GithubException:
        return rep, stars, watchers, forks, contributors, create_date, last_update_date
    try:
        contributors = len(rep.get_stats_contributors())
    except:
        pass

    stars = rep.stargazers_count
    watchers = rep.watchers_count
    forks = rep.forks_count
    create_date = rep.created_at
    last_update_date = rep.updated_at

    return rep, stars, watchers, forks, contributors, create_date, last_update_date
