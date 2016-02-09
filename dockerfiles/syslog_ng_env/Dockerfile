FROM debian:latest
MAINTAINER Andras Mitzki <andras.mitzki@balabit.com>

ENV PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig/
ADD syslog_ng_build.sh /syslog_ng_build.sh

RUN apt-get update -qq && apt-get install -y \
    wget

RUN wget -qO - http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/Debian_8.0/Release.key | apt-key add -
RUN echo 'deb http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/Debian_8.0 ./' | tee --append /etc/apt/sources.list.d/syslog-ng-obs.list

ADD dev-dependencies.txt .
RUN apt-get update -qq && cat dev-dependencies.txt | grep -v "#" | xargs apt-get install -y

ADD https://github.com/balabit/syslog-ng/blob/master/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD libsyslog-ng.conf /etc/ld.so.conf.d/libsyslog-ng.conf
ADD openjdk-libjvm.conf /etc/ld.so.conf.d/openjdk-libjvm.conf
RUN ldconfig

RUN mkdir /source
VOLUME /source
