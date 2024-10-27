# run from server
import os
import time
import shutil
import subprocess
import pandas as pd

from dashcam_backup.params import (
    COMMA_IP,
    COMMA_DATA_DIR,
    BACKUP_CATALOG_FP,
    COMMA_CATALOG_FP,
    ARCHIVE_CATALOG_FP,
    RAW_DATA_DIR,
    WANTED_COMMA_FILES,
)


def check_for_missing_files(cat: pd.DataFrame) -> pd.DataFrame:
    # check for local files not in the catalog
    missing = []
    for root, _, files in os.walk(RAW_DATA_DIR):
        for f in files:
            fp = os.path.join(root, f)
            if fp not in cat["local_path"].values and f in WANTED_COMMA_FILES:
                missing.append({
                    "remote_path": "missing",
                    "local_path": fp,
                    "size": "missing",
                    "downloaded_at": time.ctime()
                })

    # add missing file to catalog
    if missing:
        cat = pd.concat([cat, pd.DataFrame(missing)])

    return cat

def catalog_validation():
    # read the catalog
    cat = pd.read_csv(BACKUP_CATALOG_FP)

    # check if the tgt_path from copy exists
    cat["local_exists"] = cat["local_path"].apply(os.path.exists)

    # check if the local size is similar to the remote size
    cat["local_size"] = cat["local_path"].apply(
        lambda x: os.path.getsize(x) if os.path.exists(x) else 0
    )
    cat["same_size"] = cat.apply(
        lambda x: x["local_size"] == int(x["size"])
        if x["size"] != "missing" else False,
        axis=1
    )

    # remove rows from catalog that do not exist or incomplete
    cat = cat.loc[cat["local_exists"] & cat["same_size"]]

    # check for local files not in the catalog
    cat = check_for_missing_files(cat)

    # save the updated catalog
    cat.to_csv(BACKUP_CATALOG_FP, index=False)


def main():
    resp = subprocess.run(
        ["ssh", COMMA_IP, "ls", COMMA_DATA_DIR],
        capture_output=True,
        text=True
    )
    device_online = len(resp.stdout) > 0

    if device_online:
        # update code on the device before running the backup
        subprocess.run([
            "ssh", COMMA_IP,
            "cd /data/media/0/dashcam-backup && git pull && pip install ."
        ])

        if os.path.exists(BACKUP_CATALOG_FP):
            # archive the old catalog
            shutil.copy(BACKUP_CATALOG_FP, ARCHIVE_CATALOG_FP)

            # send the catalog to the device
            subprocess.run(
                ["scp", BACKUP_CATALOG_FP, f"{COMMA_IP}:{COMMA_CATALOG_FP}"]
            )

        # have the device copy over the new files to the server
        # script send updated catalog back to server
        subprocess.run([
            "ssh", COMMA_IP,
            "bash /data/media/0/dashcam-backup/dashcam_backup/startup.sh"
        ])

        # remove files from catalog that didn't copy correctly
        catalog_validation()


if __name__ == "__main__":
    while True:
        main()
        # sleep for 5 minutes
        time.sleep(300)
