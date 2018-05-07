#!/bin/sh
if [$(command -v ffmpeg) == ''];then
    sudo apt-get update
    sudo apt-get install ffmpeg -y
fi
