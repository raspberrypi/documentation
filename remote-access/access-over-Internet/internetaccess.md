# Access your Raspberry Pi over the Internet

You can connect to your Raspberry Pi over the Internet from another computer or mobile device.  

One method is to set-up port forwarding on your router.   Port forwarding requires that you change the configuration of your router to forward inbound Internet traffic on a specific port to the local IP address of your Raspberry Pi.  Most routers have this feature available.  However, every router is different so you will need to consult your router user manual.  The settings can be tricky if your Pi is behind a firewall or behind more than one router.  One disadvantage of port forwarding is that it leaves a network port on your private LAN open to the public Internet.  This is a well known security vulnerability and must be managed carefully.

One alternative to port forwarding is the use of Weaved services.  Weaved is free software you install on your Raspberry Pi that allows you to connect to your Pi from anywhere over the Internet.  SSH, VNC, HTTP, SFTP or any other TCP Port (or "TCP service") running on your Pi can be enabled for secure remote access over the Internet without port forwarding.



There are several video tutorials to help you if needed.

You will now be able to connect to your Raspberry Pi using SSH over the Intenet without port forwarding.

For further assistance you may email support@weaved.com.

