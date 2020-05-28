# Installing Python packages

## apt

Some Python packages can be found in the Raspberry Pi OS archives and can be installed using apt. For example:

```bash
sudo apt update
sudo apt install python3-picamera
```

This is the preferred method of installing software, as it means that the modules you install can be kept up to date easily with the usual `sudo apt update` and `sudo apt full-upgrade` commands.

Python packages in Raspberry Pi OS which are compatible with Python 2.x will always have a `python-` prefix. So, the `picamera` package for Python 2.x is named `python-picamera` (as shown in the example above). Python 3 packages always have a `python3-` prefix. So, to install `picamera` for Python 3 you would use:

```bash
sudo apt install python3-picamera
```

Uninstalling packages installed via APT can be accomplished as follows:

```bash
sudo apt remove python3-picamera
```

They can be completely removed with `purge`:

```bash
sudo apt purge python3-picamera
```

## pip

Not all Python packages are available in the Raspberry Pi OS archives, and those that are can sometimes be out-of-date. If you can't find a suitable version in the Raspberry Pi OS archives, you can install packages from the [Python Package Index](http://pypi.python.org/) (PyPI). To do so, use the `pip` tool.

`pip` is installed by default in Raspberry Pi OS Desktop images (but not Raspberry Pi OS Lite). You can install it with `apt`:

```bash
sudo apt install python3-pip
```

To get the Python 2 version:

```bash
sudo apt install python-pip
```

`pip3` installs modules for Python 3, and `pip` installs modules for Python 2.

For example, the following command installs the Unicorn HAT library for Python 3:

```bash
sudo pip3 install unicornhat
```

The following command installs the Unicorn HAT library for Python 2:

```bash
sudo pip install unicornhat
```

Uninstall Python modules with `sudo pip3 uninstall` or `sudo pip uninstall`.

Upload your own Python modules to `pip` with the [guide at PyPI](https://wiki.python.org/moin/CheeseShopTutorial#Submitting_Packages_to_the_Package_Index).

## piwheels

The official Python Package Index (PyPI) hosts files uploaded by package maintainers. Some packages require compilation (compiling C/C++ or similar code) in order to install them, which can be a time-consuming task, particlarly on the single-core Raspberry Pi 1 or Pi Zero.

piwheels is a service providing pre-compiled packages (called Python wheels) ready for use on the Raspberry Pi. Raspberry Pi OS is pre-configured to use piwheels for pip. Read more about the piwheels project at [www.piwheels.org](https://www.piwheels.org/).
