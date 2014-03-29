# Installing Python packages

## APT

Some Python packages can be found in the Raspbian archives, and can be installed using APT, for example:

```
sudo apt-get update
sudo apt-get install python-picamera
```

This is a preferable method of installing things as it means that the modules you install can be kept up to date easily with the usual `sudo apt-get update` and `sudo apt-get upgrade` commands.

Python packages in Raspbian compatible with Python 2.x will always have a `python-` prefix. So, the `picamera` package for Python 2.x is named `python-picamera` (as shown in the example above). Python 3 packages always have a `python3-` prefix. So, to install `rpi.gpio` for Python 3 you would use:

```
sudo apt-get install python3-rpi.gpio
```

Uninstalling packages installed via APT can be accomplished as follows:

```
sudo apt-get remove python3-rpi.gpio
```

## pip

Not all Python packages are available in the Raspbian archives, and those that are can sometimes be out of date. If you can't find a suitable version in the Raspbian archives you can install packages from the [Python Package Index](http://pypi.python.org/) (also known as PyPI). To do so, use the `pip` tool (which is installed from the `python-pip` package in Raspbian):

```
sudo apt-get install python-pip
sudo pip install simplejson
```

Note that no `python-` prefix is required when using `pip`. To update a Python package that was installed with `pip`, use the following command:

```
sudo pip install -U simplejson
```

You can only specify a single package to upgrade at a time, and there is no option to upgrade all packages installed with `pip` universally (hence why APT-based installations are generally considered easier to maintain).

Uninstalling packages installed with pip can be accomplished like so:

```
sudo pip uninstall simplejson
```

All the above commands apply to Python 2.x only. To use PyPI with Python 3 you need to install the `pip-3.2` tool from the `python3-pip` package in Raspbian:

```
sudo apt-get install python3-pip
```

Then simply substitute `pip` in the commands above with `pip-3.2`. For example:

```
sudo pip-3.2 install six
sudo pip-3.2 install -U six
sudo pip-3.2 uninstall six
```

## Conflicting Installations

It is possible to install a package with APT *and* pip, as each system installs to a different location. For example:

```
sudo apt-get install python-picamera
sudo pip install picamera
```

In this case, the package installed with pip will take precedence when importing it in the Python interpreter. This can cause hard to spot issues if the APT-installed package is subsequently upgraded, but the pip one is not (which is likely given the requirement to upgrade pip-installed packages one-by-one). While you'll have an up to date installation, it will be "hidden" by an out of date one, at least as far as the Python interpreter is concerned.

The simplest solution is to pick one of the installations to remove. You can either uninstall the pip-installed package, which will allow the APT-installed package to be used normally:

```
sudo pip uninstall picamera
```

Or you can uninstall the APT-installed package, and manage the pip-installed package on its own. For example:

```
sudo apt-get remove python-picamera
sudo pip install -U picamera
```
