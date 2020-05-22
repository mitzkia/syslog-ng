# Description of python functional test framework (aka Light)

## What is Light

* Ligth was written to add a fast and easy to use test framework into syslog-ng maintainers hand

*

## Package dependencies of Light

* Currently Light supports both Python2 and Python3 versions
* The first class python dependecy of Light is: pytest
* Other runtime package dependencies are: psutil, pathlib2
* If you want to implement some tests in Light you may install also pre-commit as a linter manager
* You can always find Light dependencies in one of the following requirements.txt files:
  * requirements.txt
  * dbld/pip_packages.manifest

* In summary, installation of python3 runtime dependencies for Light:
* $ python3 -m pip install pytest psutil pathlib2
* Installation of python3 developement dependencies for Light:
* $ python3 -m pip install pre-commit pre-commit-hook

## Environment dependencies of Light

* syslog-ng install dir

## How to use Light

* There are two main usages:
  * with make targets
  * natively with pytest itself
