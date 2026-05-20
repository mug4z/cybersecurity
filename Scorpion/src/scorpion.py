#!/usr/bin/env python3

from PIL import Image 
from PIL.ExifTags import TAGS
import os
import argparse

def read_EXIF_data(img_exif: Image.Exif) -> dict:
    res = dict()
    for key, val in img_exif.items():
        res[TAGS[key]] = val
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="The path where to download the images")
    args = parser.parse_args()
    for file in args.files:
        print(f"FILENAME: {file}")
        print(f"SIZE in BYTES: {os.path.getsize(file)}")
        print(f"Creation date: {os.path.getctime(file)}")
        img = Image.open(file)
        img_exif = img.getexif()
        exif_data = read_EXIF_data(img_exif)
        for data, value in exif_data.items():
            print(f"{data}: {value}")
        print(f"IMAGE SIZE: {img.size}")
        print(f"IMAGE FORMAT: {img.format}\n")

if __name__ == "__main__":
    main()
