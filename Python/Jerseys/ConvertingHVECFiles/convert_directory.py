import os
from random import sample

import moviepy


# root = r"D:\Quebec 2024"
root = r"D:\Quebec 2025"
suf_to_rem = ".ts.mp4"


if __name__ == '__main__':

    if not os.path.exists(root):
        raise NotADirectoryError(f"Could not find directory '{root}'")

    for file_name in [fn for fn in os.listdir(root) if fn.lower().endswith(suf_to_rem)]:
        l_file_name = file_name.lower().strip()
        o_file_name = f"{file_name[:len(file_name) - len(suf_to_rem)]}.mp4"
        a_o_file_name = os.path.join(root, o_file_name)
        if not os.path.exists(a_o_file_name):
            clip = moviepy.VideoFileClip(os.path.join(root, file_name))
            clip.write_videofile(a_o_file_name)
            clip.close()

        else:
            print(f"B '{l_file_name}'")
