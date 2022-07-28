#!/bin/env python3


import sys
import pathlib
import subprocess


DEFAULT_OUTPUT_WIDTH  = '720'
DEFAULT_OUTPUT_CRF    = '24'
DEFAULT_OUTPUT_VIDEO  = '900k'
DEFAULT_OUTPUT_AUDIO  = '96k'
DEFAULT_OUTPUT_PRESET = 'slow'


if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} input_file.webm')
    sys.exit(1)

input_file  = sys.argv[1]
output_file = pathlib.Path(input_file).parent / f'{pathlib.Path(input_file).stem}_out.mp4'

print('Input file: ', input_file)
print('Output file:', output_file)
print()

output_width   = input(f'Enter width [{DEFAULT_OUTPUT_WIDTH}]: ') or DEFAULT_OUTPUT_WIDTH

output_crf     = input(f'Enter crf [{DEFAULT_OUTPUT_CRF}]: ') or DEFAULT_OUTPUT_CRF
output_quality = f'-crf "{output_crf}"'

if output_crf.lower() == 'no':
    output_video = input(f'Enter video [{DEFAULT_OUTPUT_VIDEO}]: ') or DEFAULT_OUTPUT_VIDEO
    output_quality = f'-b:v "{output_video}"'

output_audio   = input(f'Enter audio [{DEFAULT_OUTPUT_AUDIO}]: ') or DEFAULT_OUTPUT_AUDIO
output_preset  = input(f'Enter preset [{DEFAULT_OUTPUT_PRESET}]: ') or DEFAULT_OUTPUT_PRESET

output_scale   = f'-2:{output_width}:flags=lanczos'
output_comment = f'CRF={output_crf},PRESET={output_preset},INPUT={pathlib.Path(input_file).name}'

ffmpeg_command = f'''\
ffmpeg -i "{input_file}" \
-vf scale="{output_scale}" \
-preset "{output_preset}" \
{output_quality} \
-b:a "{output_audio}" \
-map_metadata "-1" \
-metadata comment="{output_comment}" \
"{output_file}" \
'''

print()
print('Executing ffmpeg with the following command:')
print()
print(ffmpeg_command)
print(flush=True)

subprocess.call(ffmpeg_command, shell=True)
