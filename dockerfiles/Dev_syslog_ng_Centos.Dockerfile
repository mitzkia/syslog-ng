FROM centos:latest
MAINTAINER Andras Mitzki <andras.mitzki@balabit.com>

# init
RUN yum install -y epel-release wget
ENV PACKAGE_SOURCE="https://copr.fedoraproject.org/coprs/czanik/syslog-ng39/repo/epel-7/czanik-syslog-ng39-epel-7.repo"
ENV PATH=$PATH:/install/sbin/:/opt/gradle/bin
ENV PYTHONPATH=$PYTHONPATH:/install
COPY scripts/rpm_install_package_repository.sh /rpm_install_package_repository.sh
RUN ./rpm_install_package_repository.sh

# action
COPY scripts/download_java_destination_libraries.sh /download_java_destination_libraries.sh
RUN ./download_java_destination_libraries.sh

COPY syslog_ng_dep_packages/rpm_packages.txt /rpm_packages.txt
COPY scripts/rpm_install_and_setup_packages.sh /rpm_install_and_setup_packages.sh
RUN ./rpm_install_and_setup_packages.sh

COPY scripts/checkout_and_build_syslog_ng.sh /checkout_and_build_syslog_ng.sh
RUN ./checkout_and_build_syslog_ng.sh

# test
COPY scripts/check_syslog_ng_start.sh /check_syslog_ng_start.sh
COPY syslog_ng_config/sngexample.py /install/sngexample.py
COPY syslog_ng_config/syslog-ng-compact.conf /syslog-ng-compact.conf
RUN ./check_syslog_ng_start.sh
