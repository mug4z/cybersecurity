#!/usr/bin/env python3

# TODO: Implement test with pytest
# TODO: Check if the content of the file given in argument is a 64 character hexadecimal string

import hmac
from hashlib import sha1
import struct
import time
import argparse
import os
import math

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

def get_content_file(path_to_file: str) -> bytes:
    content = None
    with open(path_to_file, 'rb') as file:
        content = file.read()
        file.close()
    return content



def encrypt_file(file_to_encrypt: str, path_to_key: str):
        key = get_content_file(path_to_key)
        f = Fernet(key)
        content_to_encrypt = get_content_file(file_to_encrypt)
        token = f.encrypt(content_to_encrypt)
        if os.path.isfile("ft_otp.key"):
            raise Exception("ft_otp.key already exists")
        with open('ft_otp.key','wb') as file:
            file.write(token)

def decrypt_file(file_to_decrypt: str, path_to_key: str):
        content_to_decrypt = None
        key = get_content_file(path_to_key)
        f = Fernet(key)
        content_to_decrypt = get_content_file(file_to_decrypt)
        return f.decrypt(content_to_decrypt)
def check_hex(content: str) -> bool:
    try:
        int(content, 16)
        return True
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--hex-key",help="The path of the key file, must be at least 64 character in hexadecimal")
    parser.add_argument("-k","--gen-password",action="store_true",help="generate a new temporary password")
    args = parser.parse_args()

    if args.hex_key:
        try:
            content = get_content_file(args.hex_key)
            if not check_hex(content.decode()):
                print("The file content is not valid hexadecimal")
                exit(-1)
            if len(content.decode()) < 64:
                print("The hexadecimal is less than 64 character")
                exit(-1)
            create_key('./.key')
            encrypt_file(args.hex_key,'./.key')
            exit(1)
        except Exception as e:
            print(f"Failed because of {e}")
    
    if args.gen_password:
        try:
            #  NOTE: return the time in seconds since the epoch
            T = get_time_counter(time.time(), 0, 30)
            count = struct.pack('>Q',T)
            secret = decrypt_file('ft_otp.key', './.key')
            if not secret:
                print('error')
                exit(-1)
            hashed1 = hmac.new(secret, count, sha1)
            
            otp = gen_HOTP(hashed1.digest())
            
            if int(math.log10(otp) + 1) != 6:
                print("0",end='')
            print(otp)
        except Exception as e:
            print(f"Failed because of {e}")
        



if __name__ == "__main__":
    main()

