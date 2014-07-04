Setting wifi up via the commandline
===================================

This method is suitable if you do not have access to the graphical user interface we normally use to set up wifi on the Raspberry Pi.   
It is especailly suited for use with a serial console cable if you don't have access to a screen or wired ethernet network.   
Also note, no additional software is required that isn't already included on the Raspberry Pi.   

###Getting wifi network details  
To scan for wifi networks, use  
```sudo iwlist wlan0 scan```
   
This will list all wifi networks that have been plus some other useful information.   
The important ones to look for are   
```ESSID:"testing"``` - This is the name of the wifi network.   
```IE: IEEE 802.11i/WPA2 Version 1``` - This is the authentication used, in my case WPA2, the newer more secure wireless standard which replaces WPA1.      
This guide should work fine for WEP, WPA or WPA2 but may not work for WPA2 enterprise.   
   
   
I also have also got the password for the wifi network. For most home routers this is located on a sticker on the back of the router.   
The ESSID (ssid) for my network is ```testing``` and the password (psk) ```testingPassword```

###Adding the network details to the Raspberry Pi
   
Open the wpa-supplicant configuration file   
```sudo nano etc/wpa_supplicant/wpa_supplicant.conf```   
Go to the bottom of the file and add in   

```
network={
    ssid="The_ESSID_from_earlier"
    psk="Your_wifi_password"
}
```

So for me, I would enter   
```
network={
    ssid="testing"
    psk="testingPassword"
}
```
   
Now save the file by hitting __ctrl+x__ then __y__ then finally hit __enter__.  

At this point, wpa-supplicant will normally notice a change has occurred within a few seconds will try and connect to the network.   
If it does not, either manually restart the interface with ```sudo ifdown wlan0``` and ```sudo ifup wlan0``` or reboot your Raspberry Pi with ```sudo reboot```.   

You can verify if it has successfully connected using ```ifconfig wlan0```. If the ```inet addr``` field has an address beside it, you are sorted. If not, check your password and ESSID are correct.   
