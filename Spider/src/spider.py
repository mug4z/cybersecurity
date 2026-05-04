#!/usr/bin/env python3

import requests
import os
from bs4 import BeautifulSoup


def create_dir(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def BeautifulSoup_test():
    with open("./data/korbenHome.html", "wb") as file:
        soup = BeautifulSoup(file)
    soup = BeautifulSoup("<html>data</html>")
    print(soup)
        


def download_page(url: str, dir: str = "./data/") -> None:
    create_dir(dir)
    print(requests.get(url).status_code)
    with open(dir + "test.html", "wb") as file:
        file.write(requests.get(url).content)
    file.close()


def main():
    print("hello world")
    # download_page("https://lwn.net/")
    BeautifulSoup_test()


if __name__ == "__main__":
    main()


# TODO: Function to download all image (jpg/jpeg, .png,.gif, .bmp) from a single page
# TODO: Function to follow links
# TODO: Get all the image from a given url
# TODO: website to check are korben.info and lwn.net
