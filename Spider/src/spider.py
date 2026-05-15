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


def is_relative_img(src: str) -> bool:
    split_result = urlsplit(src)
    if split_result.scheme and split_result.netloc:
        return True
    return False


def download_images(base_url: str, images: bs4.element.ResultSet, path: str = "./data/") -> None:
    create_dir(path)
    for image in images:
        img_link = image.get('src')
        print(f"IMAGE LINK {img_link}")
        if not is_relative_img(img_link):
            img_link = base_url + img_link
        try:
            print(f"Try to download {img_link} ")
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

    # pattern = re.compile(
    #     r"^http?s:\/\/(" + re.escape(name) + r")|(www."+ re.escape(name) + r").*"
    # )

def link_finder_all(data: bs4.BeautifulSoup) -> bs4.element.ResultSet: 
    return data.find_all("a",href=re.compile(r"."))

# WARN: FOLLOW INTERNAL LINK ONLY
# NOTE: change domain_name by base_url ?
def internal_link(links: bs4.element.ResultSet, domain_name: str) -> list:
    name = urlsplit(domain_name).netloc
    pattern = [
        re.compile(r"^https?:\/\/(?:www\.)?("+ re.escape(name) + r").*"),
        re.compile(r"^\/.*")
    ]
    res = []
    #NOTE: When we have https://domain_name
    #NOTE: When we have just the / character
    for link in links:
        link_to_add = link.get('href')
        if re.search(pattern[0], link_to_add ) is not None:
            res.append(link_to_add )
        elif re.search(pattern[1], link_to_add) is not None:
            res.append(domain_name + link_to_add)
        else:
            continue
    return res

#NOTE: scheme+ :// + netloc = base_url
def extract_base_url(url: str) -> str:
    split = urlsplit(url)
    return split.scheme + "://" + split.netloc
    

def beautiful_soup_creator(response: str) -> bs4.BeautifulSoup:
    return BeautifulSoup(response, "html.parser")

# WARN: if an url was already viewed it should not be Donwloaded again
# NOTE: Donwload breadth-first. as https://www.gnu.org/software/wget/manual/wget.html#Recursive-Download
def recursive_download(domain_name: str, links: list , depth: int, visited_link: set) -> None:
    link_depth = {}
    actual_depth = 1

    next_link = list()
    while(actual_depth <= depth):
        print(f"[ACTUAL DEPTH] {actual_depth}")
        for link in links:
            if link in visited_link:
                continue
            response = get_web_page(link, headers)
            soup = beautiful_soup_creator(response.text)
            print(f"Will download for {link}")
            download_images(domain_name, img_finder_all(soup))
            links = internal_link(link_finder_all(soup), domain_name)
            next_link.extend(links)
            visited_link.add(link)
        actual_depth += 1
        links.clear()
        links = next_link.copy()
        next_link.clear()
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",help="The path where to download the images")
    parser.add_argument("-r","--recursive",action="store_true",help="Download images recursively")
    parser.add_argument("-l","--level",type=int,help="The level of recursion, by default it is 5")
    parser.add_argument("url",help="The target website to download from, in the form https://url")
    args = parser.parse_args()
    try:
        response = get_web_page(args.url, headers)
        soup = beautiful_soup_creator(response.text)
        download_images(extract_base_url(args.url), img_finder_all(soup))
        if args.recursive:
            visited_link = set()
            links = internal_link(link_finder_all(soup), args.url)
            visited_link.add(args.url)
            recursive_download(args.url, links, 1, visited_link)
    except Exception as e:
        print(f"Failed for {e}")


if __name__ == "__main__":
    main()


# TODO: Function to download all image (jpg/jpeg, .png,.gif, .bmp) from a single page -> DONE
# TODO: add arguments -> DONE 
# TODO: Get all the image from a given url -> DONE
# TODO: All internal linke from a url -> DONE
# TODO: Function to follow links
# TODO: Implement arguments
# TODO: Make logs
#
# NOTE: website to check are korben.info and lwn.net
#
