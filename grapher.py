import argparse
import datetime
import pathlib
import string

import pandas as pd
import numpy as np
import git

RNG = np.random.default_rng(123)



def load_art(csv_path: str) -> list[list[int]]:
    df = pd.read_csv(csv_path, index_col="Day", header=0)
    return df.T.to_numpy().tolist()

def flat_dummy()-> list[list[int]]:
    return [[1 for _ in range(7)] for __ in range(50)]


def get_date_zero()-> datetime.datetime:
    now = datetime.datetime.now(datetime.UTC)
    delta_to_sunday = (now.weekday() + 1) % 7
    this_sunday = now - datetime.timedelta(days=delta_to_sunday)
    zero_date = this_sunday - datetime.timedelta(days=7*51)
    return zero_date

def spoof_commit(repo_root: pathlib.Path, date_zero: datetime.datetime, day: int, week: int, target_file: str = "dummy_data.txt", data_size: int = 32) -> None:
    REPO = git.Repo(repo_root)
    data = "".join(RNG.choice(a=list(string.ascii_letters), size=data_size).tolist())
    
    target_path = repo_root.joinpath(target_file)
    with open(target_path, "w") as fout:
        fout.write(data)

    delta_days = 7*week + day
    fake_date = date_zero + datetime.timedelta(days=delta_days)

    REPO.index.add(target_path)
    REPO.index.commit(f"Commit for day={day} week={week}", author_date=fake_date, commit_date=fake_date)
    REPO.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_repo", type=pathlib.Path)
    parser.add_argument("--csv-art", required=False, default=None)
    args = parser.parse_args()

    if args.csv_art is not None:
        data = load_art(args.csv_art)
    else:
        data = flat_dummy()
    
    date_zero = get_date_zero()
    
    for w_idx, week_list in enumerate(data):
        for d_idx, day_value in enumerate(week_list):
            for _ in range(day_value):
                spoof_commit(
                    repo_root=args.target_repo,
                    date_zero=date_zero,
                    day=d_idx,
                    week=w_idx
                )
    



