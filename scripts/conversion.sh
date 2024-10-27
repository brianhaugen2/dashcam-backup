#!/usr/bin/env bash

docker run -d \
--name rlog-conversion \
-v /media:/media \
-v /home/brian/repos/dashcam-backup:/tmp/dashcam-backup \
ghcr.io/commaai/openpilot-prebuilt \
cd /tmp/dashcam-backup && \
pip install . && \
python scripts/rlog_to_parquet.py