# Pi is working, but I've got no networking


- [Is it the ethernet that isn't working?](#ethernet-problems)
- [Is it the wireless that isn't working?](#wireless-problems)


# Ethernet Problems

First thing to ensure, that the ethernet cable is plugged in to the Pi and to your router or switch. 

### I'm not using a router or switch, but connecting straight to another computer

This isn't a standard configuration, and needs a bit more setting up, which is out of the scope of this troubleshooter and we don't currently have any documentation for it. Try Googling for connecting my Raspberry Pi directly to another computer.

### Check for an IP address

If you are connected up, but nothing seems to work, lets see if you have been assigned as IP address by your network. Type in ```ifconfig``` on the console. This will display the status of all networking devices. For ethernet, we need to look at the ```eth0``` entry, something like this, the actual numbers have been replaced by xx/yy/zz etc.

```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet xx.xx.xx.xx  netmask 255.255.255.0  broadcast 10.3.14.255            <<<<<<< IPv4 address
        inet6 yyyy::yyyy:yyyy:yyyy:yyyy  prefixlen 64  scopeid 0x20<link>         <<<<<<< IPv6 address 
        inet6 zzzz:zzzz:zzzz:zz:zzzz:zzzz:zzzz:zzz  prefixlen 64  scopeid 0x0<global>
        ether qq:qq:qq:qq:qq:qq  txqueuelen 1000  (Ethernet)                      <<<<<<< MAC address
        ...
```

So if you have an IP address, there will be numbers in the inet or inet6 lines or both. If not, then your router has not assigned you an IP address.

#### Hold on, I don't even have an entry for eth0...

This would be unusual, it implies that the Ethernet HW on the Raspberry Pi isn't working, or has been specifically disabled. If you are using a new Raspbian install, and haven't made any changes, this is probably a broken ethernet chip.

#### eth0 is present, but I don't have the inet or inet6 lines

OK, so the ethernet port appears to be working, but your router has not allocated your Raspberry pi an ethernet address. You need to check out your router isntructions to find out why that might be. It might be doing something called MAC address filtering, or similar which means it only allocates addresses to devices it knows about. You can use the `ifconfig` command to find the MAC address of your Raspberry Pi, it's the hexadecimal number in the form `qq:qq:qq:qq:qq:qq` on the line starting with `ether`.

### I have an IP address but no internet connection

So, the connection to your internal network is working OK, but you don't appear to have an internet connection. This could be a number of things. 

TODO

### Slow connection

If you are using a Pi3B+ this has a gigbit ethernet adapter, and you might be expecting to get gigabit speeds. However, the Pi cannot communicate with the ethernet chip at that sort of speed due to inrerface limitation, so you will et less than that. It would normally be expected to get up to 250-300MBits/s. 

#### But I only get about 85MBits/s!

This almost certainly a flow control problem. You need to turn on flow control on your router to help with the slower speed of the Pi ethernet. It might be called pause frames or similar. Most redidential routers have flow control turned on automatically. Commercial routers will probably need it to be turned on.

## Wireless problems


