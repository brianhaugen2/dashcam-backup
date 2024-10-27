#!/usr/bin/env bash

git pull
docker build -t dashcam-backup:latest .
docker kill dashcam-backup
docker rm dashcam-backup
docker run -d \
--name dashcam-backup \
--restart always \
-v /home/brian/.ssh:/home/brian/.ssh \
-v /media/:/media/ \
dashcam-backup:latest \
python dashcam_backup/main.py