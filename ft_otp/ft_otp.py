#!/usr/bin/env python3

# TODO: encrypt the key and decrypt it when creating the password
# TODO: Implement test with pytest

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



# def gen_TOTP(key_hex: string, time: string):
    
def main():
    encrypt_file('key.txt', './.key')
    print(decrypt_file('ft_otp.key', './.key'))
    parser = argparse.ArgumentParser()
    parser.add_argument("-g",help="The path of the key file, must be at least 64 character in hexadecimal")
    parser.add_argument("-k","--key",action="store_true",help="generate a new temporary password")
    args = parser.parse_args()

    # NOTE: This part is OK !!!
    testSecret = b"12345678901234567890"
    T = get_time_counter(time.time(), 0, 30)
    testCount = struct.pack('>Q',T)

    #  NOTE: return the time in seconds since the epoch
    # print(f"time {time.time()}")

    print(f"\nTEST FOR TOTP")

    hashed1 = hmac.new(testSecret, testCount, sha1)
    print(f"hashed1 hexdigest {hashed1.hexdigest()}")
    print(len(hashed1.hexdigest()))
    hexhash1 = hashed1.hexdigest()
    print(f"HOTP {gen_HOTP(hashed1.digest())}")
    print(f"String = {hexhash1}")



if __name__ == "__main__":
    main()

