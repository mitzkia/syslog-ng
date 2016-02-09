#!/bin/bash -x

cd /source
mkdir -p ./build/ /install
./autogen.sh
cd build/
../configure --prefix=/install --enable-debug
make
make install
make check