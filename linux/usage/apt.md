# APT

The easiest way to manage installing, upgrading, and removing software is using APT (Advanced Packaging Tool) from Debian. If a piece of software is packaged in Debian and it works on the Raspberry Pi's ARM architecture, it should also be available in Raspberry Pi OS.

To install or remove packages you need root user permissions, so your user needs to be in `sudoers` or you must be logged in as `root`. Read more about [users](../usage/users.md) and [root](../usage/root.md).

To install new packages, or update existing ones, you'll need an internet connection.

Note that installing software uses up disk space on your SD card, so you should keep an eye on disk usage and use an appropriately sized SD card.

Also note that a lock is performed while software is installing, so you can't install multiple packages at the same time.

## Software sources

APT keeps a list of software sources on your Pi in a file at `/etc/apt/sources.list`. Before installing software, you should update your package list with `apt update`:

```bash
sudo apt update
```

## Installing a package with APT

```bash
sudo apt install tree
```

Typing this command should inform the user how much disk space the package will take up and asks for confirmation of the package installation. Entering `Y` (or just pressing `Enter`, as yes is the default action) will allow the installation to occur. This can be bypassed by adding the `-y` flag to the command:

```bash
sudo apt install tree -y
```

Installing this package makes `tree` available for the user.

## Using an installed package

`tree` is a command-line tool which provides a visualisation of the structure of the current directory, and all its contents.

- Typing `tree` runs the tree command. For example:

```bash
tree
..
├── hello.py
├── games
│   ├── asteroids.py
│   ├── pacman.py
│   ├── README.txt
│   └── tetris.py

```

- Typing `man tree` gives the manual entry for the package `tree`.
- Typing `whereis tree` shows where `tree` lives:

```bash
tree: /usr/bin/tree
```

## Uninstalling a package with APT

### Remove

You can uninstall a package with `apt remove`:

```bash
sudo apt remove tree
```

The user is prompted to confirm the removal. Again, the `-y` flag will auto-confirm.

### Purge

You can also choose to completely remove the package and its associated configuration files with `apt purge`:

```bash
sudo apt purge tree
```

## Upgrading existing software

If software updates are available, you can get the updates with `sudo apt update` and install the updates with `sudo apt full-upgrade`, which will upgrade all of your packages. To upgrade a specific package, without upgrading all the other out-of-date packages at the same time, you can use `sudo apt install somepackage` (which may be useful if you're low on disk space or you have limited download bandwidth).

## Searching for software

You can search the archives for a package with a given keyword with `apt-cache search`:

```bash
apt-cache search locomotive
sl - Correct you if you type `sl' by mistake
```

You can view more information about a package before installing it with `apt-cache show`:

```bash
apt-cache show sl
Package: sl
Version: 3.03-17
Architecture: armhf
Maintainer: Hiroyuki Yamamoto <yama1066@gmail.com>
Installed-Size: 114
Depends: libc6 (>= 2.4), libncurses5 (>= 5.5-5~), libtinfo5
Homepage: http://www.tkl.iis.u-tokyo.ac.jp/~toyoda/index_e.html
Priority: optional
Section: games
Filename: pool/main/s/sl/sl_3.03-17_armhf.deb
Size: 26246
SHA256: 42dea9d7c618af8fe9f3c810b3d551102832bf217a5bcdba310f119f62117dfb
SHA1: b08039acccecd721fc3e6faf264fe59e56118e74
MD5sum: 450b21cc998dc9026313f72b4bd9807b
Description: Correct you if you type `sl' by mistake
 Sl is a program that can display animations aimed to correct you
 if you type 'sl' by mistake.
 SL stands for Steam Locomotive.
```
