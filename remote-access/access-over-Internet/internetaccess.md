# Access your Raspberry Pi over the Internet

You can connect to your Raspberry Pi from another computer anywhere in the world over the Internet.   One method is to use port forwarding.   Port forwarding requires you to change the configuration settings on your router.   You must configure your router to forward the Internet traffic delivered to your public IP address on a specific TCP port number, to automatically route to the local network IP address of your Raspberry Pi.  Most routers have this feature available through their configuration webpage.  However, every router is different and there is no single set of instructions that applies to every router in use today.  You will need to refer to the instruction manual for your router.  The configurations can be tricky if your Pi is behind a firewall, or behind more than one router.  One disadvantage of port forwarding is that it leaves a TCP port on your public IP address open on the Internet.  This is a well known security vulnerability and must be managed carefully.

One alternative method to port forwarding is the use of Weaved services.  Weaved is free software you can install on your Raspberry Pi that allows you to connect to your Pi from anywhere over the Internet.  SSH, VNC, HTTP, SFTP or any other TCP Port (or "TCP service") can be enabled securely over the Internet without port forwarding.

For example, to enable SSH connections to your Raspberry Pi over the Internet using any standard SSH client software follow the instructions at:  

https://developer.weaved.com/portal/members/betapi.php

There are several video tutorials to help you if needed.

You will now be able to connect to your Raspberry Pi using SSH over the Intenet without port forwarding.

For further assistance you may email support@weaved.com.

