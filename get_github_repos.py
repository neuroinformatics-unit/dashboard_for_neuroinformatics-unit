from github import Github
from github.GithubException import RateLimitExceededException

from sksurgerystats.common import add_github_package
from sksurgerystats.from_github import get_token

token = None
token = get_token()

if token is not None:
    g = Github(token)
    reps = g.search_repositories(query="{} in:name".format("neuroinformatics-unit"))

    try:
        for rep in reps:
            add_github_package(rep)
    except RateLimitExceededException:
        print(
            "Got a rate limit exception from Github, probably because ",
            "your search term returned too many matches. ",
            "I've halted adding new libraries from GitHub",
        )
