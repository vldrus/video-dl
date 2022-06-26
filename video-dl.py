#!/usr/bin/env python3

import os
import sys
import pathlib
import subprocess

if 'norestart' not in sys.argv:
    subprocess.call(f'"{sys.executable}" -m pip install -qq --user -U yt-dlp', shell=True)
    subprocess.call(f'"{sys.executable}" "{sys.argv[0]}" norestart', shell=True)
    sys.exit()

try:
    import yt_dlp as downloader

    if sys.platform.startswith('linux'):
        os.chdir(os.popen('echo -n $(xdg-user-dir DOWNLOAD)').read())
    else:
        os.chdir(pathlib.Path.home() / 'Downloads')

    print(f'Downloader version: {downloader.version.__version__}')

    print()

    video_link = input('Enter video link: ')
    options = {
        'listformats': True
    }
    with downloader.YoutubeDL(options) as d:
        d.download([video_link])

    print()

    video_format = input('Enter download format: ')
    options = {
        'format': video_format,
        'outtmpl': '%(id)s.%(ext)s'
    }
    with downloader.YoutubeDL(options) as d:
        d.download([video_link])

except Exception as e:
    print(e)
    pass

print()
input('Press <Enter> to close...')
