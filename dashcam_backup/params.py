import os


COMMA_DATA_DIR = "/data/media/0/realdata/"
COMMA_IP = "comma@192.168.10.154"
COMMA_CATALOG_FP = "/tmp/catalog.csv"
SERVER_LAPTOP_IP = "brian@192.168.10.11"
WANTED_COMMA_FILES = [
    "dcamera.hevc",
    "ecamera.hevc",
    "fcamera.hevc",
    "qcamera.ts",
    "qlog",
    "rlog",
]
BACKUP_DIR = "/media/brian/ac8adcce-128e-4090-998e-40f2f6da43f1/dashcam_backup/"
BACKUP_CATALOG_FP = os.path.join(BACKUP_DIR, "catalog.csv")
ARCHIVE_CATALOG_FP = os.path.join(BACKUP_DIR, "catalog_archive.csv")
RAW_DATA_DIR = os.path.join(BACKUP_DIR, "raw_data/")
BACKUP_LOG_FN = "rsync_backup.log"
TRANSFER_LOCK = os.path.join(RAW_DATA_DIR, "transfer.lock")
T_DELAY = 300
