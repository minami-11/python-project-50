#### Hexlet tests, Github Actions and CodeClimate marks:
[![Actions Status](https://github.com/minami-11/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/minami-11/python-project-50/actions)
[![Build test Workflow](https://github.com/minami-11/python-project-50/actions/workflows/on_push_test_build.yml/badge.svg?branch=main)](https://github.com/minami-11/python-project-50/actions/workflows/on_push_test_build.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/6878188d39a7847f8557/maintainability)](https://codeclimate.com/github/minami-11/python-project-50/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6878188d39a7847f8557/test_coverage)](https://codeclimate.com/github/minami-11/python-project-50/test_coverage)


### Description:
Here is the Gendiff programm. It compares two files and marks differences between them
(flat or nested - doesn't matter). This revision works only with json and yaml formats.
Has three output formats (default one - is stylish):
- stylish: nested output (tree view) with changing marks
- plain: if there is a difference it will be shown in a line
- json: raw output file with changing marks

#### How to use:
* enter outout format ('stylish' - is the default)
* and two file names (json or yaml)
* ..
* profit

#### Installation process and commands:
Staying in the root project directory use these commands:
```
make build              #poetry build distribution package file in .whl format
make package-install	#pip install Gendiff from .whl file
```
No errors occured - the installation has been success.

```
make package-uninstall  #pip uninstall the Gendiff
```

#### Other commands for devepolers:
```
make lint                   #check quality of Python Code with flake8
make shell                  #enter virtual env
make publish                #perform all actions for publishing, except uploading the package
make automate_build         #start commans 1by1: shell, lint, build, publish, pip list
make check                  #runs pytest and shows which tests have been run
make test-cover             #runs pytest cover and saves report in xml
gendiff1                    #runs gendiff with file1.json and file2.json from main root dir
```

### Installation:
[![asciicast](https://asciinema.org/a/6qE0shSule2Z1eU28sLkVupQc.svg)](https://asciinema.org/a/6qE0shSule2Z1eU28sLkVupQc)

### How Gendiff works:
[![asciicast](https://asciinema.org/a/s7bsfFbxDvxXkHXQPtdHHgdMG.svg)](https://asciinema.org/a/s7bsfFbxDvxXkHXQPtdHHgdMG)
