# Run from device
import os
import time
import logging
import subprocess

from dashcam_backup.params import (
    SERVER_LAPTOP_IP,
    COMMA_IP,
    COMMA_DATA_DIR,
    BACKUP_DIR,
    RAW_DATA_DIR,
)


def setup_logging():
    logging.basicConfig(
        filename = os.path.join(BACKUP_DIR, "rsync_backup.log"),
        level = logging.INFO,
        format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)

    return logger


def main():
    logger = setup_logging()

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

