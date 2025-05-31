#!/bin/sh

ffmpeg -y -r 1 -i thumbnail/link/%05d.png \
       -vcodec libx264 -profile:v baseline -pix_fmt yuv420p -movflags +faststart \
       gh-pages/thumbnail.mp4
