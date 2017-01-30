#!/bin/bash -xe

cat rpm_packages.txt | xargs yum install -y --skip-broken

curl https://bootstrap.pypa.io/get-pip.py | python
find / | grep 'libjvm\.so' | xargs dirname > /etc/ld.so.conf.d/openjdk-libjvm.conf
ldconfig