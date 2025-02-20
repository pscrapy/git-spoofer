import os
import pathlib
import logging
import argparse

import git
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
USER = os.environ["SPOOF_USER"]

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def delete_remote(repo_name: str) -> None:
    url = f"https://api.github.com/repos/{USER}/{repo_name}"
    heads = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    resp = requests.delete(
        url=url,
        headers=heads
    )
    logger.info("Delete request returned code %s" % resp.status_code)
    if resp.status_code != 204:
        logger.error("Repo delete failed")
        raise RuntimeError("Repo deletion failed")



def create_remote(repo_name: str) -> None:
    url = "https://api.github.com/user/repos"
    heads = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    payload = {
        "name": repo_name,
        "private": True
    }
    resp = requests.post(
        url=url,
        headers=heads,
        json=payload
    )
    logger.info("Create request returned code %s" % resp.status_code)
    if resp.status_code != 201:
        logger.error("Repo create failed")
        raise RuntimeError("Repo creation failed")



def reset_repo(repo_root: pathlib.Path) -> None:
    repo_name = repo_root.parts[-1]
    REPO = git.Repo(repo_root)
    REPO.git.reset('--hard', "ROOT")
    logger.info("Reset repo to ROOT tag")

    delete_remote(repo_name)
    create_remote(repo_name)

    REPO.git.push("--set-upstream")
    logger.info("Pushed clean repo to upstream")
    REPO.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_repo", type=pathlib.Path)
    args = parser.parse_args()

    reset_repo(args.target_repo)