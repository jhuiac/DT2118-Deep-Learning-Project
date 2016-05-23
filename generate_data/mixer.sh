#!/bin/bash
#
# Assuming: on the generate_data folder
#

# Takes one parameter: the sphere file to noisify
noisify() {
    filename=$(basename "$1")
    duration="$(sox --i -D $1)"

    # Generate noise
    sox -n -r 20000 ../data/noise/${filename} synth ${duration} whitenoise vol 0.02
    # Copy clean data
    sox -t sph $1 -b 16 -t wav ../data/clean/${filename}
    # Mix noise + clean
    sox -m ../data/noise/${filename} ../data/clean/${filename} \
        ../data/noisy/${filename} gain -n
}

dir="./tidigits/disc_4.1.1/tidigits/train/man"
rm -rf ../data
rm -rf ../data/clean
rm -rf ../data/noise
rm -rf ../data/noisy
mkdir ../data
mkdir ../data/clean
mkdir ../data/noise
mkdir ../data/noisy

for d in ${dir}/*; do
    echo ${d}
    for s in ${d}/*; do
        noisify ${s}
    done
done
