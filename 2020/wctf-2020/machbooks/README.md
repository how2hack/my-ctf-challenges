# Machbooks

OSX Small Heap Region Metadata Corruption (Overlapped Chunk) + FILE structure exploitation

Description:

```
What kind of books do you like? I like Machbooks!
```

Solves: 1/7

## Writeup slide

* [Machbooks writeup](20201121_WCTF2020_Machbooks.pdf)

## Unintended Solution

* There is an unintended solution found by [kylebot](https://twitter.com/jkjh1jkjh1) from Shellphish, which you can brute-force the libc address by partial overwrite the `fp`. If the file operations still work, then the `fp` is not corrupted. Amazing technique! His writeup: http://kylebot.net/2020/11/20/WCTF-2020-machbooks/


