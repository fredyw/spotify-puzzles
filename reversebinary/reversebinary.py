#!/usr/bin/env python

def reverse_binary(n):
    r = 0
    while n != 0:
        x = (n & 1)
        n = n >> 1  
        r = r << 1
        r |= x
    return r

if __name__ == "__main__":
    n = raw_input()
    print reverse_binary(int(n))
