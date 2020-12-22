#!/bin/bash

[ ! -d "./tmp" ] && mkdir ./tmp
CURDIR=`pwd`
NEWDIR=`mktemp -d ./tmp/XXXXXXXXXXXXXXXX`
cd $NEWDIR
sandbox-exec -f $CURDIR/machbooks.sb $CURDIR/machbooks
cd $CURDIR
rm -rf $NEWDIR
