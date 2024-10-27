# Run from device
import os
import subprocess
import time
from typing import List

from dashcam_backup.params import (
    SERVER_LAPTOP_IP,
    COMMA_DATA_DIR,
    COMMA_CATALOG_FP,
    BACKUP_CATALOG_FP,
    RAW_DATA_DIR,
)


def load_catalog() -> List[str]:
    if os.path.exists(BACKUP_CATALOG_FP):
        with open(BACKUP_CATALOG_FP, "r") as f:
            lines = f.readlines()[1:]
        device_paths = [line.strip().split(",")[0] for line in lines]
    else:
        with open(COMMA_CATALOG_FP, "w") as f:
            f.writelines(["remote_path,local_path,size,downloaded_at\n"])
        device_paths = []
    return device_paths


def download_min_file(
    inpath: str,
    outpath: str,
) -> str:
    subprocess.run(["scp", inpath, f"{SERVER_LAPTOP_IP}:{outpath}"])
    f_size = os.path.getsize(outpath)
    cat_entry = [inpath, outpath, str(f_size), time.ctime()]
    return ",".join(cat_entry) + "\n"


def main():
    dev_paths = load_catalog()

    files_to_download = []
    for root, _, files in os.walk(COMMA_DATA_DIR):
        for f in files:
            src_fp = os.path.join(root, f)
            if src_fp not in dev_paths:
                files_to_download.append(src_fp)

    dirs_to_create = set([os.path.dirname(f) for f in files_to_download])
    existing_dirs = subprocess.run(
        ["ssh", SERVER_LAPTOP_IP, f"ls {RAW_DATA_DIR}"],
        capture_output=True,
        text=True,
    ).stdout.split("\n")
    existing_dirs = [os.path.join(RAW_DATA_DIR, d) for d in existing_dirs]
    for d in dirs_to_create:
        d = d.replace(COMMA_DATA_DIR, RAW_DATA_DIR)
        if d not in existing_dirs:
            subprocess.run(["ssh", SERVER_LAPTOP_IP, f"mkdir -p {d}"])

    new_cat = []
    for src_fp in files_to_download:
        tgt_fp = src_fp.replace(COMMA_DATA_DIR, RAW_DATA_DIR)
        cat_entry = download_min_file(src_fp, tgt_fp)
        new_cat.append(cat_entry)

    if new_cat:
        with open(COMMA_CATALOG_FP, "a") as f:
            f.writelines(new_cat)

    subprocess.run(
        ["scp", COMMA_CATALOG_FP, f"{SERVER_LAPTOP_IP}:{BACKUP_CATALOG_FP}"]
    )

    os.remove(COMMA_CATALOG_FP)


if __name__ == "__main__":
    main()
