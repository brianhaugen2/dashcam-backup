#!/usr/bin/env bash

git pull
docker build -t dash-backup:latest .
docker kill dash-backup
docker rm dash-backup
docker run -d --name dashcam-backup --restart always -v /home/brian/.ssh:/home/brian/.ssh -v /media/:/media/ dashcam-backup:latest python dashcam_backup/main.py