## pxetools
We have created a Python script that is used internally to quickly set up Pi's that will network boot. It takes a serial number, which you can find in `cat /proc/cpuinfo`, an owner name and the name of the Pi. It then creates a root filesystem for that Pi from a Raspberry Pi OS image. There is also a --list option which will print out the IP address of the Pi, and a --remove option. The following instructions describe how to set up the environment required by the script starting from a fresh Raspberry Pi OS lite image. It might be a good idea to mount a hard disk or flash drive on /nfs so that your SD card isn't providing filesystems to multiple Pi's. This is left as an exercise for the reader.

```
sudo apt update
sudo apt full-upgrade -y
sudo reboot

wget https://raw.githubusercontent.com/raspberrypi/documentation/master/hardware/raspberrypi/bootmodes/pxetools/prepare_pxetools
bash prepare_pxetools
```

When prompted about saving iptables rules, say no.

prepare_pxetools should prepare everything you need to use pxetools.

We found that we needed to restart the nfs server after using pxetools for the first time. Do this with:
```
sudo systemctl restart nfs-kernel-server
```

Then plug in your Pi and it should boot!
