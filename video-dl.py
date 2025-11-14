#!/usr/bin/env python3

# Copyright (c) 2026 Vlad
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import shutil
import pathlib
import subprocess

exe_file = 'yt-dlp' # https://github.com/yt-dlp/yt-dlp

def exit_with_pause(exit_code, need_pause):
    if need_pause:
        print()
        input('Press <Enter> to close...')

    sys.exit(exit_code)

def main():
    if shutil.which('xdg-user-dir'):
        os.chdir(os.popen('echo -n $(xdg-user-dir DOWNLOAD)').read())
    else:
        os.chdir(pathlib.Path.home() / 'Downloads')

    need_pause = False

    if len(sys.argv) < 2:
        need_pause = True

    cmd_line = f'"{exe_file}" --update'

    if subprocess.call(args=cmd_line, shell=True) != 0:
        exit_with_pause(1, need_pause)

    print()

    video_link = ''

    if len(sys.argv) > 1:
        video_link = sys.argv[1]
        print(f'Video link: {video_link}')
    else:
        video_link = input('Enter video link: ')

    print()

    cmd_line = f'"{exe_file}" --no-playlist --list-formats "{video_link}"'

    if subprocess.call(args=cmd_line, shell=True) != 0:
        exit_with_pause(1, need_pause)

    print()

    video_format = input('Enter download format: ')

    print()

    video_output = '%(id)s.%(ext)s'
    video_merge = 'mkv'

    cmd_line = f'"{exe_file}" --no-playlist --format "{video_format}" --output "{video_output}" --merge-output-format "{video_merge}" "{video_link}"'

    if subprocess.call(args=cmd_line, shell=True) != 0:
        exit_with_pause(1, need_pause)

    exit_with_pause(0, need_pause)

if __name__ == '__main__':
    main()
