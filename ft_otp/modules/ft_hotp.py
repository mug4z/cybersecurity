"""ft_hotp

This modules provide the function to help make HOTP password

"""


import math


def get_time_counter(current_unix_time: float, 
                     unix_start_time: float, 
                     time_step:int ) -> int:
    return math.floor((current_unix_time - unix_start_time) / time_step)

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
