#!/usr/bin/env python3

import re
import requests
from urllib.parse import urlsplit
import os
import bs4
from bs4 import BeautifulSoup
import argparse

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) \
         Gecko/20100101 Firefox/144.0"
}

def get_web_page(url: str, headers: dict) -> requests.models.Response:
        return requests.get(url, headers=headers, timeout=10)

def create_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)


def is_external_img(src: str) -> bool:
    split_result = urlsplit(src)
    if split_result.scheme and split_result.netloc:
        return True
    return False


def download_images(domain_name: str, images: bs4.element.ResultSet, path: str = "./data/",) -> None:
    create_dir(path)
    for image in images:
        img_link = image.get('src')
        if not is_external_img(img_link):
            img_link = domain_name + img_link
        try:
            content = get_web_page(img_link ,headers=headers).content
        except Exception as e:
            print(f"Failed to get {img_link} for {e}")
            continue
        if not os.path.isfile(path+image.get('src').split('/')[-1]):
            with open(path+image.get('src').split('/')[-1],'wb') as file:
                file.write(content)

    

def img_finder_all(data: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return data.find_all("img", src=re.compile(r"(\.jpe?g)|(\.png)|(\.gif)|(\.bmp)$"))

# TODO: make a function to handle full or relative url

# WARN: FOLLOW INTERNAL LINK ONLY
def link_finder_all(domain_name: str, data: bs4.BeautifulSoup): 
    name = urlsplit(domain_name).netloc
    pattern = re.compile(
        r"^http?s:\/\/(" + re.escape(name)+r")|(www."+ re.escape(name) + r").*"
    )
    for link in data.find_all("a",href=pattern):
        print (urlsplit(str(link.get('href'))).netloc)
        # print(link.get("href"))
    # for link in data.find_all("a"):
    #     print(link.get("href"))


def beautiful_soup_creator(response: str) -> bs4.BeautifulSoup:
    return BeautifulSoup(response, "html.parser")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",help="The path where to download the images")
    parser.add_argument("-r","--recursive",help="Download images recursively")
    parser.add_argument("-l","--level",type=int,help="The level of recursion, by default it is 5")
    parser.add_argument("url",help="The target website to download from, in the form https://url")
    args = parser.parse_args()
    try:
        response = get_web_page(args.url, headers)
        soup = beautiful_soup_creator(response.text)
        link_finder_all(args.url, soup)
    except Exception as e:
        print(f"Failed for {e}")
    # images = img_finder_all(soup)
    # download_images(args.url,images)


if __name__ == "__main__":
    main()


# TODO: Function to download all image (jpg/jpeg, .png,.gif, .bmp) from a single page -> DONE
# TODO: add arguments -> DONE 
# TODO: Get all the image from a given url -> DONE
# TODO: Function to follow links
# TODO: Implement arguments
# TODO: Make logs
#
# NOTE: website to check are korben.info and lwn.net
