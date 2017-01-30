#!/bin/bash -xe

wget -O - $PACKAGE_SOURCE_KEY | apt-key add -
echo "deb $PACKAGE_SOURCE" | tee --append /etc/apt/sources.list.d/syslog-ng-obs.list
apt-get update