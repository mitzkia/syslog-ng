FROM debian:latest
MAINTAINER Andras Mitzki <andras.mitzki@balabit.com>

# init
RUN apt-get update && apt-get install -y --no-install-recommends python-wrapt wget
ENV PACKAGE_SOURCE="http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/Debian_8.0/ /"
ENV PACKAGE_SOURCE_KEY="http://download.opensuse.org/repositories/home:laszlo_budai:syslog-ng/Debian_8.0/Release.key"
ENV PATH=$PATH:/install/sbin/:/opt/gradle/bin
ENV PYTHONPATH=$PYTHONPATH:/install
COPY scripts/deb_install_package_repository.sh /deb_install_package_repository.sh
RUN ./deb_install_package_repository.sh

# action
COPY scripts/download_java_destination_libraries.sh /download_java_destination_libraries.sh
RUN ./download_java_destination_libraries.sh

COPY syslog_ng_dep_packages/deb_packages.txt /deb_packages.txt
COPY scripts/deb_install_and_setup_packages.sh /deb_install_and_setup_packages.sh
RUN ./deb_install_and_setup_packages.sh

COPY scripts/checkout_and_build_syslog_ng.sh /checkout_and_build_syslog_ng.sh
RUN ./checkout_and_build_syslog_ng.sh

# test
COPY scripts/check_syslog_ng_start.sh /check_syslog_ng_start.sh
COPY syslog_ng_config/sngexample.py /install/sngexample.py
COPY syslog_ng_config/syslog-ng-compact.conf /syslog-ng-compact.conf
RUN ./check_syslog_ng_start.sh
