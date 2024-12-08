# Run from device
import time
import subprocess

from dashcam_backup.params import (
    COMMA_IP,
    COMMA_DATA_DIR,
    RAW_DATA_DIR,
    BACKUP_LOG_FN
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
        result = subprocess.run(
            ["rsync", f"{COMMA_IP}:{COMMA_DATA_DIR}/*", f"{RAW_DATA_DIR}", "-av"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)

        if (time.time() - start_t) < 60:
            logger.info(f"Sleeping for {60 - time.time() + start_t} sec")
            time.sleep(60 - time.time() + start_t)

        i += 1


if __name__ == "__main__":
    main()
