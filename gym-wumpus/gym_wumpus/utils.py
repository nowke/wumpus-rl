from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from pathlib import Path


def wumpus_to_np_array(env_str):
    """ Converts wumpus rendered string representation into
    numpy pixels array, which can be used  as an image
    """
    script_dir = Path(os.path.dirname(__file__))
    lines = env_str.split('\n')[1:-1]  # Discard scores line

    # Split the time_step line into 2 lines
    #  0   1   2   3   4   5    time_step=1
    #       |
    #       v
    #  0   1   2   3   4   5
    #  time_step = 1
    time_step = lines[0][27:]
    lines[0] = lines[0][:27]
    lines = [time_step] + lines

    base = Image.open(
        f'{script_dir}/assets/base.png').convert('RGBA')  # base image
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype(f'{script_dir}/assets/FreeMono.ttf', 14)
    d = ImageDraw.Draw(txt)  # draw context

    # draw the text in each lines
    for i, line in enumerate(lines):
        d.text((10, 10 + i * 20), line, font=fnt, fill=(255, 255, 255, 255))

    img = Image.alpha_composite(base, txt)  # generate image
    np_arr = np.asarray(img)  # convert to `np.array`

    return np_arr
