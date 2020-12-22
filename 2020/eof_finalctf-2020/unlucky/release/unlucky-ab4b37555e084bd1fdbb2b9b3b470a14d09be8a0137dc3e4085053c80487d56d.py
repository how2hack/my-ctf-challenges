#!/usr/bin/env python3 -u

import os
import shutil
import subprocess

def main():
    rng = open('/dev/urandom', encoding='ISO-8859-1').read(32)
    rng = int.from_bytes(bytes(rng, 'utf-8'), 'little')

    dirname = open('/dev/urandom', encoding='ISO-8859-1').read(32)
    dirname = int.from_bytes(bytes(dirname, 'utf-8'), 'little')
    dirname = '/tmp/{}'.format(dirname)

    filename = open('/dev/urandom', encoding='ISO-8859-1').read(32)
    filename = int.from_bytes(bytes(filename, 'utf-8'), 'little')
    filename = '{}/{}'.format(dirname, filename)

    os.mkdir(dirname)
    f = open(filename, 'w')
    f.write('{}\n'.format(rng))
    f.flush()

    shutil.rmtree(dirname)
    chance()
    guess(rng)

def chance():
    cmd = input('Give you a chance to find the flag: ').strip()[:20]
    try:
        p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p.communicate()[0].decode('utf-8'))
    except:
        pass

def guess(rng):
    lucky = input("Can't find the flag? Then guess the lucky number: ").strip()
    if int(lucky) == rng:
        print('Enjoy your shell :)')
        os.system('/bin/bash')
    else:
        print('May the luck be with you')

if __name__ == "__main__":
    main()

