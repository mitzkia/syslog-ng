FROM ubuntu:latest
MAINTAINER Andras Mitzki <andras.mitzki@balabit.com>

# init
RUN apt-get update && apt-get install -y --no-install-recommends python-software-properties wget
ENV PACKAGE_SOURCE="http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04 ./"
ENV PACKAGE_SOURCE_KEY="http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04/Release.key"
ENV PATH=$PATH:/install/sbin/:/opt/gradle/bin
ENV PYTHONPATH=$PYTHONPATH:/install
COPY scripts/deb_install_package_repository.sh /deb_install_package_repository.sh
RUN ./deb_install_package_repository.sh

# action
COPY scripts/download_java_destination_libraries.sh /download_java_destination_libraries.sh
RUN ./download_java_destination_libraries.sh
RUN apt-get update && apt-cache search syslog-ng && apt-get install -y syslog-ng libdbd-mysql

# test
COPY scripts/check_syslog_ng_start.sh /check_syslog_ng_start.sh
COPY syslog_ng_config/sngexample.py /install/sngexample.py
COPY syslog_ng_config/syslog-ng-compact.conf /syslog-ng-compact.conf
RUN ./check_syslog_ng_start.sh

# grant
EXPOSE 514/udp
EXPOSE 601/tcp
EXPOSE 6514/tcp

# image start
ENTRYPOINT ["/usr/sbin/syslog-ng", "-F"]