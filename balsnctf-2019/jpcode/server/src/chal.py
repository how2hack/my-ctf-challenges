#!/usr/bin/env python

import os

def error():
    print "Nope"
    exit(1)

def toHEX(a):
    result = hex(0o200 + int(oct(a)[-2:], 8))[2:]
    result = hex(0o200 + int(oct(a)[-4:-2], 8))[2:] + result
    result = hex(0o340 + int(oct(a)[-6:-4], 8))[2:] + result

    return result.decode('hex')

def getJapList():
    jap = list(range(0x3041, 0x3096+1))     # U+3041 ~ U+3096
    jap += list(range(0x3099, 0x309f+1))    # U+3099 ~ U+309F
    jap += list(range(0x30a0, 0x30ff+1))    # U+30A0 ~ U+30FF
    jap += list(range(0x3190, 0x319f+1))    # U+3190 ~ U+319F
    jap += list(range(0x31f0, 0x31ff+1))    # U+31F0 ~ U+31FF
    jap += list(range(0xff66, 0xff9f+1))    # U+FF66 ~ U+FF9F

    japlist = []

    for i in jap:
        japlist.append(toHEX(i))
    
    return japlist

def checkInput(payload):
    japlist = getJapList()

    if len(payload) == 0 or len(payload) % 3 != 0:
        error()

    for i in range(len(payload)//3):
        if payload[i*3:i*3+3] not in japlist:
            error()

if __name__ == "__main__":
    payload = raw_input().strip('\n')
    MAX_NUM = 90*3
    payload = payload[:MAX_NUM]
    checkInput(payload)
    os.execve('./chal', ['./chal', payload], os.environ)
