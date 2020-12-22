# RRPS

Predicting Mersenne Twister with partial states (Crypto) + House of Einherjar with null byte off-by-one (Pwn)

Description:

```
A universe that rocks don't always crush scissors...
nc IP 19091

Patch file: librps.so
Additional note, you can only patch these functions: 
- play
- add_move
- remove_move
- edit_move
Patch size limit: 44040 bytes
Max patch size: 100 bytes

Run: LD_LIBRARY_PATH=./ ./chal <num_of_bytes_you_patched>
```

Hints given on Day-2:

```
1) Mersenne Twister
2) House of Einherjar
```

Solves: 0/6 (Crypto), 0/6 (Pwn)

## Vulnerabilities

### Predicting Mersenne Twister's state with partial states (Crypto)

* Given $state_t[i]$, $state_t[i+1]$, $state_t[i+M]$, you can predict $state_{t+1}[i]$

### House of Einherjar with null byte off-by-one (Pwn)

* There is an information leak vulnerability
* There is a null byte off-by-one vulnerability

## Thoughts

* I am so sad that no one successfully exploit during the competition.
* After the contest, one team which is `10sec` said they managed to exploit using the Crypto bug, but their exploit was too slow and couldn't successfully attack other teams due to timeout.
* One of my teammate `kevin47` managed to create the Pwn exploit in 4 hours on Day-2 of the contest :O
  * I asked him to exploit this challenge during the competition to make sure my challenge wasn't too hard
* Stripping a C++ binary makes teams not to play this challenge :(
* I won't release my exploit, please DM me if you successfully exploit the Pwn part :)