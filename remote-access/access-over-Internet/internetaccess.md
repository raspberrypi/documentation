# Access your Raspberry Pi over the internet

You can connect to your Raspberry Pi over the internet from another computer or a mobile device. There are a number of ways to do this, which we cover below. 

## Port Forwarding

One method is to set port forwarding up on your router. To set port forwarding up, you must change the configuration of your router to forward all inbound traffic from the internet on a specific port to the local IP address of your Raspberry Pi. Most routers have this feature available. However, every router is different so you will need to consult your router's user manual for instructions. The settings can be tricky if your Pi is behind a firewall or if there is more than one router. One disadvantage of port forwarding is that it exposes a network port on your private LAN to the public internet. This is a known security vulnerability and must be managed carefully.

## Weaved

One secure alternative to port forwarding is the Weaved service. Weaved is software you install on your Raspberry Pi which lets you connect to your Pi from anywhere over the internet. SSH, VNC, HTTP, SFTP file transfer, and any other TCP service running on your Pi can be enabled for secure remote access over the internet without port forwarding.

On your Pi (using a monitor or via SSH), update your Raspbian package lists:

```bash
sudo apt-get update
```

Install the weavedconnectd package:

```bash
sudo apt-get install weavedconnectd
```

Next, run the weavedinstaller. The weavedinstaller will ask you to input your Weaved account user name (email) and password. You can create a Weaved user account [here](https://developer.weaved.com/portal/index.php). After you have created an account, go back to the Pi command line window. Enter the command below to run the weavedinstaller on your Pi. Follow the on-screen instructions in the Pi terminal window.

```bash
sudo weavedinstaller
```

Your Weaved account is now a private internet VPN connection service to your Pi without port forwarding. Access your Pi by logging into your account at www.weaved.com.

For further assistance, email support@weaved.com.

## Alternatives

- Dataplicity: this connects to your Pi using client-initiated HTTPS. See the [Dataplicity website](https://dataplicity.com) for more information. 
