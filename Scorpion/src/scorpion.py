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

def remove_EXIF_data(img_path: str, img_exifless_path: str):
    image = Image.open(img_path)
    data = image.get_flattened_data()
    image2 = Image.new(image.mode, image.size)
    image2.putdata(data)
    image2.save(img_exifless_path)   
    image2.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strip-exif",action="store_true",help="Create a new image with exif data removed, based on the image given in arguments")
    parser.add_argument("files", nargs="+", help="The path where to download the images")
    args = parser.parse_args()

    if args.strip_exif:
        for file in args.files:
            print(f"Removing EXIF for {file}")
            try:
                prefix = '_exif_less'
                filename, file_ext = os.path.splitext(file)
                new_name = filename + prefix + file_ext
                remove_EXIF_data(file, new_name)
            except Exception as e:
                print(f"Failed for {e}")
        print("Done")
        exit(1)


    for file in args.files:
        try: 
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
        except Exception as e:
            print(f"Failed for {e}")

if __name__ == "__main__":
    main()
