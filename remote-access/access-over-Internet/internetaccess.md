# Access your Raspberry Pi over the Internet

You can connect to your Raspberry Pi over the Internet from another computer or a mobile device.  

One method is to set-up port forwarding on your router.   To set-up port forwarding you must change the configuration of your router to forward all inbound traffic from the Internet on a specific port to the local IP address of your Raspberry Pi.  Most routers have this feature available.  However, every router is different so you will need to consult your router's user manual for instructions.  The settings can be tricky if your Pi is behind a firewall or more than one router.  One disadvantage of port forwarding is that it exposes a network port on your private LAN to the public Internet.   This is a known security vulnerability and must be managed carefully.

One secure alternative to port forwarding is the Weaved service.   Weaved is software you install on your Raspberry Pi that lets you connect to your Pi from anywhere over the Internet.   SSH, VNC, HTTP, SFTP file transfer and any other TCP service running on your Pi can be enabled for secure remote access over the Internet without port forwarding.

On your Pi (using a monitor or via SSH), update your Raspbian package lists:
```
sudo apt-get update
```

Install the weavedconnectd package:
```
sudo apt-get install weavedconnectd
```
Next run the weavedinstaller.  The weavedinstaller will ask you to input your Weaved account user name (email) and password.  You can create a Weaved user account here: https://developer.weaved.com/portal/index.php.   After you have created an account, go back to the Pi command line window.  Enter the command below to run the weavedinstaller on your Pi.  Follow the on-screen instructions in the Pi terminal window.

```
sudo weavedinstaller
```
Your Weaved account is now a private Internet VPN connection service to your Pi without port forwarding.  Access your Pi by logging in to your account at www.weaved.com.

For further assistance you may email support@weaved.com.


