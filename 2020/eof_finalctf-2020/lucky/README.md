# Lucky

Breaking Mersenne Twister with only 2 values

Description:

```
Can't solve Unlucky? Try your luck here!

nc eof.ais3.org 39091
```

Solves: 8/15

## Idea

Check this recent [blog post](https://www.ambionics.io/blog/php-mt-rand-prediction).

## Exploit
* Get the first random value
* Get the 227th random value
* Calculate the seed and return 228th random value

