import os


COMMA_DATA_DIR = "/data/media/0/realdata/"
COMMA_IP = "comma@192.168.10.154"
COMMA_CATALOG_FP = "/tmp/catalog.csv"
SERVER_LAPTOP_IP = "brian@192.168.10.174"
BACKUP_DIR = "/media/brian/7ef70690-cfa7-4aea-9ae2-cb402f50dec0/dashcam_backup/"
WANTED_COMMA_FILES = [
    "dcamera.hevc",
    "ecamera.hevc",
    "fcamera.hevc",
    "qcamera.ts",
    "qlog",
    "rlog",
]
BACKUP_CATALOG_FP = os.path.join(BACKUP_DIR, "catalog.csv")
ARCHIVE_CATALOG_FP = os.path.join(BACKUP_DIR, "catalog_archive.csv")
