# Machbook Air

APFS Normalization

Description:

```
I developed this safe project on my old linux server.
I recently move this project to a new Macbook Air.
It is still safe, right?

`nc machbookair.balsnctf.com 19091`

Author: how2hack
```

Solves: 4/490

## Inspiration

One day, I cloned a [repository](https://github.com/HexHive/T-Fuzz) from Github to one of the directory in a docker container (Ubuntu), which is mounted to host (macOS) directory. However, I can never install the program successfully due to some files missing. Then I checked `git status` and tried to restore the missing file using `git checkout` and no matter how I did the file `TFuzz` and the directory `tfuzz` can never exist at the same time. This is because macOS uses APFS which is a different file system from Linux.

Then on DEFCON'28, one of the challenge `parallel-af` can `cat` any files except the file includes the name `flag`. However, due to the similar setup as above (mounted directory from host inside a container), we can read the flag by `cat Flag`. Of course this solution will not work on remote :P

I found this very interesting and did some research on APFS, so I created this challenge.

## Concept

APFS is normalization-insensitive, which all the filenames are case-insensitive (e.g `abc` and `ABC` can't coexist). This is also affecting Unicode, such as Unicode `c3 a9` and Unicode `65 cc 81` are the same character `é` but different representation in Unicode.

## Vulnerability

The binary will check if a user is trying to overwrite the `admin`'s password file by banning all the characters used as the `admin`'s password filename. However, due to APFS normalization, we can still overwrite the `admin`'s filename if the filename uses Unicode such as `c3 a9` (character `é`), and overwrite the file using filename as `65 cc 81` (also character `é`). There are many other possible Unicodes can trigger this bug.

By overwriting the `admin`'s password file, you can login as `admin`. Also, it will lead to buffer overflow at `Admin Area` if your password is longer than `0x30`. Using this vulnerability to leak `code`, `stack`, and `canary` and trigger ROP to read the flag.

## Fun Fact

This challenge is slightly similar to the challenge [`Does Linux Dream of Windows?`](https://gist.github.com/ytoku/ffd67666953d707040b391e17218dccb) (Great Challenge btw) in `TokyoWesterns CTF 6th 2020`. However, I created the challenge before that CTF held, so I decided to still release on `Balsn CTF 2020` :P

## Writeup
* https://github.com/perfectblue/ctf-writeups/tree/master/2020/BalsnCTF/machbookair