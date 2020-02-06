# Unlucky

Basic Linux Knowledge

Description:

```
Can't solve Lucky? Try your skill here!

nc eof.ais3.org 29091
```

Solves: 9/15

## Idea

The idea is from [@LiveOverflow](https://twitter.com/LiveOverflow)'s Youtube [video](https://www.youtube.com/watch?v=1hScemFvnzw). You can recover your deleted file from `/proc/*/fd` if the `fd` is not closed.

## Exploit
* Find the `pid` of the process
    * You can use `ps aux` to find the `pid` first and create a new connection
    * The new connection `pid` should be the previous `pid+4`
    * You may get the wrong `pid` if too many users connecting to the server
    * Just keep trying, the success rate is very high
* Read the lucky number from `/proc/pid+4/fd/3`
* Get shell and execute `/readflag`
    * A very basic format string vulnerability
    * Input `%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.` then you will find the flag

