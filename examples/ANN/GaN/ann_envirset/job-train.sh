#!/bin/bash
#SBATCH -p test -n 80 -J GaN 
#yhrun  generate.x-2.1.0-ifort_mpi generate.in > generate.out
if [ -f "train.out" ]; then
    rm -f "train.out"
fi
if [ -f "train.restart" ]; then
    rm -f "train.restart"
fi
if [ -f "train.rngstate" ]; then
    rm -f "train.rngstate"
fi
if [ -f "train.time" ]; then
    rm -f "train.time"
fi
if [ -f "Ga.10t-10t.nn" ]; then
    rm -f "Ga.10t-10t.nn"
fi
if [ -f "N.10t-10t.nn" ]; then
    rm -f "N.10t-10t.nn"
fi
if [ -f "GaN.train.scaled" ]; then
    rm -f "GaN.train.scaled"
fi
if [ -f "GaN.train.asc" ]; then
    rm -f "GaN.train.asc"
fi
yhrun  train.x-2.1.0-ifort_mpi train.in > train.out
./trnset2ASCII.x GaN.train.scaled GaN.train.asc
if [ ! -d "output" ]; then
    mkdir output
else
    rm -rf output
    mkdir output
fi
cp nga.py ./output
find -maxdepth 1 -name "*.10t-10t.nn-*" -exec mv {} output \;
