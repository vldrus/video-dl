#!/bin/env python3


import sys
import pathlib
import subprocess


DEFAULT_OUTPUT_WIDTH = '720'
DEFAULT_OUTPUT_CRF = '24'
DEFAULT_OUTPUT_AUDIO = '96k'
DEFAULT_OUTPUT_PRESET = "veryslow"


if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} input_file.webm')
    sys.exit(1)


input_file = sys.argv[1]
output_file = pathlib.Path(input_file).parent / f'{pathlib.Path(input_file).stem}_out.mp4'

print('Input file: ', input_file)
print('Output file:', output_file)


output_width = input(f'Enter width [{DEFAULT_OUTPUT_WIDTH}]: ') or DEFAULT_OUTPUT_WIDTH
output_crf = input(f'Enter crf [{DEFAULT_OUTPUT_CRF}]: ') or DEFAULT_OUTPUT_CRF
output_audio = input(f'Enter audio [{DEFAULT_OUTPUT_AUDIO}]: ') or DEFAULT_OUTPUT_AUDIO


output_scale=f'-2:{output_width}:flags=lanczos'
output_preset=f'{DEFAULT_OUTPUT_PRESET}'
output_comment=f'WIDTH={output_width},CRF={output_crf},AUDIO={output_audio},INPUT={pathlib.Path(input_file).name}'


ffmpeg_command=f'''ffmpeg -i "{input_file}" \
                          -vf scale="{output_scale}" \
                          -preset "{output_preset}" \
                          -crf "{output_crf}" \
                          -b:a "{output_audio}" \
                          -map_metadata "-1" \
                          -metadata comment="{output_comment}" \
                          "{output_file}" '''

subprocess.call(ffmpeg_command, shell=True)
