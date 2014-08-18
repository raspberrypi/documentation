# Zeroconf or Bonjour (Apple)

If you have a network with Apple products or hardware using Zeroconf (e.g., printers, IP cameras) setting up Avahi will allow these devices to see each other easily.

First install [Avahi](http://avahi.org) and [Netatalk](http://netatalk.sourceforge.net):

    sudo apt-get install avahi-daemon
    sudo apt-get install netatalk

You should not see your Raspberry appear in OSX's Finder and you should be able to move documents between your Mac and Raspberry Pi easily. 

## SSH

Additionally, if you want to login to your raspberry pi using `ssh`, you can now do:

    ssh pi@raspberry.local

Other commands will be able to resolve your raspberry.local name into an IP address now.

    ping raspberry.local