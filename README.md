# Git Spoofer
Channel your vision for the perfect GitHub activity graph!

Using the scripts in this repo you can generate an arbitrary number of commits for the repo of your choice.
Also included is a handy resetter script to clean the canvas and start from scratch.

## Setup
### Variables
For the grapher script all you need to do is set the following environment variables:
- `SPOOF_USER` your GitHub username
- `SPOOF_EMAIL` your GitHub email

To use the reset script you will also need to create a [fine grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) with "Administration" repository permissions (write).
Set the token into the environment variable `GITHUB_TOKEN` and you are good to go

### Python
Dependencies are managed using [poetry](https://python-poetry.org/): after installing it just run
```shell
poetry install --no-root
```
to create the virtual environment.

## Usage
To run the grapher script use the command 
```shell
poetry run python grapher.py [PATH TO TARGET REPO]
```

To run the resetter script use the command
```shell
poetry run python resetter.py [PATH TO TARGET REPO]
```