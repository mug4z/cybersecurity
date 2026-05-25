#!/usr/bin/env python3

# TODO: encrypt the key and decrypt it when creating the password
# TODO: Implement test with pytest

import hmac
from hashlib import sha1
import struct
import time
import math

def get_time_counter(current_unix_time: float, 
                     unix_start_time: float, 
                     time_step:int ) -> int:
    return math.floor((current_unix_time - unix_start_time) / time_step)


# def gen_TOTP(key_hex: string, time: string):
    


# NOTE: function is ok tested with the test case of the rfc4226
def gen_HOTP(hash: bytes):
    # NOTE: get the last_4_bits
    offset =  hash[len(hash) - 1] & 0xf 
    # print(f"hash[offset] {hash[offset]}")
    # print(f"hash[offset] & 0x7f: {hash[offset] & 0x7f}")

    # print(f"hash[offset + 1 ] {hash[offset + 1]}")
    # print(f"hash[offset + 1] & 0xff: {hash[offset + 1] & 0xff}")
    # print(f"hash[offset:offset+4] {int.from_bytes(hash[offset:offset + 4])}")
    binary =  (
                ((hash[offset] & 0x7f) << 24) 
              | ((hash[offset + 1] & 0xff) << 16) 
              | ((hash[offset + 2] & 0xff) << 8) 
              | ((hash[offset + 3]) & 0xff)
              )
    
    #  NOTE: Return the 6 digits HOTP Code (10^digits) 10^6 = 1000000
    return binary % 1000000
 

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

