#!/usr/bin/env python3

import os
import sys
import pathlib
import subprocess

exe_file = 'yt-dlp'

subprocess.call(f'"{exe_file}" --update', shell=True)

if sys.platform.startswith('linux'):
    os.chdir(os.popen('echo -n $(xdg-user-dir DOWNLOAD)').read())
else:
    os.chdir(pathlib.Path.home() / 'Downloads')

print()

need_pause = False

if len(sys.argv) > 1:
    video_link = sys.argv[1]
    print(f'Video link: {video_link}')
else:
    video_link = input('Enter video link: ')
    need_pause = True

print()

if subprocess.call(f'"{exe_file}" --no-playlist --list-formats "{video_link}"', shell=True) != 0:
    sys.exit(1)

print()

video_format = input('Enter download format: ')

video_output = '%(id)s.%(ext)s'

video_merge  = 'mkv'

print()

subprocess.call(f'"{exe_file}" --no-playlist --format "{video_format}" --output "{video_output}" --merge-output-format "{video_merge}" "{video_link}"', shell=True)

if need_pause:
    input('Press <Enter> to close...')
