import os
import re

base_path = "/home/shahbaz/Manga/C"

# Match only Chapter_### folders
chapter_dirs = [
    d for d in os.listdir(base_path)
    if os.path.isdir(os.path.join(base_path, d)) and re.match(r"Chapter_\d+$", d)
]

# Sort by chapter number
chapter_dirs.sort(key=lambda x: int(x.split('_')[1]))

for chapter in chapter_dirs:
    chapter_path = os.path.join(base_path, chapter)

    # Walk through all subdirectories and count JPG files (case-insensitive)
    jpg_count = 0
    for root, _, files in os.walk(chapter_path):
        jpg_count += sum(1 for f in files if f.lower().endswith(".jpg"))

    print(f'"{chapter}": {jpg_count},')
