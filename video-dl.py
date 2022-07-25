#!/usr/bin/env python3

import os
import sys
import pathlib
import subprocess

subprocess.call(f'"{sys.executable}" -m pip install -qq --user -U yt-dlp', shell=True)

try:
    import yt_dlp as downloader

    if sys.platform.startswith('linux'):
        os.chdir(os.popen('echo -n $(xdg-user-dir DOWNLOAD)').read())
    else:
        os.chdir(pathlib.Path.home() / 'Downloads')

    print(f'Downloader version: {downloader.version.__version__}')

    print()

    if len(sys.argv) > 1:
        video_link = sys.argv[1]
        print(f'Video link: {video_link}')
        print()
    else:
        video_link = input('Enter video link: ')

    options = {
        'noplaylist': True,
        'listformats': True
    }
    with downloader.YoutubeDL(options) as d:
        d.download([video_link])

    print()

    video_format = input('Enter download format: ')

    options = {
        'noplaylist': True,
        'format': video_format,
        'outtmpl': '%(id)s.%(ext)s'
    }
    with downloader.YoutubeDL(options) as d:
        d.download([video_link])

except Exception as e:
    print(e)
    pass

print()

if len(sys.argv) < 2:
    input('Press <Enter> to close...')
