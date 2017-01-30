#!/bin/bash -xe
syslog-ng -V

nohup syslog-ng -Fedv --no-caps --enable-core & 
sleep 3
pkill syslog-ng

nohup syslog-ng -Fedv --no-caps --enable-core -f /syslog-ng-compact.conf &
sleep 10
pkill syslog-ng