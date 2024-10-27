#!/usr/bin/env bash

docker container rm rlog-conversion && \
docker run -it \
--entrypoint bash \
--name rlog-conversion \
-v /media:/media \
-v /home/brian/repos/dashcam-backup:/tmp/dashcam-backup \
ghcr.io/commaai/openpilot-prebuilt \
cd /tmp/dashcam-backup && \
python scripts/rlog_to_parquet.py
