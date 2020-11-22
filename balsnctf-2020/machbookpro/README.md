# Machbook Pro

OSX Tiny Heap Region Metadata Corruption (Double Free)

Description:

```
Mach Apple Better Again!!!

`nc machbookpro.balsnctf.com 19091`

Author: how2hack
```

Solves: 1/490

## Tiny Heap Metadata

In Tiny Heap, each block is 0x10 bytes. In macOS Catalina 10.15.7, heap metadata is located at the beginning of each magazine. Tiny Heap's metadata is used to describe if the block is inused and if the block is the beginning of a chunk (header). Every 32 blocks use a `uint32_t` to indicate `header` bits and a `uint32_t` to indicate `inuse` bit. For instance, the first `header & 0x1` and the first `inuse & 0x1` will describe the status of the first block of tiny heap.

## Double Free in Tiny Heap

As mentioned above, the metadata consists of each block's `inuse` status, so if we can corrupt the metadata, we probably can trick Tiny Heap to double free a block!

Here is the [poc](./doublefree_poc.c) of Double Free in Tiny Heap.

## Vulnerability

This challenge has an out-of-bound write on `Create Post` operation, you can give negative index to overwrite the metadata which can be used to trigger the Double Free exploitation.

