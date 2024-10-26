# Run from device
import os
import subprocess
import pandas as pd
from datetime import datetime
from typing import Dict, Union

from dashcam_backup.params import (
    SERVER_LAPTOP_IP,
    COMMA_DATA_DIR,
    COMMA_CATALOG_FP,
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
    subprocess.run(["scp", inpath, f"{SERVER_LAPTOP_IP}:{outpath}"])
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


def main():
    cat = load_catalog()

    new_cat = []
    for root, _, files in os.walk(COMMA_DATA_DIR):
        for f in files:
            src_fp = os.path.join(root, f)
            if f not in cat["remote_path"].values:
                tgt_fp = src_fp.replace(COMMA_DATA_DIR, BACKUP_DIR)
                cat_entry = download_min_file(
                    src_fp, tgt_fp, os.path.getsize(src_fp)
                )
                new_cat.append(cat_entry)

    if new_cat:
        new_cat = pd.concat([cat, pd.DataFrame(new_cat)])
        new_cat.to_csv(BACKUP_CATALOG_FP, index=False)

    subprocess.run(
        ["scp", COMMA_CATALOG_FP, f"{SERVER_LAPTOP_IP}:{BACKUP_CATALOG_FP}"]
    )

    os.remove(COMMA_CATALOG_FP)


if __name__ == "__main__":
    main()
