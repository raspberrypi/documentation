# Access your Raspberry Pi over the internet

You can connect to your Raspberry Pi over the internet from another computer or a mobile device. There are a number of ways to do this, which we cover below.

## Port forwarding (IPv4)

One method is to set up port forwarding on your router. To do this, you must change the configuration of your router to forward all inbound traffic from the internet on a specific port to the local IP address of your Raspberry Pi. Most routers have this feature available. However, every router is different so you will need to consult your router's user manual for instructions. The settings can be tricky if your Pi is behind a firewall or if there is more than one router. One disadvantage of port forwarding is that it exposes a network port on your private LAN to the public internet. This is a known security vulnerability and must be managed carefully.

## Port releasing (IPv6, e.g. DS-lite)

Another method is to release the IP address (also called "exposed host") or ports of that IP address on your router. To do this, you must change the firewall configuration to allow inbound traffic to a specific port/IP. Sometimes it is called "interface id" or just "host part" of the IPv6 address. To get a stable interface id you should change "slaac private" to "slaac hwaddr" /etc/dhcpcd.conf . Afterwards you can use DNS-services like dynv6.com or myfritz.net. Security considerations are the same as for IPv4 mentioned above. Addtionally you may lose a little bit privacy while using the hwaddr.


## Alternatives

Rather than using port forwarding, there are a number of alternative third-party services available. These provide varying levels of functionality - see their websites for more details.

- [Remote.it](https://www.remote.it)
- [Dataplicity](https://dataplicity.com)
- [Yaler.net](https://yaler.net/)
- [Losant](https://losant.com)
- [Remote IoT](https://remote-iot.com)
