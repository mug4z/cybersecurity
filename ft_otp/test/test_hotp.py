#!/usr/bin/env python3

""" Test case for HOTP

Make sure the gen_HOTP function respect the test case in the RFC 4226

"""
import hmac
from hashlib import sha1
import struct

from modules.ft_hotp import gen_HOTP

hashs = [
    "cc93cf18508d94934c64b65d8ba7667fb7cde4b0",
    "75a48a19d4cbe100644e8ac1397eea747a2d33ab",
    "0bacb7fa082fef30782211938bc1c5e70416ff44",
    "66c28227d03a2d5529262ff016a1e6ef76557ece",
    "a904c900a64b35909874b33e61c5938a8e15ed1c",
    "a37e783d7b7233c083d4f62926c7a25f238d0316",
    "bc9cd28561042c83f219324d3c607256c03272ae",
    "a4fb960c0bc06e1eabb804e5b397cdc4b45596fa",
    "1b3c89f65e6c9e883012052823443f048b4332db",
    "1637409809a679dc698207310c8c7fc07290d9e5"
]
testSecret = b"12345678901234567890"

values = [
    755224,
    287082,
    359152,
    969429,
    338314,
    254676,
    287922,
    162583,
    399871,
    520489
]
def test_hotp_hash():
    i = 0
    while i < 10:
        testCount = struct.pack('>Q',i)
        hashed1 = hmac.new(testSecret, testCount, sha1)
        assert hashed1.hexdigest() == hashs[i]
        i+= 1

def test_hotp_value():
    i = 0
    while i < 10:
        testCount = struct.pack('>Q',i)
        hashed1 = hmac.new(testSecret, testCount, sha1)
        assert gen_HOTP(hashed1.digest()) == values[i]
        i+= 1

