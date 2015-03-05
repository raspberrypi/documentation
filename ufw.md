ufw
===

`ufw` (*Uncomplicated FireWall*) is a program for managing a netfilter firewall which aims to provide an easy to use interface for the user.

You can also look at gui frontends such as `gufw` or use `iptables` which has deep learning curve.

## Install ufw

First install the `ufw` package by typing the following command in to the
Terminal:

```bash
sudo apt-get -y install ufw
```

## Usage

|--------------------------------------|---------------------------------------|
| `sudo ufw enable`                    | enable ufw                            |
| `sudo ufw status verbose numbered`   | show status of firewall verbosely     |
| `sudo ufw default deny incoming`     | deny all incoming by default          |
| `sudo ufw allow from 192.168.0.0/24` | allow any protocol from intranet      |
| `sudo ufw allow 53/tcp`              | allow incoming tcp packets on port 53 |
| `sudo ufw allow SSH`                 | allow ssh from anywhere               |
| `sudo ufw limit SSH`                 | rate limiting for ssh                 |
| `sudo ufw delete allow SSH`          | remove standard ssh rules             |
| `sudo ufw logging on`                | enable logging                        |
| `sudo ufw app list`                  | list default port for common programs |
|--------------------------------------|---------------------------------------|
