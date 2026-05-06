#!/usr/bin/env python3

import re
import requests
# import os
import bs4
from bs4 import BeautifulSoup


def get_web_page(url: str, headers: dict) -> requests.models.Response:
    return requests.get(url, headers=headers)


def img_finder_all(data: bs4.BeautifulSoup) -> str:
    # lol = data.find_all('img',{'src':re.compile(r'(jpe?g)|(png)|(.gif)|(.bmp)$')})
    lol = data.find_all('img','.png')
    print(type(lol))
    # for link in data.find_all("img"):
    #     list.append(link.get("src"))
    # print(list)
    # NOTE: (jpe?g)|(png)|(.gif)|(.bmp)$ regex to use
    return "lol"


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
    img_finder_all(soup)


if __name__ == "__main__":
    main()


# TODO: Function to download all image (jpg/jpeg, .png,.gif, .bmp) from a single page
# TODO: Function to follow links
# TODO: Get all the image from a given url
# TODO: website to check are korben.info and lwn.net
