#!/usr/bin/env python3

# TODO: Generate an HMAC-SHA-1 value Let HS = HMAC-SHA-1(K,C)  // HS is a 20-byte string
#       Generate a 4-byte string (Dynamic Truncation) Let Sbits = DT(HS)   //  DT, defined below, //  returns a 31-bit string
#       Compute an HOTP value    Let Snum  = StToNum(Sbits)   // Convert S to a number in 0...2^{31}-1
#       Return D = Snum mod 10^Digit //  D is a number in the range

# TODO: encrypt the key and decrypt it when creating the password

import hmac
# from hashlib import sha512
from hashlib import sha1
import struct
# from hashlib import sha256


# def create_htop_value(k, c):

def get_last_4bit(c :bytes):
    return int.from_bytes(c,byteorder='little') & 15

def dynamic_truncation(HS: str):
    # NOTE: isoler les deux dernier character en hexa
    #       Les convertir en int et prendre les 4 lower bits
    last_byte_hex = HS[-2:]
    last_byte_hex_byte = int(last_byte_hex, 16).to_bytes()
    OffsetBits =  get_last_4bit(last_byte_hex_byte)
    # ------------ SHOULD BE GOOD UNTIL NOW



    P = HS[OffsetBits:OffsetBits + 8]
    print(P)
    n = int(P, 16)  & 2147483647
    big_end = struct.pack('>i',n)
    print(f"Big_end {int.from_bytes(big_end, 'little')}")
    y = int.from_bytes(big_end, 'big')
    print(f"Modulo {y % 1000000}")
    # print(f"n is {n}")
    # print(f"n hex is {hex(n)}")
    # print(n.bit_length())
    #
    # big_end = struct.pack('>i',n)
    # print(hex(int.from_bytes(big_end)))

    # 41397eea
    # n.to_bytes(n.bit_length() + 7) // 8, 'big')
    # return (int(P, 16)  & 2147483647)

def gen_HOTP(hash: bytes):
    # NOTE: get the last_4_bits
    offset =  hash[len(hash) - 1] & 0xf 
    print(hash[offset] << 24)
    binary =  (
                ((hash[offset] & 0x7f) << 24) 
              | ((hash[offset + 1] & 0xff) << 16) 
              | ((hash[offset + 2] & 0xff) << 8) 
              | ((hash[offset + 3]) & 0xff)
              )
    # NOTE: Return the 6 digits HOTP Code (10^digits) 10^6 = 1000000
    return binary % 1000000
 

def main():
    testSecret = b"12345678901234567890"
    testCount = struct.pack('>Q',0)
    # hashed1 = hmac.new(key,raw, sha1)
    # hexhash1 = hashed1.hexdigest()
    # hashed256 = hmac.new(key,raw, sha256)
    # hexhash256 = hashed256.hexdigest()
    # print(hexhash1)
    # print(hexhash256)
    # NOTE: See if the 20 byte correspondance from hexadecimal what it should be represented
    hashed1 = hmac.new(testSecret,testCount, sha1)
    print(hashed1.hexdigest())
    hexhash1 = hashed1.hexdigest()
    P = dynamic_truncation(hexhash1)

    # print(last_4_bits)

    # print(hexhash512)
    # print(type(0b1111))
    print(f"String = {hexhash1}")
    # print(P)
    # print (f"Offsetbits {OffsetBits}")
    # print(f"String[OffsetBits] {hexhash512[OffsetBits]}\nString[OffsetBits + 3] {hexhash512[OffsetBits + 3]}")
    
    # print(99 & 15)



if __name__ == "__main__":
    main()


# DT(String) // String = String[0]...String[19]
#  Let OffsetBits be the low-order 4 bits of String[19]
#  Offset = StToNum(OffsetBits) // 0 <= OffSet <= 15
#  Let P = String[OffSet]...String[OffSet+3]
#  Return the Last 31 bits of P
