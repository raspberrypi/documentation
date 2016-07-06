# Installing Python packages

## APT

Some Python packages can be found in the Raspbian archives and can be installed using APT, for example:

```bash
sudo apt-get update
sudo apt-get install python3-picamera
```

This is a preferable method of installing software, as it means that the modules you install can be kept up to date easily with the usual `sudo apt-get update` and `sudo apt-get upgrade` commands.

Python packages in Raspbian which are compatible with Python 2.x will always have a `python-` prefix. So, the `picamera` package for Python 2.x is named `python-picamera` (as shown in the example above). Python 3 packages always have a `python3-` prefix. So, to install `picamera` for Python 3 you would use:

```bash
sudo apt-get install python3-picamera
```

Uninstalling packages installed via APT can be accomplished as follows:

```bash
sudo apt-get remove python3-picamera
```

or completely remove with `purge`:

```bash
sudo apt-get purge python3-picamera
```

## pip

Not all Python packages are available in the Raspbian archives, and those that are can sometimes be out of date. If you can't find a suitable version in the Raspbian archives you can install packages from the [Python Package Index](http://pypi.python.org/) (PyPI). To do so, use the `pip` tool.

`pip` is installed by default in Raspbian Jessie (but not Raspbian Wheezy or Jessie Lite). You can install it with `apt`:

```bash
sudo apt-get install python3-pip
```

or the Python 2 version:

```bash
sudo apt-get install python-pip
```

`pip3` installs modules for Python 3 and `pip` installs modules for Python 2.

For example, the following command installs the Unicirn HAT library for Python 3:

```bash
pip3 install unicornhat
```

and the following command installs the Unicorn HAT library for Python 2:

```bash
pip install unicornhat
```

Note: In Raspbian Wheezy, the command for managing Python 3 packages was `pip-3.2` not `pip3`.

Uninstall Python modules with `pip3 uninstall` or `pip uninstall`.

Upload your own Python modules to `pip` with the [guide at PyPI](https://wiki.python.org/moin/CheeseShopTutorial#Submitting_Packages_to_the_Package_Index).
