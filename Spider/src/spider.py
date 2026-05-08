#!/usr/bin/env python3

import re
import requests
from urllib.parse import urlsplit
import os
import bs4
from bs4 import BeautifulSoup

def get_web_page(url: str, headers: dict) -> requests.models.Response:
    return requests.get(url, headers=headers)

def create_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)

def download_images(domain_name: str, images: bs4.element.ResultSet, path: str = "./data/",) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) \
         Gecko/20100101 Firefox/144.0"
    }
    create_dir(path)
    for image in images:
        if not os.path.isfile(image.get('src').split('/')[-1]):
            with open(path+image.get('src').split('/')[-1],'wb') as file:
                file.write(get_web_page(domain_name+image.get('src'),headers=headers).content)
    

def img_finder_all(data: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return data.find_all("img", src=re.compile(r"(\.jpe?g)|(\.png)|(\.gif)|(\.bmp)$"))


def link_finder_all(data: bs4.BeautifulSoup):
    for link in data.find_all("a"):
        print(link.get("href"))


def beautiful_soup_creator(response: str) -> bs4.BeautifulSoup:
    return BeautifulSoup(response, "html.parser")


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) \
         Gecko/20100101 Firefox/144.0"
    }
    response = get_web_page("https://korben.info/", headers)
    print(type(headers))
    if response.status_code != 200:
        print("NOT GOOD")
        exit(1)
    soup = beautiful_soup_creator(response.text)
    images = img_finder_all(soup)
    download_images("https://korben.info",images)


if __name__ == "__main__":
    main()


# TODO: Function to download all image (jpg/jpeg, .png,.gif, .bmp) from a single page
# TODO: Function to follow links
# TODO: Get all the image from a given url
# TODO: website to check are korben.info and lwn.net
