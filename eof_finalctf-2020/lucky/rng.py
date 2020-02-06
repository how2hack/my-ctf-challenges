#!/usr/bin/env python3 -u
import random

class RNG:
    def __init__(self):
        self.f = 1812433253
        (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
        self.a = 0x9908b0df
        (self.u, self.d) = (11, 0xffffffff)
        (self.s, self.b) = (7, 0x9d2c5680)
        (self.t, self.c) = (15, 0xefc60000)
        self.l = 18
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (1 << self.r)

        self.index = self.n + 1
        self.state = [0]*self.n
        self.seed = None

    def srand(self, seed):
        self.seed = seed
        self.state[0] = seed & 0xffffffff

        for i in range(1, self.n):
            self.state[i] = (self.f * (self.state[i-1] ^ (self.state[i-1] >> (self.w-2))) + i) & 0xffffffff
            
    def rand(self):
        if self.seed == None:
            self.srand(random.randrange(1, 0xffffffff))
        if self.index >= self.n:
            self.twist()
        
        y = self.state[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)

        self.index += 1

        return y & 0xffffffff

    def twist(self):
        for i in range(self.n):
            x = self.state[i] & self.upper_mask
            x += self.state[(i+1) % self.n] & self.lower_mask
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.a
            self.state[i] = self.state[(i+self.m) % self.n] ^ xA
        self.index = 0

def win():
    print('Congratulation!')
    flag = open('/flag', 'r').read()
    print(flag)
    exit(0)

def shuffle(rng):
    print('How many times do you want to shuffle?')
    n = int(input('> ').strip())
    if n < 0:
        print("Don't mess with your luck >:(")
        exit(-1)
    for _ in range(n):
        rng.rand()

def guess(rng):
    print('Now guess the lucky number!')
    n = int(input('> ').strip())
    lucky_number = rng.rand()
    print('Lucky Number:', lucky_number)
    print('Your Guess:', n)
    if n == lucky_number:
        win()
    else:
        print('Better luck next time :(')
    

if __name__ == "__main__":
    rng = RNG()
    
    for _ in range(3):
        shuffle(rng)
        guess(rng)
