#!/usr/bin/env python3

# TODO: Implement test with pytest
# TODO: Check if the content of the file given in argument is a 64 character hexadecimal string

import hmac
from hashlib import sha1
import struct
import time
import argparse
import os

from cryptography.fernet import Fernet

from modules.ft_hotp import gen_HOTP, get_time_counter

def create_key(path_to_key: str):
    print("Try to create key")
    try:
        key = Fernet.generate_key()
        if os.path.isfile(path_to_key):
            raise Exception("Key already exist")
        with open(path_to_key,'wb') as file:
            file.write(key)
        print("Key created")
    except Exception as e:
        print(f"Faild because of {e}")

def encrypt_file(file_to_encrypt: str, path_to_key: str):
    try:
        content_to_encrypt = None
        f = None
        with open(path_to_key,'rb') as file:
            key = file.read()
            f = Fernet(key)
            file.close()
        with open(file_to_encrypt,'rb') as file:
            content_to_encrypt = file.read()
            file.close()
        token = f.encrypt(content_to_encrypt)
        if os.path.isfile("ft_otp.key"):
            raise Exception("ft_otp.key already exists")
        with open('ft_otp.key','wb') as file:
            file.write(token)
    except Exception as e:
        print(f"Faild because of {e}")

def decrypt_file(file_to_decrypt: str, path_to_key: str):
    try:
        f = None
        content_to_encrypt = None
        with open(path_to_key,'rb') as file:
            key = file.read()
            f = Fernet(key)
            file.close()
        with open(file_to_decrypt,'rb') as file:
            content_to_encrypt = file.read()
            file.close()
        return f.decrypt(content_to_encrypt)

    except Exception as e:
        print(f"Faild because of {e}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--hex-key",help="The path of the key file, must be at least 64 character in hexadecimal")
    parser.add_argument("-k","--gen-password",action="store_true",help="generate a new temporary password")
    args = parser.parse_args()

    if args.hex_key:
        create_key('./.key')
        encrypt_file(args.hex_key,'./.key')
        exit(1)
    
    if args.gen_password:
        #  NOTE: return the time in seconds since the epoch
        T = get_time_counter(time.time(), 0, 30)
        count = struct.pack('>Q',T)
        secret = decrypt_file('ft_otp.key', './.key')
        if not secret:
            print('error')
            exit(1)
        hashed1 = hmac.new(secret, count, sha1)
        print(gen_HOTP(hashed1.digest()))
        exit(1)



if __name__ == "__main__":
    main()

