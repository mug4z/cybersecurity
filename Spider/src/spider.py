#!/usr/bin/env python3

import re
import requests
from urllib.parse import urlsplit
import urllib.robotparser
import os
import bs4
from bs4 import BeautifulSoup
import argparse
import time

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) \
         Gecko/20100101 Firefox/144.0"
}

def content_type_checker(url: str) -> bool:
    html = re.compile(r".*text/html.*")
    content_type = requests.head(url).headers['content-type']
    if re.search(html, content_type):
        return True
    return False

def get_web_page(url: str, headers: dict, rate: int) -> requests.models.Response:
        time.sleep(rate)
        return requests.get(url, headers=headers, timeout=10)

def create_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)


def is_relative_img(src: str) -> bool:
    split_result = urlsplit(src)
    if split_result.scheme and split_result.netloc:
        return True
    return False

def download_images(base_url: str, images: bs4.element.ResultSet, rate: int ,path: str = "./data/") -> None:
    create_dir(path)
    for image in images:
        img_link = image.get('src')
        if not is_relative_img(img_link):
            img_link = base_url + img_link
        try:
            response = get_web_page(img_link ,headers, rate)
            content = response.content
            if response.status_code >= 400:
                raise Exception(f"BAD request with status {response.status_code}")
        except Exception as e:
            print(f"Failed to get {img_link} for {e}")
            continue
        if not os.path.isfile(path+image.get('src').split('/')[-1]):
            with open(path+image.get('src').split('/')[-1],'wb') as file:
                file.write(content)
        else:
            print(f"Image {path+image.get('src')} already downloaded")

    

def img_finder_all(data: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return data.find_all("img", src=re.compile(r"(\.jpe?g)|(\.png)|(\.gif)|(\.bmp)$"))

def link_finder_all(data: bs4.BeautifulSoup) -> bs4.element.ResultSet: 
    return data.find_all("a",href=re.compile(r"."))

def internal_link(links: bs4.element.ResultSet, domain_name: str) -> list:
    name = urlsplit(domain_name).netloc
    pattern = [
        re.compile(r"^https?:\/\/(?:www\.)?("+ re.escape(name) + r").*"),
        re.compile(r"^\/.*")
    ]
    res = []
    for link in links:
        link_to_add = link.get('href')
        if re.search(pattern[0], link_to_add ) is not None:
            res.append(link_to_add )
        elif re.search(pattern[1], link_to_add) is not None:
            res.append(domain_name + link_to_add)
        else:
            continue
    return res

def extract_base_url(url: str) -> str:
    split = urlsplit(url)
    return split.scheme + "://" + split.netloc
    

def beautiful_soup_creator(response: str) -> bs4.BeautifulSoup:
    return BeautifulSoup(response, "html.parser")

# TEST: Check if the donwload on 42lausanne.ch with wget and this script are the same.
# TEST: wget with recursive 5 get 734 images.
def recursive_download(base_url: str, links: list , depth: int, visited_link: set, rate: int) -> None:
    actual_depth = 1

    next_link = list()
    while(actual_depth <= depth):
        print(f"[ACTUAL DEPTH] {actual_depth}")
        for link in links:
            if link in visited_link:
                continue
            print(f"ANALYSE LINK {link}")
            try:
                response = get_web_page(link, headers, rate)
                soup = beautiful_soup_creator(response.text)
            except Exception as e:
                print(f"{link} could not be used because of {e}")
                continue
            print(f"Will download for {link}")
            download_images(base_url, img_finder_all(soup), rate)
            links = internal_link(link_finder_all(soup), base_url)
            next_link.extend(links)
            print(f"SIZE OF next_link is {len(next_link)}")
            visited_link.add(link)
        actual_depth += 1
        print(f"SIZE OF visited_link is {len(visited_link)}")
        links.clear()
        links = next_link.copy()
        next_link.clear()
        

def robots_rule(base_url: str) -> urllib.robotparser.RobotFileParser :
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url + "/robots.txt")
    rp.read()
    return rp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",help="The path where to download the images")
    parser.add_argument("-r","--recursive",action="store_true",help="Download images recursively")
    parser.add_argument("-l","--level",type=int,help="The level of recursion, by default it is 5")
    parser.add_argument("-nc","--nice",action="store_true",help="Respect the crawl_delay of the robots.txt")
    parser.add_argument("url",help="The target website to download from, in the form https://url")
    args = parser.parse_args()
    try:
        if args.nice:
            rp = robots_rule(extract_base_url(args.url))
            rate = rp.crawl_delay("*")
            if rate is None:
                rate = 0
        else:
            rate = 0
        if not content_type_checker(args.url):
            print(f"WRONG TYPE")
            exit(1)
        response = get_web_page(args.url, headers,int(rate))
        soup = beautiful_soup_creator(response.text)
        download_images(extract_base_url(args.url),img_finder_all(soup),int(rate))
        if args.recursive:
            level = args.level if args.level is not None else 5
            visited_link = set()
            links = internal_link(link_finder_all(soup), args.url)
            visited_link.add(args.url)
            recursive_download(extract_base_url(args.url), links, level, visited_link, int(rate))
    except Exception as e:
        print(f"Failed for {e}")


if __name__ == "__main__":
    main()

# TODO: Function to download all image (jpg/jpeg, .png,.gif, .bmp) from a single page -> DONE
# TODO: add arguments -> DONE 
# TODO: Get all the image from a given url -> DONE
# TODO: All internal linke from a url -> DONE
# TODO: Function to follow links -> DONE ?
# TODO: Follow the robots.txt directive -> only crawl_delay
# TODO: Implement arguments -> DONE
# TODO: Make logs
#
# NOTE: website to check are korben.info and lwn.net and 42lausanne.ch
#
