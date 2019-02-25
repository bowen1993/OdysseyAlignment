#!/usr/bin/env bash

./plain2snt.out $1 $2

./mkcls -m2 -p$1 -c50 -V$1.vcb.classes
./mkcls -m2 -p$2 -c50 -V$2.vcb.classes

./GIZA++ gizaConfig -s $1.vcb -t $2.vcb -c $1_$2.snt -o $3
