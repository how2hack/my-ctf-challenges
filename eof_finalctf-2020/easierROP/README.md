# easierROP

ROP without leak + fork process debugging + dlsym

Description:

```
Enjoy ROP

nc eof.ais3.org 19091
```

Solves: 4/15

## Idea

The idea is from Trend Micro Final CTF 2019 and EOF CTF Qualification. In EOF CTF Qualification, there is a challenge `EasyROP` (designed by [@tensxu](https://twitter.com/tensxu)) which uses `strcpy` to create any ROP gadgets using libc addresses without any leak in 32-bits ELF binary. However, only 1 team solved the challenge. So I try to create another version similar to `EasyROP` using the idea I get from TMCTF Final, which uses `dlsym` to get arbitrary libc addresses in 64-bits ELF binary.

## Challenge
* You can't leak anything because `stdin`, `stdout` and `stderr` are closed
* Child process must exit with status code `222`
* Parent process can only get input from child process
* Pwn 2 processes in 1 ROP :D

## Vulnerability
* Both child and parent process has trivial buffer overflow vulnerability

## Exploit
* Child process
    * `dlsym` to get `write` libc address
    * Use `ret2csu` to control the registers for `write`
    * `dlsym` to get `exit` libc address
    * Call `exit` with status code `222`
* Parent process
    * `dlsym` to get `system` libc address
    * Call `system` and print flag to your remote machine


