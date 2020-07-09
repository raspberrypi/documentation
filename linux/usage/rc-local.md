# rc.local

The `rc.local` file is used on Raspberry Pi OS to print the IP address, or addresses, of the system to the screen at boot time. Because Raspberry Pi OS uses `systemd`, you should not use `rc.local` to run programs at startup. Instead, create a [`systemd` service](systemd.md).
