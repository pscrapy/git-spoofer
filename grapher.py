import argparse
import datetime
import os
import pathlib
import string

import git
import numpy as np
import tqdm
import pandas as pd

WEEK_RANGE = 51
USER = os.environ["SPOOF_USER"]
EMAIL = os.environ["SPOOF_EMAIL"]
SEED = os.getenv("RNG_SEED", 123)

RNG = np.random.default_rng(SEED)

def load_art(csv_path: str) -> list[list[int]]:
    df = pd.read_csv(csv_path, index_col="Day", header=0)
    return df.T.to_numpy().tolist()

def random_dummy(dmin: int, dmax: int)-> list[list[int]]:
    return [[RNG.integers(low=dmin,high=dmax) for _ in range(7)] for __ in range(WEEK_RANGE)]


def get_date_zero()-> datetime.datetime:
    now = datetime.datetime.now(datetime.UTC)
    delta_to_sunday = (now.weekday() + 1) % 7
    this_sunday = now - datetime.timedelta(days=delta_to_sunday)
    zero_date = this_sunday - datetime.timedelta(days=7*WEEK_RANGE)
    return zero_date

def spoof_commit(repo_root: pathlib.Path, date_zero: datetime.datetime, day: int, week: int, target_file: str = "dummy_data.txt", data_size: int = 32) -> None:
    REPO = git.Repo(repo_root)
    AUTHOR = git.Actor(name=USER, email=EMAIL)
    data = "".join(RNG.choice(a=list(string.ascii_letters), size=data_size).tolist())

    target_path = repo_root.joinpath(target_file)
    with open(target_path, "w") as fout:
        fout.write(data)

    delta_days = 7*week + day
    fake_date = date_zero + datetime.timedelta(days=delta_days)

    REPO.index.add(target_path)
    REPO.index.commit(f"Commit for day={day} week={week}", 
                      author_date=fake_date, commit_date=fake_date, 
                      committer=AUTHOR, author=AUTHOR)
    REPO.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_repo", type=pathlib.Path)
    parser.add_argument("--csv-art", required=False, default=None)
    parser.add_argument("--dummy-min", type=int, default=0, required=False)
    parser.add_argument("--dummy-max", type=int, default=10, required=False)
    args = parser.parse_args()

    if args.csv_art is not None:
        data = load_art(args.csv_art)
    else:
        data = random_dummy(args.dummy_min, args.dummy_max)

    date_zero = get_date_zero()

    for w_idx, week_list in enumerate(tqdm.tqdm(data)):
        for d_idx, day_value in enumerate(week_list):
            for _ in range(day_value):
                spoof_commit(
                    repo_root=args.target_repo,
                    date_zero=date_zero,
                    day=d_idx,
                    week=w_idx,
                )




