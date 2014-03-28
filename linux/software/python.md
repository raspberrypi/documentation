# Installing Python packages

## Apt

Some Python packages can be found in the Raspbian archives, and can be installed using Apt, for example:

```
sudo apt-get update
sudo apt-get install python-picamera
```

This is a preferable method of installing things as it means that the modules you install can be kept up to date easily with the usual `sudo apt-get update` and `sudo apt-get upgrade` commands.

Python packages in Raspbian compatible with Python 2.x will always have a `python-` prefix. So, the `picamera` package for Python 2.x is named `python-picamera` (as shown in the example above). Python 3 packages always have a `python3-` prefix. So, to install `rpi.gpio` for Python 3 you would use:

```
sudo apt-get install python3-rpi.gpio
```

## Pip

Not all Python packages are available in the Raspbian archives, and those that are can sometimes be out of date. If you can't find a suitable version in the Raspbian archives you can install packages from the [Python Package Index](http://pypi.python.org/) (also known as PyPI). To do so, use the `pip` tool (which is installed with the `python-pip` package in Raspbian:

```
sudo apt-get install python-pip
sudo pip install simplejson
```

Note that no `python-` prefix is required when using `pip`. To update a Python package that was installed with `pip`, use the following command:

```
sudo pip install -U simplejson
```

You can only specify a single package to upgrade at a time, and there is no option to upgrade all packages installed with `pip` universally (hence why Apt-based installations are generally considered easier to maintain).
