#!/bin/bash -xe

cat /deb_packages.txt | xargs apt-get install -y --no-install-recommends
