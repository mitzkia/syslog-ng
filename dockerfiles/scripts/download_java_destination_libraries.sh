#!/bin/bash -x

find / | grep 'libjvm\.so' | xargs dirname > /etc/ld.so.conf.d/openjdk-libjvm.conf
ldconfig

mkdir -p /downloaded_java_based_packages
cd /downloaded_java_based_packages

elasticsearch_versions="
https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.5.tar.gz
https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.3/elasticsearch-2.3.3.tar.gz
"
for elasticsearch_version in $elasticsearch_versions; do
    wget --no-check-certificate $elasticsearch_version
    tar -xf $(basename $elasticsearch_version)
done

kafka_versions="
http://xenia.sote.hu/ftp/mirrors/www.apache.org/kafka/0.9.0.1/kafka_2.10-0.9.0.1.tgz
"
for kafka_version in $kafka_versions; do
    wget --no-check-certificate $kafka_version
    tar -xf $(basename $kafka_version)
    ls -la
done

hdfs_versions="
http://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-2.7.2/hadoop-2.7.2.tar.gz
"

for hdfs_version in $hdfs_versions; do
    wget --no-check-certificate $hdfs_version
    mv $(basename $hdfs_version) $(basename http://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-2.7.2/hadoop-2.7.2.tar.gz | sed 's/.gz//g')
    tar -xf $(basename $hdfs_version | sed 's/.gz//g')
    ls -la
done
