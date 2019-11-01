# SSHFS (SSH Filesystem)

SSHFS allows you to mount a Raspberry Pi's files over an SSH session.

## Install

### Linux

Install SSHFS on your computer with:

```bash
sudo apt install sshfs
```

(This assumes you are using a Debian-based system)

### Mac

See [osxfuse](https://github.com/osxfuse/osxfuse/wiki/SSHFS)

## Usage

First, create a directory on your host computer:

```bash
mkdir pi
```

Then mount the Raspberry Pi's filesystem to this location:

```bash
sshfs pi@192.168.1.3: pi
```

Now enter this directory as if it is a regular folder; you should be able to see and access the contents of the Raspberry Pi:

```bash
cd pi
ls
```

You can also browse the Pi's filesystem using your computer's file manager (including drag-and-drop to copy files between devices), and use your computer's applications (text editors, image processing tools, and so on) to edit files directly on the Pi.
