# APT

The easiest way to manage installing, upgrading and removing software is using APT (Advanced Packaging Tool) which comes from Debian. If a piece of software is packaged in Debian, and works on the Raspberry Pi's ARM architecture, it should also be available in Raspbian.

To install or remove packages you need root user permissions, so your user needs to be in ```sudoers``` or you must be logged in as ```root```. Read more about [users](../../users.md) and [root](../../root.md).

To install new packages or update existing ones you will need an internet connection.

Note that installing software uses up disk space (on your SD card) so you should keep ene eye on disk usage and use an appropriately sized SD card.

Also note that a lock is performed while software is installing, so you cannot install multiple packages at the same time.

## Software sources

APT keeps a list of software sources on your Pi, in a file at  ```/etc/apt/sources.list```. Before installing software, you should update your package list with ```apt-get update```:

```
sudo apt-get update
```

## Installing a package with APT

Installing a package with APT:

```
sudo apt-get install tree
```
    
Typing this command should prompt the user informing them how much disk space the package will take up and to ask for confirmation of the package installation. Entering '```Y```' will allow the installation to occur. This can be bypassed by adding the ```-y``` flag to the command:

```
sudo apt-get install tree -y
```

Installing this package makes ```tree``` available for the user.

## Using an installed package

```tree``` is a command line tool which provides a visualisation of the directory structure of the current directory and all it contains.

- Typing ```tree``` runs the tree command. For example:

```
tree
..
├── hello.py
├── games
│   ├── asteroids.py
│   ├── pacman.py
│   ├── README.txt
│   └── tetris.py

```
 
- Typing ```man tree``` gives the manual entry for the package ```tree```

- Typing ```whereis tree``` shows where ```tree``` lives:

```
tree: /usr/bin/tree
```
    
## Uninstalling a package with APT
    
### Remove

You can uninstall a package with ```apt-get remove```:

```
sudo apt-get remove tree
```
    
The user is prompted to confirm the removal. Again, the ```-y``` flag will auto-confirm.

### Purge

You can also choose to completely remove the package and its associated configuration files with ```apt-get purge```:

```
sudo apt-get purge tree
```
    
## Upgrading existing software

If software updates are available, you can get the updates with ```apt-get update``` and install the updates with ```apt-get upgrade``` which will upgrade all of your packages.

## Searching for software

You can search the archives for a package with a given keyword with ```apt-cache search```:
    
```
apt-cache search locomotive
sl - Correct you if you type `sl' by mistake
```
