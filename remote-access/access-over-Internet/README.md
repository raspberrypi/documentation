# Access your Raspberry Pi over the internet

You can connect to your Raspberry Pi over the internet from another computer or a mobile device. There are a number of ways to do this, which we cover below.

## Port forwarding (IPv4)

One method is to set up port forwarding on your router. To do this, you must change the configuration of your router to forward all inbound traffic from the internet on a specific port to the local IP address of your Raspberry Pi. Most routers have this feature available. However, every router is different so you will need to consult your router's user manual for instructions. The settings can be tricky if your Pi is behind a firewall or if there is more than one router. One disadvantage of port forwarding is that it exposes a network port on your private LAN to the public internet. This is a known security vulnerability and must be managed carefully.

## Introduction for IPv6 newcomers

There are big differences in handling IPv4 and IPv6 for remote access in residential environments(dsl,cable,fibre, maybe mobile too).
With IPv4 it was and is still very common to use the public address of the router in combination with port forwarding. The router is the only device with a public address. So the router gets a packet and translates it (address and port) to a private IP address on the lan. Also the router is (mostly) responsible for getting a (nice) DNS name.
With IPv6 some things have changed. Depending on your isp (different types of dualstack-lite and dualstack) you don't get a public IPv4 address anymore.
Instead of one public IPv4 address you get a whole network with IPv6 addresses. Your devices share a common public prefix, usually with a length of 64bit or less.
Your computers assign themself one or more addresses from that network(SLAAC) or they get it assigned(DHCPv6). They all are public, but usually protected by the routers firewall against unwanted inbound traffic.
To use these addresses for remote access we need to do at least two things. 

* Open the routers firewall or a particularly service/port for the device on the lan. There is no NAT anymore. (NAT = network address/port translation, where the IPv4 port forwarding is based on).

* Create one DNS name for that device (not for the routers IP address anymore).

Opening/configuring the firewall has to be done on the router. Maybe on your Pi too if you are using iptables/nft.
DNS updates can be managed by the device itself(similar to IPv4 updaters) or by the router. 
Since privacy extensions (randomizing IP addresses) are in conflict with server use, it is recommend to disable privacy extensions for that use case.
It is possible to use IPv4 port forwarding and IPv6 port opening at the same time. It depends on your ISP.
In case of ds-lite you have only the choice to use IPv6 directly or to use some cloud relays/mappers.


## Port opening (IPv6, e.g. DS-lite)

Another method is to release the IP address (also called "exposed host") or ports of that IP address on your router. To do this, you must change the firewall configuration to allow inbound traffic to a specific port/IP. Sometimes it is called "interface id" or just "host part" of the IPv6 address. To get a stable interface id you should change `slaac private` to `slaac hwaddr` in `/etc/dhcpcd.conf` . Afterwards you can use IPv6 capable DNS-services. Security considerations are the same as for IPv4 mentioned above. Additionally you may lose a little bit privacy while using the `hwaddr`.

This description was tested with dynv6.com service(DNS-updater installed on the PI) and with myfritz a dns service by avm (DNS-updater integrated in the fritzbox). It should also work with other IPv6 capable dyndns providers.




## Alternatives

Rather than using port forwarding on your local router, there are a number of third-party online port forwarding services available. These provide varying levels of functionality - see their websites for more details. 

