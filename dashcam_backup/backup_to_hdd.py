import os
import time
import subprocess

from dashcam_backup.params import (
    COMMA_IP,
    COMMA_DATA_DIR,
    RAW_DATA_DIR,
    BACKUP_LOG_FN,
    T_DELAY,
    TRANSFER_LOCK,
    SSH_TIMEOUT,
)
from dashcam_backup.utils import (
    setup_logging
)


def main():
    logger = setup_logging(BACKUP_LOG_FN)

    i = 1
    while True:
        logger.info(f"Loop {i}")
        start_t = time.time()
        try:
            # check if device is online
            result = subprocess.run(
                ["ssh",
                 "-o", f"ConnectTimeout={SSH_TIMEOUT}",
                 "-o", "StrictHostKeyChecking=no",
                 "-o", "BatchMode=yes",
                 COMMA_IP, "ls"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # if device is online, transfer data
            if result.returncode == 0:
                logger.info("Device online, starting transfer")
                # Create lock file to prevent conversion from starting
                with open(TRANSFER_LOCK, "w") as f:
                    f.write("1")

                try:
                    # Transfer data
                    result = subprocess.run(
                        ["rsync",
                         "-e", f"ssh -o ConnectTimeout={SSH_TIMEOUT} -o StrictHostKeyChecking=no",
                         f"{COMMA_IP}:{COMMA_DATA_DIR}*",
                         RAW_DATA_DIR, "-av", "--timeout=120"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    if result.returncode == 0:
                        logger.info("Transfer complete")
                        if result.stdout:
                            logger.info(result.stdout)
                    else:
                        logger.warning(f"rsync failed (exit {result.returncode}): {result.stderr.strip()}")
                finally:
                    # Always clean up lock file, even if rsync fails
                    if os.path.exists(TRANSFER_LOCK):
                        os.remove(TRANSFER_LOCK)
            else:
                logger.info(f"Device offline (ssh exit {result.returncode})")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # Clean up lock file on unexpected errors too
            if os.path.exists(TRANSFER_LOCK):
                os.remove(TRANSFER_LOCK)

        # Sleep for T_DELAY sec
        elapsed = time.time() - start_t
        if elapsed < T_DELAY:
            sleep_time = T_DELAY - elapsed
            logger.info(f"Sleeping for {sleep_time:.0f} sec")
            time.sleep(sleep_time)

        i += 1


if __name__ == "__main__":
    main()
