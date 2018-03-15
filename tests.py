#!/usr/bin/python
# -*- coding: utf-8 -*-

from binascii import hexlify, unhexlify

from prince import Prince
import os


def test(ptxt, key, exp):
    cipher = Prince()
    ctxt = cipher.encrypt(ptxt, key)
    #print(exp)
    #print(ctxt)
    if ctxt != exp:
        print("FAILED encryption of {" + ptxt + "} with key {" + key + "}. Expected: {" + exp + "}, got: {" + ctxt + "}")
    else:
        print("PASSED encryption of {" + ptxt + "} with key {" + key + "}. Yields:   {" + exp + "}")
    dec = cipher.decrypt(ctxt, key)
    if dec != ptxt:
        print("FAILED decryption of {" + ctxt + "} with key {" + key + "}. Expected: {" + ptxt + "}, got: {" + dec + "}")
    else:
        print("PASSED decryption of {" + ctxt + "} with key {" + key + "}. Yields:   {" + dec + "}")


if __name__ == "__main__":
    cipher = Prince()
    print("Running test1")
    test("00" * 8, "00" * 16, "818665aa0d02dfda")

    print("\nRunning test2")
    test("ff" * 8, "00" * 16, "604ae6ca03c20ada")

    print("\nRunning test3")
    test("00" * 8, "ff" * 8 + "00" * 8, "9fb51935fc3df524")

    print("\nRunning test4")
    test("00" * 8, "00" * 8 + "ff" * 8, "78a54cbe737bb7ef")

    print("\nRunning test5")
    test("0123456789abcdef", "00" * 8 + "fedcba9876543210", "ae25ad3ca8fa9ccf")
