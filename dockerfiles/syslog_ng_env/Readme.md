# The goal of this docker image
 * This image is for create a clean Ubuntu Trusty environment where you can build you local syslog-ng source

# Usage
 * Let assume your local syslog-ng path is at $HOME/syslog-ng/, than you can run this image to build your source.
```
$ docker run --interactive=true --tty=true --volume=$HOME/syslog-ng:/source balabit/syslog_ng_env:latest /bin/bash
```
 * After you have entered to the container you can run the helper build script:
```
# ./syslog_ng_build.sh
```

# Important
 * The main use case for this image is: 
   * You change your code on your host, and in the docker container you can build it.
 * If you made changes inside the container it can change the file permissions on your source, 
 because inside the container you work with root user.