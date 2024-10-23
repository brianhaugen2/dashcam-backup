import os
import subprocess
import pandas as pd
from datetime import datetime
from typing import Dict, Union, List

from dashcam_backup.params import (
    COMMA_IP,
    COMMA_DATA_DIR,
    WANTED_COMMA_FILES,
    BACKUP_DIR,
    BACKUP_CATALOG_FP,
)


def load_catalog() -> pd.DataFrame:
    if os.path.exists(BACKUP_CATALOG_FP):
        cat = pd.read_csv(BACKUP_CATALOG_FP)
    else:
        cat = pd.DataFrame(
            columns=["remote_path", "local_path", "size", "downloaded_at"]
        )
    return cat


def download_min_file(
    inpath: str,
    outpath: str,
    f_size: int,
) -> Dict[str, Union[str, int, datetime]]:
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    subprocess.run(["scp", f"{COMMA_IP}:{inpath}", outpath])
    print(f"Downloaded {inpath} to {outpath}")
    if os.path.exists(outpath):
        local_f_size = os.path.getsize(outpath)
        if local_f_size == f_size:
            cat_entry = {
                "remote_path": inpath,
                "local_path": outpath,
                "size": f_size,
                "downloaded_at": datetime.now(),
            }
            return cat_entry


def download_min_folder(
    min_dir: str,
    d: str,
    cat: pd.DataFrame,
) -> List[Dict[str, Union[str, int, datetime]]]:
    min_files = subprocess.run(
        ["ssh", COMMA_IP, "ls", "-la", min_dir],
        capture_output=True,
        text=True
    ).stdout.split("\n")
    min_cat = []
    for f_str in min_files[3:-1]:
        f = f_str.split()
        if len(f) > 8:
            f_name = f[-1]
            f_size = f[4]
            f_size = int(f_size)
            if f_name in WANTED_COMMA_FILES:
                inpath = os.path.join(min_dir, f_name)
                outpath = os.path.join(BACKUP_DIR, d, f_name)
                if not cat["local_path"].isin([outpath]).any():
                    cat_entry = download_min_file(inpath, outpath, f_size)
                    if cat_entry:
                        min_cat.append(cat_entry)
    return min_cat


def main():
    cat = load_catalog()

    remote_folders = subprocess.run(
        ["ssh", COMMA_IP, "ls", COMMA_DATA_DIR],
        capture_output=True,
        text=True
    ).stdout.split("\n")

    new_cat = []
    for d in remote_folders:
        min_dir = os.path.join(COMMA_DATA_DIR, d)
        min_cat = download_min_folder(min_dir, d, cat)
        new_cat += min_cat

    if new_cat:
        new_cat = pd.concat([cat, pd.DataFrame(new_cat)])
        new_cat.to_csv(BACKUP_CATALOG_FP, index=False)


if __name__ == "__main__":
    main()
