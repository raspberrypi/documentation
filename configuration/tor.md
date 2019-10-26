# Onionizing Repositories

```bash
sudo dpkg-reconfigure tzdata

sudo nano /etc/apt/sources.list

deb http://deb.debian.org/debian buster main contrib non-free
deb-src http://deb.debian.org/debian buster main contrib non-free

deb http://deb.debian.org/debian-security buster/updates main contrib non-free
deb-src http://deb.debian.org/debian-security buster/updates main contrib non-free

deb http://deb.debian.org/debian buster-updates main contrib non-free
deb-src http://deb.debian.org/debian buster-updates main contrib non-free

deb http://deb.debian.org/debian buster-backports main contrib non-free
deb-src http://deb.debian.org/debian buster-backports main contrib non-free

sudo nano /etc/apt/sources.list.d/raspi.list

deb http://archive.raspberrypi.org/debian buster main ui
deb-src http://archive.raspberrypi.org/debian buster main ui

wget https://archive.raspberrypi.org/debian/raspberrypi.gpg.key -O - | sudo apt-key add -

sudo apt update -y
sudo apt install apt-transport-https curl debian-keyring -y

sudo nano /etc/apt/sources.list

deb https://deb.debian.org/debian buster main contrib non-free
deb-src https://deb.debian.org/debian buster main contrib non-free

deb https://deb.debian.org/debian-security buster/updates main contrib non-free
deb-src https://deb.debian.org/debian-security buster/updates main contrib non-free

deb https://deb.debian.org/debian buster-updates main contrib non-free
deb-src https://deb.debian.org/debian buster-updates main contrib non-free

deb https://deb.debian.org/debian buster-backports main contrib non-free
deb-src https://deb.debian.org/debian buster-backports main contrib non-free

sudo nano /etc/apt/sources.list.d/raspi.list

deb https://archive.raspberrypi.org/debian buster main ui
deb-src https://archive.raspberrypi.org/debian buster main ui

sudo nano /etc/apt/sources.list.d/torproject.list

deb https://deb.torproject.org/torproject.org buster main
deb-src https://deb.torproject.org/torproject.org buster main

curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt update -y
sudo apt install apt-transport-tor tor deb.torproject.org-keyring -y

sudo nano /etc/apt/sources.list

deb tor+http://vwakviie2ienjx6t.onion/debian buster main contrib non-free
deb-src tor+http://vwakviie2ienjx6t.onion/debian buster main contrib non-free

deb tor+http://sgvtcaew4bxjd7ln.onion/debian-security buster/updates main contrib non-free
deb-src tor+http://sgvtcaew4bxjd7ln.onion/debian-security buster/updates main contrib non-free

deb tor+http://vwakviie2ienjx6t.onion/debian buster-updates main contrib non-free
deb-src tor+http://vwakviie2ienjx6t.onion/debian buster-updates main contrib non-free

deb tor+http://vwakviie2ienjx6t.onion/debian buster-backports main contrib non-free
deb-src tor+http://vwakviie2ienjx6t.onion/debian buster-backports main contrib non-free

sudo nano /etc/apt/sources.list.d/raspi.list

deb tor+https://archive.raspberrypi.org/debian buster main ui
deb-src tor+https://archive.raspberrypi.org/debian buster main ui

sudo nano /etc/apt/sources.list.d/torproject.list

deb tor+http://sdscoq7snqtznauu.onion/torproject.org buster main
deb-src tor+http://sdscoq7snqtznauu.onion/torproject.org buster main

sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade --auto-remove --purge -y
```
