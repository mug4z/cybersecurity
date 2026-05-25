#!/usr/bin/env python3

# TODO: encrypt the key and decrypt it when creating the password
# TODO: Implement test with pytest

import hmac
from hashlib import sha1
import struct
import time

from modules.ft_hotp import gen_HOTP, get_time_counter


# def gen_TOTP(key_hex: string, time: string):
    
def main():
    
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

